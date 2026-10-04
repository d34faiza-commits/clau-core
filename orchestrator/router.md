# Router

Tabel routing request → pilar → skill. Kolom **intent** dipakai juga oleh platform clau-ai-agents (`agents/registry.json` → field `intents`).

## Tabel Routing

| Intent | Contoh request | Pilar | Skill / prompt | Repo | Approval minimum |
|---|---|---|---|---|---|
| `caption` | "Bikin caption IG untuk room tour" | 1 Marketing | `draft-caption` | clau-ai-marketing | L1–L2 |
| `reel-script` | "Script reels 20 detik pagi di villa" | 1 Marketing | `draft-reel-script` | clau-ai-marketing | L2 |
| `stories` | "Story 3 frame menu hari ini" | 1 Marketing | prompt `stories-sequence` | clau-ai-marketing | L1–L2 |
| `ota-listing` | "Update deskripsi Booking.com" | 1 Marketing | `write-ota-listing` | clau-ai-marketing | L2 |
| `review-reply` | "Balas review Google bintang 2" | 1 Marketing* | `reply-guest-review` | clau-ai-marketing | L1 (positif) / L3 (negatif) |
| `content-calendar` | "Kalender konten bulan depan" | 1 Marketing | `build-content-calendar` | clau-ai-marketing | L1 |
| `seasonal-campaign` | "Promo Ramadan & Lebaran" | 1 Marketing | `plan-seasonal-campaign` | clau-ai-marketing | L2–L3 |
| `localize` | "Terjemahkan caption ke EN" | 1 Marketing | `localize-content` | clau-ai-marketing | Mengikuti konten asal |
| `inquiry-reply` | "Balas DM tanya harga & tanggal" | 2 Sales | — | — | **Planned → eskalasi** |
| `guest-message` | "Pesan pre-arrival ke tamu" | 3 Guest Experience | — | — | **Planned → eskalasi** |
| `sop` | "SOP housekeeping" | 4 Operations | — | — | **Planned → eskalasi** |
| `report` | "Report performa bulanan" | 5 Analytics | template `monthly-report` (Pilar 1) | clau-ai-marketing | L1 |

\* `review-reply` sementara di Pilar 1. Saat Pilar 3 aktif, intent ini dipindah (**NEXT ACTION** saat aktivasi Pilar 3).

## Aturan

- Intent tidak dikenal → tanyakan klarifikasi ke requester; jangan menebak pilar.
- Request yang mengandung beberapa intent (mis. "caption + balas DM harga") dipecah per intent.
- Intent di pilar *Planned* tidak dikerjakan; buat task di board dengan label pilar dan eskalasi ke owner.
- Level approval di tabel adalah **minimum**; rules pilar bisa menaikkannya (mis. ada harga/promo → minimal L2).
