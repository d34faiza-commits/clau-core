# 5-Pillar Architecture

> **Status: Approved — AI-CONSTITUTION v3.0.0 (2026-10-09).** Struktur **5 pilar v2** disetujui owner (Dea Karisna / d34faiza). Pilar 1 aktif; pilar 2–5 Planned sampai workflow & skill pilarnya di-approve. Cetak biru tiap pilar: [blueprints/](./blueprints/README.md) · vertical fokus: [verticals.md](./verticals.md) · otonomi bertingkat: AI-CONSTITUTION §4a.

## Lapisan

| Lapisan | Repo | Isi |
|---|---|---|
| **Foundation** | clau-core | Constitution, boundary, pipeline, orchestrator, kontrak data |
| **Pilar** | clau-ai-<pilar> (1 repo per pilar) | Rules, skills, prompts, knowledge, templates, QA khusus domain |
| **Platform** | clau-agent | UI, API, registry agent; menjalankan skill pilar, tidak menyimpan aturan |

Aturan mengalir **satu arah**: core → pilar → platform. Platform membaca skill pilar; pilar tidak bergantung pada platform.

## Pilar

| # | Pilar | Masalah yang diselesaikan | Contoh output | Rule kunci | Intent & agent | Status |
|---|---|---|---|---|---|---|
| 1 | **AI Marketing** | Konten jujur & on-brand tanpa klaim palsu | Caption, reel script, story, listing OTA, balasan review, kalender; berikutnya landing page, iklan, branding | Klaim (rule 02), consent (04), approval (08) | 8 intent · Tara, Raka, Sekar, Bayu, Laras, Dimas, Ayu, Nara | **Aktif** (clau-market) |
| 2 | AI Sales | Inquiry & customer service cepat, akurat, tanpa janji harga sembarangan | WhatsApp assistant, FAQ, balasan inquiry, pesan tamu, follow-up, lead/CRM, eskalasi keluhan | Harga & komitmen komersial, privacy tamu, otonomi A/B/C, keluhan serius = L3/Level C | `inquiry-reply` · Galih; `guest-message` · Sari | Planned |
| 3 | AI Admin | Pekerjaan administrasi tanpa salah angka | Quotation, invoice (draft), data entry, laporan, financial summary, inventory, SOP | Angka bisa ditelusuri ke data sumber; dokumen = Level B | `sop` · Teguh | Planned |
| 4 | AI Business Intelligence | Keputusan berbasis data lintas pilar | Laporan bulanan, KPI, insight, forecast stok/penjualan | Angka apa adanya, tanpa atribusi palsu, forecast = ASSUMPTION | `report` · Intan (aktif, sementara template `monthly-report` Pilar 1) | Planned |
| 5 | AI Automation | Pekerjaan belakang layar berjalan sendiri | Alur WA/IG → CRM → Sheets → invoice → email → follow-up | Setiap langkah punya level otonomi; audit log; tombol berhenti | Memanggil intent pilar lain (tanpa intent sendiri) | Planned |

### Sumber yang harus sinkron

| Data | Sumber | Ikut diperbarui |
|---|---|---|
| Nama, status, repo pilar | Tabel **5 Pilar CLAU AI** di [README](../README.md) | `clau-agent/agents/registry.json` → `pillars` (dicek test), tabel di atas |
| Intent → pilar → agent | [orchestrator/router.md](../orchestrator/router.md) | `registry.json` → `agents` (dicek test) |
| Permukaan UI per pilar | `clau-content/design/pillars.md` | Wireframe Studio & Portal, frontend clau-agent |
| Level otonomi per intent | Kolom **Otonomi** di [router](../orchestrator/router.md) | `registry.json` → `autonomy_max` (dicek test) |
| Rencana aktivasi | Board `clau-content/tasks/` (TASK-035–039, TASK-041–042) | `clau-agent/docs/post-vps-checklist.md` |

### Usulan nama repo pilar (**ASSUMPTION**)

Mengikuti pola `clau-ai-<pilar>`; dibuat saat pilar diaktifkan.

| # | Usulan repo |
|---|---|
| 2 | `clau-ai-sales` |
| 3 | `clau-ai-admin` |
| 4 | `clau-ai-intelligence` |
| 5 | `clau-ai-automation` (atau modul di clau-agent; keputusan engine = TASK-039) |

## Menambah Pilar

1. Owner menyetujui scope pilar (catat di Revision History [AI-CONSTITUTION](../AI-CONSTITUTION.md)).
2. Buat repo `clau-<pilar>` (public hanya untuk dilihat dengan `LICENSE` yang sama, kecuali owner memutuskan private) dengan struktur seperti clau-market: `rules/`, `prompts/`, `skills/`, `knowledge/`, `templates/`, `qa/`, workflow pilar, dan submodule `core/`.
3. Tambah intent di [orchestrator/router.md](../orchestrator/router.md) dan agent di `clau-agent/agents/registry.json`; ubah `pillars` (status `active` + `repo`) di registry yang sama.
4. Jalankan pilot SIMULASI end-to-end sebelum dipakai untuk client.
5. Update tabel di atas dan README core (status **Aktif** + repo) — test registry di clau-agent gagal bila tidak sama.
6. Aktifkan permukaan UI pilar sesuai `clau-content/design/pillars.md` dan pindahkan task pilar di board ke Done.

## Ketergantungan Antar Pilar

| Dari | Ke | Contoh |
|---|---|---|
| Pilar 1 Marketing | Pilar 4 BI | Data performa konten untuk laporan |
| Pilar 2 Sales | Pilar 1 Marketing | Paket/promo yang disetujui → materi campaign; insight review → angle konten |
| Pilar 2 Sales | Pilar 3 Admin | Order/booking → quotation & invoice draft |
| Pilar 2 Sales | Pilar 4 BI | Jumlah inquiry, konversi, tema keluhan (tanpa data pribadi tamu) |
| Pilar 3 Admin | Pilar 4 BI | Transaksi & stok → insight & forecast |
| Pilar 3 Admin | Pilar 2 Sales | SOP & katalog terbaru → jawaban FAQ yang konsisten |
| Pilar 5 Automation | Semua | Menyambungkan langkah antar pilar; tidak punya aturan domain sendiri |

Data lintas pilar mengikuti [shared/data-flow.md](../shared/data-flow.md).
