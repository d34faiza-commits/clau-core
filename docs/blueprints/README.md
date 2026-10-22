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
