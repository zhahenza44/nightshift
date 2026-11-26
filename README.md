# NIGHT//SHIFT landing page

The main portfolio page keeps the `NIGHT//SHIFT` identity and adds Alan Nawa's real CV after the manifesto. Work and Services share one section, and the studio location reads Surabaya, ID. The page has two clearly separated parts:

- The NightShift showcase: fictional case studies, metrics, status, email address, phone number, boot sequence, ghost cursor, scanline, ticker, magnetic buttons, scroll reveals, process fill, project dialogs, copy-email toast, clock, and mobile menu. The contact section discloses that this part is fictional.
- The CV section: Alan Nawa, Web & AI Automation, two services, six demo links, and three real contact channels. A note in the section says it is the owner's real CV and that the case studies below it are fictional.

The hero shows `Projects 1` and `Response <24h`; the Experience stat is gone. The GitHub link in the contact section reads `GITHUB` and still points to `https://github.com/zhahenza44/otomasi-web`.

All visitor copy is English. Type comes from Google Fonts, with local fallbacks when the network is unavailable.

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
├── index.html            # NightShift markup plus the real CV section, lang="en"
├── css/styles.css        # NightShift visual system plus additive CV rules
├── js/main.js            # NightShift behavior, English visitor strings
├── assets/favicon.svg    # NightShift favicon
├── demos/                # all six demos, unchanged and linked from the CV section
├── docs/superpowers/     # approved design docs and implementation plans
├── tests/test_portfolio.py
├── tests/browser_smoke.py
├── .githooks/pre-commit  # runs both test commands before each commit
├── PRODUCT.md            # product truth and owner-directed decisions
└── README.md
```

`index.html`, `js/main.js`, and the favicon come from `demos/nightshift/`. Their differences are translated visitor strings, the document language, the CV section, and the combined Work & Services section. The stylesheet keeps every demo rule and adds a CV block plus a small `services-block` spacing rule that use the same tokens. No file inside `demos/` was changed.

## The CV section

The section sits between the manifesto and the combined Work & Services section. It links to these demos:

- AI Lead Capture → `demos/ai-lead-capture/dashboard/index.html`
- Servis AC → `demos/servis-ac/index.html`
- Ruang Rapi → `demos/ruang-rapi/index.html`
- Kedai Kopi Oak → `demos/kedai-kopi/index.html`
- Rental Mobil → `demos/rental-mobil/index.html`
- NIGHT//SHIFT → `demos/nightshift/index.html`

The real contact channels are Instagram `@zhahenzar`, GitHub `zhahenza44`, and `zhahenza666@proton.me`.

## Tests

Run the static contract checks:

```bash
cd /home/asnodt/Projects/Portofolio
python3 -m unittest discover -s tests -v
```

They read `index.html`, `css/styles.css`, `js/main.js`, and the favicon. They pin the English NightShift copy, the fictional disclosure, the CV content and links, the merged section order and nav labels, the Surabaya location, the hero stats, the `GITHUB` label, and the preserved effects.

Run the rendered checks with Firefox installed:

```bash
python3 tests/browser_smoke.py
```

The script serves the page over HTTP and checks a 390px pass, a 320px pass, and a reduced-motion pass. It uses `/index.html?noboot` for interaction, sends a real Escape key to close the case-file dialog, and reports console errors in every pass. Blocked Google Fonts downloads from `fonts.gstatic.com` are ignored; every other console error fails the run. No third-party Python package is needed.

Both commands run through `.githooks/pre-commit`. Enable the hook once after cloning:

```bash
git config core.hooksPath .githooks
```
