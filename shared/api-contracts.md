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
| `POST /requests` | **Implemented** (0.7.0) | `{client_code, intent, text, deadline?, impact?, risk?}` | 201 `Request`; `pillar`/`approval_min` dari registry (`risk = 3` → `L3`, rule 08), `priority` dari priority engine. 422 `unknown_intent`, 404 `client_not_found`, 403 `forbidden` |
| `GET /requests` · `GET /requests/{id}` | **Implemented** (0.7.0) | query `client_code?`, `status?`, `limit?`, `offset?` | `Page<Request>` · `Request`. 403 `forbidden` (client_code di luar akses), 404 `not_found` |
| `POST /drafts` | **Implemented** (0.7.0) | `{request_id, brief_id?, fact_sheet_id?, content, claims: [ClaimIn]}` | 201 `Draft` (+ `claims`); `version`, `skill`, `mode`, `created_by` diisi server. 409 `intent_not_active` (pilar/agent planned), `draft_client_mismatch`, `request_closed`, 422 `claim_fact_key_required` / `claim_source_required` |
| `GET /drafts` · `GET /drafts/{id}` | **Implemented** (0.7.0) | query `request_id?`, `client_code?`, `limit?`, `offset?` | `Page<DraftSummary>` · `Draft` (+ `claims`, `latest`) |
| `POST /qa-records` | **Implemented** (0.7.0) | `{draft_id, gate, result, independent}` | 201 `QARecord`; `reviewer_id`/`reviewer_role` dari sesi. 403 `independent_review_not_allowed`, 409 `qa_reviewer_is_author` |
| `GET /qa-records` · `GET /qa-records/{id}` | **Implemented** (0.7.0) | query `draft_id?`, `limit?`, `offset?` | `Page<QARecord>` · `QARecord` |
| `POST /approvals` | **Implemented** (0.7.0) | `{draft_id, level, decision, channel_ref?}` | 201 `Approval`; `approver_id`/`approver_role`/`mode` diisi server, status request diperbarui. 403 `level_not_allowed`, 409 kode § Kode Aturan Approval |
| `GET /approvals` · `GET /approvals/{id}` | **Implemented** (0.7.0) | query `draft_id?`, `limit?`, `offset?` | `Page<Approval>` · `Approval` |
| `GET /clients` · `POST /clients` | **Implemented** (0.8.0); POST owner | — · `{client_code, vertical, business_type, location_area?, approver_role, simulation?}` | `{items: [Client]}` (hanya klien yang boleh dilihat) · 201 `Client`. 409 `client_exists` |
| `POST /fact-sheets` | **Implemented** (0.8.0) | `{client_code, document_ref, facts: [FactIn]}` (1–100 fakta) | 201 `FactSheetDetail`; `version`, `created_by` diisi server, belum disetujui. 403 `forbidden` (bukan staf agency), 404 `client_not_found` |
| `GET /fact-sheets` · `GET /fact-sheets/{id}` | **Implemented** (0.8.0) | query `client_code?`, `approved?`, `limit?`, `offset?` | `Page<FactSheet>` (urut klien, versi terbaru dulu) · `FactSheetDetail` |
| `POST /fact-sheets/{id}/confirmations` | **Implemented** (0.8.0) | `{fact_key, decision: "confirmed"\|"corrected", value_after?, channel_ref?}` | 201 `FactAnswer`; `value_before`, `confirmed_by`, `confirmed_by_role` diisi server. 409 `fact_not_in_sheet`, `fact_sheet_frozen`, `approval_by_author`, `approval_needs_written_evidence` |
| `POST /fact-sheets/{id}/approve` | **Implemented** (0.8.0) | `{approval_ref?}` | 200 `FactSheetDetail`. 409 `facts_unconfirmed`, `fact_sheet_empty`, `fact_sheet_frozen`, `approval_by_author`, `approval_needs_written_evidence` |

Semua endpoint workflow butuh login siap (`Me.next = ready`); `POST` juga CSRF + Origin. Body maks. 64 KB (413 `payload_too_large`); teks di-trim, teks kosong atau berisi karakter NUL = 422 `validation_error`; nilai di luar batas database = 422 `invalid_input`. Body menolak field lain (`extra = forbid`): peran, id user, mode, versi, pilar, dan prioritas **tidak pernah** diterima dari pengirim. Setiap `POST` menulis `audit_log` di transaksi yang sama (tanpa isi konten). Tidak ada endpoint publish/kirim ke platform atau tamu.

### Matriks Izin Workflow (Rule 08)

