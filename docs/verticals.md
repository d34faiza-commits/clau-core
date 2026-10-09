# Vertical — Jenis Usaha yang Dilayani

> **Status: Draft.** Daftar jenis usaha CLAU AI dan urutan perluasannya. **Fokus sekarang: hospitality.** Vertical berstatus *Planned* sudah disiapkan knowledge awalnya (**ASSUMPTION**) supaya saat siap tinggal diverifikasi & diaktifkan, tetapi **tidak dipakai untuk client** sebelum checklist aktivasi selesai. Perluasan scope di luar hospitality menunggu amandemen §2 AI-CONSTITUTION ([proposals/autonomy-levels.md](./proposals/autonomy-levels.md), TASK-040).

## Daftar Vertical

| Vertical | Kelompok | Status | Knowledge segment (clau-ai-marketing) | Gelombang |
|---|---|---|---|---|
| Villa / guesthouse / homestay | Hospitality | **Aktif** | `knowledge/segments/villa.md` | — |
| Hotel / resort | Hospitality | **Aktif** | `knowledge/segments/hotel.md` | — |
| Restaurant / cafe / beach club | Hospitality | **Aktif** | `knowledge/segments/restaurant.md` | — |
| Spa / wellness / retreat | Hospitality | **Aktif** | `knowledge/segments/spa.md` | — |
| Wedding & event | Hospitality-dekat | Planned | `knowledge/segments/wedding.md` | 1 |
| Travel & tour operator | Tourism | Planned | `knowledge/segments/travel.md` | 1 |
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

1. Owner menyetujui vertical (TASK-041) dan, untuk non-hospitality, amandemen scope §2 sudah berlaku.
2. Knowledge segment: setiap baris ASSUMPTION diverifikasi (sumber + tanggal akses) atau diganti **CLIENT CONFIRMATION** per client.
3. Rules: cek apakah rules pilar cukup; tambah rule khusus bila ada regulasi sektor (mis. BPOM, etika profesi, perizinan usaha).
4. Voice guide & contoh fiktif ("Contoh") untuk vertical.
5. Eval agent ditambah ≥ 2 kasus per vertical.
6. Pilot SIMULASI, lalu 1 client pilot dengan review manusia penuh.
7. Ubah status di tabel ini → **Aktif**.
