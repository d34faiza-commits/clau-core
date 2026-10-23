# Blueprint 5 Pilar — Konsep v2

> **Status: struktur Approved (AI-CONSTITUTION v3.0.0, 2026-10-09).** Owner (Dea Karisna / d34faiza) menyetujui 5 pilar v2 dan otonomi bertingkat. Isi tiap blueprint (intent usulan, paket jual, integrasi) tetap **Draft/ASSUMPTION** sampai pilarnya diaktifkan. Fokus sekarang: vertical villa, restoran/cafe, wedding, travel.

## Konsep v2 vs Pilar Sekarang

| v2 (berlaku sejak v3.0.0) | Menjual | Asal dari pilar v1 | Blueprint |
|---|---|---|---|
| 🟣 1 AI Marketing | Website, landing page, copywriting, social media, caption, content calendar, video, foto produk, branding, iklan | 1 Marketing & Content (**Aktif**) — diperluas | [marketing.md](./marketing.md) |
| 🔵 2 AI Sales | WhatsApp assistant, customer service, FAQ, sales assistant, lead management, follow-up, booking, CRM | 2 Sales & Reservations + 3 Guest Experience & Reputation (digabung) | [sales.md](./sales.md) |
| 🟢 3 AI Admin | Invoice, quotation, data entry, dokumen, laporan, financial summary, inventory, SOP | 4 Operations — diperluas | [admin.md](./admin.md) |
| 🟠 4 AI Business Intelligence | Insight penjualan, pelanggan, biaya iklan, stok, prediksi | 5 Analytics & Insights — diperdalam | [business-intelligence.md](./business-intelligence.md) |
| 🔴 5 AI Automation | Alur end-to-end: WA/IG → AI → CRM → Sheets → invoice → email → follow-up | **Baru** — lapisan penghubung antar pilar, dijual sebagai langganan | [automation.md](./automation.md) |

Jenis usaha (vertical) dan urutan perluasannya: [../verticals.md](../verticals.md).

## Status Penerapan

| Item | Status |
|---|---|
| AI-CONSTITUTION §2 (5 pilar v2, vertical fokus) & §4a (otonomi bertingkat) | ✅ v3.0.0 Approved |
| Tabel pilar [README](../../README.md), [router](../../orchestrator/router.md) (kolom Otonomi), `registry.json` (`pillars`, `autonomy_max`) | ✅ Diterapkan bersama v3.0.0 |
| Perluasan scope ke jenis usaha di luar hospitality (§2 Usulan 2) | ⬜ Masih usulan ([proposals/autonomy-levels.md](../proposals/autonomy-levels.md)) |
| Intent baru per pilar & agent baru di registry | ⬜ Saat pilar diaktifkan (butuh nama disetujui owner, avatar, persona, eval) |
| Level A untuk intent mana pun | ⬜ Semua intent masih Level B |

## Urutan Aktivasi (usulan)

| Fase | Isi | Prasyarat |
|---|---|---|
| 0 | Fondasi platform: VPS, database, auth, panggilan AI model | `clau-agent/docs/post-vps-checklist.md` |
| 1 | Marketing v2 (landing page, iklan, branding) + vertical wedding & travel | Fase 0 untuk platform; knowledge segment sudah ada (Planned) |
| 2 | Sales: WhatsApp assistant dengan otonomi bertingkat | Amandemen otonomi Approved; integrasi WhatsApp Business Platform |
| 3 | Admin: quotation & invoice draft, laporan | Database + izin akses data keuangan |
| 4 | Business Intelligence | Data Sales & Admin terkumpul ≥ 1–3 bulan |
| 2→ | Automation sebagai lapisan sejak Fase 2 | Konektor per integrasi + audit log |

## Gerbang Umum Pilar 2–5 (keputusan owner 2026-10-22/23)

Pilar 2–5 **ditunda**: fokus sekarang Pilar 1 hospitality sampai berjalan. Blueprint di folder ini adalah rencana jangka panjang; tidak ada pekerjaan aktivasi sebelum **semua** syarat ini terpenuhi (kecuali owner memutuskan lain):

| # | Syarat | Cara cek |
|---|---|---|
| G1 | ≥ 3 klien Pilar 1 nyata aktif ≥ 3 bulan, tanpa insiden publikasi berat | Log publikasi & insiden (clau-market `commercial/delivery-sop.md` § 7) |
| G2 | Independent score rata-rata ≥ 85 pada sampling bulanan | clau-market `qa/independent-review-worksheet.md` |
| G3 | Legal & UU PDP selesai untuk Pilar 1 (TASK-053); kontrak + DPA dipakai | Kartu TASK-053 Closed |
| G4 | Platform hidup: VPS 2 (TASK-065), provider AI nyata (TASK-052), domain + HTTPS (TASK-047) | `clau-agent/CLAUDE.md` status |
| G5 | ≥ 2 reviewer manusia (owner tidak lagi satu-satunya), SOP tim (TASK-059) | Kartu TASK-059 |
| G6 | Minimal 1 klien Pilar 1 meminta layanan pilar itu (permintaan nyata, bukan asumsi) | Catatan discovery/klien |

Urutan bila gerbang terbuka: **Sales (2) → BI (4, dari laporan Pilar 1) → Admin (3) → Automation (5)**. Alasannya: Sales dan BI paling dekat dengan data & klien Pilar 1; Admin butuh data keuangan (risiko lebih tinggi); Automation hanya menyambung pilar yang sudah aktif.

Model jual jangka panjang: **upsell ke klien Pilar 1**, bukan cari klien baru per pilar. Klien yang sudah percaya pada konten & review → ditawari balasan inquiry (Sales) → laporan & insight (BI) → dokumen (Admin) → alur otomatis (Automation).

## Format Setiap Blueprint

Scope (yang dijual) · intent & agent usulan · level otonomi per aksi · data & privacy · integrasi · risiko · KPI · checklist aktivasi. Intent di blueprint **belum** masuk `router.md`; saat aktivasi, salin ke router + registry (test konsistensi menjaga keduanya).

## Checklist Aktivasi Umum (semua pilar)

1. Owner approve scope pilar (TASK-034) → catat di Revision History AI-CONSTITUTION.
2. Buat repo pilar `clau-<pilar>` (nama usulan di [5-pillar-architecture](../5-pillar-architecture.md); struktur seperti clau-market + submodule `core/`).
3. Tulis rules pilar (lebih ketat dari core, tidak boleh lebih longgar), skills, prompts, templates, QA.
4. Tambah intent ke `orchestrator/router.md` + agent ke `registry.json` (nama, avatar, persona, eval).
5. Ubah tabel pilar README core + `registry.json` → `pillars` (test gagal bila beda).
6. Aktifkan layar UI sesuai `clau-content/design/pillars.md`.
7. Pilot SIMULASI end-to-end, lalu 1 client pilot dengan review manusia penuh.