Sesuai `clau-ai-marketing/rules/08-APPROVAL-PUBLICATION-STANDARD.md`. Peran dan `max_level` selalu diambil dari **satu membership yang sama**: membership agency diutamakan, lalu membership scope klien itu. Database mengecek ulang bahwa `approver_role`/`reviewer_role` benar-benar peran user tersebut (`approval_role_mismatch` / `qa_role_mismatch`).

| Peran | Baca | Buat request | Tulis draft | QA | Approval |
|---|---|---|---|---|---|
| `owner`, `content_lead` (agency) | Semua klien | Ya | Ya | Ya; `independent = true` hanya bila bukan pembuat draft | Semua level: Approved hanya mencatat persetujuan tertulis klien (`channel_ref` wajib); Revise/Rejected boleh tanpa bukti |
| `content_staff` (agency) | Semua klien | Ya | Ya | Hanya `independent = false` (pre-check) | Tidak |
| `client_approver` (klien X) | Klien X | Ya, klien X | Tidak | Tidak | Ya, klien X, sampai `max_level` |
| `viewer` (klien X) | Klien X | Tidak | Tidak | Tidak | Tidak |

Data klien lain: detail → 404 `not_found` (keberadaan objek tidak dibocorkan); list/tulis dengan `client_code` di luar akses → 403 `forbidden`. Level approval > `max_level` → 403 `level_not_allowed` (untuk **semua** keputusan, termasuk Revise/Rejected).

Aturan keputusan (semua ditegakkan database, berlaku untuk Approved, Revise, dan Rejected): pembuat draft tidak memutuskan drafnya sendiri; level ≥ level minimum draft; request yang sudah selesai (`approved`/`rejected`/`closed`) tidak menerima draft atau keputusan baru (`request_closed`, revisi = request baru). Level minimum draft = `approval_min` request, naik ke `L2` bila draft memuat klaim ber-`fact_key` (rule 08: klaim fasilitas/harga = L2). Yang dihitung untuk L2/L3 = claim verification independen **terakhir** (Fail setelah Pass membatalkan).

`channel_ref` (bukti tertulis) hanya menerima skema `https://`, `mailto:`, atau `workspace://` (tanpa spasi/karakter kontrol, maks. 500); skema lain (mis. `javascript:`) = 422.

### Konfirmasi Fakta (0.8.0)

Alur `design/user-flow/client-portal-flow.md` § Konfirmasi Fakta, ditegakkan database (migrasi `0005`):

1. Staf agency (`owner`/`content_lead`/`content_staff`) menyusun versi fact sheet + daftar fakta. Versi = max + 1 per klien; belum disetujui.
2. Setiap fakta dijawab **klien**: `confirmed` (nilai benar) atau `corrected` + `value_after` (nilai yang benar). Yang menjawab: `client_approver` klien itu (berapa pun `max_level`-nya), atau `owner`/`content_lead` yang mencatat jawaban tertulis klien dengan `channel_ref`. Pembuat fact sheet tidak menjawab faktanya sendiri. Jawaban append-only; yang berlaku = jawaban terakhir per fakta. `value_before` = nilai fakta saat dijawab (diisi database).
3. Fact sheet disetujui (sekali) setelah **semua** fakta dijawab, oleh peran yang sama (agency wajib `approval_ref`; bukan pembuatnya). Sesudah disetujui fact sheet, faktanya, dan jawabannya beku: perubahan = versi baru.
4. Draft yang klaimnya ber-`fact_key` bisa di-approve hanya bila `drafts.fact_sheet_id` = fact sheet yang disetujui lewat alur ini (ada penyetujunya), setiap kunci klaim ada di daftar faktanya, dan versi itu adalah versi disetujui **terbaru** klien (`fact_sheet_superseded`: versi lama yang sudah dikoreksi tidak bisa dipakai lagi; simpan draft versi baru). Reviewer & approver melihat nilai yang dijawab klien (termasuk koreksi) di samping setiap klaim.

