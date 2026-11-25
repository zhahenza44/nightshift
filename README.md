# Alan Nawa portfolio

A static one-page CV for Alan Nawa: web development, landing pages, and AI workflow automation. The shell copy is in English. The visual system is cyberpunk x TRON: cyan actions, a magenta technical accent, clipped corners, a thin horizon grid, a rotating text orb, and a real-label ticker. Two loops run unless reduced motion is enabled or the visitor presses the Pause motion button, whose label stays fixed while `aria-pressed` reports the state. Six demos live in `demos/` and open directly from the project cards.

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
├── js/main.js          # filters, menu, motion pause, scroll progress, reveal
├── assets/favicon.svg
├── PRODUCT.md          # product truth and constraints
├── demos/              # six local demo pages, unchanged contents
├── tests/test_portfolio.py
├── tests/browser_smoke.py # rendered Firefox checks at 390px and 320px
├── .githooks/pre-commit   # runs both checks before each commit
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

The tests read `index.html`, `css/styles.css`, and `js/main.js` as text. They check structure, contacts, the six demo files, English copy, the cyberpunk TRON tokens, the governed motion budget, and responsive rules.

For rendered checks at 390px and 320px, run the Firefox smoke script. It requires Firefox but no third-party package:

```bash
python3 tests/browser_smoke.py
```

It serves the page locally, clicks the filters, menu, and Pause motion button, checks the action gap, magnetic cap, scroll progress, project reveal, focus outlines, and overflow at both widths, then repeats with reduced motion enabled.

Both checks run before each commit through `.githooks/pre-commit`. Enable the hook once after cloning:

```bash
git config core.hooksPath .githooks
```
