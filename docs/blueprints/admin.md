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

## Checklist Aktivasi

1. Scope Approved (TASK-034); database + auth + audit log tersedia (Fase 0).
2. Repo `clau-admin` (usulan): rules angka & dokumen, template quotation/invoice/laporan.
3. Intent → router + registry; agent + persona + eval.
4. Pilot SIMULASI dengan data fiktif (≥ 500 transaksi contoh), lalu 1 client.
