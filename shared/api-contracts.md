# API Contracts

Kontrak HTTP antara frontend dan backend clau-ai-agents, dan antara platform dengan konsumen lain. Endpoint bertanda **Implemented** sudah ada di scaffold backend; sisanya **Planned**.

## Prinsip

- JSON, UTF-8, timestamp ISO 8601 dengan zona waktu.
- Tidak ada endpoint yang **publish** ke platform sosial/OTA atau **mengirim** pesan ke tamu. Release dilakukan manusia (Constitution §4.7).
- Tidak ada endpoint yang menerima credential platform client.
- Error: `{"error": {"code": "<snake_case>", "message": "<teks>"}}`.

## Endpoint

| Method & path | Status | Request | Response |
|---|---|---|---|
| `GET /health` | **Implemented** | — | `{"status": "ok", "service": "clau-ai-agents-backend", "version": "<semver>"}` |
| `GET /agents` | **Implemented** | — | `{"agents": [Agent]}` dari `agents/registry.json` |
| `POST /route` | **Implemented** (statis) | `{"intent": "<intent>"}` | `{"intent", "pillar", "skill", "repo", "approval_min", "status": "active"\|"planned"}`. Intent tidak dikenal → 404 `unknown_intent` |
| `POST /requests` | Planned | `{client_code, intent, text, deadline}` | `Request` dengan `priority` dari priority engine |
| `POST /drafts` | Planned | `{request_id, brief_id}` | `Draft` + `claims[]`, `mode` |
| `POST /qa-records` | Planned | `{draft_id, gate, result, reviewer_role, independent}` | `QARecord` |
| `POST /approvals` | Planned | `{draft_id, level, decision, approver_role}` | `Approval` (ditolak bila mode SIMULASI + Approved) |

## Bentuk Objek

```json
{
  "Agent": {
    "id": "caption-writer",
    "pillar": 1,
    "status": "active",
    "intents": ["caption"],
    "skill": "draft-caption",
    "skill_repo": "clau-ai-marketing",
    "approval_min": "L1",
    "forbidden_actions": ["publish", "send_external", "self_approve"]
  }
}
```

Field `intent`, `pillar`, `skill`, dan `approval_min` mengikuti [orchestrator/router.md](../orchestrator/router.md). Bila router berubah, `agents/registry.json` di clau-ai-agents wajib ikut diperbarui.

## Versioning

- Versi API mengikuti versi backend (SemVer). Perubahan breaking = MAJOR dan dicatat di README backend.
