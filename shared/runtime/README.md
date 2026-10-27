---
document_title: "Hospitality Runtime — H1 Core Contracts"
document_owner: "Dea Karisna / AI Marketing"
version: "1.0.0"
status: "For Review"
classification: "Internal"
---

# Hospitality Runtime — H1

**Status: For Review; belum terhubung ke worker, API, atau database production.**
Kontrak ini menyiapkan Golden Path Tara (`caption-writer`, intent `caption`, Pilar 1)
sesuai blueprint Hospitality Agent Runtime v1.0 yang diberikan owner pada
2026-10-27. Schema, fixtures, dan conformance tests tersedia; H2–H7 belum selesai.
Semua contoh fiktif **SIMULASI**, bukan hasil model atau bukti approval manusia.

[AI-CONSTITUTION](../../AI-CONSTITUTION.md), [AI-BOUNDARY](../../AI-BOUNDARY.md),
[API aktif](../api-contracts.md), dan [database aktif](../database-schema.md)
tetap berlaku. H1 tidak mengaktifkan pilar 2–5, external write tool, atau Level A.

## 1. Sumber kontrak dan batas enforcement

- [JSON Schema Draft 2020-12](./v1/contracts.schema.json): pilih `#/$defs/<nama>`;
  root sengaja menolak payload tanpa tipe kontrak. Semua object menolak field tambahan.
- [Error registry](./v1/error-codes.json): kode stabil dan retry policy authoritative.
- [Fixtures](./v1/examples.json): bentuk payload yang valid. Digest placeholder adalah
  data uji, **bukan bundle yang dapat dipasang**; file `fixture/*` tidak disertakan.
- [Reference checks](../../scripts/runtime_contracts.py): schema + invariant lintas field,
  pemilihan memory dan fingerprint. Bukan authorization middleware atau worker runtime.
- [Tests](../../tests/test_runtime_contracts.py): positive/negative conformance.

| Kontrak | Producer yang dipercaya | Consumer dan tujuan |
|---|---|---|
| `PromptBundle` | Build/CI setelah review | Loader: manifest immutable + digest semua komponen |
| `Provenance` | Server/retrieval terotorisasi | Context assembler: source/version/client/sensitivity |
| `MemoryRecord` | Server setelah keputusan manusia | Retrieval: approved, validity, scope, provenance |
| `WorkPlan` | Planner (untrusted sampai divalidasi) | Server menentukan draft/clarify/escalate dan tool yang boleh |
| `ToolContract` | Registry server | Tool runner: read-only, server-bound scope, timeout, output bound |
| `TaraGeneration` | Provider (untrusted) | Validator: 3 variants atau clarification/escalation tanpa draft |
| `ValidationResult` | Server validators + critic sebagai self-review | Review UI; tidak pernah menjadi approval |
| `AgentRun` | Worker/server | Audit metadata per attempt; provenance hingga draft/hash |
| `Usage` | Adapter provider yang diverifikasi | Ledger append-only, integer micro-USD, termasuk call gagal |
| `RuntimeError` | Server/adapter | Stable error mapping; bukan pesan mentah provider |

Schema-valid bukan berarti fakta benar atau data aman. String berisi instruksi
berbahaya tetap **data**, bukan instruction. Authorization, redaction, rights/consent,
claim reconciliation, database membership, dan independent approval harus ditegakkan
server di H3–H5. Test schema tidak boleh dilaporkan sebagai penetration test atau eval AI.

## 2. Bundle, taxonomy, dan fingerprint

`PromptBundle` wajib membawa constitution, boundary, rules (seluruh rule yang relevan,
minimal 01/08/09), skill, persona, hospitality voice/humanize guide, vertical/platform
knowledge, prompt template, output schema, validator configuration, tool contracts,
dan escalation rules. Calendar ikut bila task membutuhkan tanggal/event lokal.
H2 menyusun isi sebenarnya; H3 memverifikasi checksum **exact bytes** terhadap
manifest yang dipin oleh deployment, lalu menolak symlink/path escape/missing files.
Checksum bukan pengganti trusted artifact provenance: manifest dari model tidak dipercaya.

Taxonomy `supported_verticals` mengikuti database sekarang; jenis usaha lebih spesifik
ada di `supported_business_types`, bukan enum database baru.

| Vertical canonical | Business types / knowledge selection |
|---|---|
| `accommodation` | villa, guesthouse, homestay, hotel, resort |
| `food-beverage` | restaurant, cafe, beach-club |
| `spa-wellness` | spa, wellness, retreat |
| `wedding-event` | wedding-event |
| `travel-tour` | travel-tour |
| `experience` | tourism-experience |

