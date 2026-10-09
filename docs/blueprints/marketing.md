# Blueprint — 🟣 AI Marketing (v2)

> **Status: pilar Approved (v3.0.0); isi blueprint Draft (ASSUMPTION).** Perluasan Pilar 1 AI Marketing (dulu "Marketing & Content") yang sudah **Aktif** di clau-ai-marketing. Bagian yang sudah ada tetap berlaku; tabel di bawah menandai yang baru.

## Scope — Yang Dijual

| Layanan | Status | Catatan |
|---|---|---|
| Caption, reel script, story, listing OTA, balasan review, kalender konten, campaign musiman, lokalisasi | **Aktif** | 8 agent (Tara, Raka, Sekar, Bayu, Laras, Dimas, Ayu, Nara) |
| Copywriting website & landing page | Baru | Struktur halaman, headline, CTA, FAQ; fakta dari fact sheet |
| Konsep & brief iklan (Meta, Google, TikTok Ads) | Baru | AI tidak memegang akun iklan, tidak mengatur budget, tidak publish |
| Brief foto produk & video | Baru | Shot list, art direction; visual AI mengikuti rule 07 (disclosure) |
| Branding (voice guide, tagline, konsep logo) | Baru | Logo final = desainer manusia; cek merek terdaftar (PDKI) = **CLIENT CONFIRMATION** |

## Intent & Agent Usulan

| Intent usulan | Fungsi | Approval min | Agent |
|---|---|---|---|
| `landing-page` | Copy landing page / website per section | L2 | Baru (nama ditentukan owner) |
| `ad-brief` | Konsep iklan + 3 varian copy + target audiens | L2 | Baru |
| `visual-brief` | Shot list foto/video produk | L1 | Baru |
| `brand-voice` | Voice guide & tagline | L3 | Baru |

## Otonomi

Semua aksi Marketing tetap **Level B (draft)**: AI menyiapkan, manusia publish. Tidak ada auto-publish (lihat [autonomy-levels](../proposals/autonomy-levels.md)).

## Data & Privacy

Sama dengan Pilar 1: consent untuk wajah/nama/UGC (rule 04), data iklan hanya agregat.

## Risiko

| Risiko | Mitigasi |
|---|---|
| Klaim iklan berlebihan ("terbaik", "garansi") | Rule 02 + kebijakan iklan platform; QA klaim per kalimat |
| Iklan kategori sensitif (alkohol, kesehatan, finansial, properti) | **RISK** → legal review + kebijakan platform terbaru |
| Logo mirip merek lain | Cek PDKI sebelum dipakai; konsep AI hanya eksplorasi |

## KPI

Waktu produksi per konten, rasio approval tanpa revisi, temuan QA klaim, performa (hanya dari data platform yang tersambung).

## Checklist Aktivasi

1. Template & skill baru di `clau-ai-marketing` (`landing-page`, `ad-brief`, `visual-brief`, `brand-voice`) + QA.
2. Rules: tambah standar iklan berbayar (atau perluas rule 05 platform).
3. Intent → `router.md`, agent → `registry.json` (+ persona, eval, avatar).
4. Pilot SIMULASI per layanan.
