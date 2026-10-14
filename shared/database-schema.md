# Database Schema (Design)

> **Status: Draft (kontrak hidup), diimplementasikan.** PostgreSQL 16 di clau-ai-agents: migrasi `0001` (skema + Constraint Wajib), `0002` (login), `0003` (kode cadangan 2FA), dan `0004` (workflow request → draft → QA → approval). Kontrak ini tetap sumber kebenaran: tabel di database dites sama dengan daftar di bawah (`backend/tests/test_db.py`), jadi perubahan skema dimulai dari dokumen ini. Detail implementasi: `clau-ai-agents/backend/README.md` § Database.

## Prinsip

- **Minimum data tamu.** Platform tidak menyimpan identitas tamu kecuali benar-benar dibutuhkan pilar aktif. Consent dan media disimpan di sistem client; platform hanya menyimpan **referensi opaque**.
- **Client code, bukan nama legal**, sebagai kunci (`client_code`, mis. `VCU`).
- **Label evidence** ikut tersimpan pada setiap klaim (enum 6 label, sama dengan schema brief).
- Tidak ada credential **akun platform client** (OTA, sosial media) di database aplikasi; credential itu di secret manager. Login staf/approver sendiri hanya disimpan sebagai hash Argon2id, secret 2FA terenkripsi.

## Entitas

