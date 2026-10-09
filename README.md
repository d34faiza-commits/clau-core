# clau-ai-core

**Fondasi CLAU AI** untuk bisnis hospitality & tourism Indonesia: konstitusi AI, boundary data, pipeline kerja, orchestrator (routing antar pilar), dan kontrak data bersama. Dipakai oleh semua repo pilar dan platform lewat **git submodule** di path `core/`.

> **Status:** Private — v0.1.0 (split dari `CLAU-AI-CONTENT`, 2026-10-04)
> **Dokumen induk:** [AI-CONSTITUTION.md](./AI-CONSTITUTION.md) (v3.0.0, **Approved**)
> **Boundary:** [AI-BOUNDARY.md](./AI-BOUNDARY.md)
> **Credit:** [ACKNOWLEDGMENT.md](./ACKNOWLEDGMENT.md)

## Ekosistem Repo

| Repo | Peran | Isi utama | Submodule |
|---|---|---|---|
| **clau-ai-core** (repo ini) | Foundation | Constitution, boundary, pipeline, orchestrator, kontrak data | — |
| [clau-ai-marketing](https://github.com/d34faiza-commits/clau-ai-marketing) | Pilar 1: AI Marketing | Rules, prompts, skills, knowledge, templates, QA, contoh | `core/` → repo ini, `agents/` → clau-ai-agents |
| [clau-ai-agents](https://github.com/d34faiza-commits/clau-ai-agents) | Platform | Frontend (Next.js), backend (FastAPI), registry agent | `core/` → repo ini |
| [CLAU-AI-CONTENT](https://github.com/d34faiza-commits/CLAU-AI-CONTENT) | Arsip / backup | Repo awal sebelum split; task board & riwayat pilot | — |

```text
            ┌────────────────────┐
            │   clau-ai-core     │  constitution · boundary · orchestrator · shared contracts
            └─────────┬──────────┘
          submodule   │   submodule
        ┌─────────────┴─────────────┐
┌───────▼──────────┐       ┌────────▼─────────┐
│ clau-ai-marketing│       │  clau-ai-agents  │
│  (Pilar 1)       │◄──────│  (platform)      │  agents memanggil skill pilar lewat registry
└──────────────────┘ refs  └──────────────────┘
   marketing juga memuat agents sebagai submodule agents/ (pin core harus sama)
   sync otomatis: core/agents push → notify-downstream → sync-submodules + cross-repo-validate
```

## 5 Pilar CLAU AI

| # | Pilar | Fungsi | Repo | Status |
|---|---|---|---|---|
| 1 | **AI Marketing** | Caption, reel, story, listing OTA, balasan review, campaign, kalender konten; berikutnya landing page, iklan, branding | clau-ai-marketing | **Aktif** |
| 2 | AI Sales | WhatsApp assistant, customer service, FAQ, lead, follow-up, booking, CRM | — | Planned |
| 3 | AI Admin | Invoice, quotation, data entry, laporan, financial summary, inventory, SOP | — | Planned |
| 4 | AI Business Intelligence | Insight penjualan, pelanggan, biaya iklan, stok; laporan bulanan & KPI | — | Planned |
| 5 | AI Automation | Alur end-to-end antar pilar (WA/IG → AI → CRM → Sheets → invoice → email → follow-up) | — | Planned |

> **Approved (AI-CONSTITUTION v3.0.0, 2026-10-09):** struktur 5 pilar v2 dan otonomi bertingkat A/B/C (default Level B). Vertical fokus: villa, restoran/cafe, wedding, travel ([docs/verticals.md](./docs/verticals.md)). Cetak biru tiap pilar: [docs/blueprints/](./docs/blueprints/README.md). Detail: [docs/5-pillar-architecture.md](./docs/5-pillar-architecture.md).

> **Sinkron:** tabel ini adalah sumber nama, repo, dan status pilar. `clau-ai-agents/agents/registry.json` → `pillars` dites sama dengan tabel ini (`backend/tests/test_registry.py`); ubah keduanya bersamaan. Keputusan owner: TASK-034 (selesai, v3.0.0).

## Struktur

```text
clau-ai-core/
├── README.md
├── AI-CONSTITUTION.md        # Aturan induk semua pilar (v3.0.0, Approved)
├── AI-BOUNDARY.md            # Boundary data & repo
├── AGENTS.md                 # Instruksi umum AI agent lintas repo
├── WORKFLOW.md               # Pipeline kerja umum (intake → monitor)
├── ACKNOWLEDGMENT.md · LICENSE
├── orchestrator/             # Routing request ke pilar & skill
│   ├── README.md · router.md · decision-tree.md · priority-engine.md
├── shared/                   # Kontrak bersama antar repo
│   ├── database-schema.md · api-contracts.md · data-flow.md · integrations.md
├── docs/
│   ├── getting-started.md · 5-pillar-architecture.md
│   ├── verticals.md          # Jenis usaha: aktif & planned (Draft)
│   ├── blueprints/           # Cetak biru konsep v2: marketing, sales, admin, BI, automation (Draft)
│   └── proposals/            # Usulan amandemen (otonomi bertingkat), belum berlaku
└── scripts/validate_core.py  # Validator (dipakai CI)
```

## Versi Dokumen

| Dokumen | Versi | Status |
|---|---|---|
| [AI-CONSTITUTION.md](./AI-CONSTITUTION.md) | 3.0.0 | Approved |
| [AI-BOUNDARY.md](./AI-BOUNDARY.md) | 1.1.1 | Approved |
| [WORKFLOW.md](./WORKFLOW.md) | 1.0.1 | Approved |
| [AGENTS.md](./AGENTS.md) | 1.0.0 | Approved |

> **Otoritas perubahan:** Perubahan atas dokumen berstatus Approved hanya dilakukan atas perintah **Pak Indra** atau **Dea Karisna (d34faiza)**. AI agent tidak mengubah aturan Approved atas inisiatif sendiri; usulan perbaikan boleh ditulis sebagai catatan/issue, lalu menunggu perintah.

Validator mengecek tabel ini cocok dengan frontmatter dan Revision History tiap dokumen.

## Quick Start

1. Baca [docs/getting-started.md](./docs/getting-started.md).
2. Baca [AI-CONSTITUTION.md](./AI-CONSTITUTION.md) dan [AI-BOUNDARY.md](./AI-BOUNDARY.md).
3. Untuk kerja konten, buka repo pilar [clau-ai-marketing](https://github.com/d34faiza-commits/clau-ai-marketing).
4. Untuk menambah pilar baru, ikuti [docs/5-pillar-architecture.md](./docs/5-pillar-architecture.md) §Menambah pilar.

## Validation

```text
python scripts/validate_core.py
```

## Lisensi

Proprietary, private use. Lihat [LICENSE](./LICENSE).
