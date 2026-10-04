---
document_title: "CLAU AI Work Pipeline"
document_owner: "Dea Karisna / AI Marketing"
version: "1.0.0"
status: "Draft"
classification: "Internal"
---

# CLAU AI Work Pipeline

Pipeline umum untuk semua pilar. Setiap pilar mendetailkan langkah 4–6 di workflow pilarnya; pipeline ini menetapkan **gate minimum** yang tidak boleh dilewati di pilar mana pun.

```text
1 Intake → 2 Classify → 3 Route → 4 Produce → 5 Verify → 6 Approve → 7 Release → 8 Monitor
```

| # | Langkah | Isi | Gate minimum |
|---|---|---|---|
| 1 | **Intake** | Request masuk (chat, task board, platform). Catat requester, client (kode), objective, deadline | Requester & client jelas |
| 2 | **Classify** | Label evidence untuk fakta yang tersedia; 4 axis data ([AI-CONSTITUTION §5](./AI-CONSTITUTION.md#5-evidence--action-classification)) | Tidak ada data `Restricted` di input |
| 3 | **Route** | Tentukan pilar, skill, dan prioritas lewat [orchestrator/](./orchestrator/README.md) | Pilar aktif; pilar *Planned* → eskalasi |
| 4 | **Produce** | Kerjakan dengan skill/prompt pilar | Hanya fakta **DATA FINAL** sebagai fakta |
| 5 | **Verify** | QA gate pilar + sanity check strategi | Output berisiko: review independen (bukan self-review) |
| 6 | **Approve** | Approval tertulis approver client sesuai level | Tanpa approval → stop |
| 7 | **Release** | Publish/kirim/terapkan oleh **manusia** atau platform dengan tombol manusia | AI tidak release sendiri |
| 8 | **Monitor** | Pantau respons, koreksi, report | Insiden dicatat |

## Workflow per Pilar

| Pilar | Workflow detail | Status |
|---|---|---|
| 1 Marketing & Content | [clau-ai-marketing/CONTENT-WORKFLOW.md](https://github.com/d34faiza-commits/clau-ai-marketing/blob/main/CONTENT-WORKFLOW.md) (9 langkah, termasuk Mode SIMULASI) | Aktif |
| 2–5 | Dibuat saat pilar diaktifkan (lihat [5-pillar-architecture](./docs/5-pillar-architecture.md)) | Planned |

## Mode SIMULASI

Pilot dan contoh memakai data fiktif dan **tidak pernah** sampai langkah 7. Aturan rinci di workflow pilar.

## Revision History

| Version | Date | Status | Summary |
|---|---|---|---|
| 1.0.0 | 2026-10-04 | Draft | Pipeline umum lintas pilar; workflow konten 9 langkah dipindah ke clau-ai-marketing/CONTENT-WORKFLOW.md |
