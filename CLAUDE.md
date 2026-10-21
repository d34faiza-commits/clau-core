# CLAUDE.md — clau-core

> Peta repo untuk AI agent. Baca file ini dulu sebelum menjelajah repo. Last updated: 2026-10-22

> 🔔 **Sesi baru: baca [status & handoff CLAU AI](https://github.com/d34faiza-commits/clau-content/blob/main/docs/status.md) dulu** (otoritas, keputusan yang sudah diambil, status, pekerjaan terbuka). Repo Jerco milik Pak Indra: jangan disentuh tanpa persetujuan beliau.

## 1. Identitas

| Item | Nilai |
|---|---|
| Repo | `d34faiza-commits/clau-core` (public, hanya untuk dilihat; LICENSE) |
| Peran | Fondasi CLAU AI: constitution, boundary, workflow lintas pilar, orchestrator, kontrak data |
| Dipakai oleh | `clau-market` (`core/`), `clau-agent` (`core/`), dan `clau-market/agents/core/` |
| Default branch | `main` (wajib PR + CI hijau, tanpa push langsung; dijaga `main-guard`; lihat AI-BOUNDARY) |

## 2. Peta File

| Path | Fungsi |
|---|---|
| `AI-CONSTITUTION.md` | Aturan induk semua pilar (v3.1.0 Approved: 5 pilar v2, otonomi A/B/C default B, 4 vertical fokus, `main` wajib lewat PR + CI hijau) |
| `AI-BOUNDARY.md` | Peran repo, storage zones, aturan submodule & push, kapan PR boleh disebut selesai, versi live hanya maju (v1.6.0) |
| `AGENTS.md` · `WORKFLOW.md` | Instruksi agent lintas repo · pipeline 8 langkah |
| `orchestrator/` | `router.md` (12 intent), `decision-tree.md`, `priority-engine.md` |
| `shared/` | `database-schema.md`, `api-contracts.md`, `data-flow.md`, `integrations.md` |
| `docs/` | `getting-started.md` (alur sync antar repo), `5-pillar-architecture.md`, `verticals.md`, `blueprints/` (5 pilar), `proposals/` (jejak usulan; `tahap-2-ai-drafting.md` = rancangan AI menulis draft, Draft) |
| `.github/ISSUE_TEMPLATE/` | Issue → board task di clau-content |
| `scripts/validate_core.py` | Validator (file wajib, versi governance, link, JSON, secret) |
| `.github/workflows/` | `validate.yml`, `main-guard.yml` (cek push ke `main`), `notify-downstream.yml` (memicu sync di agents; marketing menyusul lewat agents) |
| `.github/dependabot.yml` | Update GitHub Actions mingguan (tanpa versi mayor); Actions dipin ke commit SHA |

## 3. Command

```bash
python scripts/validate_core.py
```

Mengubah intent di `orchestrator/router.md` → `agents/registry.json` di clau-agent juga harus diubah (ada test konsistensi).

## Aturan Kerja untuk Agent

- Baca `AGENTS.md` (instruksi agent) dan, untuk aturan induk, `AI-CONSTITUTION.md` + `AI-BOUNDARY.md`.
- **Otoritas perubahan:** dokumen berstatus Approved hanya diubah atas perintah **Pak Indra** atau **Dea Karisna (d34faiza)**.
- AI **tidak** publish, kirim ke pihak luar, atau self-approve. Review independen L2/L3 = manusia.
- **Jangan** commit data client nyata (brief, fact sheet, caption, harga, foto, data tamu), `.env`, atau credential. Data client nyata ada di Client Workspace (Drive), bukan repo.
- Label evidence dipakai persis: `DATA FINAL`, `ASSUMPTION`, `CLIENT CONFIRMATION`, `FIELD VERIFICATION`, `RISK`, `NEXT ACTION`.
- Commit message: `feat:`, `fix:`, `docs:`, `refactor:`, `chore:`, `test:`. Jalankan validator sebelum push.
