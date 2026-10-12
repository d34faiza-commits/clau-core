# Database Schema (Design)

> **Status: Draft (kontrak hidup), diimplementasikan.** PostgreSQL 16 di clau-ai-agents: migrasi `0001` (skema + Constraint Wajib) dan `0002` (login). Kontrak ini tetap sumber kebenaran: tabel di database dites sama dengan daftar di bawah (`backend/tests/test_db.py`), jadi perubahan skema dimulai dari dokumen ini. Detail implementasi: `clau-ai-agents/backend/README.md` § Database.

## Prinsip

- **Minimum data tamu.** Platform tidak menyimpan identitas tamu kecuali benar-benar dibutuhkan pilar aktif. Consent dan media disimpan di sistem client; platform hanya menyimpan **referensi opaque**.
- **Client code, bukan nama legal**, sebagai kunci (`client_code`, mis. `VCU`).
- **Label evidence** ikut tersimpan pada setiap klaim (enum 6 label, sama dengan schema brief).
- Tidak ada credential **akun platform client** (OTA, sosial media) di database aplikasi; credential itu di secret manager. Login staf/approver sendiri hanya disimpan sebagai hash Argon2id, secret 2FA terenkripsi.

## Entitas

| Tabel | Kolom utama | Catatan |
|---|---|---|
| `clients` | `client_code` (PK), `vertical`, `business_type`, `location_area`, `approver_role`, `created_at` | Tanpa kontak pribadi; kontak approver di workspace client |
| `fact_sheets` | `id`, `client_code` (FK), `version`, `approved_at`, `document_ref` | Isi mengikuti template fact sheet Pilar 1; `document_ref` opaque |
| `briefs` | `brief_id` (PK), `client_code` (FK), `schema_version`, `payload` (JSON), `status` | `payload` divalidasi terhadap `clau-ai-marketing/schemas/content-brief.schema.json` |
| `requests` | `id`, `client_code`, `intent`, `pillar`, `priority`, `status`, `requested_by_role`, `created_at` | Hasil orchestrator (router + priority engine) |
| `drafts` | `id`, `request_id` (FK), `brief_id` (FK), `skill`, `version`, `content` (text), `mode` (`NYATA`/`SIMULASI`), `created_by` (FK users, nullable bila dibuat agent), `agent_id` | Satu baris per versi; tanpa data pribadi tamu |
| `claims` | `id`, `draft_id` (FK), `text`, `category`, `evidence_label`, `source`, `source_date`, `implied` (bool) | Termasuk klaim tersirat |
| `qa_records` | `id`, `draft_id` (FK), `gate`, `result` (`Pass`/`Conditional`/`Fail`/`N/A`), `reviewer_id` (FK users, null = agent), `reviewer_role`, `independent` (bool), `created_at` | `independent=false` untuk self-review AI/creator |
| `approvals` | `id`, `draft_id` (FK, versi yang disetujui), `level` (`L1`–`L3`), `decision`, `approver_id` (FK users), `approver_role`, `channel_ref`, `decided_at`, `mode` | Mode SIMULASI tidak bisa `Approved`; approval terikat ke **versi** draft |
| `publications` | `id`, `draft_id` (FK), `channel`, `published_at`, `url_ref`, `published_by_role` | Diisi manusia setelah publish |
| `consent_refs` | `id`, `client_code`, `consent_ref` (opaque), `scope`, `valid_until` | **Tidak** menyimpan nama/foto; hanya referensi ke consent register client |
| `users` | `id`, `display_name`, `email`, `locale` (`id`/`en`), `timezone` (`Asia/Jakarta`/`Asia/Makassar`/`Asia/Jayapura`), `salutation`, `created_at`; login: `password_hash` (Argon2id), `must_change_password`, `totp_secret_enc`, `totp_enabled`, `totp_last_counter`, `failed_logins`, `locked_until`, `disabled_at`, `last_login_at` | Akun Portal/Studio (staf agency & approver client), bukan tamu. Email unik tanpa beda huruf besar/kecil |
| `sessions` | `token_hash` (PK, SHA-256 token cookie), `user_id` (FK), `mfa_ok`, `created_at`, `last_seen_at`, `expires_at`, `revoked_at` | Sesi login di server; token asli hanya di cookie `HttpOnly; Secure`. `mfa_ok=false` = 2FA wajib belum aktif |
| `memberships` | `user_id` (FK), `scope` (`agency` / `client_code`), `role` (`owner`/`content_lead`/`content_staff`/`viewer`/`client_approver`), `max_level` (`L1`–`L3`) | Izin per klien; klien hanya melihat `client_code` miliknya |
| `fact_confirmations` | `id`, `fact_sheet_id` (FK), `fact_key`, `value_before`, `value_after`, `decision` (`confirmed`/`corrected`), `confirmed_by` (FK users), `confirmed_at` | Hasil fitur **Konfirmasi Fakta** di Portal; `confirmed` = bukti tertulis owner → klaim boleh `DATA FINAL` |
| `notifications` | `id`, `user_id` (FK), `type`, `object_ref`, `channel` (`in_app`/`email`/`whatsapp`), `sent_at`, `read_at` | Tanpa isi pesan sensitif; link ke objek |
| `audit_log` | `id`, `actor_id` (FK users, null = system/agent), `action`, `object_type`, `object_id`, `meta` (JSON), `created_at` | Append-only: approve, tandai tayang, ubah fakta, ubah akses, ubah setting |

