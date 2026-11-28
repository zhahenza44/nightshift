# Web Scraping Real Case Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add one Web Scraping Portfolio real case with a single GitHub link and English copy, then verify and push to `origin/master`.

**Architecture:** The five scraper examples become one static `<li>` inside the existing `#work .real-case-list`, after the six demo rows. Static tests pin the exact row, the seven-row count, and the single external link. The Firefox smoke then pins visibility and new-tab behavior for that link. No JavaScript or CSS change.

**Tech Stack:** Static HTML, Python unittest, Firefox browser smoke.

**Spec:** `docs/superpowers/specs/2026-11-28-scraping-real-case-design.md`

## Global Constraints

- Visitor copy stays English. No em dash in new copy.
- Exact section meta: `07 REAL / 03 FICTIONAL / 04 MODULES`.
- Exact group meta: `07 CASES / REAL WORK`.
- Exact intro phrase: `Seven real cases and three fictional case studies`.
- Exact description: `Five working scrapers cover static HTML, pagination, a JSON API, JavaScript rendering, and a 1,000 row catalog export. Built for small businesses and companies that need to track competitor prices, watch job and property listings, follow public headlines, and export clean CSV, Excel, or JSON files.`
- Exact link: `https://github.com/zhahenza44/web-scraping-portfolio`, one occurrence in the real case list, `target="_blank"`, `rel="noopener noreferrer"`.
- Exactly seven `<li class="reveal">` rows in `#work .real-case-list`: six demos unchanged, then the scraper row last.
- `demos/` stays unchanged. No `js/main.js` or `css/styles.css` change.
- Baseline before Task 1: `Ran 39 tests ... OK`, `checks=159 failed=0`.

## Review Focus

1. Indonesian copy from the owner's request reaching the page. Pinned by the exact English description markers in Task 1.
2. Five scrapers becoming five rows or a separate group. Pinned by the seven-row count and single repo link in Task 1.
3. The new external link being dead or lacking new-tab behavior. Pinned by the two rendered checks in Task 2.
4. The six demo paths or `demos/` changing by accident. Pinned by `test_cv_demo_links` and `git diff --stat -- demos` in Task 2 and Task 3.
5. The longer row breaking 320px, reduced motion, or 1366px layout. Pinned by the full smoke run in Task 2 and again in Task 3.

---

### Task 1: Pin the single-row contract

**Files:**
- Modify: `tests/test_portfolio.py`

**Interfaces:**
- Consumes: the exact copy and link from the spec.
- Produces: two failing assertions that Task 2 must satisfy, plus the `blocks` split shape used by the new test.

- [ ] **Step 1: Replace the count markers and extend the work assertion**

In `ContentTest.test_real_cases_move_into_work`, replace `'06 REAL / 03 FICTIONAL / 04 MODULES'` with `'07 REAL / 03 FICTIONAL / 04 MODULES'` and add `'07 CASES / REAL WORK'` to the same marker tuple. Keep the six `demos/` hrefs, the six demo names, the `.cv-demo-list` absence checks, and `self.assertEqual(work_block.count('href="demos/'), 6)` unchanged. Add this line after that assertion:

```python
        self.assertEqual(work_block.count('href="https://github.com/zhahenza44/web-scraping-portfolio"'), 1)
```

- [ ] **Step 2: Add the exact row test**

Add this method directly after `test_real_cases_move_into_work`:

```python
    def test_scraping_real_case_contract(self):
        work_block = re.search(r'<section[^>]+id="work".*?</section>', HTML, re.S).group(0)
        blocks = work_block.split('<li class="reveal">')
        self.assertEqual(len(blocks) - 1, 7)
        if len(blocks) != 8:
            return
        self.assertIn("Web Scraping Portfolio", blocks[-1])
        row = blocks[-1]
        for marker in (
            "Web Scraping Portfolio",
            "Five working scrapers cover static HTML, pagination, a JSON API, JavaScript rendering, and a 1,000 row catalog export.",
            "Built for small businesses and companies that need to track competitor prices, watch job and property listings, follow public headlines, and export clean CSV, Excel, or JSON files.",
            "<li>Scrapy</li>",
            "<li>Playwright</li>",
            "<li>CSV</li>",
            'href="https://github.com/zhahenza44/web-scraping-portfolio"',
            'target="_blank"',
            'rel="noopener noreferrer"',
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, row)
```

