# Blueprint — 🔴 AI Automation

> **Status: pilar Approved (v3.0.0, Pilar 5); isi blueprint Draft (ASSUMPTION).** Secara teknis adalah **lapisan penghubung** antar pilar (bukan aturan domain baru); secara bisnis dijual sebagai **paket langganan bulanan** (recurring).

## Scope — Yang Dijual

Alur kerja belakang layar yang berjalan sendiri; owner bekerja seperti biasa.

| Contoh alur | Pilar yang disambung |
|---|---|
| Instagram/WhatsApp → AI → CRM → Google Sheets → invoice → email → follow-up | Sales → Admin → Sales |
| Form order → AI baca order → quotation → kirim WhatsApp → simpan database | Sales → Admin |
| Penjualan harian → rekap → insight mingguan ke owner | Admin → BI |
| Review baru → draft balasan → notifikasi approver | Marketing |

## Prinsip

1. **Setiap langkah punya level otonomi** ([autonomy-levels](../proposals/autonomy-levels.md)). Alur boleh otomatis penuh hanya bila **semua** langkahnya Level A; satu langkah Level B = alur berhenti menunggu manusia di langkah itu.
2. **Aturan tetap di pilar.** Automation hanya memanggil skill pilar lewat router; tidak punya aturan konten/harga sendiri.
3. **Idempotent & bisa diulang.** Setiap langkah punya ID; gagal → retry aman, tidak mengirim dua kali.
4. **Audit log.** Siapa/apa memicu, input, output, approval, waktu — untuk setiap run.
5. **Tombol berhenti.** Owner bisa mematikan satu alur atau semua alur client seketika.
6. **Credential di secret manager.** Tidak pernah di repo, prompt, atau log.

## Komponen

| Komponen | Isi | Catatan |
|---|---|---|
| Trigger | Pesan masuk, form, jadwal, webhook | |
| Konektor | WhatsApp Business Platform, Instagram, Google Sheets, email, CRM, akuntansi | Read/write minimum per alur |
| Runner | Engine alur (bangun sendiri di clau-ai-agents, atau n8n self-hosted di VPS) | Keputusan teknis = TASK-039 |
| Approval queue | Langkah Level B/C masuk antrean "Menunggu manusia" di Studio | Sudah ada di desain Studio |

## Intent & Agent

Automation tidak punya intent konten sendiri. Intent usulan: `workflow-run` (menjalankan alur yang sudah disetujui) dan `workflow-design` (AI membantu menyusun alur baru; Level B, L3 karena mengubah sistem client).

## Paket Jual (usulan)

| Paket | Isi | Harga |
|---|---|---|
| Starter | 1 alur (mis. WA → lead → Sheets) | **CLIENT CONFIRMATION** (keputusan owner) |
| Growth | 3 alur + laporan mingguan | **CLIENT CONFIRMATION** |
| Custom | Alur sesuai kebutuhan | **CLIENT CONFIRMATION** |

## Risiko

| Risiko | Mitigasi |
|---|---|
| Alur salah mengirim massal | Batas jumlah per run, mode uji (dry run), tombol berhenti |
| Integrasi pihak ketiga berubah/putus | Monitoring + notifikasi error; alur berhenti aman |
| Mengubah sistem client tanpa izin | `workflow-design` = L3; setiap alur baru di-approve owner client |

## Checklist Aktivasi

1. Amandemen otonomi Approved; Sales/Admin minimal 1 intent aktif.
2. Keputusan engine (TASK-039); konektor pertama: WhatsApp + Google Sheets.
3. Audit log, tombol berhenti, dry run tersedia di platform.
4. Pilot 1 alur di SIMULASI, lalu 1 client dengan monitoring harian 2 minggu.
