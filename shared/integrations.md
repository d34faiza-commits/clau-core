# Integrations

Daftar integrasi eksternal, statusnya, dan batasnya. Level otomasi mengikuti `clau-ai-marketing/automations/` (saat ini **Level 1: manual**).

## Status Integrasi

| Sistem | Kegunaan | Arah | Status | Batas |
|---|---|---|---|---|
| AI model provider (Claude API, Anthropic) | Drafting, klasifikasi, first-pass QA | Platform (worker VPS 2) → provider | Antrean + worker + provider tiruan (backend 0.9.0); provider Claude menyusul (Tahap 2 PR 4c). Belum ada panggilan ke provider nyata | AI-BOUNDARY § Data ke Provider AI. Per environment dicatat di bawah |
| GitHub (repo CLAU) | Sumber rules/skills/knowledge | Platform ← repo | Planned (baca registry & skill) | Read-only |
| Instagram / Facebook (Meta) | Insight, jadwal post | — | Tidak diintegrasikan | Level 1: manusia publish lewat tools resmi platform |
| TikTok | Insight, post | — | Tidak diintegrasikan | Sama seperti di atas |
| Google Business Profile | Post, review | — | Tidak diintegrasikan | Balasan review dipublish manusia |
| OTA (Traveloka, tiket.com, Booking.com, Agoda, Airbnb) | Listing | — | Tidak diintegrasikan | Listing diupdate manusia di extranet |
| WhatsApp Business | Inquiry, broadcast | — | Tidak diintegrasikan (Pilar 2 AI Sales planned; Level A hanya via template disetujui client, AI-CONSTITUTION §4a) | Broadcast hanya ke kontak opt-in |
| PMS / booking engine | Ketersediaan, harga | — | Tidak diintegrasikan | AI tidak mengubah harga/ketersediaan |

## Provider AI per Environment

| Environment | Provider | Model (arahan owner 2026-10-15) | Wilayah & masa simpan di provider | Status |
|---|---|---|---|---|
| Lokal / CI | Tiruan (`CLAU_AI_PROVIDER=fake`) | — | Tidak ada data keluar | Aktif |
| VPS 2 | Claude API (Anthropic) | Sulit: `claude-fable-5-1` · Utama: `claude-opus-5-5` · Ringan: `claude-haiku-5-5` (setelah lolos eval) | **NEXT ACTION:** dicatat saat akun provider dibuat (owner). `claude-fable-5-1` mensyaratkan retensi minimal 30 hari (tidak bisa zero data retention) | Belum (menunggu akun & biaya, TASK-052) |

## Aturan Menambah Integrasi

1. Tulis use case, data yang mengalir, dan zona penyimpanannya ([data-flow.md](./data-flow.md)).
2. Pastikan tidak ada aksi publish/kirim/ubah sistem client tanpa langkah approval manusia.
3. Credential lewat secret manager; scope akses minimum (read-only bila cukup).
4. Approval owner tertulis; update tabel ini dan [AI-BOUNDARY.md](../AI-BOUNDARY.md) bila ada zona baru.
5. Pemilihan vendor/tool dievaluasi tersendiri; dokumen ini tidak merekomendasikan merek.
