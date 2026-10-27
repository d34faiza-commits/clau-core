"""H1 reference conformance checks. Not imported by the production worker.

No network or tenant-data lookup. Structural validation cannot prove authorization,
claim completeness, consent, or factual truth; the server must enforce those gates.
"""
from __future__ import annotations

import copy
import hashlib
import json
import re
from datetime import datetime
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / 'shared/runtime/v1/contracts.schema.json').read_text())
ERRORS = json.loads((ROOT / 'shared/runtime/v1/error-codes.json').read_text())['errors']
CONTRACTS = ('PromptBundle', 'AgentRun', 'TaraGeneration', 'ToolContract', 'MemoryRecord',
             'WorkPlan', 'ValidationResult', 'RuntimeError', 'Usage', 'Provenance')
REQUIRED_COMPONENTS = {'constitution', 'boundary', 'rule', 'skill', 'persona',
                       'voice_guide', 'humanize_guide', 'vertical', 'platform',
                       'prompt_template', 'output_schema', 'validator_config',
                       'tool_contract', 'escalation_rules'}
REQUIRED_CONTEXT = {'approved_facts', 'voice_card', 'brief', 'platform', 'format',
                    'objective', 'audience', 'language', 'assets'}
REQUIRED_VALIDATORS = {'structured_output', 'claim_coverage', 'privacy_consent',
                       'platform_rules', 'brand_voice', 'duplicate_copy'}
FORMATS = FormatChecker()


@FORMATS.checks('date-time', raises=(ValueError, TypeError))
def is_timestamp(value):
    # jsonschema's optional RFC3339 extra is not required by this repo.
    if not isinstance(value, str):
        return True
    if not re.fullmatch(r'\d{4}-\d{2}-\d{2}[Tt]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:[Zz]|[+-]\d{2}:\d{2})', value):
        return False
    parsed = datetime.fromisoformat(value.upper().replace('Z', '+00:00'))
    return parsed.utcoffset() is not None


class ContractError(ValueError):
    """Stable local conformance code; never includes client payload values."""


def require(ok: bool, code: str) -> None:
    if not ok:
        raise ContractError(code)


def timestamp(value: str) -> datetime:
    return datetime.fromisoformat(value.upper().replace('Z', '+00:00'))


def unique(items: list[dict], key: str) -> bool:
    return len({item[key] for item in items}) == len(items)


