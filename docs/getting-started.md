# Getting Started

Panduan memakai ekosistem CLAU AI setelah split menjadi 3 repo.

## 1. Clone dengan Submodule

```bash
# Repo pilar atau platform (otomatis menarik core ke folder core/)
git clone --recurse-submodules https://github.com/d34faiza-commits/clau-market.git
git clone --recurse-submodules https://github.com/d34faiza-commits/clau-agent.git

# Kalau sudah ter-clone tanpa submodule
cd clau-market
git submodule update --init --recursive   # marketing: core/, agents/, agents/core/
```

Semua repo private: akun yang meng-clone harus punya akses ke **clau-core** juga, karena submodule ikut di-clone.

## 2. Update Core di Repo Konsumen

Perubahan aturan bersama dilakukan di **clau-core** (lewat PR, AI-BOUNDARY § Disiplin Push). Setelah di-merge, repo konsumen menarik versi baru **otomatis**:

```text
core main ──notify──► agents: sync-submodules (PR bot) ──CI hijau──► merge
                                                                       │ notify
                                                                       ▼
                       marketing: sync-submodules (PR bot): agents + core (= pin agents/core) ──CI hijau──► merge
```

Pin dimajukan **hanya bila validator & test lulus**. Bila gagal, pin lama tetap dipakai dan workflow merah, sehingga perubahan aturan yang merusak repo konsumen tidak ikut masuk diam-diam. Core di marketing selalu sama dengan core di agents (`scripts/check-core-pins.sh --strict` di CI).

Manual (bila perlu, juga lewat PR):

```bash
cd clau-market
scripts/sync-submodules.sh --pr-branch chore/bump-submodules   # sync + validasi + commit + push branch
# lalu buka PR ke main dan tunggu CI hijau; push langsung ke main ditolak script
```

## 3. Mengedit Aturan

| Mau mengubah | Edit di | Lalu |
|---|---|---|
| Constitution, boundary, pipeline, orchestrator, kontrak data | clau-core | Bump submodule di marketing & agents |
| Rules, skill, prompt, knowledge, template, QA konten | clau-market | — |
| Kode platform, registry agent | clau-agent | Bila intent berubah, update juga `orchestrator/router.md` di core |

Jangan mengedit file di dalam folder `core/` milik repo lain. Perubahan di sana tidak ikut ke clau-core dan akan tertimpa saat update submodule.

## 4. Validasi

| Repo | Perintah |
|---|---|
| clau-core | `python scripts/validate_core.py` |
| clau-market | `python scripts/validate.py --require-submodules` (cek link ke `core/` & `agents/`) |
| clau-agent | `cd backend && pip install -r requirements.txt && pytest` |

Ada dua lapis CI:

| Workflow | Butuh token? | Cek |
|---|---|---|
| `validate.yml` / `ci.yml` | Tidak | Validasi repo sendiri; link ke submodule dilewati |
| `cross-repo-validate.yml` (marketing, agents) | `SUBMODULE_READ_TOKEN` (read-only, disarankan) atau `SUBMODULE_TOKEN`; tanpa token = gagal | Checkout semua submodule, validator core, validator marketing dengan `--require-submodules`, test backend agents terhadap router core, pin core wajib sama |
| `sync-submodules.yml` (harian + dipicu `notify-downstream`) | `SUBMODULE_TOKEN` | Majukan pin submodule, validasi, commit `chore(<path>): bump …` di branch `bot/sync-submodules`, PR, merge setelah check wajib hijau |
| `main-guard.yml` (core, marketing, agents) | — | Setiap push ke `main` harus dari PR yang semua check wajibnya hijau sebelum merge |

Panduan lengkap (update, sync, troubleshooting, setup token): `SUBMODULE.md` di clau-market dan clau-agent.

## 5. Alur Kerja Harian

Untuk konten (Pilar 1): ikuti `clau-market/automations/level-1-manual/README.md`. Routing request: [orchestrator/router.md](../orchestrator/router.md).
