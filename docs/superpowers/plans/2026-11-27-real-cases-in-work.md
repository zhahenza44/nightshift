# Real Cases in Work & Services Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Move the six real demos out of the CV and into Work & Services, ahead of the fictional cases, with both case groups clearly labeled.

**Architecture:** One HTML move, one CSS selector rename plus small spacing rule, then matching test and documentation updates. No JavaScript changes. The six demo items move verbatim, so links and disclosure text stay intact.

**Tech Stack:** Static HTML, CSS, vanilla JavaScript, Python unit checks, Firefox rendered smoke script.

**Spec:** `docs/superpowers/specs/2026-11-27-real-cases-in-work-design.md`

## Global Constraints

- All visitor-facing copy stays English.
- Keep the NIGHT//SHIFT brand, the real CV section, and the fictional showcase disclosures.
- Keep `Response <24h`, the terminal line, and the contact copy unchanged.
- Every demo title, description, tag, href, `target="_blank"`, and `rel="noopener noreferrer"` stays verbatim.
- Keep every file inside `demos/` unchanged.
- The rendered smoke suite must stay green at 390px, 320px, reduced motion, and 1366px with `failed=0`.
- Push to `origin/master` only after the owner answers yes.

## Review Focus

1. A reader must not see the same demo list twice. Pinned in Task 1 by `test_real_cases_move_into_work` and the rendered `CV holds no demo list` check.
2. The groups must read real, then fictional, then CAPABILITIES. Pinned in Task 1 by `case groups are labeled and ordered`.
3. All six links must keep their exact hrefs and new-tab behavior after the move. Pinned in Task 1 by `six real demo links are visible` and the renamed `six real demo links open in a new tab`.
4. The fictional disclosure must survive the move. Pinned in Task 1 by the unchanged `This section is my real CV` static marker and the `cv note separates real CV from fictional case files` rendered check.
5. Adding a block to `#work` must not create overflow or a wide empty band at 320px, 390px, or 1366px. Pinned in Task 1 by `real case list fits 320px`, `1366px work bottom padding stays compact`, and the full existing smoke suite.

---

### Task 1: Pin the new case-group structure with failing tests

**Files:**
- Test: `tests/test_portfolio.py:101-118`, `tests/test_portfolio.py:242-269`, `tests/test_portfolio.py:333-335`
- Test: `tests/browser_smoke.py:384-392`, `tests/browser_smoke.py:414-416`, `tests/browser_smoke.py:502-509`, `tests/browser_smoke.py:637-643`

**Interfaces:**
- Consumes: the current `.cv-demo-list` markup in `#cv`, the `#work` section head, `.section-label` texts, and the `check(name, pass, detail)` helper.
- Produces: tests that require `#work .real-case-list`, the two group labels in order, no demo links inside `#cv`, and all six real demo links visible.

- [ ] **Step 1: Add the failing static assertions**

In `tests/test_portfolio.py`:
- In `test_sections_and_disclosure_are_english`, replace the marker `"Three fictional case studies"` with `"Six real demos and three fictional case studies"`.
- Add a new method:

```python
    def test_real_cases_move_into_work(self):
        for marker in (
            '>REAL CASES / LIVE DEMOS</span>',
            '>FICTIONAL CASE STUDIES</span>',
            '06 REAL / 03 FICTIONAL / 04 MODULES',
            'CV / PROFILE',
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, HTML)
        for phrase in ('CV / SIX DEMOS', '03 FILES / 04 MODULES', 'class="cv-demo-list"'):
            with self.subTest(absent=phrase):
                self.assertNotIn(phrase, HTML)
        cv_block = re.search(r'<section[^>]+id="cv".*?</section>', HTML, re.S).group(0)
        work_block = re.search(r'<section[^>]+id="work".*?</section>', HTML, re.S).group(0)
        self.assertNotIn('href="demos/', cv_block)
        self.assertEqual(work_block.count('href="demos/'), 6)
```

- In `test_cv_demo_links`, keep the existing href, name, target, and rel assertions unchanged.
- In the CSS parity test at line 333, replace `".cv-demo-list"` with `".real-case-list"`.

- [ ] **Step 2: Run the static suite and verify RED**

Run: `python3 -m unittest discover -s tests`
Expected: failures in `test_real_cases_move_into_work`, `test_sections_and_disclosure_are_english`, and the CSS parity test.

- [ ] **Step 3: Add the failing rendered checks**

In `tests/browser_smoke.py`, `NORMAL_SCRIPT_B`, replace the `CV demo links are visible` block with:

```js
      const realDemoAnchors = Array.from(doc.querySelectorAll('#work .real-case-list a'));
      check('six real demo links are visible',
        realDemoAnchors.length === 6 && realDemoAnchors.every((link) => {
          const rect = link.getBoundingClientRect();
          return rect.width > 0 && rect.height > 0;
        }), 'visible=' + realDemoAnchors.filter((link) => {
          const rect = link.getBoundingClientRect();
          return rect.width > 0 && rect.height > 0;
        }).length + '/6');
      check('CV holds no demo list',
        doc.querySelectorAll('#cv a[href^="demos/"]').length === 0 &&
          !doc.querySelector('#cv .real-case-list'),
        'cvDemoLinks=' + doc.querySelectorAll('#cv a[href^="demos/"]').length);
      const workLabels = Array.from(doc.querySelectorAll('#work .section-label'))
        .map((el) => el.textContent.trim());
      const realIndex = workLabels.indexOf('REAL CASES / LIVE DEMOS');
      const fictionalIndex = workLabels.indexOf('FICTIONAL CASE STUDIES');
      const capabilitiesIndex = workLabels.indexOf('CAPABILITIES');
      check('case groups are labeled and ordered',
        realIndex > -1 && fictionalIndex > realIndex && capabilitiesIndex > fictionalIndex,
        workLabels.join(' | '));
```

Also rename the check `six CV demo links open in a new tab` to `six real demo links open in a new tab` and change its selector from `a[href^="demos/"]` to `#work .real-case-list a`. Keep its assertions and detail unchanged.

In `NARROW_SCRIPT`, replace lines 502-509 with:

```js
      const cvBlocks = [doc.querySelector('.cv-grid')];
      check('cv section fits 320px', cvBlocks.every(Boolean) && cvBlocks.every((el) => {
        const rect = el.getBoundingClientRect();
        return rect.left >= -1 && rect.right <= 321;
      }), cvBlocks.filter(Boolean).map((el) => {
        const rect = el.getBoundingClientRect();
        return Math.round(rect.left) + '..' + Math.round(rect.right);
      }).join(' | ') || 'missing');
      const realList320 = doc.querySelector('#work .real-case-list');
      const realRect320 = realList320 ? realList320.getBoundingClientRect() : null;
      check('real case list fits 320px',
        Boolean(realRect320) && realRect320.left >= -1 && realRect320.right <= 321,
        realRect320 ? Math.round(realRect320.left) + '..' + Math.round(realRect320.right) : 'missing');
```

In the 1366px pass, replace the `content` array with `['#cv .section-head', '#cv .cv-grid', '#work .real-case-list']` and rename the check to `CV and real case content stays visible`. Keep its visibility assertion and detail unchanged.

- [ ] **Step 4: Run the smoke suite and verify RED**

Run: `python3 tests/browser_smoke.py | grep -E 'CHECK FAIL|checks='`
Expected: failures for `six real demo links are visible`, `CV holds no demo list`, `case groups are labeled and ordered`, `six real demo links open in a new tab`, `real case list fits 320px`, and `CV and real case content stays visible`. Other checks stay green.

- [ ] **Step 5: Commit RED**

```bash
git add tests/test_portfolio.py tests/browser_smoke.py
git commit --no-verify -m "test: pin real cases in Work and Services"
```

Use `--no-verify` because the hook runs both suites and this commit is intentionally red.

---

### Task 2: Move the six demos and relabel the case groups

**Files:**
- Modify: `index.html:226`, `index.html:259-308`, `index.html:318`, `index.html:324`, `index.html:327-328`
- Modify: `css/styles.css:3507-3555`

**Interfaces:**
- Consumes: the six existing `<li>` items from `.cv-demo-list` and the `.section-head` pattern at `css/styles.css:1501-1506`.
- Produces: `#work .real-case-list` with six verbatim demo items, `#work .section-label` values `REAL CASES / LIVE DEMOS`, `FICTIONAL CASE STUDIES`, and `CAPABILITIES` in that order, and no demo link inside `#cv`.

- [ ] **Step 1: Move the demo list out of the CV**

Delete `<ul class="cv-demo-list">` and its six `<li>` children from `index.html:259-308`. Change `CV / SIX DEMOS` to `CV / PROFILE` at line 226. Leave the CV contact links, both `.cv-service` articles, and the note `This section is my real CV. The case studies below are fictional.` unchanged.