| Tabel | Kolom utama | Catatan |
|---|---|---|
| `clients` | `client_code` (PK), `vertical`, `business_type`, `location_area`, `approver_role`, `simulation` (bool, default false), `created_at` | Tanpa kontak pribadi; kontak approver di workspace client. `simulation = true` = klien fiktif (pilot/SIMULASI): semua draft-nya otomatis mode `SIMULASI` |
| `fact_sheets` | `id`, `client_code` (FK), `version`, `approved_at`, `document_ref` | Isi mengikuti template fact sheet Pilar 1; `document_ref` opaque |
| `briefs` | `brief_id` (PK), `client_code` (FK), `schema_version`, `payload` (JSON), `status` | `payload` divalidasi terhadap `clau-ai-marketing/schemas/content-brief.schema.json` |
| `requests` | `id`, `client_code`, `intent`, `pillar`, `approval_min` (`L1`–`L3`), `text`, `deadline`, `impact` (0–3), `risk` (0–3), `priority`, `status` (`open`/`in_progress`/`approved`/`rejected`/`closed`), `requested_by` (FK users, null = sistem/seed), `requested_by_role`, `created_at` | Hasil orchestrator: `pillar` & `approval_min` dari router (registry), `priority` dari priority engine. `text` = permintaan kerja, tanpa data pribadi tamu |
| `drafts` | `id`, `request_id` (FK), `brief_id` (FK), `fact_sheet_id` (FK, nullable), `skill`, `version`, `content` (text), `mode` (`NYATA`/`SIMULASI`), `created_by` (FK users, nullable bila dibuat agent), `agent_id` | Satu baris per versi (versi = max + 1 per request, dihitung server); tanpa data pribadi tamu. `mode` = dari `clients.simulation` |
| `claims` | `id`, `draft_id` (FK), `text`, `category`, `evidence_label`, `source`, `source_date`, `implied` (bool), `fact_key` (nullable) | Termasuk klaim tersirat. `fact_key` = kunci fakta di fact sheet klien (format `^[a-z0-9]+([._-][a-z0-9]+)*$`, ≤ 64), wajib untuk kategori faktual |
| `qa_records` | `id`, `draft_id` (FK), `gate`, `result` (`Pass`/`Conditional`/`Fail`/`N/A`), `reviewer_id` (FK users, null = agent), `reviewer_role`, `independent` (bool), `created_at` | `independent=false` untuk self-review AI/creator |
| `approvals` | `id`, `draft_id` (FK, versi yang disetujui), `level` (`L1`–`L3`), `decision`, `approver_id` (FK users), `approver_role`, `channel_ref`, `decided_at`, `mode` | Mode SIMULASI tidak bisa `Approved`; approval terikat ke **versi** draft. `channel_ref` = referensi bukti tertulis (email/pesan arsip; skema `https://`, `mailto:`, `workspace://`), wajib bila agency mencatat Approved (semua level) |
| `publications` | `id`, `draft_id` (FK), `channel`, `published_at`, `url_ref`, `published_by_role` | Diisi manusia setelah publish |
| `consent_refs` | `id`, `client_code`, `consent_ref` (opaque), `scope`, `valid_until` | **Tidak** menyimpan nama/foto; hanya referensi ke consent register client |
| `users` | `id`, `display_name`, `email`, `locale` (`id`/`en`), `timezone` (`Asia/Jakarta`/`Asia/Makassar`/`Asia/Jayapura`), `salutation`, `created_at`; login: `password_hash` (Argon2id), `must_change_password`, `totp_secret_enc`, `totp_enabled`, `totp_last_counter`, `failed_logins`, `locked_until`, `disabled_at`, `last_login_at` | Akun Portal/Studio (staf agency & approver client), bukan tamu. Email unik tanpa beda huruf besar/kecil |
| `mfa_recovery_codes` | `id`, `user_id` (FK), `code_hash` (HMAC-SHA256), `created_at`, `used_at` | 10 kode cadangan 2FA sekali pakai (HP hilang); kode asli hanya ditampilkan sekali saat dibuat |
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
users 1─n notifications ; users 1─n sessions ; users 1─n mfa_recovery_codes ; audit_log → semua objek
```

## Constraint Wajib (saat implementasi)

| Constraint | Alasan |
|---|---|
| `approvals.decision = 'Approved'` hanya bila `mode = 'NYATA'` | Mode SIMULASI tidak pernah approved |
| `publications` hanya bila keputusan **terakhir** draft itu Approved dan draft = versi terbaru request | Tidak ada publish tanpa approval yang masih berlaku |
| Approval L2/L3 butuh claim verification independen **terakhir** yang lulus (`Pass`/`Conditional`); Fail yang lebih baru membatalkan | Review independen |
| `claims.evidence_label = 'DATA FINAL'` wajib `source` dan `source_date` | Traceability (selaras schema brief v1.2+) |
| Reviewer `independent = true` ≠ `drafts.created_by` (dan bukan agent) | Pembuat tidak boleh me-review drafnya sendiri (rule 08) |
| `approvals` Approved (semua level) ditolak bila draft punya klaim ber-`fact_key` yang belum dikonfirmasi: `drafts.fact_sheet_id` kosong, fact sheet belum `approved_at`, atau tidak ada `fact_confirmations` (`confirmed`/`corrected`) untuk `fact_key` itu di fact sheet tersebut → `facts_unconfirmed` | Tombol *Setujui* terkunci di UI juga ditegakkan di server |
| `approvals` Approved hanya untuk versi draft tertinggi di request yang sama (request dikunci saat cek) → `approval_version_mismatch` | Approval terikat versi terbaru; tidak ada race dengan draft baru |
| `approvals.level` (semua keputusan) ≥ level minimum draft: `requests.approval_min` (`risk = 3` → L3 saat request dibuat), naik ke L2 bila draft punya klaim ber-`fact_key` → `approval_level_too_low` | Konten L2 tidak bisa diputuskan sebagai L1 untuk melewati review independen |
| `approvals` (semua keputusan) oleh pembuat draft (`drafts.created_by`) ditolak → `approval_by_author` | Tidak ada self-approve (AI-CONSTITUTION §4, rule 08) |
| Approved oleh peran agency (`owner`/`content_lead`), semua level, wajib `channel_ref` → `approval_needs_written_evidence` | Rule 08: persetujuan dari klien; agency hanya mencatat persetujuan tertulis klien |
| `approvals.approver_role` / `qa_records.reviewer_role` harus ada di `memberships` user itu (klien request atau agency) → `approval_role_mismatch` / `qa_role_mismatch`; `qa_records.independent` hanya owner/content_lead → `independent_review_not_allowed` | Database tidak percaya peran yang dikirim aplikasi |
| Draft/approval baru untuk request berstatus `approved`/`rejected`/`closed` ditolak → `request_closed` | Revisi setelah selesai = request baru |
| Klaim kategori faktual (`facility`, `location`, `price`, `rating`, `certification`, `halal-dietary`, `food-beverage`, `treatment`, `capacity`, `safety`, `license`, `itinerary`) wajib `fact_key` berawalan kategorinya (`facility.pool-private`) | Setiap fakta bisa ditelusuri ke fact sheet; konfirmasi fakta kategori lain tidak bisa dipinjam |
| `drafts.brief_id` / `drafts.fact_sheet_id` milik klien yang sama dengan request → `draft_client_mismatch`; `drafts.mode` = mode klien → `draft_mode_mismatch` | Tidak ada data lintas klien di satu draft |
| `claims` tidak bisa diubah/dihapus, dan tidak bisa ditambah setelah draft punya QA/approval; `qa_records`, `approvals`, `fact_confirmations` append-only; `fact_sheets` yang sudah `approved_at` dibekukan → `draft_version_immutable` / `decision_record_append_only` | Jejak keputusan tidak bisa ditulis ulang |
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
| Mode draft (2026-10-14, migrasi `0004`) | `SIMULASI` bila `clients.simulation`, selain itu `NYATA`; ditentukan server, tidak bisa dipilih pengirim |
| Klien SIMULASI saat upgrade (migrasi `0004`) | Hanya daftar eksplisit klien fiktif seed (`CTHVILLA`, `CTHCAFE`, `CTHWED`, `CTHTRIP`) ditandai `simulation = true`; tidak ada tebakan dari awalan kode. Klaim faktual lama tanpa kunci diberi `fact_key = <kategori>.legacy-<id>` (tidak pernah cocok dengan fact sheet, jadi tetap fail closed) |
| Status request (0004) | `open` → `in_progress` (draft dibuat / Revise) → `approved` / `rejected` (approval versi terbaru); `closed` disiapkan untuk penutupan manual |
| Isi draft | Baris versi yang tersimpan tidak bisa diubah; revisi = versi baru (approval terikat versi) |
| Enum lain | `clients.vertical` & `claims.category` = `content-brief.schema.json`; `requests.priority` = priority engine (`Low`/`Normal`/`High`/`Urgent`) |

## Open Items

- **CLIENT CONFIRMATION:** pilihan database (PostgreSQL disarankan untuk JSON + constraint) dan lokasi hosting (data residency Indonesia?).
- ~~NEXT ACTION: buat migration awal saat backend butuh persistence.~~ Selesai 2026-10-12 (migrasi `0001`–`0003`).
- ~~NEXT ACTION: hubungkan klaim ke fakta (`claims.fact_key` + `drafts.fact_sheet_id`).~~ Selesai 2026-10-14 (migrasi `0004`, berlaku untuk semua level, bukan hanya L2/L3).
- **NEXT ACTION:** endpoint kelola klien, fact sheet, dan Konfirmasi Fakta (`fact_confirmations`) belum ada; sampai ada, approval untuk draft dengan klaim faktual tetap terkunci (fail closed).
- Tabel `users`, `memberships`, `fact_confirmations`, `notifications`, `audit_log` ditambahkan 2026-10-06 agar sesuai spesifikasi UI (repo `CLAU-AI-CONTENT/design/`).
