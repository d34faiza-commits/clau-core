# Getting Started

Panduan memakai ekosistem CLAU AI setelah split menjadi 3 repo.

## 1. Clone dengan Submodule

```bash
# Repo pilar atau platform (otomatis menarik core ke folder core/)
git clone --recurse-submodules https://github.com/d34faiza-commits/clau-ai-marketing.git
git clone --recurse-submodules https://github.com/d34faiza-commits/clau-ai-agents.git

# Kalau sudah ter-clone tanpa submodule
cd clau-ai-marketing
git submodule update --init --recursive
```

Semua repo private: akun yang meng-clone harus punya akses ke **clau-ai-core** juga, karena submodule ikut di-clone.

## 2. Update Core di Repo Konsumen

Perubahan aturan bersama dilakukan di **clau-ai-core**. Setelah di-push, repo konsumen menarik versi baru:

```bash
cd clau-ai-marketing
git submodule update --remote core          # ambil commit terbaru core (branch main)
git add core
git commit -m "chore(core): bump core to $(git -C core rev-parse --short HEAD)"
git push
```

Submodule terkunci ke satu commit. Repo konsumen tidak otomatis memakai perubahan core sampai langkah di atas dijalankan. Ini disengaja, supaya perubahan aturan bisa direview per repo.

## 3. Mengedit Aturan

| Mau mengubah | Edit di | Lalu |
|---|---|---|
| Constitution, boundary, pipeline, orchestrator, kontrak data | clau-ai-core | Bump submodule di marketing & agents |
| Rules, skill, prompt, knowledge, template, QA konten | clau-ai-marketing | — |
| Kode platform, registry agent | clau-ai-agents | Bila intent berubah, update juga `orchestrator/router.md` di core |

Jangan mengedit file di dalam folder `core/` milik repo lain. Perubahan di sana tidak ikut ke clau-ai-core dan akan tertimpa saat update submodule.

## 4. Validasi

| Repo | Perintah |
|---|---|
| clau-ai-core | `python scripts/validate_core.py` |
| clau-ai-marketing | `python scripts/validate.py` (cek link ke `core/` bila submodule ter-init) |
| clau-ai-agents | `cd backend && pip install -r requirements.txt && pytest` |

CI di GitHub Actions tidak meng-clone submodule private (butuh token tambahan), jadi link ke `core/` hanya dicek saat validasi lokal dengan submodule ter-init.

## 5. Alur Kerja Harian

Untuk konten (Pilar 1): ikuti `clau-ai-marketing/automations/level-1-manual/README.md`. Routing request: [orchestrator/router.md](../orchestrator/router.md).
