# Vertical — Jenis Usaha yang Dilayani

> **Status: fokus Approved (AI-CONSTITUTION v3.0.0 §2, 2026-10-09).** Fokus sekarang: **villa, restoran/cafe, wedding & event, travel & tour**, dibuat siap enterprise lebih dulu. Hotel dan spa tetap dilayani. Vertical di luar hospitality & tourism berstatus *Planned*: knowledge awal sudah disiapkan (**ASSUMPTION**) tetapi **tidak dipakai untuk client** sebelum amandemen scope ([proposals/autonomy-levels.md](./proposals/autonomy-levels.md) Usulan 2) dan checklist aktivasi selesai.

## Daftar Vertical

| Vertical | Kelompok | Status | Knowledge segment (clau-market) | Gelombang |
|---|---|---|---|---|
| Villa / guesthouse / homestay | Hospitality | **Fokus — Aktif** | `knowledge/segments/villa.md` · fact sheet `templates/property-fact-sheet.md` · pilot `examples/pilot-villa-contoh-ubud`, `pilot-2` | — |
| Restaurant / cafe / beach club | Hospitality | **Fokus — Aktif** | `knowledge/segments/restaurant.md` · fact sheet `templates/fnb-fact-sheet.md` · pilot `examples/pilot-kafe-contoh-canggu` | — |
| Wedding & event | Hospitality | **Fokus — aktivasi** (knowledge ASSUMPTION; Status Verifikasi di segment) | `knowledge/segments/wedding.md` · fact sheet `templates/wedding-fact-sheet.md` · pilot `examples/pilot-wedding-contoh-uluwatu` | 1 |
| Travel & tour operator | Tourism | **Fokus — aktivasi** (knowledge ASSUMPTION; Status Verifikasi di segment) | `knowledge/segments/travel.md` · fact sheet `templates/travel-fact-sheet.md` · pilot `examples/pilot-trip-contoh-labuan-bajo` | 1 |
| Hotel / resort | Hospitality | Aktif (dilayani) | `knowledge/segments/hotel.md` | — |
| Spa / wellness / retreat | Hospitality | Aktif (dilayani) | `knowledge/segments/spa.md` | — |
| Salon & barbershop | Jasa lokal | Planned | `knowledge/segments/salon.md` | 2 |
| Toko / retail / UMKM produk | Retail | Planned | `knowledge/segments/retail.md` | 2 |
| Rental (kendaraan, alat) | Jasa lokal | Planned | `knowledge/segments/rental.md` | 3 |
| Kontraktor & renovasi | Jasa proyek | Planned | `knowledge/segments/contractor.md` | 3 |
| Jasa profesional (konsultan, akuntan, notaris, klinik, dll.) | Profesional | Planned | `knowledge/segments/professional-services.md` | 4 |

Gelombang = urutan usulan (1–2 vertical per kuartal setelah Fase 0 platform). Urutan final = keputusan owner (TASK-041).

## Kenapa Urutan Ini

| Gelombang | Alasan |
|---|---|
| 1 Wedding, travel | Dekat dengan knowledge hospitality yang ada (venue, destinasi, paket, musim); klien villa/hotel sering juga menjual wedding & tur |
| 2 Salon, retail | Pasar besar & berulang; klaim produk/kecantikan butuh rules tambahan (BPOM, before/after) |
| 3 Rental, kontraktor | Transaksi besar, butuh Sales & Admin (quotation, kontrak, deposit) yang kuat |
| 4 Jasa profesional | Aturan etika profesi membatasi iklan; risiko hukum tertinggi |

## Checklist Aktivasi Vertical

1. Owner menyetujui vertical (TASK-041). Wedding & travel sudah masuk scope v3.0.0; vertical non-hospitality butuh amandemen scope §2 lebih dulu.
2. Knowledge segment: setiap baris ASSUMPTION diverifikasi (sumber + tanggal akses) atau diganti **CLIENT CONFIRMATION** per client.
3. Rules: cek apakah rules pilar cukup; tambah rule khusus bila ada regulasi sektor (mis. BPOM, etika profesi, perizinan usaha).
4. Voice guide & contoh fiktif ("Contoh") untuk vertical.
5. Eval agent ditambah ≥ 2 kasus per vertical.
6. Pilot SIMULASI, lalu 1 client pilot dengan review manusia penuh.
7. Ubah status di tabel ini → **Aktif**.
