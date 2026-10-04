# Integrations

Daftar integrasi eksternal, statusnya, dan batasnya. Level otomasi mengikuti `clau-ai-marketing/automations/` (saat ini **Level 1: manual**).

## Status Integrasi

| Sistem | Kegunaan | Arah | Status | Batas |
|---|---|---|---|---|
| AI model provider (mis. Claude API) | Drafting, klasifikasi, first-pass QA | Platform → provider | Planned (backend belum memanggil model) | Tanpa credential/data tamu mentah; model & retensi dicatat per environment |
| GitHub (repo CLAU) | Sumber rules/skills/knowledge | Platform ← repo | Planned (baca registry & skill) | Read-only |
| Instagram / Facebook (Meta) | Insight, jadwal post | — | Tidak diintegrasikan | Level 1: manusia publish lewat tools resmi platform |
| TikTok | Insight, post | — | Tidak diintegrasikan | Sama seperti di atas |
| Google Business Profile | Post, review | — | Tidak diintegrasikan | Balasan review dipublish manusia |
| OTA (Traveloka, tiket.com, Booking.com, Agoda, Airbnb) | Listing | — | Tidak diintegrasikan | Listing diupdate manusia di extranet |
| WhatsApp Business | Inquiry, broadcast | — | Tidak diintegrasikan (Pilar 2/3 planned) | Broadcast hanya ke kontak opt-in |
| PMS / booking engine | Ketersediaan, harga | — | Tidak diintegrasikan | AI tidak mengubah harga/ketersediaan |

## Aturan Menambah Integrasi

1. Tulis use case, data yang mengalir, dan zona penyimpanannya ([data-flow.md](./data-flow.md)).
2. Pastikan tidak ada aksi publish/kirim/ubah sistem client tanpa langkah approval manusia.
3. Credential lewat secret manager; scope akses minimum (read-only bila cukup).
4. Approval owner tertulis; update tabel ini dan [AI-BOUNDARY.md](../AI-BOUNDARY.md) bila ada zona baru.
5. Pemilihan vendor/tool dievaluasi tersendiri; dokumen ini tidak merekomendasikan merek.
