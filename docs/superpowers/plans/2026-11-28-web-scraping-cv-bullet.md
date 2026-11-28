# Web Scraping CV Bullet Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the owner's first-job scraping capability to the existing CV service list and keep a local reference copy of the public repo, without adding a case or touching `demos/`.

**Architecture:** The static test suite pins one new English bullet inside the first CV service. The public repo is cloned into a new folder under `~/Projects` as a reference only. HTML gains the bullet, owner docs record it, and the existing tests and Firefox smoke verify all widths plus reduced motion.

**Tech Stack:** Static HTML, Python unittest, Firefox WebDriver BiDi smoke script, `gh`/`git` CLI.

**Spec:** `docs/superpowers/specs/2026-11-28-web-scraping-cv-bullet-design.md`

## Global Constraints

- All visitor-facing copy stays English.
- Bullet text is exactly `E-commerce price &amp; catalog scraping, job/property listings, scheduled monitoring, and CSV/Excel/JSON delivery`.
- The two CV service cards stay two cards; no CSS or grid change.
- No new real case, no change to `06 REAL / 03 FICTIONAL / 04 MODULES`.
- `demos/` stays byte-identical and `git diff --stat -- demos` stays empty.
- Unit tests and rendered smoke stay green at 390px, 320px, reduced motion, and 1366px.
- The downloaded reference copy stays unchanged; the public repo is not pushed again.
- Work stays on `master` with linear commits; push to `origin/master` only after full verification.

## Review Focus

1. Indonesian copy from the repo README must not leak into the page. Pinned in Task 1 by the exact English marker and by the existing English-copy static tests.
2. The CV must keep two service cards, not grow a third. Pinned in Task 1 by asserting exactly two `<article class="cv-service reveal">` elements.
3. The six real cases, three fictional cases, and four capability modules must not change. Pinned by the full existing static and rendered suite in Task 2 and Task 3.
4. `demos/` must stay untouched. Pinned by `git diff --stat -- demos` in Task 2 and Task 3.
5. Adding a long bullet must not overflow narrow widths or hidden reduced-motion content. Pinned by the full rendered smoke in Task 2 and Task 3.

---

### Task 1: Pin the CV scraping bullet contract

**Files:**
- Modify: `tests/test_portfolio.py`

**Interfaces:**
- Consumes: the approved bullet text and the two-card CV structure from the spec.
- Produces: a failing static assertion that Task 2 must satisfy.

- [ ] **Step 1: Add the failing static assertions**

In `ContentTest.test_cv_identity_and_services`, add this marker to the existing tuple of pinned markers:

```python
"E-commerce price &amp; catalog scraping, job/property listings, scheduled monitoring, and CSV/Excel/JSON delivery",
```

After the existing `for marker in (...)` loop, add:

```python
self.assertEqual(HTML.count('<article class="cv-service reveal">'), 2)
```

- [ ] **Step 2: Verify RED**

Run:

```bash
python3 -m unittest discover -s tests
python3 tests/browser_smoke.py | tail -1
```

Expected: static suite `FAILED (failures=2)` and rendered `checks=158 failed=0`. The two failures are the missing bullet and the service-card count is already correct, so the count assertion passes; if the count fails, stop and inspect the template before continuing.

- [ ] **Step 3: Commit the tests**

```bash
git add tests/test_portfolio.py
git commit --no-verify -m "test: pin CV scraping bullet"
```

Use `--no-verify` only for this intentional RED commit because the repo's pre-commit hook reruns the full suite.

### Task 2: Add the local reference copy and the bullet

**Files:**
- Create (outside the repo): `~/Projects/web-scraping-portfolio/`
- Modify: `index.html:240-244`

**Interfaces:**
- Consumes: the bullet marker from Task 1.
- Produces: the final CV markup that makes Task 1 pass.

- [ ] **Step 1: Clone the public reference repo**

Run:

```bash
gh repo clone zhahenza44/web-scraping-portfolio /home/asnodt/Projects/web-scraping-portfolio
git -C /home/asnodt/Projects/web-scraping-portfolio status --porcelain
git -C /home/asnodt/Projects/web-scraping-portfolio remote get-url origin
```

Expected: clean status output and an `origin` URL pointing to `zhahenza44/web-scraping-portfolio`. If the target directory already exists, stop and inspect it before overwriting anything.

- [ ] **Step 2: Add the bullet in `index.html`**

In the first `.cv-service` list, insert the new `<li>` between `Webhooks &amp; API integrations` and `Google Sheets / CRM`:

```html
<li>E-commerce price &amp; catalog scraping, job/property listings, scheduled monitoring, and CSV/Excel/JSON delivery</li>
```

Change no other markup, attribute, href, or copy.

- [ ] **Step 3: Verify GREEN**

Run:

```bash
python3 -m unittest discover -s tests
python3 tests/browser_smoke.py | tail -1
git diff --stat -- demos
git diff --check
```

Expected: `Ran 38 tests ... OK`, `checks=158 failed=0`, empty `demos` diff, and no `git diff --check` output.

- [ ] **Step 4: Commit the source change**

```bash
git add index.html
git commit -m "feat: list scraping work in CV services"
```

### Task 3: Record the capability and push

**Files:**
- Modify: `PRODUCT.md`
- Modify: `README.md`

**Interfaces:**
- Consumes: the final bullet from Task 2.
- Produces: owner-facing docs that match the shipped page, then the remote push.

- [ ] **Step 1: Update `PRODUCT.md`**

In the Capabilities and Constraints bullet that says the CV lists two services, add one sentence naming the scraping services now listed under `AI & workflow automation`. Keep the phrase "two services" and the six/three/four Work counts unchanged.

- [ ] **Step 2: Update `README.md`**

In "The CV section", add one sentence naming the same scraping services. Keep the phrase "two services" and every existing contact and case description unchanged.

- [ ] **Step 3: Verify before push**

Run:

```bash
python3 -m unittest discover -s tests
python3 tests/browser_smoke.py | tail -1
git diff --stat -- demos
git diff --check
git status --short --branch
```

Expected: `OK`, `checks=158 failed=0`, empty `demos` diff, clean `git diff --check`, and only the two docs files modified.

- [ ] **Step 4: Commit and push**

```bash
git add PRODUCT.md README.md
git commit -m "docs: record CV scraping capability"
git push origin master
git status --short --branch
```

Expected: push succeeds and `git status --short --branch` shows `## master...origin/master` with no ahead or behind count.
