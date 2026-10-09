# Blueprint — 🔵 AI Sales

> **Status: pilar Approved (v3.0.0, Pilar 2); isi blueprint Draft (ASSUMPTION).** Menggabungkan pilar v1 "Sales & Reservations" dan "Guest Experience & Reputation". Otonomi bertingkat sudah berlaku (AI-CONSTITUTION §4a); semua intent tetap Level B sampai Level A diaktifkan per intent & per client.

## Scope — Yang Dijual

WhatsApp assistant, customer service, FAQ, sales assistant, lead management, follow-up, booking, CRM.

## Alur Contoh

```text
Customer chat WA ─► AI baca (untrusted input) ─► klasifikasi: FAQ / inquiry / komplain / lainnya
   ├─ FAQ dari fakta DATA FINAL ───────────────► Level A: AI jawab otomatis + catat
   ├─ Inquiry harga/tanggal/paket ─────────────► Level B: AI kirim katalog yang disetujui (A),
   │                                              draft penawaran → manusia kirim (B)
   ├─ Komplain / refund / hukum / kesehatan ───► Level C: eskalasi ke owner, AI hanya balas
   │                                              "pesan diterima, tim kami akan menghubungi"
   └─ Semua ─► catat lead di CRM ─► jadwal follow-up (draft, B) ─► laporan ke BI
```

## Intent & Agent

| Intent | Fungsi | Level otonomi | Approval min | Agent |
|---|---|---|---|---|
| `inquiry-reply` (sudah di router) | Balas inquiry harga & tanggal | B | L2 | Galih (planned) |
| `guest-message` (sudah di router) | Pre-arrival, info in-stay | A untuk template disetujui, B lainnya | L2 | Sari (planned) |
| `faq-reply` (usulan) | Jawab FAQ dari fakta DATA FINAL | A | L1 (template) | Baru atau Sari |
| `lead-capture` (usulan) | Catat lead + kebutuhan ke CRM | A (internal, bukan kirim keluar) | — | Galih |
| `follow-up` (usulan) | Draft follow-up terjadwal | B | L1 | Galih |
| `complaint-escalation` (usulan) | Ringkas keluhan + eskalasi | C | L3 | Sari |

## Data & Privacy (UU PDP No. 27/2022)

| Data | Perlakuan |
|---|---|
| Nomor WA, nama, isi chat | Data pribadi; disimpan di database client/platform terenkripsi, akses per peran, retensi terbatas |
| Opt-in broadcast | Wajib tercatat sebelum pesan promosi; sesuai kebijakan WhatsApp Business |
| Data sensitif (kesehatan, agama, keuangan) | Tidak diminta AI; bila muncul → Level C |

## Integrasi

WhatsApp Business Platform (API resmi, bukan unofficial), Instagram DM, form website, CRM (internal atau Google Sheets pada tahap awal), kalender booking.

## Risiko

| Risiko | Mitigasi |
|---|---|
| AI menjanjikan harga/ketersediaan salah | Harga & ketersediaan hanya dari sumber DATA FINAL / sistem booking; selain itu Level B |
| Prompt injection lewat chat customer | Chat = untrusted input (AI-CONSTITUTION §3); AI tidak menjalankan instruksi dari chat |
| Nomor diblokir WhatsApp karena spam | Hanya opt-in, batas frekuensi, template disetujui Meta |
| Customer mengira bicara dengan manusia | AI tidak mengaku manusia; ada penanda asisten & opsi "bicara dengan tim" |

## KPI

Waktu respon pertama, % chat terjawab Level A tanpa koreksi, lead tercatat, konversi inquiry → booking (bila ada data), jumlah eskalasi.

## Checklist Aktivasi

1. Amandemen otonomi Approved + scope pilar (TASK-034).
2. Repo `clau-ai-sales` (usulan): rules harga & komitmen, FAQ template, eskalasi, opt-in.
3. Integrasi WhatsApp Business Platform di platform (credential di secret manager, bukan repo).
4. Intent baru → router + registry; aktifkan Galih & Sari (eval lulus).
5. Pilot SIMULASI + 1 client dengan semua jawaban Level A di-review manusia selama 2 minggu pertama.