`prompt_version` = SHA-256 penuh (64 lowercase hex) atas canonical JSON manifest:

1. Copy manifest; urutkan `components` berdasarkan `path` (path unik).
2. Sort object keys, UTF-8 tanpa BOM, tanpa ASCII escaping, tanpa whitespace di separator.
3. Array selain `components` mempertahankan urutan. Integer untuk numeric model settings
   (`temperature_milli` = temperature × 1000); tidak ada floating point di hash basis.
4. Hash bytes tersebut. Jangan masukkan field hash dirinya sendiri.

Hash mencakup manifest, exact component digests, model/provider/settings, tool dan
validator versions. Perubahan satu komponen membutuhkan regression eval sebelum promosi.
File output schema dan validator config aktual harus masuk components, bukan nama saja.
Adapter wajib menolak setting unsupported; jangan diam-diam memakai default provider.

`context_sha256` terpisah: SHA-256 canonical JSON context yang **benar-benar dikirim**
setelah redaction, termasuk provenance/version, brief, Voice Card, facts dan safe asset
context. H3 harus mendefinisikan context schema sebelum mengimplementasikan hash ini.
Context hash tidak mencampur data ke bundle global. Cache key minimal client_code +
prompt_version + context_sha256; cache provider reusable prefix tidak berisi data klien.

## 3. Memory dan provider boundary

Memory dibagi permanent approved, campaign, working, historical reference. Mapping
`memory_type` pada schema mengidentifikasi kegunaannya. Historical approved content
boleh menjadi contoh style, **tidak menjadi fakta baru**. Working memory tidak ikut
approved retrieval. Revisi manusia harus melewati review sebelum dipromosikan.

Retrieval melakukan query scoped dengan client dari sesi/job, bukan model. Pilih hanya
status approved, approved_at ≤ now, valid_from ≤ now < valid_until (null = tidak ada
expiry), belum superseded, sensitivity bukan Restricted. Approved fact wajib
`DATA FINAL` dengan sumber fact sheet aktif; key/nilai harus cocok ke konfirmasi terbaru.
`approved_memory_eligible()` hanya reference predicate setelah scoped lookup: tidak
membuktikan membership, bahwa sumber masih terbaru, atau izin provider.

`MemoryRecord.source` adalah referensi operational, bukan raw source document.
Sensitivity source dan record harus sama; tidak boleh downgrade. Content/metadata
request, OCR, review, tools tetap untrusted. Brief tidak boleh mengalahkan approved facts.
Conflicting facts → clarification; expired facts → re-confirm; Restricted data → stop.

Provider gate harus memeriksa **semua context sources**, bukan request text saja;
redaction nama/room/booking/contact, minimization, client scope, rights, consent,
retention requirement dan allowlist berlaku sebelum panggilan. Approved internal note
bukan otomatis boleh dikirim ke provider. Setelah model selesai, ulangi gate konteks.

## 4. Planner, tools, dan generation

Planner menyimpan hasil operasional (decision, fakta perlu/tersedia/hilang, angle,
format, risk flags, selected tools), **bukan hidden reasoning**. Server memverifikasi
missing facts, risk flags dan tool selection; model tidak menetapkan akses atau approval.

Tool registry terverifikasi memuat input/output schema sebagai pinned components.
`client_scope=server_bound`: runner menyuntikkan client scope dari job, menolak argumen
scope/role yang dikirim model, lalu memeriksa provenance setiap hasil. Tidak ada arbitrary
SQL/HTTP/filesystem atau external write. Tools wajib bounded timeout/result size, schema
validation, sensitivity gate dan metadata-only audit. Input/output schema aktual ada di
bundle H2; H1 tidak mengklaim tool sudah dibuat.

Tara menghasilkan:

- `draft`: persis 3 styles berbeda; semua factual/implied claims dipetakan ke indexes
  varian, termasuk hook, body, CTA, hashtags dan alt text. Alt text memakai `asset_id`
  agar tidak bergantung urutan array. Language per varian ID/EN; job bilingual memakai
  output terpisah per bahasa dan parity check, bukan 6 varian yang melanggar batas.
- `clarification_required`: pertanyaan spesifik, tanpa variants/claims.
- `escalation_required`: alasan untuk reviewer, tanpa variants/claims.

Maksimal 30 claims sesuai backend aktif. `fact_key=null` diperbolehkan di output model
untuk menampung kegagalan secara jujur, tetapi factual/implied unsupported claim wajib
FAIL di validation. Model tidak mengisi evidence label, approval level atau approval.
Kategori `other`/`experience` tidak boleh dipakai menghindari claim reconciliation.

