# Decision Tree

Dipakai saat intent tidak langsung jelas dari [router.md](./router.md).

```mermaid
flowchart TD
    A["Request masuk"] --> B{"Input berisi data Restricted?<br/>(credential, KTP/paspor, kartu)"}
    B -- Ya --> X1["STOP: minta disamarkan / hapus; lapor owner"]
    B -- Tidak --> C{"Client & objective jelas?"}
    C -- Tidak --> X2["Tanya requester"]
    C -- Ya --> D{"Output akan dilihat pihak luar?<br/>(publik, tamu, OTA)"}
    D -- Tidak --> E["Internal: dokumen/analisis → pilar sesuai topik"]
    D -- Ya --> F{"Ke audiens luas atau satu orang?"}
    F -- "Audiens luas (post, listing, ads)" --> P1["Pilar 1 AI Marketing"]
    F -- "Satu tamu/calon tamu" --> G{"Tentang harga, ketersediaan, booking?"}
    G -- Ya --> P2["Pilar 2 AI Sales (Planned → eskalasi)"]
    G -- Tidak --> H{"Review publik?"}
    H -- Ya --> P1R["Pilar 1: reply-guest-review<br/>(sementara)"]
    H -- Tidak --> P3["Pilar 2 AI Sales: pesan tamu & customer service (Planned → eskalasi)"]
    E --> I{"SOP, invoice, quotation, data entry?"}
    I -- Ya --> P4["Pilar 3 AI Admin (Planned → eskalasi)"]
    I -- Tidak --> J{"Angka/performa/report?"}
    J -- Ya --> P5["Pilar 4 AI Business Intelligence (sementara: template monthly-report Pilar 1)"]
    J -- Tidak --> X3["Tanya requester / eskalasi owner"]
```

## Pertanyaan Tambahan Setelah Pilar Ditentukan

1. Ada harga, promo, atau komitmen komersial? → approval minimal L2; komitmen baru → eskalasi.
2. Ada orang yang dapat dikenali di aset? → cek consent sebelum produce.
3. Menyentuh agama/adat/tempat suci, bencana, atau isu sensitif? → L3 + eskalasi.
4. Keluhan serius tamu (keracunan, cedera, pelecehan, kehilangan, ancaman hukum)? → jangan draft balasan final; eskalasi L3 (Level C).
5. Boleh dikirim otomatis (Level A)? → hanya bila kolom Otonomi intent = A **dan** jawabannya persis template yang disetujui client dengan fakta DATA FINAL; selain itu Level B (draft).
