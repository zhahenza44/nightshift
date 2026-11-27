# Header and Hero Foot Location Cleanup Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove `SURABAYA, ID` from the header brand block and the hero foot row without changing any other visible copy or layout.

**Architecture:** Two direct text-node deletions in `index.html`, one CSS selector change that preserves the existing 320px hiding rule, then matching test and documentation updates. No JavaScript changes.

**Tech Stack:** Static HTML, CSS, vanilla JavaScript, Python unit checks, Firefox rendered smoke script.

**Spec:** `docs/superpowers/specs/2026-11-27-header-hero-foot-location-design.md`

## Global Constraints

- All visitor-facing copy is English.
- Keep `Response <24h`, the terminal line, and the contact copy unchanged.
- Keep the NIGHT//SHIFT brand, the real CV section, and the fictional showcase disclosures.
- Keep every file inside `demos/` unchanged.
- The rendered smoke suite must stay green at 390px, 320px, reduced motion, and 1366px with `failed=0`.
- Push to `origin/master` only after the owner answers yes.

## Review Focus

1. At 320px, `SIGNAL 98.2%` must stay hidden after the sibling span is deleted. Pinned in Task 1 by the `320px signal stays hidden` rendered check.
2. The header brand block must keep `DIGITAL STUDIO` as its only text. Pinned in Task 1 by the exact static marker and the `header and hero foot omit Surabaya` rendered check.
3. `SURABAYA, ID` must remain in the mobile menu, CV base, and terminal. Pinned in Task 1 by the three retained static markers and the existing `location is Surabaya` rendered check.
4. The hero foot must keep its padding, border, and scroll cue. Pinned in Task 1 by the `hero foot keeps its remaining copy` rendered check plus the existing 320px overflow check.
5. Contact actions and reduced motion must not regress. Pinned in Task 1 by running the full existing smoke suite, which covers the DM box, the phone action row, focus, and reduced motion.

---

### Task 1: Remove the two labels and preserve the 320px state

**Files:**
- Modify: `index.html:49`, `index.html:159-163`
- Modify: `css/styles.css:3258-3260`
- Test: `tests/test_portfolio.py:196-210`, `tests/browser_smoke.py` in `NORMAL_SCRIPT_B` after the `location is Surabaya` check and in `NARROW_SCRIPT`

**Interfaces:**
- Consumes: `.brand-meta`, `.hero-foot`, the two `.hero-foot .mono` spans, the narrow-width rule at `css/styles.css:3258`, and the `check(name, pass, detail)` helper in both smoke scripts.
- Produces: brand meta text exactly `DIGITAL STUDIO`; hero foot with one mono span carrying `SIGNAL 98.2%` and one `.scroll-cue`; no `SURABAYA` text in header or hero foot; the remaining mono span hidden at 320px.

- [ ] **Step 1: Write the failing static assertions**

In `tests/test_portfolio.py`, method `ContentTest.test_surabaya_and_github_label`:
- Replace marker `'DIGITAL STUDIO<br>SURABAYA, ID'` with `'<span class="brand-meta">DIGITAL STUDIO</span>'`.
- Delete marker `'<span class="mono">SURABAYA, ID</span>'`.
- Add the two old strings to the existing absent-phrase tuple:
  `'DIGITAL STUDIO<br>SURABAYA, ID'` and `'<span class="mono">SURABAYA, ID</span>'`.
- Keep the other present markers unchanged, including `'<span>SURABAYA, ID</span>'`, `'<dd>Surabaya, ID</dd>'`, the lowercase terminal key, and `'<div class="terminal-foot"><span>SURABAYA, ID</span>'`.

- [ ] **Step 2: Run the static suite and verify RED**

Run: `python3 -m unittest discover -s tests`
Expected: failures in `test_surabaya_and_github_label` for the new brand marker and the two newly absent phrases.

- [ ] **Step 3: Write the failing rendered checks**

In `tests/browser_smoke.py`, `NORMAL_SCRIPT_B`, after the `location is Surabaya` check, add:

```js
const brandMeta = doc.querySelector('.brand-meta');
const heroFoot = doc.querySelector('.hero-foot');
check('header and hero foot omit Surabaya',
  Boolean(brandMeta) && Boolean(heroFoot) &&
    brandMeta.textContent.trim() === 'DIGITAL STUDIO' &&
    !brandMeta.textContent.includes('SURABAYA') &&
    !heroFoot.textContent.includes('SURABAYA'),
  (brandMeta ? brandMeta.textContent.trim() : 'missing') + ' | ' +
    (heroFoot ? heroFoot.textContent.trim() : 'missing'));
const scrollCue = heroFoot ? heroFoot.querySelector('.scroll-cue') : null;
check('hero foot keeps its remaining copy',
  Boolean(heroFoot) && heroFoot.textContent.includes('SIGNAL 98.2%') &&
    Boolean(scrollCue) && scrollCue.textContent.includes('SCROLL TO EXPLORE'),
  heroFoot ? heroFoot.textContent.trim() : 'missing');
```

In `NARROW_SCRIPT`, after the `320px has no horizontal overflow` check, add:

```js
const narrowFoot = doc.querySelector('.hero-foot');
const narrowMono = narrowFoot ? narrowFoot.querySelector('.mono') : null;
check('320px signal stays hidden',
  Boolean(narrowFoot) && Boolean(narrowMono) &&
    win.getComputedStyle(narrowMono).display === 'none' &&
    !narrowFoot.textContent.includes('SURABAYA'),
  narrowMono ? 'display=' + win.getComputedStyle(narrowMono).display : 'missing');
```

- [ ] **Step 4: Run the smoke suite and verify RED**

Run: `python3 tests/browser_smoke.py | grep -E 'CHECK FAIL|checks='`
Expected: the three new checks fail; the other checks stay green.

- [ ] **Step 5: Commit RED**

```bash
git add tests/test_portfolio.py tests/browser_smoke.py
git commit --no-verify -m "test: pin location removal in header and hero foot"
```

Use `--no-verify` because the pre-commit hook runs both suites and this commit is intentionally red.

- [ ] **Step 6: Remove the text in `index.html`**

At line 49, replace `<span class="brand-meta">DIGITAL STUDIO<br>SURABAYA, ID</span>` with `<span class="brand-meta">DIGITAL STUDIO</span>`. In `.hero-foot`, delete the line `<span class="mono">SURABAYA, ID</span>`. Leave `SIGNAL 98.2%`, the scroll cue, and every other Surabaya label untouched.

- [ ] **Step 7: Preserve the 320px rule in `css/styles.css`**

Replace the selector `.hero-foot .mono:nth-child(2)` on line 3258 with `.hero-foot .mono`. Keep the rule body `display: none` and its media query unchanged.

- [ ] **Step 8: Run the full verification**

Run: `python3 -m unittest discover -s tests && python3 tests/browser_smoke.py | tail -1 && git diff --stat -- demos`
Expected: unit `OK`, smoke `failed=0`, and an empty `demos/` diff.

- [ ] **Step 9: Commit GREEN**

```bash
git add index.html css/styles.css
git commit -m "feat: remove Surabaya label from header and hero foot"
```

The pre-commit hook must pass on this commit.

---

### Task 2: Record the decision and ask before shipping

**Files:**
- Modify: `PRODUCT.md:40`, after `PRODUCT.md:40`
- Modify: `README.md:3`

**Interfaces:**
- Consumes: the final DOM and CSS from Task 1.
- Produces: owner-facing docs that no longer credit the header or hero foot with a location label.

- [ ] **Step 1: Update `PRODUCT.md`**

Replace the decision at line 40 with: `- Set visitor-facing location labels to Surabaya, ID in the mobile menu, CV base, and terminal; do not show a location label in the header or hero foot.` Add one decision bullet directly after it: `- Remove the \`SURABAYA, ID\` label from the header brand block and the hero foot row, keeping \`DIGITAL STUDIO\`, \`SIGNAL 98.2%\`, and \`SCROLL TO EXPLORE\` in place.`

- [ ] **Step 2: Update `README.md`**

In the opening description, replace `and the studio location reads Surabaya, ID` with `and the studio location reads Surabaya, ID in the menu, CV, and terminal, but not in the header or hero foot`.

- [ ] **Step 3: Verify the final state**

Run: `python3 -m unittest discover -s tests && python3 tests/browser_smoke.py | tail -1 && git diff --stat -- demos && git diff --check && git status --short --branch`
Expected: unit `OK`, smoke `failed=0`, empty `demos/` diff, no whitespace errors, clean tree except the new commits.

- [ ] **Step 4: Commit the docs**

```bash
git add PRODUCT.md README.md
git commit -m "docs: record header and hero foot location cleanup"
```

- [ ] **Step 5: Ask before shipping**

Report the verification evidence and ask the owner whether to push `master` to `origin/master`. Do not push without that answer.