The early return keeps the intentional RED a clean failure instead of an `IndexError` when the seventh row is missing.

- [ ] **Step 3: Verify RED**

Run: `python3 -m unittest discover -s tests 2>&1 | tail -30`
Expected: `FAILED` with failures for the missing meta markers, the missing repo link, the row count `6 != 7`, and the missing row copy. No errors.
Run: `python3 tests/browser_smoke.py 2>&1 | tail -1`
Expected: `checks=159 failed=0`, since Task 1 only edits static tests.

- [ ] **Step 4: Commit the failing test**

```bash
git add tests/test_portfolio.py
git commit --no-verify -m "test: pin Web Scraping real case"
```

The pre-commit hook runs the full suite and would reject an intentional RED commit.

### Task 2: Add the row and keep the rendered suite green

**Files:**
- Modify: `index.html:279,285,293,345`
- Modify: `tests/browser_smoke.py:392-400,451-456,462-480`

**Interfaces:**
- Consumes: the exact row from the spec and the assertions from Task 1.
- Produces: seven visible real case rows and one new-tab GitHub link that Task 3 documents.

- [ ] **Step 1: Update the three counts in `index.html`**

Replace `<span class="section-meta">06 REAL / 03 FICTIONAL / 04 MODULES</span>` with `07 REAL / 03 FICTIONAL / 04 MODULES`. Replace the work intro sentence with `Seven real cases and three fictional case studies show how we think, design, and build.` Replace `<span class="section-meta">06 DEMOS / REAL WORK</span>` with `07 CASES / REAL WORK`.

- [ ] **Step 2: Insert the seventh row after the NIGHT//SHIFT row and before `</ul>`**

```html
          <li class="reveal">
            <div>
              <h3>Web Scraping Portfolio</h3>
              <p>Five working scrapers cover static HTML, pagination, a JSON API, JavaScript rendering, and a 1,000 row catalog export. Built for small businesses and companies that need to track competitor prices, watch job and property listings, follow public headlines, and export clean CSV, Excel, or JSON files.</p>
              <ul class="project-tags"><li>Scrapy</li><li>Playwright</li><li>CSV</li></ul>
            </div>
            <a href="https://github.com/zhahenza44/web-scraping-portfolio" target="_blank" rel="noopener noreferrer">View code <span aria-hidden="true">↗</span></a>
          </li>
```

Do not add CSS. The row uses the existing `.real-case-list`, `.project-tags`, `.reveal`, and arrow span rules.

- [ ] **Step 3: Update the rendered checks**

In `tests/browser_smoke.py`:

1. Change `doc.querySelectorAll('#work .real-case-list a')` in the `six real demo links are visible` check to `doc.querySelectorAll('#work .real-case-list a[href^="demos/"]')`. Keep the count `6` and detail text out of `6`.
2. Add this check immediately after it:

```javascript
      const codeLink = doc.querySelector('#work .real-case-list a[href="https://github.com/zhahenza44/web-scraping-portfolio"]');
      const codeRect = codeLink ? codeLink.getBoundingClientRect() : null;
      check('Web Scraping code link is visible',
        Boolean(codeRect) && codeRect.width > 0 && codeRect.height > 0,
        codeRect ? 'visible' : 'missing');
```

3. Change `Array.from(doc.querySelectorAll('.real-case-list > li > div')).length === 6` to `=== 7` in `real case rows expose hover transform`.
4. Add `https://github.com/zhahenza44/web-scraping-portfolio` to the `required` array.
5. Change the `six real demo links open in a new tab` selector from `#work .real-case-list a` to `#work .real-case-list a[href^="demos/"]`. Keep its name, count, and assertions.
6. Add this check after it:

```javascript
      check('Web Scraping code link opens in a new tab',
        Boolean(codeLink) && codeLink.getAttribute('target') === '_blank' &&
          (codeLink.getAttribute('rel') || '').includes('noopener'),
        codeLink ? 'target=' + codeLink.getAttribute('target') + ' rel=' + codeLink.getAttribute('rel') : 'missing');
```

- [ ] **Step 4: Verify GREEN**

Run: `python3 -m unittest discover -s tests 2>&1 | tail -5`
Expected: `Ran 40 tests ... OK`.
Run: `python3 tests/browser_smoke.py 2>&1 | tail -1`
Expected: `checks=161 failed=0`, including the two new checks, 320px, reduced motion, and 1366px.
Run: `printf 'demos_diff_lines=%s\n' "$(git diff --stat -- demos | wc -l)"` and `git diff --check`
Expected: `demos_diff_lines=0` and no diff-check output.

- [ ] **Step 5: Commit**

```bash
git add index.html tests/browser_smoke.py
git commit -m "feat: add Web Scraping real case"
```

### Task 3: Record the case in owner docs, review, and push

**Files:**
- Modify: `PRODUCT.md:19,23,74` and add one owner-directed bullet before `## Capabilities and Constraints`.
- Modify: `README.md:3,7,58,65`.

**Interfaces:**
- Consumes: the shipped seventh row from Task 2.
- Produces: owner docs that match the live page and a verified push to `origin/master`.

- [ ] **Step 1: Update `PRODUCT.md`**

Replace `Work & Services carries the six real demos first` with `Work & Services carries the seven real cases first`. Replace `labels the six real demos and the three fictional case studies separately` with `labels the seven real cases and the three fictional case studies separately`. Replace the Work & Services sentence in the Capabilities bullet with `Work & Services lists six real demo links, one Web Scraping code link, and three fictional case studies.` Add this owner-directed bullet before `## Capabilities and Constraints`:

```markdown
- Add the Web Scraping Portfolio as one real case with a single link to the owner's `web-scraping-portfolio` repo, covering the five scraper examples and the small business and company use cases from its README.
```

Keep `demos/` statements, contact details, dials, and every other count unchanged.

- [ ] **Step 2: Update `README.md`**

Replace `with six real demos before three fictional case studies` with `with seven real cases before three fictional case studies`. Replace the Work & Services bullet with `- Work & Services: seven real cases under `REAL CASES / LIVE DEMOS`, six demo links plus one Web Scraping code link, then three fictional case studies under `FICTIONAL CASE STUDIES`, then the CAPABILITIES modules.` Replace the sentence before the link list with `The six demo links and one Web Scraping code link sit under `REAL CASES / LIVE DEMOS`, ahead of the three fictional case studies under `FICTIONAL CASE STUDIES`:` Add this list item after the NIGHT//SHIFT item:

```markdown
- Web Scraping Portfolio → `https://github.com/zhahenza44/web-scraping-portfolio`
```

- [ ] **Step 3: Final verification**

Run: `python3 -m unittest discover -s tests 2>&1 | tail -4`, `python3 tests/browser_smoke.py 2>&1 | tail -1`, `git diff --check`, and `git diff --stat -- demos`.
Expected: `Ran 40 tests ... OK`, `checks=161 failed=0`, no diff-check output, and an empty demos diff.

- [ ] **Step 4: Commit**

```bash
git add PRODUCT.md README.md
git commit -m "docs: record Web Scraping real case"
```

- [ ] **Step 5: Independent review**

Run a fresh reviewer over `origin/master..HEAD` with the spec, plan, and ledger in scope. Address any Critical or Important finding before pushing. Record any declined judgment or deferral in the ledger.

- [ ] **Step 6: Push and confirm**

```bash
git push origin master
```

Confirm `local=remote` with `git rev-parse HEAD` and `git ls-remote origin refs/heads/master | cut -f1`, and confirm a clean working tree with `git status --short --branch`. The owner asked for a direct push to `origin/master`, so do not create a branch, merge, or pull request.
