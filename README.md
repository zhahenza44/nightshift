# Alan Nawa portfolio

A static one-page CV for Alan Nawa: web development, landing pages, and AI workflow automation. The shell copy is in English. The visual system is cyberpunk x TRON: cyan actions, a magenta technical accent, clipped corners, a thin horizon grid, and one short entrance motion. The motion is finite and stops under `prefers-reduced-motion`. Six demos live in `demos/` and open directly from the project cards.

## Open the page

Open `index.html` in a browser. There is no dependency, build step, or server requirement.

To use a local server:

```bash
cd /home/asnodt/Projects/Portofolio
python3 -m http.server 8080
```

Then open `http://localhost:8080`.

## Structure

```text
Portofolio/
├── index.html          # all page content
├── css/styles.css      # cyberpunk TRON theme, layout, responsive rules
├── js/main.js          # project filter and mobile menu
├── assets/favicon.svg
├── PRODUCT.md          # product truth and constraints
├── demos/              # six local demo pages, unchanged contents
├── tests/test_portfolio.py
├── docs/superpowers/   # approved design and implementation plan
└── README.md
```

## Change the data

- Name and role: the header and opening section in `index.html`.
- Instagram: `https://instagram.com/zhahenzar` (`@zhahenzar`).
- GitHub: `https://github.com/zhahenza44`.
- Email: `zhahenza666@proton.me`.
- Project cards: the `#project-grid` section in `index.html`. Each card has `data-track="job1"` or `data-track="job2"` for filtering.
- Demos: folders inside `demos/`. If a demo in the source repo changes, copy that folder here again. Demo contents stay as they are, including their own fonts, images, and buttons.

## Projects shown

| Card | Demo page |
|---|---|
| AI Lead Capture | `demos/ai-lead-capture/dashboard/index.html` |
| Servis AC | `demos/servis-ac/index.html` |
| Ruang Rapi | `demos/ruang-rapi/index.html` |
| Kedai Kopi Oak | `demos/kedai-kopi/index.html` |
| Rental Mobil | `demos/rental-mobil/index.html` |
| NIGHT//SHIFT | `demos/nightshift/index.html` |

Cards open the demo pages in a new tab without going through GitHub. The GitHub links in the header and footer point to source code. Each demo keeps its own assets and links.

## Tests

```bash
cd /home/asnodt/Projects/Portofolio
python3 -m unittest discover -s tests -v
```

The tests read `index.html`, `css/styles.css`, and `js/main.js` as text. They check structure, contacts, the six demo files, English copy, the cyberpunk TRON tokens, finite motion, and responsive rules.

For a rendered check at 390px, run the Firefox smoke script. It requires Firefox but no third-party package:

```bash
python3 tests/browser_smoke.py
```

It serves the page locally, clicks the filters and menu, checks focus outlines and overflow, and repeats with reduced motion enabled.
