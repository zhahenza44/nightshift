# Work and Services Merge Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Merge Work and Services into one section, switch the page location to Surabaya, and apply the owner's label and hero-stat changes without breaking the existing NightShift and CV contracts.

**Architecture:** The page stays static HTML with a single combined `section#work`. The former services section becomes a `.services-block` inside that section, reusing existing section furniture and service-card CSS with a small additive spacing rule. Tests pin the new structure before the markup changes, then the rendered smoke suite verifies 390px, 320px, and reduced motion.

**Tech Stack:** Static HTML, CSS, vanilla JavaScript, Python unittest, Firefox BiDi rendered smoke checks.

**Spec:** `docs/superpowers/specs/2026-11-26-nightshift-work-services-merge-design.md`

## Global Constraints

- Keep the `NIGHT//SHIFT` brand and hero identity.
- Keep the fictional case studies, metrics, status, email address, phone number, and fictional disclosure.
- Keep the real CV section, six demo links, and three real contact channels unchanged.
- All visitor-facing copy stays English.
- Keep `Response <24h` exactly, including the terminal line and contact copy.
- Keep Google Fonts requests and local fallbacks.
- CSS additions reuse existing tokens and add no new decorative system.
- Do not modify any file in `demos/`.
- No push or merge.

## Review Focus

- 320px combined section: the three case files and four service cards must stay inside the viewport and not collide. Pinned by the `combined section fits 320px` rendered check in Task 1.
- Removed `#services` anchor: no nav or in-page link may point to a missing section. Pinned by `test_merged_work_and_services_contract` and `services nav anchor is gone` in Task 1.
- Location consistency: every visitor-facing Jakarta or JKT string must become Surabaya, ID. Pinned by `test_surabaya_and_github_label` and `location is Surabaya` in Task 1.
- Hero count animation: `data-count="1"` must settle on `1`, not on a stale or doubled value. Pinned by `hero stats match owner update` in Task 1.
- Console harness: blocked font downloads must not hide real console errors. Pinned by `test_browser_smoke_ignores_only_font_download_errors` in Task 1 and by the full rendered suite in Task 2.

---

### Task 1: Pin the merged-page contract, RED

**Files:**
- Modify: `tests/test_portfolio.py`
- Modify: `tests/browser_smoke.py`

**Interfaces:**
- Consumes: the approved design doc and current page markup.
- Produces: static markers and rendered checks consumed by Task 2. The allowed console filter is consumed by every later smoke run.

- [ ] **Step 1: Make the rendered console check tolerate only blocked Google Fonts downloads**

  In `tests/browser_smoke.py`, replace the `errors` comprehension in `run_browser_pass` with this filter:

  ```python
  errors = [
      event for event in client.events
      if event.get("method") == "log.entryAdded"
      and event.get("params", {}).get("level") == "error"
      and not (
          "downloadable font: download failed" in str(
              event.get("params", {}).get("text", ""))
          and "fonts.gstatic.com" in str(event.get("params", {}).get("text", ""))
      )
  ]
  ```

  Run: `python3 tests/browser_smoke.py`
  Expected: the script runs; `no console errors` passes; failures come only from the checks added in later steps.

- [ ] **Step 2: Add the static harness contract**

  In `tests/test_portfolio.py`, add `test_browser_smoke_ignores_only_font_download_errors`. Read `tests/browser_smoke.py` and assert it contains `downloadable font: download failed`, `fonts.gstatic.com`, and `event.get("params", {}).get("level") == "error"`.

