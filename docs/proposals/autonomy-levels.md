# Usulan Amandemen — Otonomi Bertingkat & Perluasan Scope

> **Status: Draft — BELUM BERLAKU.** Usulan perubahan AI-CONSTITUTION v2.0.0 (Approved) untuk konsep v2 ([blueprints](../blueprints/README.md)). Hanya berlaku setelah ada perintah tertulis **Pak Indra** atau **Dea Karisna (d34faiza)**, lalu diterapkan ke [AI-CONSTITUTION.md](../../AI-CONSTITUTION.md) sebagai v2.1.0 (atau v3.0.0) dengan Revision History. Keputusan dicatat di TASK-040.

## Kenapa

AI-CONSTITUTION §4.7 sekarang: *"AI tidak publish, mengirim ke pihak luar, mengubah sistem client, atau self-approve."* Ini tepat untuk Marketing, tetapi membuat AI Sales (WhatsApp assistant) dan AI Automation tidak bisa menjawab customer secara otomatis sama sekali. §2 juga membatasi vertical ke hospitality & tourism.

## Usulan 1 — Level Otonomi

| Level | Arti | Boleh untuk | Contoh |
|---|---|---|---|
| **A — Otomatis** | AI boleh mengirim/menjalankan sendiri | Jawaban dari **template yang disetujui client** + fakta **DATA FINAL**; aksi internal read/write yang tidak keluar ke pihak luar | Jam buka, lokasi, katalog yang disetujui, "pesan diterima", catat lead, rekap stok |
| **B — Draft** | AI menyiapkan, manusia menekan kirim/terapkan | Harga khusus, penawaran, quotation, invoice, follow-up promosi, konten publik | Quotation, invoice, caption, iklan |
| **C — Eskalasi** | AI tidak menjawab substansi; langsung ke owner | Komplain serius, refund/kompensasi, hukum, kesehatan, keselamatan, data sensitif, permintaan di luar template | "Saya mau refund", ancaman review buruk, keluhan keracunan |

### Aturan Level A

1. Hanya aktif per client setelah client menyetujui **daftar template Level A** (tercatat, versi).
2. AI tidak membuat komitmen baru (harga, diskon, ketersediaan, refund) di Level A.
3. Setiap pesan Level A tercatat (audit log) dan bisa ditarik untuk sampel review manusia.
4. 2 minggu pertama per client: semua pesan Level A di-review manusia setelah terkirim; ambang koreksi > 5% → kembali ke Level B.
5. AI tidak mengaku manusia; customer selalu bisa meminta "bicara dengan tim".
6. Pesan promosi hanya ke kontak **opt-in**.
7. Owner bisa mematikan Level A per client seketika (tombol berhenti).

### Teks usulan §4.7 (pengganti)

> 7. **Human approval**: AI tidak publish, tidak mengubah sistem client, dan tidak self-approve. AI hanya mengirim ke pihak luar pada **Level A** (template yang disetujui client + fakta DATA FINAL, tercatat di audit log); selain itu draft (Level B) atau eskalasi (Level C). Lihat Otonomi Bertingkat.

Default untuk semua pilar tetap **Level B**. Level A harus diaktifkan eksplisit per intent di router dan per client.

## Usulan 2 — Perluasan Scope Vertical

### Teks usulan §2 (baris Vertical)

> | Vertical | Aktif: villa/guesthouse/homestay, hotel/resort, restaurant/cafe/beach club, spa/wellness/retreat, tourism experience. Planned: lihat `docs/verticals.md`; vertical Planned tidak dipakai untuk client sebelum knowledge, rules, dan pilot-nya di-approve |

§1 Purpose ikut diubah dari "bisnis hospitality & tourism Indonesia" menjadi "bisnis Indonesia, dimulai dari hospitality & tourism".

## Dampak ke Repo

| Repo | Perubahan saat amandemen berlaku |
|---|---|
| clau-ai-core | AI-CONSTITUTION versi baru; kolom **Otonomi** di `orchestrator/router.md`; `shared/api-contracts.md` (`autonomy_level` di respons `/route`) |
| clau-ai-agents | `registry.json` field `autonomy_max` per agent; `default_forbidden_actions` `send_external` menjadi kondisional (hanya Level A); test baru |
| clau-ai-marketing | Tidak berubah (semua aksi Marketing tetap Level B) |
| CLAU-AI-CONTENT/design | Badge level otonomi A/B/C di Studio; pengaturan template Level A di Portal Klien |
