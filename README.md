# NIGHT//SHIFT landing page

The main portfolio page is the `NIGHT//SHIFT` demo copied to the repository root and translated into English. It keeps the studio identity, fictional case studies, boot sequence, ghost cursor, scanline, ticker, magnetic buttons, scroll reveals, process fill, project dialogs, copy-email toast, clock, and mobile menu. The old Alan Nawa CV shell is gone from the landing page.

The studio, names, metrics, status, email address, and phone number are fictional. The contact section discloses this. Type comes from Google Fonts, with local fallbacks when the network is unavailable. The `demos/` folder is still present, but the landing page no longer links to it.

## Open the page

Open `index.html` in a browser. There is no build step or server requirement.

To use a local server:

```bash
cd /home/asnodt/Projects/Portofolio
python3 -m http.server 8080
```

Then open `http://localhost:8080`.

## What is in the root

```text
Portofolio/
├── index.html            # NightShift markup, English visitor copy, lang="en"
├── css/styles.css        # NightShift visual system, copied byte-for-byte
├── js/main.js            # NightShift behavior, English visitor strings
├── assets/favicon.svg    # NightShift favicon, copied byte-for-byte
├── demos/                # all six demos, unchanged and unlinked
├── docs/superpowers/     # approved design and implementation plan
├── tests/test_portfolio.py
├── tests/browser_smoke.py
├── .githooks/pre-commit  # runs both test commands before each commit
├── PRODUCT.md            # product truth and owner-directed decisions
└── README.md
```

The four root files are the demo files from `demos/nightshift/`. The only differences are translated visitor-facing text and the document language. No file inside `demos/` was changed.

## Tests

Run the static contract checks:

```bash
cd /home/asnodt/Projects/Portofolio
python3 -m unittest discover -s tests -v
```

They read `index.html`, `css/styles.css`, `js/main.js`, and the favicon. They pin the English NightShift copy, the disclosure, the preserved effects, and the absence of the old CV shell.

Run the rendered checks with Firefox installed:

```bash
python3 tests/browser_smoke.py
```

The script serves the page over HTTP and checks a 390px pass, a 320px pass, and a reduced-motion pass. It uses `/index.html?noboot` for interaction, sends a real Escape key to close the case-file dialog, and reports console errors in every pass. No third-party Python package is needed.

Both commands run through `.githooks/pre-commit`. Enable the hook once after cloning:

```bash
git config core.hooksPath .githooks
```
