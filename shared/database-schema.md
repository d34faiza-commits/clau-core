# Database Schema (Design)

> **Status: Draft design.** Belum ada database yang diimplementasikan. Backend scaffold di clau-ai-agents belum memakai database. Schema ini adalah kontrak awal supaya pilar dan platform memakai bentuk data yang sama.

## Prinsip

- **Minimum data tamu.** Platform tidak menyimpan identitas tamu kecuali benar-benar dibutuhkan pilar aktif. Consent dan media disimpan di sistem client; platform hanya menyimpan **referensi opaque**.
- **Client code, bukan nama legal**, sebagai kunci (`client_code`, mis. `VCU`).
- **Label evidence** ikut tersimpan pada setiap klaim (enum 6 label, sama dengan schema brief).
- Tidak ada credential di database aplikasi; credential di secret manager.

## Entitas

| Tabel | Kolom utama | Catatan |
|---|---|---|
| `clients` | `client_code` (PK), `vertical`, `business_type`, `location_area`, `approver_role`, `created_at` | Tanpa kontak pribadi; kontak approver di workspace client |
| `fact_sheets` | `id`, `client_code` (FK), `version`, `approved_at`, `document_ref` | Isi mengikuti template fact sheet Pilar 1; `document_ref` opaque |
| `briefs` | `brief_id` (PK), `client_code` (FK), `schema_version`, `payload` (JSON), `status` | `payload` divalidasi terhadap `clau-ai-marketing/schemas/content-brief.schema.json` |
| `requests` | `id`, `client_code`, `intent`, `pillar`, `priority`, `status`, `requested_by_role`, `created_at` | Hasil orchestrator (router + priority engine) |
| `drafts` | `id`, `request_id` (FK), `brief_id` (FK), `skill`, `version`, `content` (text), `mode` (`NYATA`/`SIMULASI`) | Konten draft; tanpa data pribadi tamu |
| `claims` | `id`, `draft_id` (FK), `text`, `category`, `evidence_label`, `source`, `source_date`, `implied` (bool) | Termasuk klaim tersirat |
| `qa_records` | `id`, `draft_id` (FK), `gate`, `result` (`Pass`/`Conditional`/`Fail`/`N/A`), `reviewer_role`, `independent` (bool), `created_at` | `independent=false` untuk self-review AI/creator |
| `approvals` | `id`, `draft_id` (FK), `level` (`L1`–`L3`), `decision`, `approver_role`, `channel_ref`, `decided_at`, `mode` | Mode SIMULASI tidak bisa `Approved` |
| `publications` | `id`, `draft_id` (FK), `channel`, `published_at`, `url_ref`, `published_by_role` | Diisi manusia setelah publish |
| `consent_refs` | `id`, `client_code`, `consent_ref` (opaque), `scope`, `valid_until` | **Tidak** menyimpan nama/foto; hanya referensi ke consent register client |

## Relasi

```text
clients 1─n fact_sheets
clients 1─n briefs 1─n drafts 1─n claims
clients 1─n requests 1─n drafts 1─n qa_records
drafts 1─n approvals ; drafts 1─n publications
clients 1─n consent_refs
```

## Constraint Wajib (saat implementasi)

| Constraint | Alasan |
|---|---|
| `approvals.decision = 'Approved'` hanya bila `mode = 'NYATA'` | Mode SIMULASI tidak pernah approved |
| `publications` hanya bila ada `approvals` Approved untuk draft yang sama | Tidak ada publish tanpa approval |
| Approval L2/L3 butuh minimal satu `qa_records.independent = true` untuk gate claim verification | Review independen |
| `claims.evidence_label = 'DATA FINAL'` wajib `source` dan `source_date` | Traceability (selaras schema brief v1.2+) |

## Open Items

- **CLIENT CONFIRMATION:** pilihan database (PostgreSQL disarankan untuk JSON + constraint) dan lokasi hosting (data residency Indonesia?).
- **NEXT ACTION:** buat migration awal saat backend butuh persistence.
