# API Contracts

Kontrak HTTP antara frontend dan backend clau-ai-agents, dan antara platform dengan konsumen lain. Endpoint bertanda **Implemented** sudah ada di scaffold backend; sisanya **Planned**.

## Prinsip

- JSON, UTF-8, timestamp ISO 8601 dengan zona waktu.
- Tidak ada endpoint yang **publish** ke platform sosial/OTA atau **mengirim** pesan ke tamu. Release dilakukan manusia (Constitution §4.7).
- Tidak ada endpoint yang menerima credential platform client.
- Error: `{"error": {"code": "<snake_case>", "message": "<teks>"}}` untuk semua error, termasuk validasi request (422 `validation_error`).

## Endpoint

| Method & path | Status | Request | Response |
|---|---|---|---|
| `GET /health` | **Implemented** | — | `{"status": "ok", "service": "clau-ai-agents-backend", "version": "<semver>"}` |
| `GET /agents` | **Implemented** | — | `{"agents": [Agent]}` dari `agents/registry.json` |
| `POST /route` | **Implemented** (statis) | `{"intent": "<intent>"}` | `{"intent", "agent", "pillar", "skill", "repo", "approval_min", "status": "active"\|"planned", "next_step": "produce_draft"\|"escalate_to_owner"}`. Intent tidak dikenal → 404 `unknown_intent`; body tidak valid → 422 `validation_error` |
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

| Versi backend | Tanggal | Perubahan |
|---|---|---|
| 0.1.0 | 2026-10-04 | Scaffold: `/health`, `/agents`, `/route` |
| 0.2.0 | 2026-10-06 | Error memakai bentuk kontrak (sebelumnya terbungkus `detail`); `/route` menambah `agent` dan `next_step` (planned → `escalate_to_owner`) |
