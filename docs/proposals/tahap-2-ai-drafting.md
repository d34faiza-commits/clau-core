# Usulan — Tahap 2: AI Menulis Draft

> **Status: Draft (usulan, belum diputuskan).** Ditulis 2026-10-15 atas perintah owner Dea Karisna (d34faiza) ("mulai merancang Tahap 2 — gass"). Board: TASK-052 (`CLAU-AI-CONTENT/tasks/in-progress.md`). Dokumen ini **tidak** mengubah aturan Approved. Bagian § 4 berisi teks usulan untuk AI-BOUNDARY yang baru berlaku setelah perintah owner.

## 1. Tujuan & Batas

**Tujuan.** Agent (Tara dan teman-teman, 12 agent di `clau-ai-agents/agents/registry.json`) menulis **draft** dari request di platform: draft + daftar klaim, langsung masuk alur Tahap 1 (QA → review independen → approval tertulis klien).

**Batas yang tidak berubah** (AI-CONSTITUTION §4, §4a; Rule 08):

| Batas | Penegakan |
|---|---|
| AI hanya **Level B (draft)**. Tidak publish, tidak kirim ke pihak luar, tidak self-approve | Tidak ada endpoint publish; database menolak approval/QA independen oleh agent (`approval_by_author`, `independent_review_not_allowed`) |
| Fakta hanya dari fact sheet yang dikonfirmasi klien | Prompt hanya membawa fakta dari fact sheet berstatus disetujui; klaim faktual wajib `fact_key`; approval tetap terkunci `facts_unconfirmed` |
| Klien SIMULASI tetap SIMULASI | `drafts.mode` dari `clients.simulation` (database) |
| Data tamu tidak dikirim mentah ke provider | § 4 (aturan data) + filter penyamaran sebelum panggilan + test |
| Level C (komplain serius, hukum, kesehatan, keselamatan, data sensitif) | Router mengeskalasi; worker menolak membuat draft untuk intent/pilar *Planned* |

**Di luar Tahap 2:** Level A (kirim otomatis), pilar 2–5, visual AI, integrasi platform sosial.

## 2. Arsitektur

```text
Studio (tombol "Buat draft dengan AI")
   │  POST /requests/{id}/ai-drafts          ← cek peran, isolasi klien, budget, tombol mati
   ▼
ai_jobs (antrean di PostgreSQL)               ← status queued → running → succeeded / failed
   │  worker mengambil: SELECT … FOR UPDATE SKIP LOCKED
   ▼
Worker (container terpisah, image backend yang sama)
   1. rakit prompt: [aturan + skill + persona] (cache) → [fakta klien DATA FINAL + brief] → [request]
   2. saring data: penyamaran pola data pribadi; tolak bila ada data Restricted
   3. panggil Claude API (output terstruktur: draft + klaim)
   4. validasi hasil (schema, fact_key ada di fact sheet, panjang, kata terlarang Rule 02/06)
   5. simpan drafts (created_by NULL, agent_id) + claims lewat aturan database Tahap 1
   6. catat ai_calls (token, biaya, stop_reason; tanpa isi prompt/jawaban)
   ▼
qa_records gate otomatis (independent = false) → review manusia → approval klien
```

**Kenapa antrean di PostgreSQL** (bukan Redis/broker baru): database sudah ada, ter-backup tiap 6 jam + B2, transaksi bersama tabel draft. `FOR UPDATE SKIP LOCKED` cukup untuk ribuan job/hari. Worker tambahan (server lain) tinggal menyambung ke database yang sama (rancangan skala: TASK-061).

**Kenapa worker terpisah dari backend:** API key provider hanya diberikan ke container worker (backend tidak memegangnya); panggilan AI yang lambat tidak membuat login/dashboard lambat; worker bisa diperbanyak tanpa menyentuh backend.

## 3. Komponen

### 3.1 Tabel baru (kontrak: `shared/database-schema.md`, migrasi `0006`)

| Tabel | Kolom utama | Aturan |
|---|---|---|
| `ai_jobs` | `id`, `request_id` (FK), `agent_id`, `intent`, `kind` (`draft`), `status` (`queued`/`running`/`succeeded`/`failed`/`cancelled`), `attempts`, `max_attempts`, `run_after`, `locked_at`, `locked_by`, `error_code`, `draft_id` (FK, hasil), `requested_by` (FK users), `created_at`, `finished_at` | Satu job aktif per request (unik parsial); hanya intent pilar aktif; job klien SIMULASI tetap boleh (hasil mode SIMULASI); `error_code` dari daftar tetap, bukan teks error provider |
| `ai_calls` | `id`, `job_id` (FK), `provider`, `model`, `prompt_version`, `input_tokens`, `output_tokens`, `cache_read_tokens`, `cache_write_tokens`, `cost_micro_usd`, `stop_reason`, `provider_request_id`, `latency_ms`, `created_at` | **Append-only**; tanpa isi prompt/jawaban (isi ada di `drafts`); dasar dashboard biaya (TASK-058) |
| `ai_budgets` | `scope` (`global` / `client_code`), `month`, `limit_micro_usd`, `alert_at_pct` | Job baru ditolak `ai_budget_exceeded` bila biaya bulan berjalan + perkiraan job > batas |