Transport wajib membatasi total UTF-8 bytes (maksimal 64 KiB untuk generation), bukan
sekadar panjang masing-masing field. JSON duplicate keys/NaN/Infinity harus ditolak
sebelum schema validation. Aturan platform dari bundle terversi; schema **tidak**
menetapkan batas platform terkini. H2 perlu sumber, accessed_at, status, review_due.

## 5. Run lifecycle, retry, dan atomic persistence

`AgentRun` merepresentasikan satu attempt; bukan pengganti enum `ai_jobs.status`.

| Kondisi | Stage/status internal | Aksi server |
|---|---|---|
| Awal attempt | `running`, stage policy | Authorized job/lease/budget/kill switch diperiksa |
| Normal | policy → context → bundle → plan → tools → generate → validate → persist | Stage tools boleh dilewati bila tidak ada tool |
| Input kurang / perlu owner | `clarification_required` / `escalation_required` | Simpan outcome non-draft; butuh migrasi sebelum aktif |
| Validator fail/conditional | `validation_failed` | Simpan review evidence; tidak menjadi draft ready |
| Semua gate pass | `draft_ready`, stage persist | Draft/claims/QA/evidence/run disimpan transactionally |
| Error | `failed` + stable code | Retry hanya policy yang diizinkan; attempt baru |
| Cancel sebelum hasil aktif | `cancelled` | Tidak boleh menyimpan active draft; usage tetap dicatat |

Terminal run immutable; tidak bisa kembali `running`. Claim, QA dan approval terikat
latest immutable draft version + content hash; revisi membuat versi baru. Status
`draft_ready` berarti siap **review manusia**, tidak berarti approved atau published.

Worker memegang lease/fencing token dan memverifikasi token yang sama dalam transaksi
persist. Periksa ulang request belum closed, client masih aktif, membership/scope, kill
switch, current approved fact sheet/Voice Card/brief/asset validity. Stale context atau
lease_lost: jangan menulis active draft. Pengulangan memakai attempt/run baru dengan
context baru. Jangan retry selamanya ketika fakta terus berubah.

Provider retry: maksimal 3 attempts, exponential backoff + bounded jitter untuk
provider_unavailable/worker_timeout. Timeout bisa tetap ditagih; jangan menganggap biaya
nol. Tool timeout: bounded retry dalam budget/lease yang sama. `invalid_output` hanya
satu repair call (tercatat usage), lalu fail; bukan retry seluruh job tanpa batas.
`refused`, policy/tenant/rights error, budget dan validation failure tidak auto-retry.

Usage disimpan append-only walau call ditolak, timeout, stale, cancelled, atau lease
hilang; unik per call/attempt agar tidak double count. `billing_status=pending_reconciliation`
berarti angka belum final: pertahankan budget reservation, jangan membebaskan budget
berdasarkan biaya nol sementara. Provider error detail/prompt/response tidak masuk log.

## 6. Validator dan human review

Urutan H4: schema/size → claim format → reconciliation seluruh copy → approved-fact
matching → implied claims → platform → brand → privacy/rights → parity → visual
consistency → duplicates → server approval level → reviewer summary.

Claim coverage = factual spans yang punya valid provenance / semua factual spans
teridentifikasi; jika tidak ada factual span, bernilai 1. Menghitung claim list dari
model saja tidak membuktikan coverage. Deterministic checks mengikat nilai, tanggal,
angka, enum, roles dan scope; semantic claim completeness memerlukan critic dan human
review. Jangan mengklaim deteksi implied claim 100% hanya karena schema lulus.

`pass`: errors kosong, coverage 1, siap human review. `conditional`: action dengan owner
role dan resolution evidence wajib; tidak ready sampai semua action ditangani dan
validation baru dijalankan. `fail`: errors jelas, tidak ready. Critic selalu self-review.
H4 harus memblok approval DB jika validation yang berlaku masih conditional/fail.

Risk flags tambahan pada WorkPlan belum menjadi `draft_flags` database. H4 memetakan
child/UGC → people; health/safety/legal → crisis; dietary/certification, availability,
testimonial → claim validation; translation → source-level inheritance. Model flags
hanya saran, server wajib mendeteksi ulang dan tidak boleh menurunkan min level.

Level final = maksimum aturan backend aktif: request minimum, flags, klaim, level source
translation, dan **minimal L2 untuk draft AI klien NYATA**. Peminta job dianggap pembuat;
bukan independent reviewer atau approver. Agency yang merekam persetujuan klien wajib
bukti tertulis; SIMULASI tidak pernah menjadi Approved untuk publikasi.

