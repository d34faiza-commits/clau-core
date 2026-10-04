# Priority Engine

Cara menghitung prioritas antrian kerja lintas pilar. Hasilnya dipetakan ke field `Priority` di task board (Low / Normal / High / Urgent).

## Skor

`skor = urgensi + dampak + risiko` (masing-masing 0–3, total 0–9)

| Faktor | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| **Urgensi** (tenggat) | > 2 minggu | 1–2 minggu | 2–7 hari | < 48 jam atau sudah lewat |
| **Dampak** (bisnis) | Internal kecil | Konten rutin | Promo/campaign, listing OTA | Revenue langsung atau reputasi publik (mis. review viral) |
| **Risiko** (bila salah/terlambat) | Hampir nol | Koreksi mudah | Komplain tamu / revisi besar | Legal, privacy, keselamatan, krisis |

## Pemetaan ke Priority

| Skor | Priority | Aturan |
|---|---|---|
| 8–9, atau risiko = 3 | **Urgent** | Dikerjakan hari ini; eskalasi owner bila butuh keputusan |
| 6–7 | **High** | Minggu ini |
| 3–5 | **Normal** | Bulan ini |
| 0–2 | **Low** | Kapan sempat |

## Contoh (fiktif)

| Request | Urgensi | Dampak | Risiko | Skor | Priority |
|---|---|---|---|---|---|
| Review Google menuduh keracunan makanan, diposting kemarin | 3 | 3 | 3 | 9 | Urgent (eskalasi L3) |
| Kalender konten bulan depan, tenggat 10 hari | 1 | 1 | 1 | 3 | Normal |
| Update listing OTA setelah renovasi, mulai jual 5 hari lagi | 2 | 2 | 2 | 6 | High |

## Batas

- Prioritas **tidak** mengurangi QA atau approval. Urgent tetap butuh approval sesuai level.
- Skor adalah alat bantu; owner boleh override dengan alasan tertulis di task.
- Nilai ambang di atas berstatus **ASSUMPTION**, dikalibrasi ulang setelah 1 bulan pemakaian nyata.
