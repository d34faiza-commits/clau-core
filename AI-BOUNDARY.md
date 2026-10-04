---
document_title: "CLAU AI Boundary"
document_owner: "Dea Karisna / AI Marketing"
version: "1.0.0"
status: "Draft"
classification: "Internal"
---

# CLAU AI Boundary

## Purpose

Menetapkan apa yang boleh dan tidak boleh disimpan di repo-repo CLAU AI (core, pilar, agents), serta di sistem yang dipakai platform. Diturunkan dari *CLAU Content Repository Boundary v0.1.4* (arsip `CLAU-AI-CONTENT`) dan diperluas untuk multi-repo dan platform.

## Authority

Tunduk pada [AI-CONSTITUTION.md](./AI-CONSTITUTION.md).

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
