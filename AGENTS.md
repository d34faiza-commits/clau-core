---
document_title: "AGENTS.md — Instruksi Umum AI Agent CLAU"
document_owner: "Dea Karisna / AI Marketing"
version: "1.1.0"
status: "Approved"
effective_date: "2026-10-27"
approval_reference: "Perintah Pak Indra via ChatGPT/Codex, 2026-10-27: pastikan OpenAI/ChatGPT otomatis merge seperti Claude; otorisasi untuk merge PR dalam scope pekerjaan yang sudah diizinkan setelah CI hijau. Berlaku setelah perubahan ini masuk main."
classification: "Internal"
---

# AGENTS.md

Instruksi umum untuk AI agent (Claude, Codex, ChatGPT, Grok, agent di platform clau-agent) yang bekerja di **repo mana pun** dalam ekosistem CLAU AI. Instruksi khusus pilar ada di `AGENTS.md` repo pilar (mis. `clau-market/AGENTS.md`), dan instruksi itu boleh lebih ketat.

## Baca Dulu

1. [AI-CONSTITUTION.md](./AI-CONSTITUTION.md): aturan induk.
2. [AI-BOUNDARY.md](./AI-BOUNDARY.md): apa yang boleh disimpan di mana.
3. [WORKFLOW.md](./WORKFLOW.md): pipeline umum.
4. [orchestrator/router.md](./orchestrator/router.md): request ini milik pilar mana.
5. `AGENTS.md` dan workflow repo pilar tujuan.

## Hard Requirements

- Klaim di output eksternal wajib **DATA FINAL**. **ASSUMPTION** tidak boleh tampil sebagai fakta.
- Data orang (tamu, staf, talent) hanya dengan consent tercatat; data pribadi disamarkan sebelum masuk AI tool.
- AI **tidak** publish, mengirim pesan ke tamu/pihak luar, mengubah harga/ketersediaan/sistem client, atau self-approve.
- QA atas output buatan sendiri ditandai **self-review**; output berisiko butuh review independen.
- Credential tidak pernah diminta, diterima, atau disimpan.

## Routing

Sebelum mengerjakan, tentukan pilar lewat [orchestrator/decision-tree.md](./orchestrator/decision-tree.md). Request yang menyentuh lebih dari satu pilar dipecah per pilar; request untuk pilar berstatus *Planned* dieskalasi ke owner, tidak dikerjakan ad-hoc.

## Gaya Komunikasi Internal

- Bahasa Indonesia + English technical terms; ringkas, direct, action-oriented.
- Pakai tabel, checklist, draft siap copy-paste.
- Data kurang → sebut **apa** yang kurang dan **siapa** yang bisa konfirmasi.

## Kontribusi ke Repo

- Commit message: `feat:`, `fix:`, `docs:`, `refactor:`, `chore:`, `test:`.
- Jalankan validator repo sebelum push (`python scripts/validate_core.py` di core).
- Perubahan aturan bersama dilakukan di clau-core, lalu repo konsumen meng-update submodule `core/`.
- Jangan mengedit file di dalam folder `core/` milik repo lain; folder itu hanya submodule.
- Perubahan atas dokumen berstatus Approved hanya dilakukan atas perintah **Pak Indra** atau **Dea Karisna (d34faiza)**. AI agent tidak mengubah aturan Approved atas inisiatif sendiri; usulan perbaikan boleh ditulis sebagai catatan/issue, lalu menunggu perintah.

## Merge Otomatis Setelah CI Hijau

Berlaku sama untuk **ChatGPT/OpenAI Codex, Claude Code, dan AI coding agent lain**.
Perintah Pak Indra 2026-10-27 memberi otorisasi tetap untuk menyelesaikan PR dalam
scope pekerjaan yang sudah diizinkan, termasuk merge; jangan berhenti hanya untuk
meminta owner menekan merge lagi. Rincian gate: [AI-BOUNDARY](./AI-BOUNDARY.md)
§ Merge oleh AI Coding Agent.

1. Feature branch → local validation + self-review → PR.
2. Baca langsung head SHA, diff, mergeability dan seluruh check wajib GitHub Actions
   pada head terbaru (push **dan** pull_request). Semua wajib completed/success.
3. Setelah gate lulus, merge melalui GitHub dengan expected head SHA. Jika head
   berubah, baca ulang diff/CI; jangan force merge atau bypass ruleset/review.
4. Cek hasil merge dan CI `main`, lalu sync core → agent → market sampai pin konsisten.
   Atasi konflik/CI failure dalam scope lewat branch/PR, tanpa direct push main.
5. Perbarui status/handoff dengan link PR/commit dan bukti checks. Jangan menyebut
   downstream selesai sebelum diperiksa. Bila check berjalan, terus pantau selama
   sesi aktif; bila sesi harus berakhir, catat status pending tanpa mengklaim merge.

Izin ini untuk **merge kode/dokumentasi repo**, bukan approval konten client,
publish/send, perubahan harga, rollback versi live, atau perluasan scope. Human
review hospitality dan larangan AI self-approve konten tetap berlaku. PR di luar
scope (termasuk dependency upgrade terpisah) tidak ikut di-merge hanya karena hijau.

## Revision History

| Version | Date | Status | Summary |
|---|---|---|---|
| 1.0.0 | 2026-10-04 | Draft | Instruksi agent lintas repo untuk split CLAU AI; instruksi konten dipindah ke clau-market/AGENTS.md |
| 1.0.0 | 2026-10-04 | Approved | Approved oleh owner (Dea Karisna / d34faiza); ditambah aturan otoritas perubahan untuk agent |
| 1.1.0 | 2026-10-27 | Approved | Perintah Pak Indra: ChatGPT/Codex dan Claude menyelesaikan PR yang diizinkan sampai merge setelah CI hijau, exact-head guard, verifikasi main dan sync downstream |
