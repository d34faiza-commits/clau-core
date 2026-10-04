# 5-Pillar Architecture

> **Status: Draft.** Pilar 1 aktif. Pilar 2–5 adalah usulan kerja (**ASSUMPTION**) yang menunggu keputusan owner (**CLIENT CONFIRMATION**) soal nama, urutan, dan scope.

## Lapisan

| Lapisan | Repo | Isi |
|---|---|---|
| **Foundation** | clau-ai-core | Constitution, boundary, pipeline, orchestrator, kontrak data |
| **Pilar** | clau-ai-<pilar> (1 repo per pilar) | Rules, skills, prompts, knowledge, templates, QA khusus domain |
| **Platform** | clau-ai-agents | UI, API, registry agent; menjalankan skill pilar, tidak menyimpan aturan |

Aturan mengalir **satu arah**: core → pilar → platform. Platform membaca skill pilar; pilar tidak bergantung pada platform.

## Pilar

| # | Pilar | Masalah yang diselesaikan | Contoh output | Rule kunci | Status |
|---|---|---|---|---|---|
| 1 | **Marketing & Content** | Konten jujur & on-brand tanpa klaim palsu | Caption, reel script, story, listing OTA, balasan review, kalender | Klaim (rule 02), consent (04), approval (08) | **Aktif** (clau-ai-marketing) |
| 2 | Sales & Reservations | Inquiry cepat & akurat tanpa janji harga sembarangan | Draft balasan DM/WA soal harga & tanggal, paket | Harga & komitmen komersial, ketersediaan real-time | Planned |
| 3 | Guest Experience & Reputation | Komunikasi tamu konsisten & eskalasi komplain | Pesan pre-arrival, FAQ in-stay, eskalasi keluhan | Privacy tamu, keluhan serius = L3 | Planned |
| 4 | Operations | Pengetahuan operasional terdokumentasi | SOP, checklist housekeeping/F&B, materi onboarding staf | Keselamatan, akurasi prosedur | Planned |
| 5 | Analytics & Insights | Keputusan berbasis data lintas pilar | Report bulanan, KPI dashboard | Angka apa adanya, tanpa atribusi palsu | Planned |

## Menambah Pilar

1. Owner menyetujui scope pilar (catat di Revision History [AI-CONSTITUTION](../AI-CONSTITUTION.md)).
2. Buat repo `clau-ai-<pilar>` (private) dengan struktur seperti clau-ai-marketing: `rules/`, `prompts/`, `skills/`, `knowledge/`, `templates/`, `qa/`, workflow pilar, dan submodule `core/`.
3. Tambah intent di [orchestrator/router.md](../orchestrator/router.md) dan agent di `clau-ai-agents/agents/registry.json`.
4. Jalankan pilot SIMULASI end-to-end sebelum dipakai untuk client.
5. Update tabel di atas dan README core.

## Ketergantungan Antar Pilar

| Dari | Ke | Contoh |
|---|---|---|
| Pilar 1 | Pilar 5 | Data performa konten untuk report |
| Pilar 3 | Pilar 1 | Insight review → angle konten |
| Pilar 2 | Pilar 1 | Paket/promo yang disetujui → materi campaign |

Data lintas pilar mengikuti [shared/data-flow.md](../shared/data-flow.md).