- [ ] **Step 2: Insert the real and fictional group heads in Work & Services**

Change the `#work` section meta at line 318 to `06 REAL / 03 FICTIONAL / 04 MODULES`. Change the work intro paragraph at line 324 to `Six real demos and three fictional case studies show how we think, design, and build.`

Directly after the `.work-intro` closing `</div>` at line 327, insert the real group head:

```html
        <div class="section-head case-group-head reveal">
          <span class="section-label">REAL CASES / LIVE DEMOS</span>
          <span class="section-line"></span>
          <span class="section-meta">06 DEMOS / REAL WORK</span>
        </div>
```

Follow it with `<ul class="real-case-list">`, then the six `<li>...</li>` blocks copied verbatim from the old `.cv-demo-list`, then `</ul>`. Do not alter any demo title, description, tag, href, `target`, or `rel`.

After that list, insert the fictional group head:

```html
        <div class="section-head case-group-head reveal">
          <span class="section-label">FICTIONAL CASE STUDIES</span>
          <span class="section-line"></span>
          <span class="section-meta">03 FILES / SHOWCASE</span>
        </div>
```

The existing `.project-stack` follows that fictional head.

- [ ] **Step 3: Rename and adjust the CSS**

In `css/styles.css:3507-3555`, rename every `.cv-demo-list` selector to `.real-case-list`, including the 860px rule. Change that list's `margin-top` from `clamp(36px, 5vw, 72px)` to `clamp(24px, 3vw, 40px)`. Add this rule after the renamed list rules and before `.services-block`:

```css
.case-group-head {
  margin-bottom: clamp(24px, 3vw, 40px);
}
```

Leave `.section-head`, `.services-block .section-head`, and all demo selectors unchanged.

- [ ] **Step 4: Run the full verification**

Run: `python3 -m unittest discover -s tests && python3 tests/browser_smoke.py | tail -1 && git diff --stat -- demos && git diff --check`
Expected: unit `OK`, smoke `failed=0`, empty `demos/` diff, no whitespace errors.

- [ ] **Step 5: Commit GREEN**

```bash
git add index.html css/styles.css
git commit -m "feat: move real demos into Work and Services"
```

The pre-commit hook must pass on this commit.

---

### Task 3: Record the decision and ask before shipping

**Files:**
- Modify: `PRODUCT.md:19`, `PRODUCT.md:23`, `PRODUCT.md:68-73`, `PRODUCT.md:98`
- Modify: `README.md:3`, `README.md:6`, `README.md:47`, `README.md:49-58`

**Interfaces:**
- Consumes: the final DOM from Task 2.
- Produces: owner-facing docs that place the six demos in Work & Services and keep the fictional disclosure accurate.

- [ ] **Step 1: Update PRODUCT.md**

- In the Product Purpose paragraph, state that the CV carries real identity, services, and contact channels, while Work & Services carries the six real demos and the disclosed fictional case studies.
- In the Positioning paragraph, state that Work & Services labels real cases and fictional cases separately, with real cases first.
- In Capabilities and Constraints, describe the CSS as keeping the demo selectors except the narrow hero-foot rule and the scroll-cue alignment rule, and rename the demo-list rules to `.real-case-list`.
- Replace the bullet `The CV lists two services, six demo links, and three real contact channels.` with one that gives two services and three contacts to the CV, and six demo links plus three fictional case studies to Work & Services.
- In Product Principles, add that real demo links sit in Work & Services and stay labeled separately from the fictional cases.

- [ ] **Step 2: Update README.md**

- In the opening description, move the six demo links from the CV section to Work & Services and say the real cases come before the fictional ones.
- In the file-structure paragraph, replace the CV demo-list wording with the `.real-case-list` rules in the Work block.
- In "The CV section", leave identity, services, and contacts in the CV, then add a short "Work & Services" list of the same six demos with their unchanged paths.

- [ ] **Step 3: Verify the final state**

Run: `python3 -m unittest discover -s tests && python3 tests/browser_smoke.py | tail -1 && git diff --stat -- demos && git diff --check && git status --short --branch`
Expected: unit `OK`, smoke `failed=0`, empty `demos/` diff, no whitespace errors, clean tree except the new commits.

- [ ] **Step 4: Commit the docs**

```bash
git add PRODUCT.md README.md
git commit -m "docs: record real cases in Work and Services"
```

- [ ] **Step 5: Ask before shipping**

Report the verification evidence and ask the owner whether to push `master` to `origin/master`. Do not push without that answer.
