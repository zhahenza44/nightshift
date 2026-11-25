# Add real CV to NightShift Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Keep the NIGHT//SHIFT landing page and its fictional showcase intact, and add a real Alan Nawa CV section after the manifesto.

**Architecture:** The page stays one static HTML file with the existing English NightShift copy and interaction script. A new `section#cv` reuses the section layout pattern and adds only minimal CSS from existing tokens; the case-file dialogs and all demo motion keep working unchanged. Tests pin the CV content and the untouched NightShift contract before implementation.

**Tech Stack:** Static HTML, CSS, vanilla JavaScript, Python unittest, Firefox BiDi smoke script. No build step and no new dependency.

**Spec:** `docs/superpowers/specs/2026-11-25-nightshift-cv-section-design.md`

## Global Constraints

- Brand and hero stay `NIGHT//SHIFT`; do not rename the brand or hero copy.
- Every visitor-facing string stays English, including new CV copy and accessible names.
- All fictional NightShift content stays: three case files, their metrics, `hello@nightshift.studio`, `https://wa.me/6281234567890`, status `OPEN — Q1 2027`, and the disclosure sentence.
- CV data comes verbatim from `bbebb12:index.html`; do not invent names, claims, metrics, or contact details.
- `demos/` stays unchanged; only links to it are added.
- CSS changes are additive and use existing custom properties; existing NightShift rules stay untouched.
- Reduced motion, keyboard focus, menu, dialog, toast, clock, ticker, orb, and ghost cursor behavior stay working.
- Commit on `master`, one commit per task. No push and no merge.

## Review Focus

- A fifth nav item at 320px could overflow or shrink tap targets below 24px. Pinned in Task 1 by the rendered `320px has no horizontal overflow` and `header controls fit 320px and meet 24px tap target` checks; verified in Task 2.
- Real CV data next to fictional case studies could mislead readers. Pinned in Task 1 by `test_cv_note_and_fictional_disclosure` and the rendered `cv note separates real CV from fictional case files` check.
- Demo links could point to wrong paths or navigate away from the landing page. Pinned in Task 1 by `test_cv_demo_links` and the rendered `six CV demo links open in a new tab` check.
- Renumbering could leave the nav pointing at old section numbers. Pinned in Task 1 by `test_section_numbering_and_nav` and the rendered `CV nav anchor reaches the CV section` check.
- Added CSS could disturb existing animations or reduced-motion rules. Pinned in Task 1 by `test_nightshift_visual_markers` and the existing rendered animation and reduced-motion checks; verified in Task 2.

---

### Task 1: Pin the CV contract with failing tests

**Files:**
- Modify: `tests/test_portfolio.py`
- Modify: `tests/browser_smoke.py`

**Interfaces:**
- Consumes: exact CV strings and paths from `bbebb12:index.html`, and the existing NightShift markers in the current tests.
- Produces: named static tests and rendered checks consumed by Tasks 2 and 3.

