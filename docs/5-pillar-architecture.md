# 5-Pillar Architecture

> **Status: Draft.** Pilar 1 aktif. Pilar 2–5 adalah usulan kerja (**ASSUMPTION**) yang menunggu keputusan owner (**CLIENT CONFIRMATION**) soal nama, urutan, dan scope.

## Konsep v2 (usulan untuk masa depan)

Owner menyiapkan konsep 5 pilar yang lebih luas: **AI Marketing · AI Sales · AI Admin · AI Business Intelligence · AI Automation**, untuk banyak jenis usaha. Fokus sekarang tetap hospitality; tabel di bawah tetap yang berlaku sampai TASK-034 diputuskan. Cetak biru siap aktif: [blueprints/](./blueprints/README.md) · jenis usaha: [verticals.md](./verticals.md) · amandemen yang dibutuhkan: [proposals/autonomy-levels.md](./proposals/autonomy-levels.md).

## Lapisan

| Lapisan | Repo | Isi |
|---|---|---|
| **Foundation** | clau-ai-core | Constitution, boundary, pipeline, orchestrator, kontrak data |
| **Pilar** | clau-ai-<pilar> (1 repo per pilar) | Rules, skills, prompts, knowledge, templates, QA khusus domain |
| **Platform** | clau-ai-agents | UI, API, registry agent; menjalankan skill pilar, tidak menyimpan aturan |

Aturan mengalir **satu arah**: core → pilar → platform. Platform membaca skill pilar; pilar tidak bergantung pada platform.

## Pilar

| # | Pilar | Masalah yang diselesaikan | Contoh output | Rule kunci | Intent & agent | Status |
|---|---|---|---|---|---|---|
| 1 | **Marketing & Content** | Konten jujur & on-brand tanpa klaim palsu | Caption, reel script, story, listing OTA, balasan review, kalender | Klaim (rule 02), consent (04), approval (08) | 8 intent · Tara, Raka, Sekar, Bayu, Laras, Dimas, Ayu, Nara | **Aktif** (clau-ai-marketing) |
| 2 | Sales & Reservations | Inquiry cepat & akurat tanpa janji harga sembarangan | Draft balasan DM/WA soal harga & tanggal, paket | Harga & komitmen komersial, ketersediaan real-time | `inquiry-reply` · Galih | Planned |
| 3 | Guest Experience & Reputation | Komunikasi tamu konsisten & eskalasi komplain | Pesan pre-arrival, FAQ in-stay, eskalasi keluhan | Privacy tamu, keluhan serius = L3 | `guest-message` · Sari | Planned |
| 4 | Operations | Pengetahuan operasional terdokumentasi | SOP, checklist housekeeping/F&B, materi onboarding staf | Keselamatan, akurasi prosedur | `sop` · Teguh | Planned |
| 5 | Analytics & Insights | Keputusan berbasis data lintas pilar | Report bulanan, KPI dashboard | Angka apa adanya, tanpa atribusi palsu | `report` · Intan (aktif, sementara template `monthly-report` Pilar 1) | Planned |

### Sumber yang harus sinkron

| Data | Sumber | Ikut diperbarui |
|---|---|---|
| Nama, status, repo pilar | Tabel **5 Pilar CLAU AI** di [README](../README.md) | `clau-ai-agents/agents/registry.json` → `pillars` (dicek test), tabel di atas |
| Intent → pilar → agent | [orchestrator/router.md](../orchestrator/router.md) | `registry.json` → `agents` (dicek test) |
| Permukaan UI per pilar | `CLAU-AI-CONTENT/design/pillars.md` | Wireframe Studio & Portal, frontend clau-ai-agents |
| Rencana aktivasi | Board `CLAU-AI-CONTENT/tasks/` (TASK-034 keputusan owner, TASK-035–038 per pilar) | `clau-ai-agents/docs/post-vps-checklist.md` |

### Usulan nama repo pilar (**ASSUMPTION**)

Mengikuti pola `clau-ai-<pilar>`; final setelah TASK-034 diputuskan owner.

| # | Usulan repo |
|---|---|
| 2 | `clau-ai-sales` |
| 3 | `clau-ai-guest` |
| 4 | `clau-ai-operations` |
| 5 | `clau-ai-analytics` |

## Menambah Pilar

1. Owner menyetujui scope pilar (catat di Revision History [AI-CONSTITUTION](../AI-CONSTITUTION.md)).
2. Buat repo `clau-ai-<pilar>` (private) dengan struktur seperti clau-ai-marketing: `rules/`, `prompts/`, `skills/`, `knowledge/`, `templates/`, `qa/`, workflow pilar, dan submodule `core/`.
3. Tambah intent di [orchestrator/router.md](../orchestrator/router.md) dan agent di `clau-ai-agents/agents/registry.json`; ubah `pillars` (status `active` + `repo`) di registry yang sama.
4. Jalankan pilot SIMULASI end-to-end sebelum dipakai untuk client.
5. Update tabel di atas dan README core (status **Aktif** + repo) — test registry di clau-ai-agents gagal bila tidak sama.
6. Aktifkan permukaan UI pilar sesuai `CLAU-AI-CONTENT/design/pillars.md` dan pindahkan task pilar di board ke Done.

## Ketergantungan Antar Pilar

| Dari | Ke | Contoh |
|---|---|---|
| Pilar 1 | Pilar 5 | Data performa konten untuk report |
| Pilar 3 | Pilar 1 | Insight review → angle konten |
| Pilar 2 | Pilar 1 | Paket/promo yang disetujui → materi campaign |
| Pilar 2 | Pilar 5 | Jumlah inquiry & konversi (tanpa data pribadi tamu) |
| Pilar 3 | Pilar 5 | Tema keluhan & waktu respon |
| Pilar 4 | Pilar 3 | SOP terbaru → jawaban FAQ in-stay yang konsisten |

Data lintas pilar mengikuti [shared/data-flow.md](../shared/data-flow.md).
