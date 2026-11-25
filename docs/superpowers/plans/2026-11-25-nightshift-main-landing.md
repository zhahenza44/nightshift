# Plan: NightShift becomes the main landing page

Spec: `docs/superpowers/specs/2026-11-25-nightshift-main-landing-design.md`

Direction: this is a literal copy of `demos/nightshift/` with English visitor copy. The owner approved the fictional studio identity, numbers, status, contacts, Google Fonts, boot overlay, ghost cursor, and lack of pause control as explicit overrides of the normal anti-slop defaults. The em dash is also retained as part of the exact NightShift identity, at owner direction.

## Task 1: Red tests for the NightShift contract

Files: `tests/test_portfolio.py`

- Replace the old Alan Nawa shell assertions with assertions for the incoming NightShift contract. Keep the same test file and keep every check as a real assertion, not a deletion.
- Pin these static markers:
  - root `index.html` has `<html lang="en" class="no-js">`, the NightShift title and meta description, the Google Fonts links, the inline `no-js` to `js` script, and `js/main.js` with `defer`;
  - boot overlay, custom cursor, scanline, noise, scroll progress, header, mobile menu, hero, ticker, manifesto, work, services, process, contact, footer, dialog, and toast all exist;
  - the three case files `HYPERMART`, `AEGIS`, and `VOID HOTEL` exist with their fictional metrics;
  - the disclosure text is English;
  - visitor strings in both `index.html` and `js/main.js` contain no Indonesian words or phrases;
  - the old shell contract is absent: no six-card grid, no `motion-toggle`, no `Pause motion`, no Alan contact channels, no local demo card links in the landing page.
- Pin JavaScript behavior markers for boot skip via `?noboot`, count-up, scramble, ghost cursor, magnetic buttons, menu, case-file dialog, copy-email toast, clock, and nav observer.
- Run `python3 -m unittest discover -s tests -v` and record that the new tests fail against the current shell.

Commit: `test: pin NightShift landing contract`

## Task 2: Copy and translate the landing page

Files: `index.html`, `js/main.js`, `assets/favicon.svg`

- Copy `demos/nightshift/index.html` to root `index.html`, `demos/nightshift/js/main.js` to root `js/main.js`, and `demos/nightshift/assets/favicon.svg` to root `assets/favicon.svg`.
- Translate every visitor-facing string in `index.html` to English. Keep tag names, classes, IDs, data attributes, hrefs, brand tokens, dates, numbers, and status text otherwise unchanged.
- Translate every visitor-facing string in `js/main.js` to English, including menu labels, ghost labels, cursor labels, dialog copy, meta labels, toast copy, and copy-button feedback.
- Change the document language from `id` to `en`. Keep `class="no-js"`.
- Keep the fictional disclosure in the contact section and the case-file note, translated to English.
- Do not edit `css/styles.css` in this task. CSS contains no visitor copy that needs translation.
- Run the static tests and fix any missed Indonesian string or missing contract marker.

Commit: `feat: install NightShift landing page in English`

## Task 3: Replace the stylesheet

Files: `css/styles.css`

- Copy `demos/nightshift/css/styles.css` to root `css/styles.css`.
- Keep the stylesheet byte-for-byte equivalent to the demo stylesheet. The visual identity must match NightShift exactly.
- Confirm the static CSS contract from Task 1 passes against the copied stylesheet.

Commit: `feat: install NightShift visual system`

## Task 4: Rewrite rendered checks

Files: `tests/browser_smoke.py`

- Keep the Firefox BiDi harness and the three rendered passes, but replace old shell assertions with NightShift assertions.
- Load the main pass with `/index.html?noboot` so the boot overlay does not block interaction, and assert that the boot node is absent or finished.
- In the 390px pass, check viewport width, horizontal overflow, scoped overflow scan with a live probe, hero copy visibility, orb and ticker animation names, scroll progress, mobile menu open and close with English labels, focus movement and return, case-file dialog open and close with Escape, copy-email toast, magnetic button response, link click-through, required hrefs, visible focus, and footer progress.
- In the 320px pass, check no horizontal overflow and that the header brand, menu button, primary actions, and contact controls fit and meet tap targets.
- In the reduced-motion pass, check that animations are disabled, content stays visible, the custom cursor and ghost layer stay hidden, and no old pause control is expected.
- Keep console error capture in every pass.
- Run `python3 tests/browser_smoke.py` and fix all rendered failures.

Commit: `test: verify NightShift rendered behavior`

## Task 5: Documentation and final verification

Files: `README.md`, `PRODUCT.md`, `PRODUCT.md` or `DESIGN.md` if context requires it, SDD ledger if used by the active process

- Rewrite `README.md` to describe the NightShift landing page, English copy, the fictional-data disclosure, external Google Fonts, and the preserved `demos/` folder. Remove the old CV-only claims.
- Rewrite `PRODUCT.md` to record the owner-directed decisions: literal NightShift copy, English translation, fictional studio data kept, external fonts kept, no pause control, and no changes inside `demos/`.
- Run the full verification set:
  - `python3 -m unittest discover -s tests -v`;
  - `python3 tests/browser_smoke.py`;
  - `xmllint --html --noout index.html`;
  - local HTTP checks for root, CSS, JS, favicon, and the six demo paths;
  - contrast checks on the NightShift text and background pairs used in the page;
  - `git hook run pre-commit`;
  - antislop Delivery Gate and `impeccable detect --json --changed`.
- Record that all root files match the demo except translated visitor strings and document language.
- Commit documentation and leave `master` clean. Do not push or merge.

Commit: `docs: describe NightShift landing page`

## Done when

- Root `index.html`, `css/styles.css`, `js/main.js`, and `assets/favicon.svg` are the NightShift demo files, with English visitor copy in HTML and JS.
- `demos/` is unchanged.
- Static tests and rendered smoke tests pass with checks pinning the new contract.
- HTML validation, local HTTP paths, contrast checks, pre-commit hook, and finish gate evidence are fresh.
- `master` is clean and nothing is pushed or merged.