def validate_contract(name: str, payload: dict) -> None:
    require(name in CONTRACTS, 'unknown_contract')
    schema = {'$ref': '#/$defs/' + name, '$defs': SCHEMA['$defs']}
    validator = Draft202012Validator(schema, format_checker=FORMATS)
    # Do not render jsonschema error messages: they can contain full private input.
    require(validator.is_valid(payload), 'schema_invalid')
    if name == 'PromptBundle':
        require(unique(payload['components'], 'path'), 'duplicate_component')
        require(REQUIRED_COMPONENTS <= {c['kind'] for c in payload['components']}, 'bundle_component_missing')
        require(REQUIRED_CONTEXT <= set(payload['required_context']), 'bundle_context_missing')
        for key in ('tools', 'validators'):
            require(unique(payload[key], 'id'), 'duplicate_' + key)
        require(REQUIRED_VALIDATORS <= {v['id'] for v in payload['validators']}, 'bundle_validator_missing')
    elif name == 'TaraGeneration':
        require(unique(payload['variants'], 'style'), 'duplicate_variant_style')
        for variant in payload['variants']:
            require(unique(variant['alt_texts'], 'asset_id'), 'duplicate_alt_text_asset')
        for claim in payload['claims']:
            require(all(i < len(payload['variants']) for i in claim['variant_indexes']), 'claim_variant_missing')
            if claim['fact_key'] is not None:
                require(claim['fact_key'].split('.', 1)[0] == claim['category'], 'claim_category_mismatch')
    elif name == 'MemoryRecord':
        source = payload['source']
        require(source['client_code'] == payload['client_code'], 'tenant_scope_violation')
        require(source['sensitivity'] == payload['sensitivity'], 'sensitivity_mismatch')
        if payload['valid_until'] is not None:
            require(timestamp(payload['valid_until']) > timestamp(payload['valid_from']), 'invalid_validity_window')
        if payload['status'] == 'approved':
            require(timestamp(payload['approved_at']) <= timestamp(source['retrieved_at']), 'approval_after_retrieval')
        require(payload['superseded_by'] != payload['memory_id'], 'memory_self_supersedes')
    elif name == 'AgentRun':
        require(all(p['client_code'] == payload['client_code'] for p in payload['context_sources']), 'tenant_scope_violation')
        if payload['finished_at']:
            require(timestamp(payload['finished_at']) >= timestamp(payload['started_at']), 'invalid_run_time')
    elif name == 'ValidationResult':
        require(unique(payload['validator_versions'], 'id'), 'duplicate_validators')
    elif name == 'RuntimeError':
        require(payload['retryable'] == ERRORS[payload['code']]['retryable'], 'invalid_retry_policy')
    elif name == 'ToolContract':
        path_schema = SCHEMA['$defs']['Component']['properties']['path']
        for field in ('input_schema_component', 'output_schema_component'):
            require(Draft202012Validator(path_schema).is_valid(payload[field]), 'unsafe_schema_path')
    elif name == 'WorkPlan':
        required, available, missing = (set(payload[k]) for k in
                                       ('required_fact_keys', 'available_fact_keys', 'missing_fact_keys'))
        require(missing == required - available, 'inconsistent_missing_facts')


def prompt_version(bundle: dict) -> str:
    """SHA-256 of canonical manifest, including exact component digests/settings.

    Component order is irrelevant; validator/tool/context array order is significant.
    Integers only for numeric settings, so cross-language float formatting is avoided.
    H3 MUST verify each digest against packaged bytes before calling this function.
    """
    validate_contract('PromptBundle', bundle)
    basis = copy.deepcopy(bundle)
    basis['components'].sort(key=lambda c: c['path'])
    encoded = json.dumps(basis, sort_keys=True, ensure_ascii=False, separators=(',', ':'), allow_nan=False).encode('utf-8')
    return hashlib.sha256(encoded).hexdigest()


def approved_memory_eligible(memory: dict, *, client_code: str, at: datetime, for_facts: bool = False) -> bool:
    """Conformance predicate after server-scoped retrieval; NOT authorization."""
    validate_contract('MemoryRecord', memory)
    require(at.tzinfo is not None and at.utcoffset() is not None, 'timezone_required')
    if memory['client_code'] != client_code or memory['status'] != 'approved':
        return False
    if memory['sensitivity'] == 'Restricted' or memory['superseded_by'] is not None:
        return False
    if memory['memory_type'] == 'working':
        return False
    if timestamp(memory['approved_at']) > at or timestamp(memory['valid_from']) > at:
        return False
    if memory['valid_until'] and at >= timestamp(memory['valid_until']):
        return False
    return not for_facts or (memory['memory_type'] == 'approved_fact' and memory['evidence_label'] == 'DATA FINAL')


def check_fixtures() -> int:
    Draft202012Validator.check_schema(SCHEMA)
    fixtures = json.loads((ROOT / 'shared/runtime/v1/examples.json').read_text())
    require(set(fixtures) == set(CONTRACTS), 'fixture_coverage_missing')
    require(set(ERRORS) == set(SCHEMA['$defs']['RuntimeError']['properties']['code']['enum']), 'error_registry_mismatch')
    for name, payload in fixtures.items():
        validate_contract(name, payload)
    print(f'PASS — {len(fixtures)} runtime contract fixtures (synthetic only).')
    return 0


if __name__ == '__main__':
    raise SystemExit(check_fixtures())