- [ ] **Step 3: Update the static page contract**

  In `test_nightshift_sections_exist`, remove the `id="services"` marker and keep `id="work"`.

  In `test_english_navigation_and_actions` and `test_section_numbering_and_nav`, replace the old nav markers with these, asserting each nav marker appears exactly twice:

  ```python
  '<a href="#work"><span>03</span>Work &amp; Services</a>'
  '<a href="#process"><span>04</span>Process</a>'
  '<a href="#contact"><span>05</span>Contact</a>'
  ```

  Also assert `href="#services"` and `id="services"` are absent.

  In `test_sections_and_disclosure_are_english`, replace `>SELECTED WORK</span>` with `>WORK &amp; SERVICES</span>`. Keep `>CAPABILITIES</span>`, `Four things we take seriously`, and the fictional-disclosure marker.

  Add `test_merged_work_and_services_contract` asserting the combined section head marker `>WORK &amp; SERVICES</span>`, `<span class="section-index">03</span>`, and the document order `studio` before `cv` before `work` before `process` before `contact`.

  Add `test_surabaya_and_github_label` asserting these markers are present:

  ```python
  'DIGITAL STUDIO<br>SURABAYA, ID'
  '<span>SURABAYA, ID</span>'
  '<dd>Surabaya, ID</dd>'
  '<span class="t-key">location</span>: surabaya, id'
  '<div class="terminal-foot"><span>SURABAYA, ID</span>'
  '<span class="mono">SURABAYA, ID</span>'
  'href="https://github.com/zhahenza44/otomasi-web" target="_blank" rel="noopener">GITHUB <span>↗</span></a>'
  ```

  Assert `JKT`, `Jakarta`, `jakarta`, and `SOURCE <span>↗</span>` are absent.

  Add `test_hero_stats_contract` asserting these exact markers:

  ```python
  '<div><dt>Projects</dt><dd><span class="count" data-count="1">1</span></dd></div>'
  '<div><dt>Response</dt><dd>&lt;24<span>h</span></dd></div>'
  ```

  Assert `<dt>Experience</dt>`, `data-count="40"`, and `data-count="6"` are absent.

- [ ] **Step 4: Add the rendered contract**

  In the normal pass of `tests/browser_smoke.py`:

  - Remove `'#services'` from `required` and add the check `section ids are merged`, expecting `sectionIds.join(',') === 'top,studio,cv,work,process,contact'`.
  - Add `combined work section keeps both content blocks`, expecting `section#work .project-card` count 3 and `section#work .service-card` count 4.
  - Add `services nav anchor is gone`, expecting zero `a[href="#services"]`.
  - Add `github label replaced source`, expecting the `otomasi-web` anchor text to start with `GITHUB` and the contact-links text not to contain `SOURCE`.
  - Add `location is Surabaya`, expecting body text to contain `Surabaya, ID` and `surabaya, id`, and not contain `Jakarta` or `JKT`.
  - Add `hero stats match owner update`, expecting `.hero-stats dt` labels to be `Projects,Response` and `.hero-stats dd` text values to be `1` and `<24h`.

  In the narrow pass, add `combined section fits 320px`, expecting `.services-block` to have `rect.left >= -1` and `rect.right <= 321`.

- [ ] **Step 5: Run the suites and confirm RED**

  Run: `python3 -m unittest discover -s tests -v`
  Expected: failures for the new static markers, with `test_browser_smoke_ignores_only_font_download_errors` passing.

  Run: `python3 tests/browser_smoke.py`
  Expected: failures for the new rendered checks; `no console errors` passes.

- [ ] **Step 6: Commit the RED contract**

  ```bash
  git add tests/test_portfolio.py tests/browser_smoke.py
  git commit --no-verify -m "test: pin merged work and services contract"
  ```

  Use `--no-verify` because the page implementation is intentionally absent.

### Task 2: Merge the sections and apply the page changes, GREEN

**Files:**
- Modify: `index.html`
- Modify: `css/styles.css`

**Interfaces:**
- Consumes: the markers and rendered checks from Task 1.
- Produces: `section#work` with `.services-block`, nav label `Work &amp; Services`, Surabaya location strings, `GITHUB` contact label, and the updated hero stats.

