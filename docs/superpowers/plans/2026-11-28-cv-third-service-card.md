# CV Third Service Card Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the shipped scraping bullet with a third CV service card placed below the two existing cards, then verify and push the change.

**Architecture:** The static suite pins three service cards, the exact English copy, and one full-width CSS rule. HTML gains the third card and loses the scraping bullet from the first card. CSS adds one span rule. No JavaScript changes, no carousel, no new interactive element. The existing Firefox smoke covers all widths and reduced motion, with one new 320px geometry check.

**Tech Stack:** Static HTML and CSS, Python unittest, Firefox WebDriver BiDi smoke script, `git` CLI.

**Spec:** `docs/superpowers/specs/2026-11-28-cv-third-service-card-design.md`

## Global Constraints

- All visitor-facing copy stays English. No em dash in new copy.
- Third card description is exactly `E-commerce price and catalog scraping, job and property listings, and scheduled monitoring. Data is cleaned and saved as CSV, Excel, or JSON.`
- Third card bullets are exactly `Scrapy and Playwright`, `CSS and XPath selectors`, `JSON APIs and data pipelines`.
- First card keeps its original four bullets and loses the scraping bullet. Second card is unchanged.
- No slider, no carousel controls, and no `js/main.js` change.
- No seventh real case and no change to `06 REAL / 03 FICTIONAL / 04 MODULES`.
- `demos/` stays byte-identical and `git diff --stat -- demos` stays empty.
- Unit tests and rendered smoke stay green at 390px, 320px, reduced motion, and 1366px.
- `web-scraping-portfolio` stays unchanged outside the repo and is not pushed again.
- Work stays on `master` with linear commits; push to `origin/master` only after full verification.

## Review Focus

1. Indonesian copy from the reference README must not reach the page. Pinned by the exact English markers in Task 1 Step 1.
2. The first card must keep its automation bullets in order, with no scraping line left behind. Pinned by the ordered-card assertions in Task 1 Step 1.
3. The third card must span both columns on desktop and fit 320px without overflow. Pinned by the CSS regex in Task 1 Step 2 and the smoke geometry check in Task 3 Step 3.
4. The six real cases, three fictional cases, four modules, and `demos/` must not change. Pinned by the full suites and `git diff --stat -- demos` in Tasks 2 and 3.
5. No new interactive element or motion may appear in the CV. Pinned by the no-button assertion in Task 1 Step 2 and the existing reduced-motion smoke checks in Tasks 2 and 3.

---

### Task 1: Pin the three-card contract

**Files:**
- Modify: `tests/test_portfolio.py`

**Interfaces:**
- Consumes: the exact third-card copy and the one-rule layout decision from the spec.
- Produces: failing assertions that Task 2 must satisfy, and the names `cards` and `.cv-service--wide` used by later checks.

- [ ] **Step 1: Replace the bullet pin with the three-card pin**

In `ContentTest.test_cv_identity_and_services`, remove this marker from the tuple:

```python
"E-commerce price &amp; catalog scraping, job/property listings, scheduled monitoring, and CSV/Excel/JSON delivery",
```

Add these markers to the same tuple:

```python
"Web Scraping",
"Scrapy and Playwright",
"CSS and XPath selectors",
"JSON APIs and data pipelines",
"E-commerce price and catalog scraping, job and property listings, and scheduled monitoring.",
"Data is cleaned and saved as CSV, Excel, or JSON.",
```

Replace the existing two-card assertion with the following block:

```python
        cards = re.findall(r'<article class="cv-service[^"]*">(.*?)</article>', HTML, re.S)
        self.assertEqual(len(cards), 3)
        self.assertLess(cards[0].index("Webhooks &amp; API integrations"), cards[0].index("Google Sheets / CRM"))
        self.assertNotIn("scraping", cards[0])
        self.assertNotIn("Scrapy and Playwright", cards[1])
        self.assertLess(cards[2].index("Scrapy and Playwright"), cards[2].index("CSS and XPath selectors"))
        self.assertLess(cards[2].index("CSS and XPath selectors"), cards[2].index("JSON APIs and data pipelines"))
```

- [ ] **Step 2: Pin the layout rule and the absence of new controls**

Add this method to `ContentTest`:

```python
    def test_third_service_card_layout(self):
        self.assertIn('<article class="cv-service cv-service--wide reveal">', HTML)
        self.assertRegex(CSS, r'\.cv-service--wide\s*\{\s*grid-column:\s*1\s*/\s*-1;')
        cv_block = re.search(r'<section[^>]+id="cv".*?</section>', HTML, re.S).group(0)
        self.assertNotIn("<button", cv_block)
```

- [ ] **Step 3: Verify RED**

Run:

```bash
python3 -m unittest discover -s tests
python3 tests/browser_smoke.py | tail -1
```

Expected: the static suite fails only on the new third-card assertions. The rendered smoke stays at `checks=158 failed=0`. Record the actual failure count in the ledger instead of predicting it.

- [ ] **Step 4: Commit the tests**

```bash
git add tests/test_portfolio.py
git commit --no-verify -m "test: pin third CV service card"
```

Use `--no-verify` only for this intentional RED commit because the repo hook reruns the full suite.

### Task 2: Add the third card and its span rule

**Files:**
- Modify: `index.html:236-257`
- Modify: `css/styles.css:3489-3513`

**Interfaces:**
- Consumes: the exact copy in the spec and the markers from Task 1.
- Produces: three `.cv-service` articles in the CV grid and a `.cv-service--wide` rule that makes Task 1 pass.

