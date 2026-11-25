# Design: CV asli di dalam halaman NIGHT//SHIFT

**Date:** 2026-11-25
**Status:** awaiting approval

## Intent

Halaman utama tetap NIGHT//SHIFT, termasuk identitas, case study fiksi, metrik, kontak fiksi, disclaimer, dan seluruh interaksinya. CV asli Alan Nawa ditambahkan sebagai bagian tersendiri. Ini memperbaiki kehilangan data CV ketika halaman diganti dengan salinan demo.

## Keputusan yang sudah disetujui pemilik

- Brand dan hero tetap memakai NIGHT//SHIFT.
- Semua konten fiksi NightShift tetap apa adanya, termasuk tiga case file, metrik, email, WhatsApp, dan kalimat disclaimer.
- CV memakai data dari shell lama yang masih tersimpan di git: Alan Nawa, Web & AI Automation, dua layanan, enam demo, dan tiga kanal kontak.
- Bagian CV diletakkan setelah manifesto, sebelum Selected Work.
- Bagian CV boleh menambah CSS minimal dengan token warna dan ritme yang sama. Selector lama tidak diubah.
- Semua teks pengunjung tetap bahasa Inggris.
- Tidak ada perubahan di dalam `demos/`.

## Ruang lingkup

### Yang ditambahkan

- Bagian baru `section#cv` setelah `#studio` dengan judul dan catatan yang menyatakan bagian ini adalah CV pemilik, sementara case study di bawahnya adalah demo fiksi.
- Identitas: Alan Nawa, Web & AI Automation, dan bio satu paragraf dari shell lama.
- Dua layanan: AI & workflow automation, Websites & landing pages, beserta ringkasan dan poin singkatnya dari shell lama.
- Enam tautan demo asli dengan label dan path yang sama seperti shell lama:
  - AI Lead Capture → `demos/ai-lead-capture/dashboard/index.html`
  - Servis AC → `demos/servis-ac/index.html`
  - Ruang Rapi → `demos/ruang-rapi/index.html`
  - Kedai Kopi Oak → `demos/kedai-kopi/index.html`
  - Rental Mobil → `demos/rental-mobil/index.html`
  - NIGHT//SHIFT → `demos/nightshift/index.html`
- Tiga kanal kontak asli: Instagram `https://instagram.com/zhahenzar`, GitHub `https://github.com/zhahenza44`, dan email `mailto:zhahenza666@proton.me`.
- Entri navigasi CV di header dan menu seluler. Penomoran bagian menjadi 01 Manifesto, 02 CV, 03 Work, 04 Services, 05 Process, 06 Contact.
- CSS tambahan seminimal mungkin memakai variabel yang sudah ada. Aturan untuk bagian NightShift yang lama tidak diubah.

### Yang tidak diubah

- Boot sequence, ghost cursor, scanline, orb, ticker, magnetic buttons, reveal, progress bar, process fill, project dialog, copy-email toast, clock, mobile menu, dan reduced-motion behavior.
- Tiga project card fiksi beserta isi dialognya.
- Email `hello@nightshift.studio`, nomor WhatsApp fiksi, status fiksi, dan disclaimer fiksi.
- `demos/`, favicon, dan struktur direktori.

## Alasan bentuk ini

Brand NIGHT//SHIFT tetap dipertahankan sesuai permintaan, jadi CV tidak menggantikan identitas demo. Bagian CV dipisahkan supaya pembaca tahu mana data asli dan mana yang fiksi. Tautan demo memakai path lama yang sudah terbukti berfungsi, tanpa membuat halaman baru. CSS baru memakai token lama supaya bagian CV terasa sebagai bagian dari sistem yang sama.

## Pengujian

- Tes statis diperbarui untuk memeriksa keberadaan `section#cv`, enam tautan demo dengan path yang benar, tiga kontak asli, entri navigasi CV, penomoran baru, dan tetapnya data fiksi serta disclaimer.
- `browser_smoke.py` diperbarui untuk memeriksa bagian CV pada lebar 390px dan 320px: teks terlihat, tautan dapat ditemukan, tidak ada overflow horizontal, dan focus serta menu tetap bekerja. Pemeriksaan NightShift yang lama tetap dijalankan.
- `README.md` dan `PRODUCT.md` diperbarui untuk menjelaskan bahwa halaman memuat keduanya: showcase NightShift fiksi dan CV asli.
- Verifikasi penuh: unit test, smoke test Firefox, `xmllint`, HTTP lokal, `git hook run pre-commit`, dan `impeccable detect --json --changed`.

## Risiko dan batasan

- Entri nav tambahan berisiko membuat header penuh di layar sempit. Rendered check pada 320px dan 390px menjadi penentu; jika overflow, nav disesuaikan memakai aturan yang sudah ada, bukan mengurangi isi CV.
- `css/styles.css` tidak lagi identik byte-for-byte dengan demo setelah CSS CV ditambahkan. Ini adalah konsekuensi yang disetujui dari penambahan bagian baru.
- Data fiksi dan data asli hidup di halaman yang sama. Catatan di bagian CV dan disclaimer yang sudah ada harus tetap jelas.
- Tidak ada push atau merge tanpa permintaan baru.