- [ ] **Step 1: Add static tests to `tests/test_portfolio.py`**

  Keep every existing NightShift assertion except these three changes:
  - In `ContentTest.test_nightshift_sections_exist`, add `id="cv"`.
  - In `ContentTest.test_old_shell_contract_is_absent`, remove only the phrases now intentionally restored (`"Alan Nawa"`, `"https://instagram.com/zhahenzar"`, `"zhahenza666@proton.me"`, `'href="https://github.com/zhahenza44"'`, `'href="demos/'`, `"SIX LIVE DEMOS"`); keep `not-a-dev`, `motion-toggle`, `Pause motion`, `id="project-grid"`, `id="filter-all"`, `class="sr-only"`, and `data-track=`.
  - In `CssContractTest.test_stylesheet_is_copied_from_demo`, replace the byte-for-byte equality with: the file is non-empty, every selector and keyframe marker from `demos/nightshift/css/styles.css` is still present in `CSS`, and `.cv-` selectors appear in `CSS`.

  Add these tests:
  - `ContentTest.test_section_numbering_and_nav`: assert `'<a href="#cv"><span>02</span>CV</a>'`, `'<a href="#work"><span>03</span>Work</a>'`, `'<a href="#services"><span>04</span>Services</a>'`, `'<a href="#process"><span>05</span>Process</a>'`, `'<a href="#contact"><span>06</span>Contact</a>'`, `'<span class="section-index">02</span>'`, and `'>MANIFESTO</span>'`; assert `HTML.index('id="cv"')` is between `HTML.index('id="studio"')` and `HTML.index('id="work"')`.
  - `ContentTest.test_cv_identity_and_services`: assert `"Alan Nawa"`, `"Web &amp; AI Automation"`, `"Hi, I'm Alan Nawa"`, `"I build clean websites and automated workflows"`, `"AI &amp; workflow automation"`, `"Websites &amp; landing pages"`, `"Webhooks &amp; API integrations"`, `"Google Sheets / CRM"`, `"Company profiles &amp; catalogs"`, and `"Responsive and easy to maintain"`.
  - `ContentTest.test_cv_demo_links`: assert all six exact href values (`demos/ai-lead-capture/dashboard/index.html`, `demos/servis-ac/index.html`, `demos/ruang-rapi/index.html`, `demos/kedai-kopi/index.html`, `demos/rental-mobil/index.html`, `demos/nightshift/index.html`), the six visible names (`AI Lead Capture`, `Servis AC`, `Ruang Rapi`, `Kedai Kopi Oak`, `Rental Mobil`, `NIGHT//SHIFT`), `HTML.count('href="demos/') == 6`, and every CV demo link has `target="_blank" rel="noopener noreferrer"`.
  - `ContentTest.test_cv_contacts`: assert `https://instagram.com/zhahenzar`, `https://github.com/zhahenza44`, `mailto:zhahenza666@proton.me`, and the labels `@zhahenzar`, `zhahenza44`, `zhahenza666@proton.me`.
  - `ContentTest.test_cv_note_and_fictional_disclosure`: assert `"This section is my real CV"` and keep `"names, metrics, email, and phone number are fictional"`.
  - `CssContractTest.test_cv_styles_use_existing_tokens`: assert `.cv-grid`, `.cv-service`, and `.cv-demo-list` are in `CSS`, and that the CV block uses `var(--cyan)` and `var(--muted)`.

- [ ] **Step 2: Run the static suite and confirm the new tests fail**

  Run: `python3 -m unittest discover -s tests -v`
  Expected: FAIL on the new CV assertions; existing NightShift assertions still pass.

- [ ] **Step 3: Update rendered checks in `tests/browser_smoke.py`**

  Inside the normal pass:
  - Add `'#cv'` to `required`.
  - Replace `no local demo links on landing page` with `six CV demo links open in a new tab`: collect `a[href^="demos/"]`, assert `length === 6`, every link has `target === '_blank'` and `rel` containing `noopener`, and the six hrefs match the static list.
  - Add checks: `cv section follows manifesto` (`section#cv` exists and its DOM index is after `#studio` and before `#work`), `cv identity is visible` (text contains `Alan Nawa` and `Web & AI Automation`), `cv note separates real CV from fictional case files` (text contains `This section is my real CV` and the footer disclosure still contains `fictional`), `CV nav anchor reaches the CV section` (`a[href="#cv"]` exists in both navs), and `three CV contact links present` (`instagram.com/zhahenzar`, `github.com/zhahenza44`, `mailto:zhahenza666@proton.me`).
  - Include `#cv` and `.cv-demo-list a` in the existing visibility and link checks.

  In the 320px pass, add `cv section fits 320px` using the existing overflow probe on `.cv-grid` and `.cv-demo-list`.

- [ ] **Step 4: Run the rendered suite and confirm it fails**

  Run: `python3 tests/browser_smoke.py`
  Expected: FAIL on the new CV checks because the section does not exist yet.

- [ ] **Step 5: Commit the red contract**

```bash
git add tests/test_portfolio.py tests/browser_smoke.py
git commit --no-verify -m "test: pin real CV section contract"
```

  `--no-verify` is required here: the pre-commit hook runs both suites, and this task intentionally leaves them red.

---

### Task 2: Add the CV section and minimal styles

**Files:**
- Modify: `index.html`
- Modify: `css/styles.css`

**Interfaces:**
- Consumes: the assertions from Task 1 and the exact CV copy at `bbebb12:index.html`.
- Produces: `section#cv`, nav link `#cv`, `.cv-grid`, `.cv-service`, `.cv-demo-list` used by the rendered checks.

