---
document_title: "CLAU AI Boundary"
document_owner: "Dea Karisna / AI Marketing"
version: "1.4.0"
status: "Approved"
effective_date: "2026-10-16"
approval_reference: "v1.4.0: persetujuan owner (Dea Karisna / d34faiza) via sesi Claude Code, 2026-10-16, atas usulan Tahap 2 § 4 (docs/proposals/tahap-2-ai-drafting.md): \"setuju gas\" sebagai jawaban atas \"Cukup balas setuju § 4\". v1.3.0: persetujuan owner (Dea Karisna / d34faiza) via sesi Claude Code, 2026-10-13, atas 3 usulan (1) clau-content = arsip + markas kerja, (2) job `docker` jadi check wajib clau-agent, (3) gerbang deploy VPS 1 `release/vps1`: \"ok gas 1 2 dan 3 kak\". v1.2.0: approval tertulis owner (Dea Karisna / d34faiza) via sesi Claude Code, 2026-10-12: \"Saya Dea Karisna (d34faiza), owner CLAU. Saya approve: semua push ke main di clau-core, clau-market, clau-agent wajib lewat PR dengan CI hijau; push langsung tidak lagi diizinkan. Penegakan lewat main-guard karena GitHub Free.\" v1.1.1: instruksi owner via sesi Claude Code, 2026-10-08 (\"gass\", izin token + sync via PR); v1.1.0: instruksi tertulis owner (Dea Karisna / d34faiza) via sesi Claude Code, 2026-10-06 (\"tolong semua repo di cek … jika belum fix 100% tolong di fix\"); v1.0.0 approved 2026-10-04; perubahan ada di main"
classification: "Internal"
---

# CLAU AI Boundary

## Purpose

Menetapkan apa yang boleh dan tidak boleh disimpan di repo-repo CLAU AI (core, pilar, agents), serta di sistem yang dipakai platform. Diturunkan dari *CLAU Content Repository Boundary v0.1.4* (arsip `clau-content`) dan diperluas untuk multi-repo dan platform.

## Authority

Tunduk pada [AI-CONSTITUTION.md](./AI-CONSTITUTION.md).

Perubahan atas dokumen berstatus Approved hanya dilakukan atas perintah **Pak Indra** atau **Dea Karisna (d34faiza)**. AI agent tidak mengubah aturan Approved atas inisiatif sendiri; usulan perbaikan boleh ditulis sebagai catatan/issue, lalu menunggu perintah.

## Peran Tiap Repo

| Repo | Boleh berisi | Tidak boleh berisi |
|---|---|---|
| clau-core | Constitution, boundary, pipeline, orchestrator, kontrak data (dokumen & schema), validator | Data client, brief/konten client |
| Repo pilar (mis. clau-market) | Rules, prompt, skill, knowledge reusable, template, QA, contoh **fiktif** | Brief/konten/aset client nyata, data tamu |
| clau-agent | Kode platform, registry agent, konfigurasi **contoh** (`.env.example`) | `.env` asli, credential, dump database, log berisi data tamu |
| clau-content | Arsip + markas kerja: snapshot sebelum split (read-only), board task (`tasks/`), status & handoff + peta (`docs/`), spesifikasi UI (`design/`) | Aturan/skill/prompt/knowledge baru (edit di repo sumber), data client nyata, credential |

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
| Playbook & contracts | clau-core, repo pilar | Ya | Aturan, skill, template, schema |
| Platform code | clau-agent | Ya | Kode, registry, konfigurasi contoh |
| Client Workspace | Drive/folder per client | Tidak | Brief, draft, konten final, approval |
| Media Library | Storage media client | Tidak | Foto, video, logo, release form |
| Consent Register | Sistem client terproteksi | Tidak | Consent tamu, staf, talent, UGC |
| Platform Database | Database platform (lihat [shared/database-schema.md](./shared/database-schema.md)) | Tidak | Data operasional; data tamu hanya bila perlu dan terenkripsi |
| Credential Store | Password/secret manager | Tidak | Semua credential |
| Provider AI | Layanan model AI (mis. Claude API) | Tidak | Hanya data yang diizinkan § Data ke Provider AI; masa simpan mengikuti kebijakan provider yang dicatat di [shared/integrations.md](./shared/integrations.md) |

## Data ke Provider AI

