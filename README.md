# Portofolio Alan Nawa

Halaman CV digital satu file untuk Alan Nawa: web development, landing page, dan otomasi AI. Tema visual TRON dengan grid cyan di atas latar gelap.

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
├── tests/test_portfolio.py
└── README.md
```

## Mengubah data

- Nama dan peran: header serta bagian pembuka di `index.html`.
- Instagram: `https://instagram.com/zhahenzar` (`@zhahenzar`).
- GitHub: `https://github.com/zhahenza44`.
- Email: `zhahenza666@proton.me`.
- Kartu project: bagian `#project-grid` di `index.html`. Setiap kartu punya `data-track="job1"` atau `data-track="job2"` untuk filter.

## Project yang ditampilkan

| Kartu | Folder demo |
|---|---|
| AI Lead Capture | `job1-otomasi-ai-workflow/workspace/demo-ai-lead-capture` |
| Servis AC | `job2-web-landing-maintenance/workspace/demo-landingpage-servis-ac` |
| Ruang Rapi | `job2-web-landing-maintenance/workspace/demo-company-profile-ruang-rapi` |
| Kedai Kopi Oak | `job2-web-landing-maintenance/workspace/demo-landingpage-kedai-kopi` |
| Rental Mobil | `job2-web-landing-maintenance/workspace/demo-rental-mobil-multipage` |
| Omegamoto | Demo lokal, tidak dipublikasikan |
| NIGHT//SHIFT | `job2-web-landing-maintenance/workspace/demo-portfolio-cyberpunk` |

Semua tautan mengarah ke repo `zhahenza44/otomasi-web`.

## Tes

```bash
cd /home/asnodt/Projects/Portofolio
python3 -m unittest discover -s tests -v
```

Tes membaca `index.html`, `css/styles.css`, dan `js/main.js` sebagai teks, lalu memeriksa struktur, kontak, tautan project, dan aturan tampilan responsif.