- [ ] **Step 1: Insert the CV section after `#studio`**

  In `index.html`, add `<section class="section cv" id="cv">` directly after the closing `</section>` of `#studio`. Follow the existing section pattern: `.wrap`, `.section-head reveal` with `<span class="section-index">02</span>`, `<span class="section-label">CV</span>`, `.section-line`, and `<span class="section-meta">ALAN NAWA / WEB &amp; AI AUTOMATION</span>`.

  Inside it, write:
  - A `.cv-grid` with a `.cv-intro` column containing `<h2 class="section-title reveal">Alan<br><em>Nawa.</em></h2>`, the bio `Hi, I'm Alan Nawa, not-a-dev :) I build clean websites and automated workflows so your business can respond to customers faster.`, and the note `This section is my real CV. The case studies below are fictional.`
  - An `aside class="spec-panel reveal" aria-label="CV details"` with `dl` rows `NAME / Alan Nawa`, `FOCUS / Web development & AI automation`, `PROJECTS / Six live demos`, and `CONTACT / Three channels`.
  - Two `article class="cv-service reveal"` blocks with headings `AI & workflow automation` and `Websites & landing pages`, each using the heading, paragraph, and three list items copied verbatim from `bbebb12:index.html`.
  - A `ul class="cv-demo-list"` with six `li` items. Each item has the exact name, one-sentence description, and tags copied from `bbebb12:index.html`, plus a link with the exact demo path from that file and `target="_blank" rel="noopener noreferrer"`.
  - A `.cv-contact` block with the three real contact links and labels from `bbebb12:index.html`.

- [ ] **Step 2: Add the CV nav entry and renumber sections**

  Add `<a href="#cv"><span>02</span>CV</a>` after the Work link in both `.site-nav` and `.mobile-menu nav`. Renumber Work to 03, Services to 04, Process to 05, Contact to 06 in both navs and in all five existing `section-head` blocks. Do not change the hero, ticker, footer, or dialog copy.

- [ ] **Step 3: Add minimal CSS**

  Append a CV block to `css/styles.css` before the existing `@media (prefers-reduced-motion: reduce)` section. Define only `.cv-grid`, `.cv-intro`, `.cv-service`, `.cv-service h3`, `.cv-service ul`, `.cv-demo-list`, `.cv-demo-list li`, and `.cv-contact` as needed for a two-column section that collapses to one column on narrow screens. Use existing variables (`--bg-soft`, `--surface`, `--line`, `--ink`, `--muted`, `--cyan`, `--pad`, `--wrap`, `--font-mono`) and existing spacing scale. Add no new animation and no new font or network request. Do not modify any existing selector or keyframe.

- [ ] **Step 4: Run the full local verification**

  Run: `python3 -m unittest discover -s tests -v && python3 tests/browser_smoke.py`
  Expected: both green; all existing NightShift checks still pass, and every new CV check passes at 390px, 320px, and reduced motion.

- [ ] **Step 5: Commit**

```bash
git add index.html css/styles.css
git commit -m "feat: add Alan Nawa CV section to NightShift"
```

  Commit normally; the pre-commit hook should pass.

---

### Task 3: Document the mixed page and verify the whole change

**Files:**
- Modify: `README.md`
- Modify: `PRODUCT.md`
- Modify: `.superpowers/sdd/2026-11-25-nightshift-cv-section/progress.md` if a ledger is in use

**Interfaces:**
- Consumes: the shipped CV section and the unchanged fictional showcase from Task 2.
- Produces: documentation that distinguishes real CV data from the fictional demo, and a fresh verification record.

- [ ] **Step 1: Update `README.md`**

  Describe both parts of the landing page: the untouched NightShift fictional showcase and the new real CV section. List the six demo links and real contact channels. State that `css/styles.css` now contains additive CV rules, that `demos/` is unchanged, and that the fictional disclaimer still applies to the case studies only.

- [ ] **Step 2: Update `PRODUCT.md`**

  Record the owner decisions: brand stays NIGHT//SHIFT, fictional showcase stays, CV uses data from the old shell, CV sits after the manifesto, CSS additions are allowed, and no file in `demos/` changed. Note that the `--muted-2` contrast override from the earlier design still stands.

- [ ] **Step 3: Run final verification**

  Run all of these and read the output:
  - `python3 -m unittest discover -s tests -v` → OK, 21+ tests
  - `python3 tests/browser_smoke.py` → `failed=0`
  - `xmllint --html --noout index.html` → exit 0
  - a local HTTP fetch of `/index.html`, `/css/styles.css`, `/js/main.js`, `/assets/favicon.svg`, and all six demo paths → all 200
  - `git hook run pre-commit` → exit 0
  - `impeccable detect --json --changed` → no findings for the edited files
  - `git diff --name-only <plan commit>..HEAD -- demos/` → no output

- [ ] **Step 4: Commit**

```bash
git add README.md PRODUCT.md
git commit -m "docs: describe CV section inside NightShift"
```