- [ ] **Step 1: Restore the first card**

Remove this line from the first `.cv-service` list:

```html
<li>E-commerce price &amp; catalog scraping, job/property listings, scheduled monitoring, and CSV/Excel/JSON delivery</li>
```

Leave `Webhooks &amp; API integrations`, `Google Sheets / CRM`, and `AI classification and reply drafts` in place.

- [ ] **Step 2: Add the third card**

Insert this article directly after the second `.cv-service` article and before the closing `</div>` of `.cv-grid`:

```html
          <article class="cv-service cv-service--wide reveal">
            <span class="section-index">03</span>
            <h3>Web Scraping</h3>
            <p>E-commerce price and catalog scraping, job and property listings, and scheduled monitoring. Data is cleaned and saved as CSV, Excel, or JSON.</p>
            <ul>
              <li>Scrapy and Playwright</li>
              <li>CSS and XPath selectors</li>
              <li>JSON APIs and data pipelines</li>
            </ul>
          </article>
```

- [ ] **Step 3: Add the span rule**

Insert after the `.cv-service` block in `css/styles.css`:

```css
.cv-service--wide {
  grid-column: 1 / -1;
}
```

- [ ] **Step 4: Verify GREEN**

Run:

```bash
python3 -m unittest discover -s tests
python3 tests/browser_smoke.py | tail -1
git diff --stat -- demos
git diff --check
```

Expected: `Ran 38 tests ... OK`, `checks=158 failed=0`, empty `demos` diff, and no `git diff --check` output.

- [ ] **Step 5: Commit**

```bash
git add index.html css/styles.css
git commit -m "feat: add Web Scraping CV service card"
```

### Task 3: Record the service, add the 320px check, and push

**Files:**
- Modify: `PRODUCT.md:74`
- Modify: `README.md:6,52`
- Modify: `tests/browser_smoke.py:566-573`

**Interfaces:**
- Consumes: the shipped third card from Task 2.
- Produces: owner docs that say three services, one rendered geometry check, and a verified push to `origin/master`.

- [ ] **Step 1: Update `PRODUCT.md`**

Replace this exact line:

```markdown
- The CV lists two services and three real contact channels. The `AI & workflow automation` service lists e-commerce price and catalog scraping, job and property listings, scheduled monitoring, and CSV/Excel/JSON delivery from the owner's `web-scraping-portfolio` repo. Work & Services lists six real demo links and three fictional case studies.
```

with:

```markdown
- The CV lists three services and three real contact channels. The `Web Scraping` service covers e-commerce price and catalog scraping, job and property listings, scheduled monitoring, and CSV/Excel/JSON delivery from the owner's `web-scraping-portfolio` repo. Work & Services lists six real demo links and three fictional case studies.
```

- [ ] **Step 2: Update `README.md`**

Replace the overview bullet:

```markdown
- The CV section: Alan Nawa, Web & AI Automation, two services, and three real contact channels. A note in the section says it is the owner's real CV and that the case studies below it are fictional.
```

with:

```markdown
- The CV section: Alan Nawa, Web & AI Automation, three services, and three real contact channels. A note in the section says it is the owner's real CV and that the case studies below it are fictional.
```

Replace the paragraph in "The CV section":

```markdown
The section sits between the manifesto and the combined Work & Services section. It holds Alan Nawa's identity, two services, and three real contact channels. The `AI & workflow automation` service lists e-commerce price and catalog scraping, job and property listings, scheduled monitoring, and CSV/Excel/JSON delivery. A note labels it as the real CV and says the case studies below are fictional.
```

with:

```markdown
The section sits between the manifesto and the combined Work & Services section. It holds Alan Nawa's identity, three services, and three real contact channels. The `Web Scraping` card lists e-commerce price and catalog scraping, job and property listings, scheduled monitoring, and CSV/Excel/JSON delivery. A note labels it as the real CV and says the case studies below are fictional.
```

- [ ] **Step 3: Add the 320px geometry check**

In the narrow-width script, after the existing `cv section fits 320px` check, add:

```js
      const wideCard = doc.querySelector('.cv-service--wide');
      const wideRect = wideCard ? wideCard.getBoundingClientRect() : null;
      check('third service card fits 320px',
        Boolean(wideRect) && wideRect.left >= -1 && wideRect.right <= 321,
        wideRect ? Math.round(wideRect.left) + '..' + Math.round(wideRect.right) : 'missing');
```

- [ ] **Step 4: Verify before push**

Run:

```bash
python3 -m unittest discover -s tests
python3 tests/browser_smoke.py | tail -1
git diff --stat -- demos
git diff --check
git status --short --branch
```

Expected: `OK`, `checks=159 failed=0`, empty `demos` diff, clean diff check, and only the three files in this task modified.

- [ ] **Step 5: Commit**

```bash
git add PRODUCT.md README.md tests/browser_smoke.py
git commit -m "docs: record third CV service"
```

- [ ] **Step 6: Review, push, and confirm**

Dispatch one independent reviewer over the full range from the pre-task SHA to `HEAD`, using `requesting-code-review`. Fix any Critical or Important finding before pushing. Then run:

```bash
git push origin master
git status --short --branch
printf 'local=%s\n' "$(git rev-parse HEAD)"
printf 'remote=%s\n' "$(git ls-remote origin refs/heads/master | cut -f1)"
```

Expected: clean `master...origin/master` status and identical local and remote SHAs. No branch, merge, or pull request.
