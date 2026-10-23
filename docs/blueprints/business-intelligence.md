# Blueprint — 🟠 AI Business Intelligence

> **Status: pilar Approved (v3.0.0, Pilar 4); isi blueprint Draft (ASSUMPTION).** Pendalaman pilar v1 "Analytics & Insights". Agent Intan (`report`) sudah aktif dengan template `monthly-report` Pilar 1; blueprint ini memperluasnya.

## Scope — Yang Dijual

Informasi untuk keputusan: AI membaca penjualan, produk, pelanggan, biaya iklan, dan stok, lalu menulis insight singkat yang bisa ditindaklanjuti.

| Contoh insight | Data yang dibutuhkan | Syarat agar boleh ditulis |
|---|---|---|
| "Produk A naik 24% bulan ini." | Penjualan per produk, 2 periode | Angka dihitung dari data, bukan diperkirakan |
| "Pelanggan baru turun dibanding bulan lalu." | Data pelanggan (agregat) | Definisi "pelanggan baru" disepakati client |
| "Iklan X menghasilkan lebih banyak inquiry." | Biaya iklan + inquiry dengan sumber (UTM/kode) | Ada tracking sumber; tanpa itu tulis "belum bisa diatribusikan" |
| "Stok produk Y diperkirakan habis." | Stok + laju penjualan | Ditulis sebagai **perkiraan** + asumsi + rentang tanggal |

## Intent & Agent

| Intent | Fungsi | Level otonomi | Approval min | Agent |
|---|---|---|---|---|
| `report` (sudah di router) | Laporan bulanan | B | L1 | Intan (aktif) |
| `kpi-dashboard` (usulan) | KPI lintas pilar | A (internal, read-only) | — | Intan |
| `insight` (usulan) | 3–5 insight + saran tindakan | B | L2 | Intan |
| `forecast` (usulan) | Perkiraan stok/penjualan + asumsi | B | L2 | Baru atau Intan |

## Aturan Khusus

1. **Angka apa adanya**: setiap angka menyebut sumber + waktu tarik data.
2. **Tanpa atribusi palsu**: korelasi tidak ditulis sebagai sebab.
3. **Perkiraan ≠ fakta**: forecast diberi label **ASSUMPTION** + metode + rentang.
4. **Pilar/data belum tersambung**: tulis "Belum ada data", bukan 0.

## Data & Privacy

Hanya agregat untuk laporan; tidak menampilkan data pribadi pelanggan individual.

## Integrasi

Data dari pilar Sales (lead, konversi), Admin (transaksi, stok), Marketing (insight platform), iklan (Meta/Google Ads — read-only).

## KPI

Laporan terkirim tepat waktu, insight yang ditindaklanjuti client, akurasi forecast (selisih vs aktual).

## Use Case Hospitality per Vertical

| Vertical | Pertanyaan owner yang ingin dijawab | Data yang dibutuhkan | Syarat |
|---|---|---|---|
| Villa / akomodasi | Bulan apa okupansi turun? Kanal booking mana yang paling banyak (direct vs OTA)? Review membahas apa? | Data booking per kanal, kalender, review | Data booking dari klien (CLIENT CONFIRMATION); tema review = ringkasan, bukan skor sentimen palsu |
| Restoran / cafe | Menu apa yang naik/turun? Jam ramai? Promo mana yang berpengaruh? | Export POS per item & jam, kalender promo | Atribusi promo hanya bila ada kode/voucher |
| Wedding & event | Dari mana inquiry datang? Berapa yang jadi booking? | Log inquiry + sumber | Butuh Sales/catatan klien |
| Travel & tour | Trip mana yang penuh/batal? Musim mana yang laku? | Data peserta per trip (agregat) | Tanpa data pribadi peserta |

## Produk Pertama yang Dijual

**"Laporan Bulanan Plus"**: laporan konten Pilar 1 (skill `build-monthly-report`, sudah aktif) ditambah satu halaman insight dari data yang klien sudah punya (export OTA/POS/booking). Tidak butuh integrasi; klien mengirim export, angka tetap apa adanya.

## Gerbang Khusus Pilar Ini

Selain gerbang umum: minimal 3 bulan laporan Pilar 1 tersimpan per klien (untuk pembanding), dan definisi metrik disepakati tertulis dengan klien.

## Keputusan Owner Saat Aktivasi

| Keputusan | Siapa |
|---|---|
| Isi "Laporan Bulanan Plus" & apakah jadi add-on Pilar 1 atau paket sendiri | Owner |
| Repo `clau-insight` atau tetap template di clau-market | Owner |
| Harga & paket | Owner (price sheet privat, bukan repo) |
| Nama agent baru, avatar, persona | Owner |
| Level A per intent per klien | Owner + klien, tertulis (AI-CONSTITUTION §4a) |

## Checklist Aktivasi

1. Scope Approved (TASK-034); Sales/Admin menghasilkan data ≥ 1–3 bulan.
2. Repo `clau-insight` (usulan): rules angka, template laporan per pilar (TASK-038), definisi KPI.
3. Intent → router + registry; eval Intan diperluas.
4. Pilot dengan data SIMULASI, lalu 1 client.
