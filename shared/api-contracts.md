# API Contracts

Kontrak HTTP antara frontend dan backend clau-ai-agents, dan antara platform dengan konsumen lain. Endpoint bertanda **Implemented** sudah ada di scaffold backend; sisanya **Planned**.

## Prinsip

- JSON, UTF-8, timestamp ISO 8601 dengan zona waktu.
- Tidak ada endpoint yang **publish** ke platform sosial/OTA atau **mengirim** pesan ke tamu. Release dilakukan manusia (Constitution §4.7).
- Tidak ada endpoint yang menerima credential platform client.
- Error: `{"error": {"code": "<snake_case>", "message": "<teks>"}}` untuk semua error, termasuk validasi request (422 `validation_error`).
- **Autentikasi** (0.5.0): sesi cookie dari `POST /auth/login`. Setiap request yang mengubah data (POST/PUT/PATCH/DELETE) wajib header `X-CSRF-Token` (dari `Me.csrf_token`) dan Origin aplikasi. Selama `Me.next` ≠ `ready` (ganti password sementara / aktifkan 2FA wajib owner), hanya endpoint `/auth/*` yang bisa dipakai (403 `password_change_required` / `mfa_setup_required`). Tidak ada pendaftaran publik: owner pertama dibuat lewat CLI server. Browser tidak memanggil backend langsung; frontend meneruskan `/api/*` ke backend (keputusan VPS #1).
- Pelanggaran aturan database (Constraint Wajib) = 409 dengan kode aturan, mis. `approval_needs_independent_review`, tanpa detail SQL.

## Endpoint

| Method & path | Status | Request | Response |
|---|---|---|---|
| `GET /health` | **Implemented** | — | `{"status": "ok", "service": "clau-ai-agents-backend", "version": "<semver>"}` |
| `GET /agents` | **Implemented** | — | `{"agents": [Agent]}` dari `agents/registry.json` |
| `GET /pillars` | **Implemented** | — | `{"pillars": [Pillar]}` dari `agents/registry.json` → `pillars`, plus `agents` (id agent per pilar) |
| `POST /route` | **Implemented** (statis) | `{"intent": "<intent>"}` | `{"intent", "agent", "pillar", "skill", "repo", "approval_min", "autonomy_max": "A"\|"B"\|"C", "status": "active"\|"planned", "next_step": "produce_draft"\|"escalate_to_owner"}`. Intent tidak dikenal → 404 `unknown_intent`; body tidak valid → 422 `validation_error` |
| `POST /auth/login` | **Implemented** (0.5.0) | `{email, password, totp_code?}` | `Me` + cookie sesi `__Host-clau_session` (`HttpOnly; Secure; SameSite=Lax`). 401 `invalid_credentials` (sama untuk email tidak terdaftar), 401 `mfa_required` / `invalid_mfa_code`, 429 `too_many_attempts` (5 gagal = kunci 15 menit), 403 `origin_not_allowed` |
| `GET /auth/me` | **Implemented** (0.5.0) | — (cookie) | `Me` |
| `POST /auth/logout` | **Implemented** (0.5.0) | — | 204, sesi dicabut |
| `POST /auth/password` | **Implemented** (0.5.0) | `{current_password, new_password}` | `Me` + cookie baru; sesi lain dicabut. 422 `weak_password` (min. 12 karakter, NIST SP 800-63B) |
| `POST /auth/mfa/setup` · `POST /auth/mfa/confirm` | **Implemented** (0.5.0) | — · `{code}` | `{secret, otpauth_uri}` · `Me` + cookie baru (TOTP RFC 6238, kode tidak bisa dipakai ulang) |
| `GET /users` · `POST /users` | **Implemented** (0.5.0), owner | — · `{display_name, email, temporary_password, locale?, timezone?, memberships[]}` | `{users: [User]}` · `User` (wajib ganti password saat login pertama) |
| `PUT /users/{id}/memberships` · `POST /users/{id}/disable` · `POST /users/{id}/enable` | **Implemented** (0.5.0), owner | `[{scope, role, max_level}]` · — · — | `User`; sesi user target dicabut. 409 `last_owner` / `cannot_disable_self` |
| `POST /requests` | Planned | `{client_code, intent, text, deadline}` | `Request` dengan `priority` dari priority engine |
| `POST /drafts` | Planned | `{request_id, brief_id}` | `Draft` + `claims[]`, `mode` |
| `POST /qa-records` | Planned | `{draft_id, gate, result, reviewer_role, independent}` | `QARecord` |
| `POST /approvals` | Planned | `{draft_id, level, decision, approver_role}` | `Approval` (ditolak bila mode SIMULASI + Approved) |

## Bentuk Objek

```json
{
  "Agent": {
    "id": "caption-writer",
    "display_name": "Tara",
    "pillar": 1,
    "status": "active",
    "intents": ["caption"],
    "skill": "draft-caption",
    "skill_repo": "clau-ai-marketing",
    "approval_min": "L1",
    "autonomy_max": "B",
    "persona": "agents/personas/caption-writer.md",
    "evals": "agents/evals/cases/caption-writer.json",
    "avatar": {
      "crop": "frontend/public/agents/caption-writer.webp",
      "master": "agents/avatars/caption-writer.webp",
      "figure": "female"
    },
    "forbidden_actions": ["publish", "send_external", "self_approve"]
  },
  "Pillar": {
    "id": 1,
    "name": {"en": "AI Marketing", "id": "AI Marketing"},
    "status": "active",
    "repo": "clau-ai-marketing",
    "agents": ["caption-writer", "reel-scripter"]
  }
}
```

Field `intent`, `pillar`, `skill`, `approval_min`, dan `autonomy_max` (kolom Otonomi) mengikuti [orchestrator/router.md](../orchestrator/router.md). Bila router berubah, `agents/registry.json` di clau-ai-agents wajib ikut diperbarui. Field `Pillar.name`, `status`, dan `repo` mengikuti tabel **5 Pilar CLAU AI** di [README](../README.md) (dicek `backend/tests/test_registry.py` di clau-ai-agents).

`display_name` dan `avatar` (registry 0.3.0) adalah sumber tunggal nama dan avatar agent untuk UI; `figure` mendeskripsikan figur ilustrasi (`female`/`male`), bukan data orang. Isi `forbidden_actions` = `default_forbidden_actions` registry.

`Me` = `{user: User, mfa_required, must_change_password, next: "ready"|"password_change"|"mfa_setup", csrf_token}`. `User` = `{id, display_name, email, locale, timezone, salutation, memberships: [{scope, role, max_level}], mfa_enabled, disabled}` (tanpa hash atau secret).

## Versioning

- Versi API mengikuti versi backend (SemVer). Perubahan breaking = MAJOR dan dicatat di README backend.

| Versi backend | Tanggal | Perubahan |
|---|---|---|
| 0.1.0 | 2026-10-04 | Scaffold: `/health`, `/agents`, `/route` |
| 0.2.0 | 2026-10-06 | Error memakai bentuk kontrak (sebelumnya terbungkus `detail`); `/route` menambah `agent` dan `next_step` (planned → `escalate_to_owner`) |
| 0.5.0 | 2026-10-12 | Login & hak akses: `/auth/*` (sesi cookie, CSRF, 2FA TOTP wajib owner) dan `/users` (owner); error 409 untuk aturan database |
