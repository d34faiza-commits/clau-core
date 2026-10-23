# Blueprint — 🟢 AI Admin

> **Status: pilar Approved (v3.0.0, Pilar 3); isi blueprint Draft (ASSUMPTION).** Perluasan pilar v1 "Operations" (SOP) menjadi pekerjaan administrasi bisnis.

## Scope — Yang Dijual

Invoice, quotation, data entry, dokumen, laporan, financial summary, inventory, SOP.

## Alur Contoh

```text
Data (transaksi, nota, export POS/Sheets) ─► AI baca & rapikan ─► cek konsistensi (total, duplikat)
   ─► draft laporan / quotation / invoice ─► manusia cek & setujui ─► manusia kirim / simpan
```

## Intent & Agent

| Intent | Fungsi | Level otonomi | Approval min | Agent |
|---|---|---|---|---|
| `sop` (sudah di router) | SOP & checklist | B | L1 | Teguh (planned) |
| `quotation` (usulan) | Draft penawaran dari katalog & harga DATA FINAL | B | L2 | Baru |
| `invoice-draft` (usulan) | Draft invoice dari order yang disetujui | B | L2 | Baru |
| `data-entry` (usulan) | Ekstrak data dari nota/form ke tabel | A (internal) + sampel dicek manusia | L1 | Baru |
| `financial-summary` (usulan) | Ringkasan pemasukan/pengeluaran periode | B | L2 | Baru |
| `inventory-check` (usulan) | Rekap stok + peringatan stok menipis | A (internal) | L1 | Baru |

## Aturan Khusus

| Aturan | Isi |
|---|---|
| Angka | AI tidak mengarang angka; setiap total bisa ditelusuri ke baris data sumber |
| Pajak | Perhitungan PPN/PB1/service charge mengikuti setting client yang **DATA FINAL**; dokumen pajak resmi (e-Faktur, SPT) di luar scope AI |
| Invoice & quotation | Selalu draft; nomor dokumen dari sistem, bukan dibuat AI; manusia yang mengirim |
| Bukan nasihat | Financial summary = rekap, bukan nasihat pajak/hukum/investasi |

## Data & Privacy

Data keuangan & pelanggan = **Confidential**. Disimpan terenkripsi, akses per peran, audit log setiap ekspor. Tidak pernah masuk repo.

## Integrasi

Google Sheets / Excel, export POS, akuntansi (mis. Jurnal, Accurate — **CLIENT CONFIRMATION** per client), email.

## Risiko

| Risiko | Mitigasi |
|---|---|
| Salah baca angka dari nota (OCR) | Tandai baris confidence rendah; sampel dicek manusia; total dicocokkan |
| Invoice salah terkirim ke customer | AI tidak mengirim; Level B |
| Kebocoran data keuangan | Least privilege, enkripsi, audit log |

## KPI

Jam kerja admin yang dihemat, error rate data entry (dari sampel), waktu dari order ke quotation.

## Use Case Hospitality per Vertical

| Vertical | Dokumen/pekerjaan admin yang paling makan waktu | Yang AI siapkan (draft) | Tidak dikerjakan AI |
|---|---|---|---|
| Villa / akomodasi | Konfirmasi booking & invoice DP, rekap okupansi, SOP housekeeping & check-in | Draft invoice dari booking yang disetujui, SOP (`sop`), rekap bulanan | Penagihan otomatis, setoran pajak, PHR/PB1 resmi |
| Restoran / cafe | Quotation acara privat, rekap penjualan harian dari POS, stok bahan | Quotation dari menu & harga DATA FINAL, rekap, peringatan stok | Laporan pajak resmi, pembayaran supplier |
| Wedding & event | Quotation paket + add-on, rundown, kontrak vendor | Quotation, rundown dari template, checklist vendor | Menandatangani atau mengubah kontrak |
| Travel & tour | Manifest peserta, invoice trip, itinerary | Itinerary & invoice dari paket DATA FINAL; manifest **tanpa** nomor identitas di sistem AI | Data paspor/KTP (Restricted), asuransi |

## Produk Pertama yang Dijual

**"Quotation & Invoice Draft"**: dari katalog & harga yang dikonfirmasi klien (sudah ada di fact sheet Pilar 1), AI menyusun draft quotation/invoice; staf klien memeriksa, memberi nomor dari sistem mereka, dan mengirim. Tanpa akses ke rekening, POS, atau akuntansi di tahap awal.

## Gerbang Khusus Pilar Ini

Selain gerbang umum: klasifikasi data keuangan **Confidential** sudah diterapkan di platform (enkripsi, audit log ekspor); konsultan pajak mengonfirmasi batas "draft vs dokumen pajak resmi".

## Keputusan Owner Saat Aktivasi

| Keputusan | Siapa |
|---|---|
| Produk pertama & batas data keuangan yang boleh diproses | Owner |
| Repo `clau-admin` | Owner |
| Harga & paket | Owner (price sheet privat, bukan repo) |
| Nama agent baru, avatar, persona | Owner |
| Level A per intent per klien | Owner + klien, tertulis (AI-CONSTITUTION §4a) |

## Checklist Aktivasi

1. Scope Approved (TASK-034); database + auth + audit log tersedia (Fase 0).
2. Repo `clau-admin` (usulan): rules angka & dokumen, template quotation/invoice/laporan.
3. Intent → router + registry; agent + persona + eval.
4. Pilot SIMULASI dengan data fiktif (≥ 500 transaksi contoh), lalu 1 client.