### 3.2 Model & pengaturan (keputusan owner di § 6)

| Tugas | Model awal | Pengaturan |
|---|---|---|
| Draft konten (caption, reel script, OTA listing, review reply, kalender, kampanye) | `claude-opus-5-5` | `output_config.effort` per intent (mulai `medium`, naik ke `high` hanya bila eval membuktikan perlu); thinking adaptif (bawaan model ini) |
| QA otomatis awal (cek klaim vs fakta, kata terlarang, panjang) | Kode deterministik dulu (`check_caption.py` dan sejenisnya); model hanya untuk penilaian yang tidak bisa dicek kode | Hasil `qa_records` dengan `independent = false` |
| Tugas mekanis (format ulang, ringkasan internal) | Kandidat `claude-haiku-5-5` | **Hanya** setelah eval membuktikan kualitas setara, dan atas keputusan owner (menurunkan model demi biaya adalah keputusan owner, bukan AI) |

- **Output terstruktur** (`output_config.format` dengan JSON schema / `client.messages.parse`): `{content, claims: [{text, category, evidence_label, fact_key, implied}], notes_for_reviewer}`. Jawaban yang tidak lolos schema = job gagal, tidak ada draft setengah jadi.
- **Penolakan (refusal):** cek `stop_reason` sebelum membaca isi; fallback server-side bawaan (`fallbacks: "default"`) diaktifkan supaya penolakan keliru tidak menghentikan job; penolakan final = job `failed` dengan `error_code = refused`, request kembali ke manusia.
- **Prompt caching:** urutan prompt dari paling stabil ke paling berubah: (1) aturan inti + rules pilar + skill + persona + voice guide (sama untuk semua klien per agent, di-cache), (2) fakta klien + brief (di-cache per klien bila dipakai berulang), (3) teks request. Tanpa jam/ID acak di bagian awal (merusak cache). Cache hit dipantau dari `cache_read_tokens`.
- **Batch API** (biaya lebih rendah, hasil tidak langsung): untuk pekerjaan massal yang tidak mendesak, mis. kalender konten bulanan semua klien. Tidak dipakai untuk tombol "Buat draft" yang ditunggu staf.
- **Versi prompt:** `prompt_version` = hash isi skill/persona/rules yang dipakai, dicatat di `ai_calls`; perubahan prompt = versi baru yang harus lulus eval.

### 3.3 Pengaman

| Pengaman | Rincian |
|---|---|
| Tombol mati | `CLAU_AI_ENABLED=0` (global, di `.env`) dan `ai_enabled` per intent di registry; mati = endpoint menolak `ai_disabled`, worker berhenti mengambil job |
| Gerbang eval | Agent hanya bisa dipakai bila 33 kasus `agents/evals` lulus untuk `prompt_version` aktif (otomatis + rubrik manusia, `post-vps-checklist.md` langkah 2) |
| Batas biaya | `ai_budgets` (global + per klien) + batas pengeluaran bulanan di konsol provider sebagai pagar terakhir; peringatan di 80% |
| Batas laju | Maks job paralel per worker; retry dengan jeda bertambah untuk 429/5xx; 4xx tidak di-retry |
| Input tak tepercaya | Review/DM tamu dibungkus sebagai data (bukan instruksi) dan disamarkan; isi request staf tidak pernah bisa mengubah aturan sistem |
| Rahasia | API key hanya di `.env` VPS 2 (600 root), diteruskan ke container `worker` saja; tidak pernah di log/audit/notifikasi |
| Jejak | `audit_log`: `ai_job.created`, `ai_job.succeeded`/`failed`; draft agent tercatat `agent_id` + `prompt_version` |

### 3.4 API & UI (kontrak: `shared/api-contracts.md`)

- `POST /requests/{id}/ai-drafts` → `202 {job_id}` (peran `owner`/`content_lead`/`content_staff`, klien sesuai membership).
- `GET /ai-jobs/{id}` → status, `draft_id` bila selesai, `error_code` bila gagal.
- `POST /ai-jobs/{id}/cancel` (sebelum `running`).
- `GET /ai-usage?month=` (owner): biaya per klien/agent, sisa budget.
- UI Studio: tombol **Buat draft dengan AI** di halaman request, status job, draft masuk daftar versi seperti draft manual dengan label agent; halaman owner **Pemakaian AI**.

