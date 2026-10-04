# clau-ai-core

**Fondasi CLAU AI** untuk bisnis hospitality & tourism Indonesia: konstitusi AI, boundary data, pipeline kerja, orchestrator (routing antar pilar), dan kontrak data bersama. Dipakai oleh semua repo pilar dan platform lewat **git submodule** di path `core/`.

> **Status:** Private — v0.1.0 (split dari `CLAU-AI-CONTENT`, 2026-10-04)
> **Dokumen induk:** [AI-CONSTITUTION.md](./AI-CONSTITUTION.md) (v2.0.0, **For Review**)
> **Boundary:** [AI-BOUNDARY.md](./AI-BOUNDARY.md)
> **Credit:** [ACKNOWLEDGMENT.md](./ACKNOWLEDGMENT.md)

## Ekosistem Repo

| Repo | Peran | Isi utama | Submodule |
|---|---|---|---|
| **clau-ai-core** (repo ini) | Foundation | Constitution, boundary, pipeline, orchestrator, kontrak data | — |
| [clau-ai-marketing](https://github.com/d34faiza-commits/clau-ai-marketing) | Pilar 1: Marketing & Content | Rules, prompts, skills, knowledge, templates, QA, contoh | `core/` → repo ini |
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
```

## 5 Pilar CLAU AI

| # | Pilar | Fungsi | Repo | Status |
|---|---|---|---|---|
| 1 | **Marketing & Content** | Caption, reel, story, listing OTA, balasan review, campaign, kalender konten | clau-ai-marketing | **Aktif** |
| 2 | Sales & Reservations | Inquiry WhatsApp/DM, direct booking, paket & penawaran | — | Planned |
| 3 | Guest Experience & Reputation | Pre-arrival, in-stay comms, eskalasi komplain, reputasi | — | Planned |
| 4 | Operations | SOP, checklist operasional, knowledge staf | — | Planned |
| 5 | Analytics & Insights | KPI lintas pilar, report bulanan, insight performa | — | Planned |

> **ASSUMPTION:** pembagian pilar 2–5 adalah usulan kerja berdasarkan kebutuhan umum hospitality. Nama, urutan, dan scope pilar 2–5 menunggu keputusan owner (**CLIENT CONFIRMATION**). Detail: [docs/5-pillar-architecture.md](./docs/5-pillar-architecture.md).

## Struktur

```text
clau-ai-core/
├── README.md
├── AI-CONSTITUTION.md        # Aturan induk semua pilar (v2.0.0, For Review)
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
└── scripts/validate_core.py  # Validator (dipakai CI)
```

## Versi Dokumen

| Dokumen | Versi | Status |
|---|---|---|
| [AI-CONSTITUTION.md](./AI-CONSTITUTION.md) | 2.0.0 | For Review |
| [AI-BOUNDARY.md](./AI-BOUNDARY.md) | 1.0.0 | Draft |
| [WORKFLOW.md](./WORKFLOW.md) | 1.0.0 | Draft |
| [AGENTS.md](./AGENTS.md) | 1.0.0 | Draft |

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
