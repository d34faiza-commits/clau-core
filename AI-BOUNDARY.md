---
document_title: "CLAU AI Boundary"
document_owner: "Dea Karisna / AI Marketing"
version: "1.1.1"
status: "Approved"
effective_date: "2026-10-08"
approval_reference: "v1.1.1: instruksi owner via sesi Claude Code, 2026-10-08 (\"gass\", izin token + sync via PR); v1.1.0: instruksi tertulis owner (Dea Karisna / d34faiza) via sesi Claude Code, 2026-10-06 (\"tolong semua repo di cek … jika belum fix 100% tolong di fix\"); v1.0.0 approved 2026-10-04; perubahan ada di main"
classification: "Internal"
---

# CLAU AI Boundary

## Purpose

Menetapkan apa yang boleh dan tidak boleh disimpan di repo-repo CLAU AI (core, pilar, agents), serta di sistem yang dipakai platform. Diturunkan dari *CLAU Content Repository Boundary v0.1.4* (arsip `CLAU-AI-CONTENT`) dan diperluas untuk multi-repo dan platform.

## Authority

Tunduk pada [AI-CONSTITUTION.md](./AI-CONSTITUTION.md).

Perubahan atas dokumen berstatus Approved hanya dilakukan atas perintah **Pak Indra** atau **Dea Karisna (d34faiza)**. AI agent tidak mengubah aturan Approved atas inisiatif sendiri; usulan perbaikan boleh ditulis sebagai catatan/issue, lalu menunggu perintah.

## Peran Tiap Repo

| Repo | Boleh berisi | Tidak boleh berisi |
|---|---|---|
| clau-ai-core | Constitution, boundary, pipeline, orchestrator, kontrak data (dokumen & schema), validator | Data client, brief/konten client |
| Repo pilar (mis. clau-ai-marketing) | Rules, prompt, skill, knowledge reusable, template, QA, contoh **fiktif** | Brief/konten/aset client nyata, data tamu |
| clau-ai-agents | Kode platform, registry agent, konfigurasi **contoh** (`.env.example`) | `.env` asli, credential, dump database, log berisi data tamu |
| CLAU-AI-CONTENT | Arsip read-mostly sebelum split | Data baru |

Semua repo **private**. Repo private tidak membuat data `Confidential`/`Restricted` boleh di-commit.

## Konten yang Diizinkan

1. Scope `Reusable`, sensitivity `Public` atau `Internal`.
2. Lifecycle `Approved`, atau `Draft`/`For Review` dengan status tertulis jelas.
3. Contoh memakai properti fiktif (nama mengandung "Contoh").
4. Lolos validator repo dan self-review diff sebelum push.

## Konten yang Dilarang

- Nama, kontak, nomor booking/kamar, tanggal menginap, identitas, data kesehatan, atau data pembayaran tamu.
- Foto/video asli client; review mentah yang mengidentifikasi tamu.
- Brief, kontrak, rate, revenue, occupancy, atau data komersial client.
- Password, token, OTP, cookie, API key, recovery code, `.env` asli.
- Export data platform (Meta, TikTok, GBP, OTA, PMS) yang memuat data pengguna.

## Storage Zones

| Zone | Lokasi | Di Git? | Isi |
|---|---|---:|---|
| Playbook & contracts | clau-ai-core, repo pilar | Ya | Aturan, skill, template, schema |
| Platform code | clau-ai-agents | Ya | Kode, registry, konfigurasi contoh |
| Client Workspace | Drive/folder per client | Tidak | Brief, draft, konten final, approval |
| Media Library | Storage media client | Tidak | Foto, video, logo, release form |
| Consent Register | Sistem client terproteksi | Tidak | Consent tamu, staf, talent, UGC |
| Platform Database | Database platform (lihat [shared/database-schema.md](./shared/database-schema.md)) | Tidak | Data operasional; data tamu hanya bila perlu dan terenkripsi |
| Credential Store | Password/secret manager | Tidak | Semua credential |

## Multi-Repo & Submodule

- Repo pilar dan agents memuat core sebagai submodule di path `core/`, dikunci ke commit tertentu.
- clau-ai-marketing juga memuat **clau-ai-agents** sebagai submodule di path `agents/` (referensi registry & validasi silang). `agents/core/` mengikuti pin milik clau-ai-agents dan harus sama dengan pin `core/` di marketing (dicek `scripts/check-core-pins.sh`).
- Sinkronisasi submodule otomatis lewat GitHub Actions (`sync-submodules`, `cross-repo-validate`, `notify-downstream`) dengan secret `SUBMODULE_TOKEN` (fine-grained PAT, scope hanya 3 repo CLAU, permission Contents + Pull requests, read and write, dengan tanggal kedaluwarsa). Bot sync tidak push langsung ke `main`: bump di-push ke branch `bot/sync-submodules` lalu dibuka sebagai PR dan di-merge setelah validasi. Token tidak pernah disimpan di file. Panduan: `SUBMODULE.md` di repo konsumen.
- Bump submodule oleh bot hanya dilakukan setelah validator & test lulus; gagal = tidak ada commit.
- Perubahan aturan dilakukan **di clau-ai-core**, bukan di folder `core/` dalam repo lain.
- Update submodule = commit tersendiri di repo konsumen dengan message `chore(core): bump core to <hash>`.

## Disiplin Push (GitHub Free, solo dev)

GitHub Free tidak menyediakan branch protection untuk repo private. Mitigasi:

1. Commit message format `feat:`, `fix:`, `docs:`, `refactor:`, `chore:`, `test:`.
2. Branch + PR untuk perubahan besar; wajib bila tim 2+ orang.
3. Validator lokal lulus sebelum push.
4. Backup rutin (push setelah tiap unit kerja).

**Status:** **ASSUMPTION**: sesuai realita solo dev & GitHub Free. Direview bila tim bertambah, upgrade plan, atau repo dibuka.

## Enforcement

- CI tiap repo menjalankan validator (termasuk pola secret sederhana).
- Validator tidak menangkap semua pelanggaran; self-review diff tetap wajib.
- Data terlarang terlanjur ter-commit: hapus dari konten aktif, nilai pembersihan history (otorisasi owner), rotasi credential, catat insiden.

## Revision History

| Version | Date | Status | Summary |
|---|---|---|---|
| 1.0.0 | 2026-10-04 | Draft | Diturunkan dari CLAU Content Repository Boundary v0.1.4; ditambah peran per repo, platform database, dan aturan submodule |
| 1.0.0 | 2026-10-04 | Approved | Approved oleh owner (Dea Karisna / d34faiza); ditambah otoritas perubahan |
| 1.1.0 | 2026-10-06 | Approved | Mencatat submodule `agents/` di clau-ai-marketing, aturan pin core, dan sinkronisasi otomatis via GitHub Actions + `SUBMODULE_TOKEN` (atas instruksi owner) |
| 1.1.1 | 2026-10-08 | Approved | Izin `SUBMODULE_TOKEN` jadi Contents + Pull requests (dengan kedaluwarsa); bot sync membuka PR dari `bot/sync-submodules`, bukan push langsung ke `main` (atas instruksi owner) |