- [ ] **Step 1: Merge the two sections in `index.html`**

  Keep one `<section class="section work" id="work">`. Set its head to `<span class="section-index">03</span>`, `<span class="section-label">WORK &amp; SERVICES</span>`, and `<span class="section-meta">03 FILES / 04 MODULES</span>`.

  Keep the existing `.work-intro` and `.project-stack` unchanged. Replace the separate services `<section>` with a `<div class="services-block">` inside the work section. Put a compact `.section-head` with `>CAPABILITIES</span>` inside it, followed by the existing `.services-intro` and `.service-grid` markup. Keep the sentence containing `Four things we take seriously`.

  Renumber the process section head to `04` and the contact section head to `05`.

- [ ] **Step 2: Update both navs**

  Remove the `Services` anchor. Set the work anchor to `<a href="#work"><span>03</span>Work &amp; Services</a>` in both navs. Set process to `04` and contact to `05` in both navs.

- [ ] **Step 3: Apply the owner's text and stat changes**

  Replace every visitor-facing Jakarta or JKT location with Surabaya, ID in the same casing: brand meta, mobile menu foot, manifesto spec panel, hero foot, terminal `location` line, and terminal foot. Replace the hero coordinate line with `<span class="mono">SURABAYA, ID</span>`.

  In `.hero-stats`, set the Projects item to exactly `<div><dt>Projects</dt><dd><span class="count" data-count="1">1</span></dd></div>`, delete the Experience item, and leave the Response item untouched.

  In `.contact-links`, change only the visible `SOURCE` label to `GITHUB`. Keep the href, target, and rel unchanged.

- [ ] **Step 4: Add the minimal CSS**

  Before the reduced-motion block in `css/styles.css`, add only these rules using existing tokens:

  ```css
  .services-block {
    margin-top: clamp(90px, 12vw, 160px);
    padding-top: clamp(44px, 6vw, 76px);
    border-top: 1px solid var(--line);
  }

  .services-block .section-head {
    margin-bottom: clamp(32px, 5vw, 56px);
  }
  ```

  Do not add a new background, animation, or palette.

- [ ] **Step 5: Run both suites green**

  Run: `python3 -m unittest discover -s tests -v`
  Expected: OK, all tests pass.

  Run: `python3 tests/browser_smoke.py`
  Expected: `checks=... failed=0`, including no console errors and all new merged-page checks.

  If a check fails, change the page or CSS, not the contract.

- [ ] **Step 6: Commit the implementation**

  ```bash
  git add index.html css/styles.css
  git commit -m "feat: merge work and services into one section"
  ```

### Task 3: Document the change and verify the whole page

**Files:**
- Modify: `README.md`
- Modify: `PRODUCT.md`

**Interfaces:**
- Consumes: the shipped merged section from Task 2.
- Produces: documentation that matches the page and a fresh verification record.

- [ ] **Step 1: Update `README.md`**

  Describe the page as NightShift plus the real CV, with Work and Services now one section. State that the location is Surabaya, ID, the hero shows `Projects 1` and `Response <24h`, and the GitHub contact link is labelled `GITHUB`. Keep the six demo links, three real contacts, fictional disclosure, test commands, and unchanged `demos/` statement accurate.

- [ ] **Step 2: Update `PRODUCT.md`**

  Record the new owner decisions: merge Work and Services, location Surabaya, ID, `Projects 1`, remove Experience, keep Response, label the source link `GITHUB`. Note that the console harness ignores only blocked Google Fonts downloads and still fails on every other console error.

- [ ] **Step 3: Run the full verification**

  Run and record:

  ```bash
  python3 -m unittest discover -s tests -v
  python3 tests/browser_smoke.py
  git hook run pre-commit
  xmllint --html --noout index.html
  ```

  Expected: unit OK, rendered `failed=0`, hook exit 0, xmllint exit 0.

  Also verify `git diff --name-only <design-commit>..HEAD -- demos/` is empty and `git status --short` is clean after the commit.

- [ ] **Step 4: Commit the documentation**

  ```bash
  git add README.md PRODUCT.md
  git commit -m "docs: describe merged work and services page"
  ```
