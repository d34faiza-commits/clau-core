# CLAUDE.md — clau-ai-core

> Peta repo untuk AI agent. Baca file ini dulu sebelum menjelajah repo. Last updated: 2026-10-09

> 🔔 **Sesi baru: baca [status & handoff CLAU AI](https://github.com/d34faiza-commits/CLAU-AI-CONTENT/blob/main/docs/status.md) dulu** (otoritas, keputusan yang sudah diambil, status, pekerjaan terbuka). Repo Jerco milik Pak Indra: jangan disentuh tanpa persetujuan beliau.

## 1. Identitas

| Item | Nilai |
|---|---|
| Repo | `d34faiza-commits/clau-ai-core` (private) |
| Peran | Fondasi CLAU AI: constitution, boundary, workflow lintas pilar, orchestrator, kontrak data |
| Dipakai oleh | `clau-ai-marketing` (`core/`), `clau-ai-agents` (`core/`), dan `clau-ai-marketing/agents/core/` |
| Default branch | `main` (direct push, disiplin solo dev; lihat AI-BOUNDARY) |

## 2. Peta File

| Path | Fungsi |
|---|---|
| `AI-CONSTITUTION.md` | Aturan induk semua pilar (v3.0.0 Approved: 5 pilar v2, otonomi A/B/C default B, 4 vertical fokus) |
| `AI-BOUNDARY.md` | Peran repo, storage zones, aturan submodule & push |
| `AGENTS.md` · `WORKFLOW.md` | Instruksi agent lintas repo · pipeline 8 langkah |
| `orchestrator/` | `router.md` (12 intent), `decision-tree.md`, `priority-engine.md` |
| `shared/` | `database-schema.md`, `api-contracts.md`, `data-flow.md`, `integrations.md` |
| `docs/` | `getting-started.md`, `5-pillar-architecture.md` |
| `scripts/validate_core.py` | Validator (file wajib, versi governance, link, JSON, secret) |
| `.github/workflows/` | `validate.yml`, `notify-downstream.yml` (memicu sync di agents & marketing) |

## 3. Command

```bash
python scripts/validate_core.py
```

Mengubah intent di `orchestrator/router.md` → `agents/registry.json` di clau-ai-agents juga harus diubah (ada test konsistensi).

## Aturan Kerja untuk Agent

- Baca `AGENTS.md` (instruksi agent) dan, untuk aturan induk, `AI-CONSTITUTION.md` + `AI-BOUNDARY.md`.
- **Otoritas perubahan:** dokumen berstatus Approved hanya diubah atas perintah **Pak Indra** atau **Dea Karisna (d34faiza)**.
- AI **tidak** publish, kirim ke pihak luar, atau self-approve. Review independen L2/L3 = manusia.
- **Jangan** commit data client nyata (brief, fact sheet, caption, harga, foto, data tamu), `.env`, atau credential. Data client nyata ada di Client Workspace (Drive), bukan repo.
- Label evidence dipakai persis: `DATA FINAL`, `ASSUMPTION`, `CLIENT CONFIRMATION`, `FIELD VERIFICATION`, `RISK`, `NEXT ACTION`.
- Commit message: `feat:`, `fix:`, `docs:`, `refactor:`, `chore:`, `test:`. Jalankan validator sebelum push.
