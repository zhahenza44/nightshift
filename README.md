# NIGHT//SHIFT landing page

The main portfolio page keeps the `NIGHT//SHIFT` identity and adds Alan Nawa's real CV after the manifesto. Work and Services share one section, with seven real cases before three fictional case studies. The studio location reads Surabaya, ID in the menu, CV, and terminal, but not in the header or hero foot. The page has three clearly labeled parts:

- The NightShift showcase: fictional case studies, metrics, status, boot sequence, ghost cursor, scanline, ticker, magnetic buttons, scroll reveals, process fill, project dialogs, clock, and mobile menu. The case-file dialog labels the showcase as fictional; contact actions use the owner's real channels.
- The CV section: Alan Nawa, Web & AI Automation, three services, and three real contact channels. A note in the section says it is the owner's real CV and that the case studies below it are fictional.
- Work & Services: seven real cases under `REAL CASES / LIVE DEMOS`, six demo links plus one Web Scraping code link, then three fictional case studies under `FICTIONAL CASE STUDIES`, then the CAPABILITIES modules.

The hero tag reads `EST. 2026`. The hero shows `Projects 1` and `Response <24h`; the Experience stat is gone. The contact actions read `Email`, `Send message`, and `GITHUB`: the Email button uses `zhahenza666@proton.me`, Send message opens `https://ig.me/m/zhahenzar`, and GITHUB still points to `https://github.com/zhahenza44/otomasi-web`. GITHUB is a boxed action beside Send message, and the EMAIL text link is gone. The contact section no longer carries the note about fictional names, metrics, email, and phone number; the case-file dialog and CV note do that labeling. The fictional email and WhatsApp link are gone, and the footer no longer shows `DEMO CONCEPT / FICTIONAL STUDIO`. The CV section has no vertical section padding. The contact panel also has no vertical section padding: it follows the last Process step directly and meets the footer directly. Process steps use Roman numerals I through V, and the neon process rail continues into the contact panel; when the rail finishes, all four sides of the contact frame turn magenta. Fictional case cards, CV contact links, and process steps enter through the existing reveal system, with short delays inside each group. Real-case rows lift their content and arrow on hover. All three contact actions are magnetic. Reduced motion drops those transforms and keeps every element visible.

All visitor copy is English. Type comes from Google Fonts, with local fallbacks when the network is unavailable.

## Open the page

Open `index.html` in a browser. There is no build step or server requirement.

To use a local server:

```bash
cd /home/asnodt/Projects/Portofolio
python3 -m http.server 8080
```

Then open `http://localhost:8080`.

## Live deployment

The site is published from `master` at `https://github.com/zhahenza44/nightshift` with GitHub Pages. The repository root includes a `CNAME` file for `nightshift.is-not-a.dev`. The Open Domains request was approved. The `nightshift.is-not-a.dev` CNAME resolves to `zhahenza44.github.io`, and the HTTP site serves this page. GitHub is still issuing the HTTPS certificate for the custom domain.

## What is in the root

```text
Portofolio/
├── index.html            # NightShift markup, real CV, labeled case groups, lang="en"
├── CNAME                 # GitHub Pages custom domain
├── css/styles.css        # NightShift visual system plus additive CV rules
├── js/main.js            # NightShift behavior, English visitor strings
├── assets/favicon.svg    # NightShift favicon
├── demos/                # all six demos, unchanged and linked from Work & Services
├── docs/superpowers/     # approved design docs and implementation plans
├── tests/test_portfolio.py
├── tests/browser_smoke.py
├── .githooks/pre-commit  # runs both test commands before each commit
├── PRODUCT.md            # product truth and owner-directed decisions
└── README.md
```

`index.html`, `js/main.js`, and the favicon come from `demos/nightshift/`. Their differences are translated visitor strings, the document language, the CV section, the combined Work & Services section with its real and fictional case groups, the hero year, the trimmed contact copy, the real contact address, the removed WhatsApp link and footer label, reveal classes with delays on the case cards, CV contact links, and process steps, and magnetic classes on all three contact buttons. The stylesheet keeps the demo rules except for the narrow hero-foot selector and scroll-cue alignment change, renames the demo-list rules to `.real-case-list`, and adds a CV block, padding resets for `#cv.section`, `#process.section`, and `#contact.section`, a compact bottom padding on `#work.section`, a zero top margin for the footer, `services-block` and `.case-group-head` spacing rules, card reveal easing that keeps the hover transitions, real-case hover lifts, and a reduced-motion override for the new transforms, all using the same tokens. No file inside `demos/` was changed.

## The CV section

The section sits between the manifesto and the combined Work & Services section. It holds Alan Nawa's identity, three services, and three real contact channels. The `Web Scraping` card lists e-commerce price and catalog scraping, job and property listings, scheduled monitoring, and CSV/Excel/JSON delivery. A note labels it as the real CV and says the case studies below are fictional.

The real contact channels are Instagram `@zhahenzar`, GitHub `zhahenza44`, and `zhahenza666@proton.me`.

## Work & Services

The six demo links and one Web Scraping code link sit under `REAL CASES / LIVE DEMOS`, ahead of the three fictional case studies under `FICTIONAL CASE STUDIES`:

- AI Lead Capture → `demos/ai-lead-capture/dashboard/index.html`
- Servis AC → `demos/servis-ac/index.html`
- Ruang Rapi → `demos/ruang-rapi/index.html`
- Kedai Kopi Oak → `demos/kedai-kopi/index.html`
- Rental Mobil → `demos/rental-mobil/index.html`
- NIGHT//SHIFT → `demos/nightshift/index.html`
- Web Scraping Portfolio → `https://github.com/zhahenza44/web-scraping-portfolio`

## Tests

Run the static contract checks:

```bash
cd /home/asnodt/Projects/Portofolio
python3 -m unittest discover -s tests -v
```

They read `index.html`, `css/styles.css`, `js/main.js`, and the favicon. They pin the English NightShift copy, the footer and dialog disclosure, the CV content and links, the merged section order and nav labels, the Surabaya location, the hero stats and year, the `GITHUB` label, the removed contact note, the contact panel spacing at 390px and 1366px, the pinned GitHub Pages domain, and the preserved effects.

Run the rendered checks with Firefox installed:

```bash
python3 tests/browser_smoke.py
```

The script serves the page over HTTP and checks a 390px pass, a 320px pass, and a reduced-motion pass. It uses `/index.html?noboot` for interaction, sends a real Escape key to close the case-file dialog, and reports console errors in every pass. Blocked Google Fonts downloads from `fonts.gstatic.com` are ignored; every other console error fails the run. No third-party Python package is needed.

Both commands run through `.githooks/pre-commit`. Enable the hook once after cloning:

```bash
git config core.hooksPath .githooks
```
