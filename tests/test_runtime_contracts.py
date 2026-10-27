"""Executable negative contracts, not real-model quality or production security tests."""
import copy
import json
import unittest
from datetime import datetime, timezone
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from runtime_contracts import (CONTRACTS, SCHEMA, ContractError, approved_memory_eligible,
                               check_fixtures, prompt_version, validate_contract)
from jsonschema import Draft202012Validator

EXAMPLES = json.loads((Path(__file__).resolve().parents[1] / 'shared/runtime/v1/examples.json').read_text())
NOW = datetime(2026, 10, 27, 8, tzinfo=timezone.utc)


class RuntimeContracts(unittest.TestCase):
    def example(self, name):
        return copy.deepcopy(EXAMPLES[name])

    def invalid(self, name, payload, code=None):
        with self.assertRaises(ContractError) as caught:
            validate_contract(name, payload)
        if code:
            self.assertEqual(str(caught.exception), code)

    def test_fixture_and_registry_coverage(self):
        self.assertEqual(check_fixtures(), 0)

    def test_root_requires_explicit_contract(self):
        self.assertFalse(Draft202012Validator(SCHEMA).is_valid(EXAMPLES['TaraGeneration']))

    def test_missing_required_fields(self):
        for name in CONTRACTS:
            for key in SCHEMA['$defs'][name]['required']:
                with self.subTest(contract=name, field=key):
                    payload = self.example(name)
                    del payload[key]
                    self.invalid(name, payload, 'schema_invalid')

    def test_unknown_authority_fields(self):
        for name in CONTRACTS:
            for field in ('approved', 'role', 'publish', 'system_instruction'):
                with self.subTest(contract=name, field=field):
                    payload = self.example(name)
                    payload[field] = True
                    self.invalid(name, payload, 'schema_invalid')

    def test_incompatible_contract_version(self):
        payload = self.example('PromptBundle')
        payload['contract_version'] = '2.0.0'
        self.invalid('PromptBundle', payload)

    def test_bundle_has_all_required_components(self):
        payload = self.example('PromptBundle')
        payload['components'].pop()
        self.invalid('PromptBundle', payload, 'bundle_component_missing')

    def test_bundle_has_all_context(self):
        payload = self.example('PromptBundle')
        payload['required_context'].remove('voice_card')
        self.invalid('PromptBundle', payload, 'bundle_context_missing')

    def test_bundle_has_all_validators(self):
        payload = self.example('PromptBundle')
        payload['validators'].pop()
        self.invalid('PromptBundle', payload, 'bundle_validator_missing')

    def test_bundle_duplicate_paths(self):
        payload = self.example('PromptBundle')
        payload['components'].append(payload['components'][0])
        self.invalid('PromptBundle', payload, 'duplicate_component')

    def test_path_traversal_and_urls(self):
        for path in ('../secret', '/etc/passwd', 'a/../../secret', 'https://example.test/x', 'a\\b', 'a//b'):
            with self.subTest(path=path):
                payload = self.example('PromptBundle')
                payload['components'][0]['path'] = path
                self.invalid('PromptBundle', payload)

    def test_hash_is_stable_under_object_and_component_order(self):
        payload = self.example('PromptBundle')
        expected = prompt_version(payload)
        payload['components'].reverse()
        payload = dict(reversed(list(payload.items())))
        self.assertEqual(prompt_version(payload), expected)
        self.assertEqual(len(expected), 64)

    def test_each_component_change_invalidates_hash(self):
        for index in range(len(EXAMPLES['PromptBundle']['components'])):
            payload = self.example('PromptBundle')
            payload['components'][index]['sha256'] = 'f' * 64
            self.assertNotEqual(prompt_version(payload), prompt_version(EXAMPLES['PromptBundle']))

    def test_settings_and_validator_version_invalidate_hash(self):
        for key, val in [('model', 'fake-1'), ('provider', 'other'), ('temperature_milli', 500), ('effort', 'high'), ('max_output_tokens', 2048)]:
            with self.subTest(setting=key):
                payload = self.example('PromptBundle')
                payload['model_settings'][key] = val
                self.assertNotEqual(prompt_version(payload), prompt_version(EXAMPLES['PromptBundle']))
        payload = self.example('PromptBundle')
        payload['validators'][0]['version'] = '1.0.1'
        self.assertNotEqual(prompt_version(payload), prompt_version(EXAMPLES['PromptBundle']))

    def test_no_autonomous_publish(self):
        payload = self.example('PromptBundle')
        payload['autonomy_max'] = 'A'
        self.invalid('PromptBundle', payload)

    def test_draft_has_three_distinct_styles(self):
        payload = self.example('TaraGeneration')
        payload['variants'].pop()
        self.invalid('TaraGeneration', payload)
        payload = self.example('TaraGeneration')
        payload['variants'][1]['style'] = payload['variants'][0]['style']
        self.invalid('TaraGeneration', payload, 'duplicate_variant_style')

    def test_clarification_is_not_a_draft(self):
        payload = self.example('TaraGeneration')
        payload['status'] = 'clarification_required'
        payload['clarification_questions'] = ['Apa objective yang disetujui?']
        self.invalid('TaraGeneration', payload)
        payload['variants'] = []
        validate_contract('TaraGeneration', payload)
        payload['clarification_questions'] = []
        self.invalid('TaraGeneration', payload)

    def test_escalation_has_reason_no_variants(self):
        payload = self.example('TaraGeneration')
        payload.update(status='escalation_required', variants=[], model_notes_for_reviewer=[])
        self.invalid('TaraGeneration', payload)
        payload['model_notes_for_reviewer'] = ['Perlu owner review karena isu keselamatan.']
        validate_contract('TaraGeneration', payload)

    def test_model_cannot_set_evidence_label(self):
        payload = self.example('TaraGeneration')
        payload['claims'] = [dict(text='Klaim SIMULASI', category='facility', fact_key='facility.pool', implied=False, variant_indexes=[0], evidence_label='DATA FINAL')]
        self.invalid('TaraGeneration', payload)

    def test_claim_limits_and_variant_mapping(self):
        claim = dict(text='Klaim SIMULASI', category='facility', fact_key='facility.pool', implied=False, variant_indexes=[0])
        payload = self.example('TaraGeneration')
        payload['claims'] = [claim] * 31
        self.invalid('TaraGeneration', payload)
        payload['claims'] = [dict(claim, variant_indexes=[3])]
        self.invalid('TaraGeneration', payload)
        payload['claims'] = [dict(claim, fact_key='price.pool')]
        self.invalid('TaraGeneration', payload, 'claim_category_mismatch')

    def test_tool_scope_and_side_effects(self):
        for key, val in [('side_effects', 'write'), ('client_scope', 'model_selected'), ('audit', 'raw_content'), ('sensitivity_max', 'Restricted'), ('timeout_ms', 0)]:
            with self.subTest(field=key):
                payload = self.example('ToolContract')
                payload[key] = val
                self.invalid('ToolContract', payload)

    def test_tool_schema_path(self):
        payload = self.example('ToolContract')
        payload['input_schema_component'] = '../../data.json'
        self.invalid('ToolContract', payload, 'unsafe_schema_path')

    def test_memory_cross_client_source(self):
        payload = self.example('MemoryRecord')
        payload['source']['client_code'] = 'CTHCAFE'
        self.invalid('MemoryRecord', payload, 'tenant_scope_violation')

    def test_memory_cannot_downgrade_sensitivity(self):
        payload = self.example('MemoryRecord')
        payload['source']['sensitivity'] = 'Restricted'
        self.invalid('MemoryRecord', payload, 'sensitivity_mismatch')

    def test_memory_approval_required(self):
        for key in ('approved_by', 'approved_at'):
            payload = self.example('MemoryRecord')
            payload[key] = None
            self.invalid('MemoryRecord', payload)

    def test_fact_memory_needs_final_fact_sheet(self):
        payload = self.example('MemoryRecord')
        payload['source']['source_type'] = 'approved_content'
        self.invalid('MemoryRecord', payload)
        payload = self.example('MemoryRecord')
        payload['evidence_label'] = 'ASSUMPTION'
        self.invalid('MemoryRecord', payload)

    def test_memory_eligibility(self):
        payload = self.example('MemoryRecord')
        self.assertTrue(approved_memory_eligible(payload, client_code='CTHVILLA', at=NOW, for_facts=True))
        self.assertFalse(approved_memory_eligible(payload, client_code='CTHCAFE', at=NOW))
        self.assertFalse(approved_memory_eligible(payload, client_code='CTHVILLA', at=datetime(2026,11,1,tzinfo=timezone.utc)))
        self.assertFalse(approved_memory_eligible(payload, client_code='CTHVILLA', at=datetime(2026,10,26,tzinfo=timezone.utc)))
        for status in ('draft', 'revoked'):
            payload['status'] = status
            self.assertFalse(approved_memory_eligible(payload, client_code='CTHVILLA', at=NOW))

    def test_restricted_memory_not_provider_eligible(self):
        payload = self.example('MemoryRecord')
        payload['sensitivity'] = payload['source']['sensitivity'] = 'Restricted'
        self.assertFalse(approved_memory_eligible(payload, client_code='CTHVILLA', at=NOW))

    def test_history_is_not_fact_source(self):
        payload = self.example('MemoryRecord')
        payload['memory_type'] = 'historical_reference'
        self.assertFalse(approved_memory_eligible(payload, client_code='CTHVILLA', at=NOW, for_facts=True))

    def test_invalid_validity_window(self):
        payload = self.example('MemoryRecord')
        payload['valid_until'] = payload['valid_from']
        self.invalid('MemoryRecord', payload, 'invalid_validity_window')

    def test_timezone_required(self):
        payload = self.example('MemoryRecord')
        payload['valid_from'] = '2026-10-27T07:00:00'
        self.invalid('MemoryRecord', payload)
        with self.assertRaises(ContractError):
            approved_memory_eligible(EXAMPLES['MemoryRecord'], client_code='CTHVILLA', at=datetime(2026,10,27))

    def test_superseded_memory_needs_successor(self):
        payload = self.example('MemoryRecord')
        payload['status'] = 'superseded'
        self.invalid('MemoryRecord', payload)
        payload['superseded_by'] = 'simulation-memory-2'
        self.assertFalse(approved_memory_eligible(payload, client_code='CTHVILLA', at=NOW))

    def test_plan_missing_facts(self):
        payload = self.example('WorkPlan')
        payload['required_fact_keys'] = ['price.nightly']
        self.invalid('WorkPlan', payload, 'inconsistent_missing_facts')
        payload['missing_fact_keys'] = ['price.nightly']
        self.invalid('WorkPlan', payload)
        payload['decision'] = 'clarification_required'
        validate_contract('WorkPlan', payload)

    def test_fail_cannot_be_ready(self):
        payload = self.example('ValidationResult')
        payload.update(result='fail', errors=[dict(code='claim_missing', message='SIMULASI', path='claims')])
        self.invalid('ValidationResult', payload)
        payload['ready_for_human_review'] = False
        validate_contract('ValidationResult', payload)

    def test_conditional_needs_owned_action(self):
        payload = self.example('ValidationResult')
        payload.update(result='conditional', ready_for_human_review=False)
        self.invalid('ValidationResult', payload)
        payload['actions'] = [dict(code='rights_check', description='Cek rights SIMULASI', owner_role='content_lead', resolved=False, evidence_ref=None)]
        validate_contract('ValidationResult', payload)
        payload['actions'][0]['resolved'] = True
        self.invalid('ValidationResult', payload)

    def test_pass_requires_full_claim_coverage(self):
        payload = self.example('ValidationResult')
        payload['claim_coverage'] = .5
        self.invalid('ValidationResult', payload)

    def test_critic_cannot_claim_independence(self):
        payload = self.example('ValidationResult')
        payload['review_kind'] = 'independent'
        self.invalid('ValidationResult', payload)

    def test_run_cross_client_context(self):
        payload = self.example('AgentRun')
        payload['context_sources'][0]['client_code'] = 'CTHCAFE'
        self.invalid('AgentRun', payload, 'tenant_scope_violation')

    def test_ready_run_requires_persistence_evidence(self):
        for key in ('draft_id','draft_content_sha256','validation_ref','prompt_version','context_sha256'):
            with self.subTest(field=key):
                payload = self.example('AgentRun')
                payload[key] = None
                self.invalid('AgentRun', payload)

    def test_cancelled_run_cannot_link_active_draft(self):
        payload = self.example('AgentRun')
        payload.update(status='cancelled', error_code='cancelled_by_user')
        self.invalid('AgentRun', payload)
        payload.update(draft_id=None, draft_content_sha256=None)
        validate_contract('AgentRun', payload)

    def test_run_time_monotonic(self):
        payload = self.example('AgentRun')
        payload['finished_at'] = '2026-10-26T08:00:00Z'
        self.invalid('AgentRun', payload, 'invalid_run_time')

    def test_error_retry_is_server_policy(self):
        payload = self.example('RuntimeError')
        payload['code'] = 'restricted_data'
        self.invalid('RuntimeError', payload, 'invalid_retry_policy')
        payload['retryable'] = False
        validate_contract('RuntimeError', payload)

    def test_usage_integer_cost_and_no_content(self):
        for key, value in [('cost_micro_usd', -1), ('cost_micro_usd', 1.5), ('prompt', 'private')]:
            payload = self.example('Usage')
            payload[key] = value
            self.invalid('Usage', payload)

    def test_errors_do_not_echo_private_input(self):
        payload = self.example('Usage')
        payload['private_field'] = 'DO-NOT-LOG-THIS-CONTENT'
        with self.assertRaises(ContractError) as caught:
            validate_contract('Usage', payload)
        self.assertNotIn('DO-NOT-LOG', str(caught.exception))


if __name__ == '__main__':
    unittest.main()