Koreksi wajib mengubah nilai (`fact_value_unchanged`; nilai sama = pilih `confirmed`). `fact_key` fakta = `<kategori>.<nama>`. Teks yang hanya berisi spasi/karakter tak terlihat = kosong; referensi bukti/dokumen menolak karakter kontrol dan karakter format tak terlihat (zero-width, bidi override). `staff`/`viewer` tidak menjawab atau menyetujui (403); klien lain 404. Nilai fakta adalah data klien: tidak ditulis ke `audit_log`.

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
| Request selesai tidak menerima draft/keputusan baru | `request_closed` | Implemented (0.7.0) |
| Peran yang dicatat = peran user di `memberships` (klien request / agency) | `approval_role_mismatch` / `qa_role_mismatch` | Implemented (0.7.0) |
| Review independen hanya owner/content lead | `independent_review_not_allowed` | Implemented (0.7.0; API 403, database 409) |
| Approved hanya untuk versi draft tertinggi di request | `approval_version_mismatch` | Implemented (0.7.0) |
| Level keputusan ≥ level minimum draft (`approval_min`; risk 3 = L3; klaim fakta = min. L2) | `approval_level_too_low` | Implemented (0.7.0) |
| Pembuat draft tidak boleh memutuskan (Approved/Revise/Rejected) drafnya sendiri | `approval_by_author` | Implemented (0.7.0) |
| Approved oleh agency (semua level) wajib bukti tertulis klien (`channel_ref`) | `approval_needs_written_evidence` | Implemented (0.7.0) |
| Brief/fact sheet draft milik klien request; mode draft = mode klien | `draft_client_mismatch` / `draft_mode_mismatch` | Implemented (0.7.0) |
| Klaim, QA, approval, dan konfirmasi fakta tidak bisa diubah/dihapus; fact sheet yang sudah approved dibekukan | `draft_version_immutable` / `decision_record_append_only` | Implemented (0.7.0) |
| Fakta hanya ditambah dan dijawab selama fact sheet belum disetujui | `fact_sheet_frozen` | Implemented (0.8.0) |
| Jawaban hanya untuk fakta yang ada di versi fact sheet itu | `fact_not_in_sheet` | Implemented (0.8.0) |
| Koreksi fakta wajib berisi nilai yang benar, dan berbeda dari nilai awal | `fact_value_required` (API 422 `validation_error`) / `fact_value_unchanged` | Implemented (0.8.0) |
| Approved untuk draft berklaim fakta: fact sheet disetujui klien lewat alur 0.8.0, kunci ada di daftar fakta, versi disetujui terbaru | `facts_unconfirmed` / `fact_sheet_superseded` | Implemented (0.8.0) |
| Fact sheet tanpa fakta tidak bisa disetujui; semua fakta wajib dijawab | `fact_sheet_empty` / `facts_unconfirmed` | Implemented (0.8.0) |
| Fact sheet baru belum disetujui; perubahan fact sheet hanya persetujuan; versi berurutan | `fact_sheet_approval_flow` / `fact_sheet_version_sequence` | Implemented (0.8.0) |
| Penjawab/penyetuju fakta: approver klien, atau agency dengan bukti tertulis; bukan pembuat fact sheet | `approval_role_mismatch` / `approval_needs_written_evidence` / `approval_by_author` | Implemented (0.8.0) |
| Tandai tayang: keputusan terakhir draft = Approved dan draft = versi terbaru | `publication_without_approval` | Implemented (0.7.0, diperketat) |

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

Klien & fakta (0.8.0):

- `Client` = `{client_code, vertical, business_type, location_area, approver_role, simulation, created_at}`. `approver_role` = jabatan approver di bisnis klien (mis. owner, GM), bukan nama orang.
- `FactIn` = `{fact_key, category, label, value}`: `category` kategori faktual; `fact_key` = `<kategori>.<nama>`, unik per fact sheet; `label` ≤ 200, `value` ≤ 1000.
- `FactSheet` = `{id, client_code, version, document_ref, created_by, created_at, approved_at, approved_by, approved_by_role, approval_ref, status: "pending"|"ready"|"approved", facts_total, facts_answered}`. `ready` = semua fakta sudah dijawab, menunggu disetujui.
- `FactSheetDetail` = `FactSheet` + `facts: [{fact_key, category, label, value, status: "pending"|"confirmed"|"corrected", current_value, answers: [FactAnswer]}]`. `current_value` = koreksi terakhir, atau `value`.
- `FactAnswer` = `{id, fact_sheet_id, fact_key, decision, value_before, value_after, confirmed_by, confirmed_by_role, channel_ref, confirmed_at}`.

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
| 0.7.0 | 2026-10-14 | Workflow request → draft → QA → approval (`/requests`, `/drafts`, `/qa-records`, `/approvals`), matriks izin Rule 08, kode aturan baru (`facts_unconfirmed`, `approval_version_mismatch`, `approval_level_too_low`, `approval_by_author`, `approval_needs_written_evidence`, `draft_client_mismatch`, `draft_mode_mismatch`, `decision_record_append_only`, `request_closed`, `approval_role_mismatch`, `qa_role_mismatch`; 422 `invalid_input`), body maks. 64 KB |
| 0.8.0 | 2026-10-14 | Klien (`/clients`), fact sheet & Konfirmasi Fakta (`/fact-sheets`, jawaban klien, persetujuan fact sheet); kode aturan `fact_sheet_frozen`, `fact_not_in_sheet`, `fact_value_required`, `fact_value_unchanged`, `fact_sheet_superseded`, `fact_sheet_empty`, `fact_sheet_approval_flow`, `fact_sheet_version_sequence`, `client_exists` |