## 4. Usulan teks AI-BOUNDARY — "Data ke Provider AI" (keputusan VPS #5)

> Usulan, belum berlaku. Ditambahkan ke AI-BOUNDARY (versi minor baru) **hanya** atas perintah Pak Indra atau Dea Karisna.

1. Yang boleh dikirim ke provider AI: aturan/skill/persona/knowledge reusable; fakta klien yang sudah dikonfirmasi (DATA FINAL) dan brief; teks request staf; review/DM tamu **setelah** penyamaran (`<NAMA_TAMU>`, `<NO_BOOKING>`, `<KONTAK>`).
2. Tidak pernah dikirim: data `Restricted` (credential, data pembayaran, data kesehatan, identitas resmi), nama/kontak/nomor booking/kamar tamu yang belum disamarkan, data klien lain.
3. Setiap panggilan dicatat (`ai_calls`: model, token, biaya, waktu) tanpa menyimpan isi prompt di log.
4. Provider, model, wilayah pemrosesan, dan masa simpan data di provider dicatat per environment di `shared/integrations.md`; klien dengan syarat data khusus = **CLIENT CONFIRMATION** sebelum datanya diproses.
5. API key hanya di server (VPS 2, `.env` 600), tidak pernah di repo, log, atau chat.

## 5. Rencana Implementasi (setelah § 6 diputuskan)

| PR | Isi | Bisa jalan tanpa API key? |
|---|---|---|
| 4a | Kontrak core: § 4 masuk AI-BOUNDARY (bila disetujui), `database-schema.md` (3 tabel + constraint), `api-contracts.md` (endpoint + kode error), `integrations.md` | Ya |
| 4b | Migrasi `0006`, endpoint job, worker dengan **provider tiruan** (deterministik), budget, tombol mati, test (antrean paralel, retry, isolasi klien, budget, SIMULASI) | Ya |
| 4c | Provider Claude: perakit prompt + caching, output terstruktur, penyamaran, validasi klaim, fallback refusal, pencatatan biaya; runner eval ke output nyata | Ya untuk test (provider tiruan); uji nyata di VPS 2 dengan key owner |
| 4d | UI Studio (tombol, status, label agent) + halaman Pemakaian AI | Ya |

Setiap PR: test + audit adversarial independen + CI hijau, sama seperti Tahap 1. Aktivasi per agent setelah eval lulus.

## 6. Keputusan Owner yang Dibutuhkan

| # | Keputusan | Usulan AI |
|---|---|---|
| 1 | Provider AI | Claude API (Anthropic), sesuai `integrations.md` |
| 2 | Model default & rute murah | Draft: `claude-opus-5-5`. Rute `claude-haiku-5-5` hanya untuk tugas mekanis yang lolos eval, diputuskan per intent oleh owner |
| 3 | Teks § 4 masuk AI-BOUNDARY | Setuju/ubah |
| 4 | Batas biaya bulanan (global & per klien) | Owner menentukan angka; pagar kedua di konsol provider |
| 5 | Akun & billing provider | Atas nama siapa, siapa pemegang key (key dibuat owner, dimasukkan langsung ke server) |
| 6 | Masa simpan data di provider | Cek kebijakan provider yang berlaku saat akun dibuat; catat di `integrations.md` |
| 7 | Agent pertama yang diaktifkan | Usulan: Pilar 1 intent `caption` (paling sering, eval paling lengkap), lalu bertahap |

## 7. Risiko

| Risiko | Mitigasi |
|---|---|
| **RISK:** AI mengarang fakta | Fakta hanya dari fact sheet; klaim faktual wajib `fact_key` yang ada; approval terkunci tanpa konfirmasi klien |
| **RISK:** Biaya melonjak | Budget global + per klien, pagar di konsol provider, Batch untuk massal, caching |
| **RISK:** Kualitas turun diam-diam saat prompt berubah | `prompt_version` + gerbang eval |
| **RISK:** Data pribadi terkirim | Penyamaran + test pola + aturan § 4 + review isi `ai_calls` tanpa konten |
| **RISK:** Provider tidak tersedia | Retry terbatas, job `failed` jelas, staf tetap bisa menulis draft manual (alur Tahap 1 tidak bergantung AI) |
| **ASSUMPTION:** Volume awal kecil (< 100 draft/hari) | Satu worker di VPS 2 cukup; ukur antrean sebelum menambah server |