## 7. Compatibility dan migration gate H3–H5

**H1 menambah kontrak terpisah versi 1.0.0; API/backend aktif tetap 0.10.0.**
Tidak menambah tabel ke daftar Entitas aktif, tidak mengubah CHECK/enum secara implisit.

| Gap sekarang | Prasyarat aktivasi downstream |
|---|---|
| `Generation.content` string + claims | Adapter Tara variants → immutable draft content, claim variant map, asset IDs; golden compatibility tests |
| `prompt_version` sekarang 16 hex dari system text | Migrasi/cek kapasitas kolom, dukung legacy read dan full 64 hex untuk run baru; simpan bundle/model/settings provenance |
| AiJob succeeded wajib draft_id | Migrasi eksplisit outcome non-draft + API/UI clarification/escalation; jangan menyamarkan sebagai sukses dengan draft kosong |
| Error enum 10 kode lama | Tambah error baru lewat migrasi + kontrak API/DB bersama; registry `legacy_job_code=null` berarti belum boleh ditulis ke enum lama |
| Belum ada durable run/memory/validation evidence | Rancang tabel/index/FK scoped client, append-only events, timestamps, version/hash dan retention; SQL test sesuai source contract |
| Cancel hanya queued | Running cancellation membutuhkan endpoint + lease/fencing checks; tidak berubah lewat schema H1 |
| Approved facts belum punya per-fact expiry | Migrasi validity + source freshness checks sebelum mengaktifkan memory retrieval |
| QA Conditional kini bisa diterima | Gate validation baru wajib unresolved=0; migration/test jangan mengendurkan existing independent review |
| Approval belum memakai content hash eksplisit | Ikat validation/approval ke exact persisted bytes + latest version; DB transaction/race tests |

Upgrade berurutan: owner merge H1 → CI main core → bot pin core di agent → bot pin
agent/core di market. H2 bundle content dan H3 runtime di feature branch masing-masing;
jangan mengubah submodule sebelum commit sumber tersedia. Tidak perlu paid provider
untuk menguji H1. Provider real baru H5 setelah konfigurasi secret secara aman, budget,
retention/region dan eval dipenuhi; API key tidak diminta lewat chat.

Kill switch dapat menghentikan layanan. Rollback bundle/model yang sudah live tetap
mengikuti AI-BOUNDARY: perintah eksplisit owner dengan target; H1 tidak memberi izin
rollback otomatis versi live. Rehearsal rollback dilakukan di staging/SIMULASI.

## 8. Delivery gates H1–H7

| Tahap | Deliverable / bukti |
|---|---|
| H1 (PR ini) | Contracts + synthetic fixtures + conformance tests + migration map; owner review |
| H2 | Bundle hospitality/Tara lengkap, schemas tool, platform references, eval matrix 50–60 cases dengan dimension coverage |
| H3 | Loader packaged immutable, scoped assembler, brief/Voice Card/facts/assets, provenance; migration & isolation tests |
| H4 | Validator pipeline + persisted evidence + reviewer UI + approval DB gates |
| H5 | Real provider structured output, mapped failures, ledger/budget/kill switches/redaction |
| H6 | Real model eval runner, metrics cost/latency, blind human rubric; tidak memakai fixture H1 sebagai quality evidence |
| H7 | SIMULASI end-to-end, adversarial runtime audit, independent human review, limited real client, approved feedback |

Production threshold: critical factual hallucination/leakage/privacy/injection success =
0 pada eval/pilot; schema valid ≥99%; deterministic pass ≥95%; human rubric rata-rata
≥4.2/5 tanpa dimensi <3; initial approval tanpa major revision ≥80%; bilingual factual
mismatch 0. Angka ini **target**, bukan hasil H1. Tidak menambah agent sebelum Tara stabil.

## 9. Verifikasi lokal dan self-review

```bash
python -m pip install -r scripts/requirements-contracts.txt
python scripts/validate_core.py
python scripts/runtime_contracts.py
python -m unittest discover -s tests -v
```

Self-review H1 memeriksa authority field injection, cross-client provenance, expiry dan
supersession memory, digest sensitivity, unsupported version, unsafe paths, claim
limits/category/index, clarification/escalation shape, conditional/fail gating, retry
policy, integer billing, dan error tanpa echo data. CI `validate` menjalankan semuanya.
Review independen manusia dan security audit runtime tetap belum dilakukan.

## Revision History

| Version | Date | Status | Summary |
|---|---|---|---|
| 1.0.0 | 2026-10-27 | For Review | H1 contracts Golden Path Tara, versioning, fixtures, negative tests dan migration gates |
