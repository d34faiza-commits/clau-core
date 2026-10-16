# Router

Tabel routing request → pilar → skill → level otonomi (AI-CONSTITUTION §4a). Kolom **intent** dipakai juga oleh platform clau-agent (`agents/registry.json` → field `intents`).

## Tabel Routing

| Intent | Contoh request | Pilar | Skill / prompt | Repo | Approval minimum | Otonomi |
|---|---|---|---|---|---|---|
| `caption` | "Bikin caption IG untuk room tour" | 1 AI Marketing | `draft-caption` | clau-market | L1–L2 | B |
| `reel-script` | "Script reels 20 detik pagi di villa" | 1 AI Marketing | `draft-reel-script` | clau-market | L2 | B |
| `stories` | "Story 3 frame menu hari ini" | 1 AI Marketing | prompt `stories-sequence` | clau-market | L1–L2 | B |
| `ota-listing` | "Update deskripsi Booking.com" | 1 AI Marketing | `write-ota-listing` | clau-market | L2 | B |
| `review-reply` | "Balas review Google bintang 2" | 1 AI Marketing* | `reply-guest-review` | clau-market | L1 (positif) / L3 (negatif) | B |
| `content-calendar` | "Kalender konten bulan depan" | 1 AI Marketing | `build-content-calendar` | clau-market | L1 | B |
| `seasonal-campaign` | "Promo Ramadan & Lebaran" | 1 AI Marketing | `plan-seasonal-campaign` | clau-market | L2–L3 | B |
| `localize` | "Terjemahkan caption ke EN" | 1 AI Marketing | `localize-content` | clau-market | Mengikuti konten asal | B |
| `inquiry-reply` | "Balas DM tanya harga & tanggal" | 2 AI Sales | — | — | **Planned → eskalasi** | B |
| `guest-message` | "Pesan pre-arrival ke tamu" | 2 AI Sales | — | — | **Planned → eskalasi** | B |
| `sop` | "SOP housekeeping" | 3 AI Admin | — | — | **Planned → eskalasi** | B |
| `report` | "Report performa bulanan" | 4 AI Business Intelligence | template `monthly-report` (Pilar 1) | clau-market | L1 | B |

\* `review-reply` sementara di Pilar 1. Saat Pilar 2 AI Sales aktif (customer service & reputasi), intent ini dipindah (**NEXT ACTION** saat aktivasi Pilar 2).

Pilar 5 AI Automation tidak punya intent konten sendiri; alurnya memanggil intent pilar lain (lihat [blueprints/automation.md](../docs/blueprints/automation.md)).

## Aturan

- Intent tidak dikenal → tanyakan klarifikasi ke requester; jangan menebak pilar.
- Request yang mengandung beberapa intent (mis. "caption + balas DM harga") dipecah per intent.
- Intent di pilar *Planned* tidak dikerjakan; buat task di board dengan label pilar dan eskalasi ke owner.
- Level approval di tabel adalah **minimum**; rules pilar bisa menaikkannya (mis. ada harga/promo → minimal L2).
- Kolom **Otonomi** = level maksimum yang boleh dipakai intent itu (AI-CONSTITUTION §4a). Default semua intent **B**. Mengubah ke **A** butuh perintah owner, template Level A yang disetujui per client, audit log, dan tombol berhenti; level ini juga dicerminkan di `clau-agent/agents/registry.json` → `autonomy_max`.
- Apa pun levelnya, situasi Level C (komplain serius, refund, hukum, kesehatan, keselamatan, data sensitif) selalu eskalasi ke owner.