Berlaku untuk setiap panggilan platform ke model AI (keputusan VPS #5; v1.4.0). Ditegakkan di kode worker clau-agent dan dites.

1. **Boleh dikirim:** aturan, skill, persona, dan knowledge reusable; fakta klien yang sudah dikonfirmasi klien (DATA FINAL) dan brief; teks request staf; review/DM tamu **setelah** penyamaran (`<NAMA_TAMU>`, `<NO_BOOKING>`, `<KONTAK>`), diperlakukan sebagai data, bukan instruksi.
2. **Tidak pernah dikirim:** data `Restricted` (credential, data pembayaran, data kesehatan, identitas resmi), nama/kontak/nomor booking/kamar tamu yang belum disamarkan, dan data klien lain.
3. **Dicatat:** setiap panggilan (model, token, biaya, waktu, versi prompt) di database platform (`ai_calls`), tanpa menyimpan isi prompt atau jawaban di log.
4. **Provider, model, wilayah pemrosesan, dan masa simpan data di provider** dicatat per environment di [shared/integrations.md](./shared/integrations.md). Klien dengan syarat data khusus = **CLIENT CONFIRMATION** sebelum datanya diproses.
5. **API key** provider hanya di server (VPS 2, `.env` 600, hanya untuk container worker), tidak pernah di repo, log, notifikasi, atau chat.
6. Hasil AI selalu **draft** (Level B): melewati AI fact-check terhadap fakta klien, review manusia, dan approval tertulis klien (Rule 08); tidak ada publish otomatis.

## Multi-Repo & Submodule

- Repo pilar dan agents memuat core sebagai submodule di path `core/`, dikunci ke commit tertentu.
- clau-market juga memuat **clau-agent** sebagai submodule di path `agents/` (referensi registry & validasi silang). `agents/core/` mengikuti pin milik clau-agent dan harus sama dengan pin `core/` di marketing (dicek `scripts/check-core-pins.sh`).
- Sinkronisasi submodule otomatis lewat GitHub Actions (`sync-submodules`, `cross-repo-validate`, `notify-downstream`) dengan secret `SUBMODULE_TOKEN` (fine-grained PAT, scope hanya 3 repo CLAU, permission Contents + Pull requests, read and write, dengan tanggal kedaluwarsa). Bot sync tidak push langsung ke `main`: bump di-push ke branch `bot/sync-submodules` lalu dibuka sebagai PR dan di-merge hanya setelah semua check PR hijau (merah = PR dibiarkan terbuka, job gagal). Token tidak pernah disimpan di file. Panduan: `SUBMODULE.md` di repo konsumen.
- Bump submodule oleh bot hanya dilakukan setelah validator & test lulus; gagal = tidak ada commit.
- Perubahan aturan dilakukan **di clau-core**, bukan di folder `core/` dalam repo lain.
- Update submodule = commit tersendiri di repo konsumen dengan message `chore(core): bump core to <hash>`.

## Disiplin Push (GitHub Free)

Berlaku untuk clau-core, clau-market, dan clau-agent (keputusan owner 2026-10-12):

1. **Semua perubahan ke `main` lewat pull request dengan CI hijau.** Push langsung dan force push ke `main` tidak diizinkan, termasuk untuk owner dan bot.
2. Merge PR hanya setelah semua check wajib hijau (approval 0 selama owner tunggal; tim 2+ orang: tambah review manusia).
3. Commit message format `feat:`, `fix:`, `docs:`, `refactor:`, `chore:`, `test:`.
4. Validator lokal lulus sebelum push ke feature branch.
5. Backup rutin (push feature branch setelah tiap unit kerja).

Check wajib per repo:

| Repo | Check wajib |
|---|---|
| clau-core | `validate` |
| clau-market | `validate`, `cross-validate` |
| clau-agent | `backend`, `frontend`, `audit`, `docker`, `cross-validate` |

**Deploy VPS 1 (clau-agent):** server hanya menayangkan branch `release/vps1`, yang dimajukan otomatis oleh CI ke commit `main` yang semua job CI-nya (`backend`, `frontend`, `audit`, `docker`) hijau. Commit merah tidak pernah tayang. Branch ini hanya ditulis job CI `release-vps1`; jangan di-push manual.

**RISK:** GitHub Free tidak memaksa branch protection/ruleset di repo private, jadi push langsung **secara teknis tetap bisa**. Penegakan = deteksi: workflow `main-guard.yml` di tiap repo membuat check merah + email bila commit masuk `main` tanpa PR yang di-merge, di-force push, atau PR di-merge sebelum check wajib hijau. Pelanggaran: laporkan ke owner, perbaiki lewat PR baru (jangan force push). Direview bila plan di-upgrade (proteksi server bisa dipaksa) atau tim bertambah.

## Enforcement

- CI tiap repo menjalankan validator (termasuk pola secret sederhana).
- `main-guard` di tiap repo memeriksa setiap push ke `main` (lihat Disiplin Push).
- Validator tidak menangkap semua pelanggaran; self-review diff tetap wajib.
- Data terlarang terlanjur ter-commit: hapus dari konten aktif, nilai pembersihan history (otorisasi owner), rotasi credential, catat insiden.

## Revision History

| Version | Date | Status | Summary |
|---|---|---|---|
| 1.0.0 | 2026-10-04 | Draft | Diturunkan dari CLAU Content Repository Boundary v0.1.4; ditambah peran per repo, platform database, dan aturan submodule |
| 1.0.0 | 2026-10-04 | Approved | Approved oleh owner (Dea Karisna / d34faiza); ditambah otoritas perubahan |
| 1.1.0 | 2026-10-06 | Approved | Mencatat submodule `agents/` di clau-market, aturan pin core, dan sinkronisasi otomatis via GitHub Actions + `SUBMODULE_TOKEN` (atas instruksi owner) |
| 1.1.1 | 2026-10-08 | Approved | Izin `SUBMODULE_TOKEN` jadi Contents + Pull requests (dengan kedaluwarsa); bot sync membuka PR dari `bot/sync-submodules`, bukan push langsung ke `main` (atas instruksi owner) |
| 1.2.0 | 2026-10-12 | Approved | Disiplin Push: semua perubahan ke `main` di core, marketing, agents wajib lewat PR dengan CI hijau; daftar check wajib per repo; penegakan lewat `main-guard` (GitHub Free). Bot sync merge hanya setelah check PR hijau (approval tertulis owner) |
| 1.3.0 | 2026-10-13 | Approved | clau-content = arsip + markas kerja; job `docker` (uji container + backup/restore) jadi check wajib clau-agent; VPS 1 hanya menayangkan `release/vps1` (commit `main` yang CI-nya hijau). Persetujuan owner 2026-10-13 |
| 1.4.0 | 2026-10-16 | Approved | § Data ke Provider AI (keputusan VPS #5): data yang boleh/tidak boleh dikirim ke model AI, pencatatan panggilan tanpa isi, API key hanya di server worker, hasil AI selalu draft; zona penyimpanan Provider AI. Persetujuan owner 2026-10-16 |