## Relasi

```text
clients 1─n fact_sheets
clients 1─n briefs 1─n drafts 1─n claims
clients 1─n requests 1─n drafts 1─n qa_records
drafts 1─n approvals ; drafts 1─n publications
clients 1─n consent_refs
users 1─n memberships n─1 clients ; fact_sheets 1─n fact_confirmations
users 1─n notifications ; users 1─n sessions ; audit_log → semua objek
```

## Constraint Wajib (saat implementasi)

| Constraint | Alasan |
|---|---|
| `approvals.decision = 'Approved'` hanya bila `mode = 'NYATA'` | Mode SIMULASI tidak pernah approved |
| `publications` hanya bila ada `approvals` Approved untuk draft yang sama | Tidak ada publish tanpa approval |
| Approval L2/L3 butuh minimal satu `qa_records.independent = true` untuk gate claim verification | Review independen |
| `claims.evidence_label = 'DATA FINAL'` wajib `source` dan `source_date` | Traceability (selaras schema brief v1.2+) |
| Reviewer `independent = true` ≠ `drafts.created_by` (dan bukan agent) | Pembuat tidak boleh me-review drafnya sendiri (rule 08) |
| `approvals` untuk L2/L3 ditolak bila fact sheet klien masih punya fakta terpakai yang belum `confirmed` | Tombol *Setujui* terkunci di UI juga ditegakkan di server |
| `audit_log` tidak bisa di-update/delete dari aplikasi | Jejak keputusan |
| Query Portal selalu difilter `memberships.scope = client_code` | Isolasi data antar klien |

## Keputusan Implementasi (2026-10-12)

Detail yang belum diatur kontrak dan ditetapkan saat implementasi (clau-ai-agents migrasi `0001`):

| Item | Nilai |
|---|---|
| `approvals.decision` | `Approved` / `Revise` / `Rejected` |
| `qa_records.gate` | `claim-verification`, `content-review`, `privacy-rights-review`, `visual-ai-review`, `publication-checklist` (= file di `clau-ai-marketing/qa/`) |
| Review independen yang dihitung untuk L2/L3 | gate `claim-verification`, `independent = true`, hasil `Pass` atau `Conditional` (pengecualian terkontrol dengan approval tertulis) |
| Mode approval | Harus sama dengan mode draft yang disetujui |
| Isi draft | Baris versi yang tersimpan tidak bisa diubah; revisi = versi baru (approval terikat versi) |
| Enum lain | `clients.vertical` & `claims.category` = `content-brief.schema.json`; `requests.priority` = priority engine (`Low`/`Normal`/`High`/`Urgent`) |

## Open Items

- **CLIENT CONFIRMATION:** pilihan database (PostgreSQL disarankan untuk JSON + constraint) dan lokasi hosting (data residency Indonesia?).
- ~~NEXT ACTION: buat migration awal saat backend butuh persistence.~~ Selesai 2026-10-12 (migrasi `0001`, `0002`).
- **NEXT ACTION:** Constraint Wajib "approval L2/L3 ditolak bila fakta terpakai belum `confirmed`" belum bisa ditegakkan: kontrak belum menghubungkan draft/klaim ke `fact_key`. Usulan: `claims.fact_key` + `drafts.fact_sheet_id`, lalu trigger (Tahap 1 PR 3 di clau-ai-agents).
- Tabel `users`, `memberships`, `fact_confirmations`, `notifications`, `audit_log` ditambahkan 2026-10-06 agar sesuai spesifikasi UI (repo `CLAU-AI-CONTENT/design/`).
