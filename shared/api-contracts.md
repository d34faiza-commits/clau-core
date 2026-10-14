# API Contracts

Kontrak HTTP antara frontend dan backend clau-ai-agents, dan antara platform dengan konsumen lain. Endpoint bertanda **Implemented** sudah ada di backend; sisanya **Planned**.

## Prinsip

- JSON, UTF-8, timestamp ISO 8601 dengan zona waktu.
- Tidak ada endpoint yang **publish** ke platform sosial/OTA atau **mengirim** pesan ke tamu. Release dilakukan manusia (Constitution §4.7).
- Tidak ada endpoint yang menerima credential platform client.
- Error: `{"error": {"code": "<snake_case>", "message": "<teks>"}}` untuk semua error, termasuk validasi request (422 `validation_error`).
- **Autentikasi** (0.5.0): sesi cookie dari `POST /auth/login`. Setiap request yang mengubah data (POST/PUT/PATCH/DELETE) wajib header `X-CSRF-Token` (dari `Me.csrf_token`) dan Origin aplikasi. Selama `Me.next` ≠ `ready` (ganti password sementara / aktifkan 2FA wajib owner), hanya endpoint `/auth/*` yang bisa dipakai (403 `password_change_required` / `mfa_setup_required`). Tidak ada pendaftaran publik: owner pertama dibuat lewat CLI server. Browser tidak memanggil backend langsung; frontend meneruskan `/api/*` ke backend (keputusan VPS #1).
- Pelanggaran aturan database (Constraint Wajib) = 409 dengan kode aturan, mis. `approval_needs_independent_review`, tanpa detail SQL. Daftar lengkap: § Kode Aturan Approval (sumber tunggal; UI & desain merujuk ke sini).

## Endpoint

| Method & path | Status | Request | Response |
|---|---|---|---|
| `GET /health` | **Implemented** | — | `{"status": "ok", "service": "clau-ai-agents-backend", "version": "<semver>"}` |
| `GET /agents` | **Implemented** | — | `{"agents": [Agent]}` dari `agents/registry.json` |
| `GET /pillars` | **Implemented** | — | `{"pillars": [Pillar]}` dari `agents/registry.json` → `pillars`, plus `agents` (id agent per pilar) |
| `POST /route` | **Implemented** (statis) | `{"intent": "<intent>"}` | `{"intent", "agent", "pillar", "skill", "repo", "approval_min", "autonomy_max": "A"\|"B"\|"C", "status": "active"\|"planned", "next_step": "produce_draft"\|"escalate_to_owner"}`. Intent tidak dikenal → 404 `unknown_intent`; body tidak valid → 422 `validation_error` |
| `POST /auth/login` | **Implemented** (0.5.0) | `{email, password, totp_code? \| recovery_code?}` | `Me` + cookie sesi `__Host-clau_session` (`HttpOnly; Secure; SameSite=Lax`). 401 `invalid_credentials` (sama untuk email tidak terdaftar), 401 `mfa_required` / `invalid_mfa_code`, 429 `too_many_attempts` (5 gagal = kunci 15 menit), 403 `origin_not_allowed` |
| `GET /auth/me` | **Implemented** (0.5.0) | — (cookie) | `Me` |
| `POST /auth/logout` | **Implemented** (0.5.0) | — | 204, sesi dicabut |
| `POST /auth/logout-all` | **Implemented** (0.6.0) | — | 204, semua sesi user dicabut (termasuk sesi ini) |
| `POST /auth/password` | **Implemented** (0.5.0) | `{current_password, new_password}` | `Me` + cookie baru; sesi lain dicabut. 422 `weak_password` (min. 12 karakter, NIST SP 800-63B) |
| `POST /auth/mfa/setup` · `POST /auth/mfa/confirm` | **Implemented** (0.5.0; QR & kode cadangan 0.6.0) | — · `{code}` | `{secret, otpauth_uri, qr_svg}` · `Me` + `recovery_codes` (10, ditampilkan sekali) + cookie baru (TOTP RFC 6238, kode tidak bisa dipakai ulang) |
| `POST /auth/mfa/recovery-codes` | **Implemented** (0.6.0) | `{password}` | `{recovery_codes}`: 10 kode baru, yang lama batal. Password salah dihitung gagal login |
| `GET /users` · `POST /users` | **Implemented** (0.5.0), owner | — · `{display_name, email, temporary_password, locale?, timezone?, memberships[]}` | `{users: [User]}` · `User` (wajib ganti password saat login pertama) |
| `PUT /users/{id}/memberships` · `POST /users/{id}/disable` · `POST /users/{id}/enable` | **Implemented** (0.5.0), owner | `[{scope, role, max_level}]` · — · — | `User`; sesi user target dicabut. 409 `last_owner` / `cannot_disable_self` |
| `POST /requests` | **Implemented** (0.7.0) | `{client_code, intent, text, deadline?, impact?, risk?}` | 201 `Request`; `pillar`/`approval_min` dari registry, `priority` dari priority engine. 422 `unknown_intent`, 404 `client_not_found`, 403 `forbidden` |
| `GET /requests` · `GET /requests/{id}` | **Implemented** (0.7.0) | query `client_code?`, `status?`, `limit?`, `offset?` | `Page<Request>` · `Request`. 403 `forbidden` (client_code di luar akses), 404 `not_found` |
| `POST /drafts` | **Implemented** (0.7.0) | `{request_id, brief_id?, fact_sheet_id?, content, claims: [ClaimIn]}` | 201 `Draft` (+ `claims`); `version`, `skill`, `mode`, `created_by` diisi server. 409 `intent_not_active` (pilar/agent planned), `draft_client_mismatch`, 422 `claim_fact_key_required` |
| `GET /drafts` · `GET /drafts/{id}` | **Implemented** (0.7.0) | query `request_id?`, `client_code?`, `limit?`, `offset?` | `Page<DraftSummary>` · `Draft` (+ `claims`, `latest`) |
| `POST /qa-records` | **Implemented** (0.7.0) | `{draft_id, gate, result, independent}` | 201 `QARecord`; `reviewer_id`/`reviewer_role` dari sesi. 403 `independent_review_not_allowed`, 409 `qa_reviewer_is_author` |
| `GET /qa-records` · `GET /qa-records/{id}` | **Implemented** (0.7.0) | query `draft_id?`, `limit?`, `offset?` | `Page<QARecord>` · `QARecord` |
| `POST /approvals` | **Implemented** (0.7.0) | `{draft_id, level, decision, channel_ref?}` | 201 `Approval`; `approver_id`/`approver_role`/`mode` diisi server, status request diperbarui. 403 `level_not_allowed`, 409 kode § Kode Aturan Approval |
| `GET /approvals` · `GET /approvals/{id}` | **Implemented** (0.7.0) | query `draft_id?`, `limit?`, `offset?` | `Page<Approval>` · `Approval` |

Semua endpoint workflow butuh login siap (`Me.next = ready`); `POST` juga CSRF + Origin. Body menolak field lain (`extra = forbid`): peran, id user, mode, versi, pilar, dan prioritas **tidak pernah** diterima dari pengirim. Setiap `POST` menulis `audit_log` di transaksi yang sama (tanpa isi konten). Tidak ada endpoint publish/kirim ke platform atau tamu.

### Matriks Izin Workflow (Rule 08)

Sesuai `clau-ai-marketing/rules/08-APPROVAL-PUBLICATION-STANDARD.md`. Peran dari `memberships`; level dibatasi `max_level` (scope klien diutamakan, lalu agency).

| Peran | Baca | Buat request | Tulis draft | QA | Approval |
|---|---|---|---|---|---|
| `owner`, `content_lead` (agency) | Semua klien | Ya | Ya | Ya; `independent = true` hanya bila bukan pembuat draft | L1: Ya. L2/L3: hanya mencatat persetujuan tertulis klien (`channel_ref` wajib untuk Approved) |
| `content_staff` (agency) | Semua klien | Ya | Ya | Hanya `independent = false` (pre-check) | Tidak |
| `client_approver` (klien X) | Klien X | Ya, klien X | Tidak | Tidak | Ya, klien X, sampai `max_level` |
| `viewer` (klien X) | Klien X | Tidak | Tidak | Tidak | Tidak |

Data klien lain: detail → 404 `not_found` (keberadaan objek tidak dibocorkan); list/tulis dengan `client_code` di luar akses → 403 `forbidden`. Level approval > `max_level` → 403 `level_not_allowed`.

Paginasi: `limit` 1–100 (default 50), `offset` 0–10000 (default 0); urutan terbaru dulu. `Page<T>` = `{items: [T], total, limit, offset}`.

## Kode Aturan Approval

Semua 409 dengan bentuk error kontrak. **Implemented** = ditegakkan trigger database (migrasi 0001, backend 0.4.0+) dan diteruskan backend apa adanya; **Planned** = dibuat bersama endpoint workflow (Tahap 1 PR 3).

| Aturan | Kode | Status |
|---|---|---|
| Reviewer independen ≠ pembuat draft | `qa_reviewer_is_author` | Implemented |
| Approval L2/L3 butuh claim verification independen yang lulus | `approval_needs_independent_review` | Implemented |
| Mode approval = mode draft | `approval_mode_mismatch` | Implemented |
| Isi draft versi lama tidak bisa diubah (simpan versi baru) | `draft_version_immutable` | Implemented |
| Tandai tayang butuh approval Approved | `publication_without_approval` | Implemented |
| `audit_log` tidak bisa diubah/dihapus | `audit_log_append_only` | Implemented |
| *Setujui* (semua level) butuh semua klaim ber-`fact_key` dikonfirmasi di fact sheet draft yang sudah approved | `facts_unconfirmed` | Implemented (0.7.0) |
| Approved hanya untuk versi draft tertinggi di request | `approval_version_mismatch` | Implemented (0.7.0) |
| Level approval ≥ `approval_min` intent (router) | `approval_level_too_low` | Implemented (0.7.0) |
| Pembuat draft tidak boleh menyetujui drafnya sendiri | `approval_by_author` | Implemented (0.7.0) |
| L2/L3 Approved oleh agency wajib bukti tertulis klien (`channel_ref`) | `approval_needs_written_evidence` | Implemented (0.7.0) |
| Brief/fact sheet draft milik klien request; mode draft = mode klien | `draft_client_mismatch` / `draft_mode_mismatch` | Implemented (0.7.0) |
| Klaim, QA, dan approval tidak bisa diubah/dihapus setelah tersimpan | `draft_version_immutable` / `decision_record_append_only` | Implemented (0.7.0) |

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

Workflow (0.7.0):

- `Request` = `{id, client_code, intent, pillar, agent, approval_min, text, deadline, impact, risk, priority, priority_score, status, requested_by, requested_by_role, created_at}`. `priority_score` = urgensi (dari `deadline`) + `impact` + `risk` (default 1 dan 1) sesuai `orchestrator/priority-engine.md`.
- `ClaimIn` = `{text, category, evidence_label, source?, source_date?, implied?, fact_key?}` (maks. 30 klaim per draft); `Claim` = `ClaimIn` + `id`.
- `DraftSummary` = `{id, request_id, client_code, brief_id, fact_sheet_id, skill, version, mode, created_by, agent_id, created_at, latest}`; `Draft` = `DraftSummary` + `content`, `claims: [Claim]`.
- `QARecord` = `{id, draft_id, gate, result, reviewer_id, reviewer_role, independent, created_at}`.
- `Approval` = `{id, draft_id, level, decision, approver_id, approver_role, channel_ref, mode, decided_at}`.

`Me` = `{user: User, mfa_required, must_change_password, next: "ready"|"password_change"|"mfa_setup", active_sessions, recovery_codes_left, csrf_token}`. `User` = `{id, display_name, email, locale, timezone, salutation, memberships: [{scope, role, max_level}], mfa_enabled, disabled, last_login_at}` (tanpa hash atau secret). `GET /users` juga mengembalikan `clients` (daftar `client_code`) untuk form peran.

## Versioning

- Versi API mengikuti versi backend (SemVer). Perubahan breaking = MAJOR dan dicatat di README backend.

| Versi backend | Tanggal | Perubahan |
|---|---|---|
| 0.1.0 | 2026-10-04 | Scaffold: `/health`, `/agents`, `/route` |
| 0.2.0 | 2026-10-06 | Error memakai bentuk kontrak (sebelumnya terbungkus `detail`); `/route` menambah `agent` dan `next_step` (planned → `escalate_to_owner`) |
| 0.3.0 | 2026-10-09 | `GET /pillars` (pilar jadi sumber tunggal di registry) |
| 0.4.0 | 2026-10-09 | 5 pilar v2 dan `autonomy_max` per agent (AI-CONSTITUTION v3.0.0) |
| 0.5.0 | 2026-10-12 | Login & hak akses: `/auth/*` (sesi cookie, CSRF, 2FA TOTP wajib owner) dan `/users` (owner); error 409 untuk aturan database |
| 0.6.0 | 2026-10-13 | QR 2FA, kode cadangan, keluar semua perangkat, `Me.active_sessions` / `recovery_codes_left`; penguatan hasil audit (timing, race 2FA & owner terakhir, brute force ganti password) |
| 0.7.0 | 2026-10-14 | Workflow request → draft → QA → approval (`/requests`, `/drafts`, `/qa-records`, `/approvals`), matriks izin Rule 08, kode aturan baru (`facts_unconfirmed`, `approval_version_mismatch`, `approval_level_too_low`, `approval_by_author`, `approval_needs_written_evidence`, `draft_client_mismatch`, `draft_mode_mismatch`, `decision_record_append_only`) |
