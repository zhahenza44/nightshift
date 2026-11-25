# Portofolio Alan Nawa

Halaman CV digital statis untuk Alan Nawa: web development, landing page, dan otomasi AI. Tema visual TRON dengan grid cyan di atas latar gelap. Enam demo disimpan lokal di folder `demos/` dan dibuka langsung dari kartu project.

## Membuka halaman

Buka `index.html` langsung di browser. Tidak ada dependency, build step, atau server yang perlu dijalankan.

Kalau ingin memakai server lokal:

```bash
cd /home/asnodt/Projects/Portofolio
python3 -m http.server 8080
```

Lalu buka `http://localhost:8080`.

## Struktur

```text
Portofolio/
├── index.html          # seluruh konten halaman
├── css/styles.css      # tema TRON, layout, responsif
├── js/main.js          # filter project dan menu mobile
├── assets/favicon.svg
├── demos/              # enam landing page demo, salinan lokal
├── tests/test_portfolio.py
└── README.md
```

## Mengubah data

- Nama dan peran: header serta bagian pembuka di `index.html`.
- Instagram: `https://instagram.com/zhahenzar` (`@zhahenzar`).
- GitHub: `https://github.com/zhahenza44`.
- Email: `zhahenza666@proton.me`.
- Kartu project: bagian `#project-grid` di `index.html`. Setiap kartu punya `data-track="job1"` atau `data-track="job2"` untuk filter.
- Demo: folder di dalam `demos/`. Kalau demo di repo asli berubah, salin ulang folder yang bersangkutan ke sini.

## Project yang ditampilkan

| Kartu | Halaman demo |
|---|---|
| AI Lead Capture | `demos/ai-lead-capture/dashboard/index.html` |
| Servis AC | `demos/servis-ac/index.html` |
| Ruang Rapi | `demos/ruang-rapi/index.html` |
| Kedai Kopi Oak | `demos/kedai-kopi/index.html` |
| Rental Mobil | `demos/rental-mobil/index.html` |
| NIGHT//SHIFT | `demos/nightshift/index.html` |

Kartu membuka halaman demo di tab baru tanpa melewati GitHub. Tautan GitHub di header dan footer hanya untuk source code. Isi tiap demo dibiarkan apa adanya, termasuk aset dan tautan yang dipakai demo itu sendiri.

## Tes

```bash
cd /home/asnodt/Projects/Portofolio
python3 -m unittest discover -s tests -v
```

Tes membaca `index.html`, `css/styles.css`, dan `js/main.js` sebagai teks, lalu memeriksa struktur, kontak, keberadaan enam file demo, dan aturan tampilan responsif.
