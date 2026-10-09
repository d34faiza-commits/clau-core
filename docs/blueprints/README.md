# Blueprint 5 Pilar — Konsep v2

> **Status: Draft (ASSUMPTION).** Cetak biru untuk masa depan, disiapkan 2026-10-09 atas arahan owner: *fokus sekarang hospitality, tetapi semua pilar dan jenis usaha disiapkan supaya saat modal siap tinggal diaktifkan*. Tidak ada yang berlaku untuk client sebelum keputusan di TASK-034 dan amandemen di [proposals/autonomy-levels.md](../proposals/autonomy-levels.md) di-approve **Pak Indra** atau **Dea Karisna (d34faiza)**.

## Konsep v2 vs Pilar Sekarang

| v2 | Menjual | Pilar sekarang (README core) | Blueprint |
|---|---|---|---|
| 🟣 1 AI Marketing | Website, landing page, copywriting, social media, caption, content calendar, video, foto produk, branding, iklan | 1 Marketing & Content (**Aktif**) — diperluas | [marketing.md](./marketing.md) |
| 🔵 2 AI Sales | WhatsApp assistant, customer service, FAQ, sales assistant, lead management, follow-up, booking, CRM | 2 Sales & Reservations + 3 Guest Experience & Reputation (digabung) | [sales.md](./sales.md) |
| 🟢 3 AI Admin | Invoice, quotation, data entry, dokumen, laporan, financial summary, inventory, SOP | 4 Operations — diperluas | [admin.md](./admin.md) |
| 🟠 4 AI Business Intelligence | Insight penjualan, pelanggan, biaya iklan, stok, prediksi | 5 Analytics & Insights — diperdalam | [business-intelligence.md](./business-intelligence.md) |
| 🔴 5 AI Automation | Alur end-to-end: WA/IG → AI → CRM → Sheets → invoice → email → follow-up | **Baru** — lapisan penghubung antar pilar, dijual sebagai langganan | [automation.md](./automation.md) |

Jenis usaha (vertical) dan urutan perluasannya: [../verticals.md](../verticals.md).

## Yang Sengaja Belum Diubah

| Item | Alasan | Diubah saat |
|---|---|---|
| Tabel pilar di [README](../../README.md), `router.md`, `registry.json` | Sumber yang dites; mengubahnya = mengaktifkan konsep v2 | TASK-034 diputuskan |
| AI-CONSTITUTION §2 (scope hospitality) & §4.7 (AI tidak mengirim ke pihak luar) | Dokumen Approved | Amandemen [autonomy-levels](../proposals/autonomy-levels.md) di-approve |
| Agent baru di registry | Butuh nama (approval owner), avatar, persona, eval — dicek test | Pilar terkait mulai diaktifkan |

## Urutan Aktivasi (usulan)

| Fase | Isi | Prasyarat |
|---|---|---|
| 0 | Fondasi platform: VPS, database, auth, panggilan AI model | `clau-ai-agents/docs/post-vps-checklist.md` |
| 1 | Marketing v2 (landing page, iklan, branding) + vertical wedding & travel | Fase 0 untuk platform; knowledge segment sudah ada (Planned) |
| 2 | Sales: WhatsApp assistant dengan otonomi bertingkat | Amandemen otonomi Approved; integrasi WhatsApp Business Platform |
| 3 | Admin: quotation & invoice draft, laporan | Database + izin akses data keuangan |
| 4 | Business Intelligence | Data Sales & Admin terkumpul ≥ 1–3 bulan |
| 2→ | Automation sebagai lapisan sejak Fase 2 | Konektor per integrasi + audit log |

## Format Setiap Blueprint

Scope (yang dijual) · intent & agent usulan · level otonomi per aksi · data & privacy · integrasi · risiko · KPI · checklist aktivasi. Intent di blueprint **belum** masuk `router.md`; saat aktivasi, salin ke router + registry (test konsistensi menjaga keduanya).

## Checklist Aktivasi Umum (semua pilar)

1. Owner approve scope pilar (TASK-034) → catat di Revision History AI-CONSTITUTION.
2. Buat repo pilar `clau-ai-<pilar>` (struktur seperti clau-ai-marketing + submodule `core/`).
3. Tulis rules pilar (lebih ketat dari core, tidak boleh lebih longgar), skills, prompts, templates, QA.
4. Tambah intent ke `orchestrator/router.md` + agent ke `registry.json` (nama, avatar, persona, eval).
5. Ubah tabel pilar README core + `registry.json` → `pillars` (test gagal bila beda).
6. Aktifkan layar UI sesuai `CLAU-AI-CONTENT/design/pillars.md`.
7. Pilot SIMULASI end-to-end, lalu 1 client pilot dengan review manusia penuh.
