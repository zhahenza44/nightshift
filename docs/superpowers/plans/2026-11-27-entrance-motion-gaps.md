# Entrance Motion Gaps Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add entrance motion to the six elements that still arrive flat, using the page's existing reveal and magnetic systems.

**Architecture:** Static HTML gains `reveal` classes and `--delay` values. CSS adds small hover rules and one reduced-motion override. The existing IntersectionObserver and `$$(".magnetic")` loop handle behavior, so no new script or keyframe is needed.

**Tech Stack:** Static HTML, CSS, vanilla JS, Python unittest, Firefox WebDriver BiDi smoke script.

**Spec:** `docs/superpowers/specs/2026-11-27-entrance-motion-gaps-design.md`

## Global Constraints

- All visitor-facing copy stays English.
- Real cases come first, then fictional cases, then CAPABILITIES.
- `This section is my real CV. The case studies below are fictional.` stays verbatim.
- `Response <24h`, the terminal line, and contact copy stay verbatim.
- No file inside `demos/` changes. `git diff --stat -- demos` stays empty.
- `prefers-reduced-motion: reduce` keeps all new motion quiet. No-JS fallback stays visible.
- Design dials stay ENERGY 3 / RHYTHM 3 / MOTION 3.
- Unit tests and rendered smoke stay green at 390px, 320px, reduced motion, and 1366px.
- Push to `origin/master` only after explicit owner approval. Work stays on `master` with no branch, merge, or PR.

## Review Focus

1. A hover transform on a real-case row must not fight `.js .reveal.is-in`. Pinned in Task 1 by the static selector requiring the transform on the inner `div`, not the `li`.
2. Reduced motion must leave the new hover offsets and the two new magnetic buttons quiet. Pinned in Task 1 by the static reduced-motion markers and the rendered `reduced motion leaves contact magnets inert` check.
3. Adding reveal classes must not hide content or create overflow at 320px, 390px, or 1366px. Pinned in Task 1 by the rendered reveal-transition checks and the full existing smoke suite in Task 2.
4. Real and fictional groups, their labels, and the CV disclosure must stay unchanged. Pinned by the existing `case groups are labeled and ordered` and `cv note separates real CV from fictional case files` checks plus the new static markers.
5. Hero, boot, ghost cursor, manifesto word stagger, terminal, menu, dialog, and footer motion must stay untouched. Pinned by the full rendered suite and by leaving those files and selectors outside the change.

---

### Task 1: Pin the entrance motion contract

**Files:**
- Modify: `tests/test_portfolio.py`
- Modify: `tests/browser_smoke.py`

**Interfaces:**
- Consumes: the final DOM shape and CSS selectors described in the approved spec.
- Produces: failing static tests and rendered checks that Task 2 must satisfy.

- [ ] **Step 1: Add the static DOM test**

Add `test_entrance_motion_targets_are_marked` to `ContentTest` in `tests/test_portfolio.py`. Assert these exact markers appear in `HTML`:

```python
'<article class="project-card reveal" data-project="hypermart">'
'<article class="project-card project-card--reverse reveal" data-project="aegis" style="--delay:.08s">'
'<article class="project-card reveal" data-project="voidhotel" style="--delay:.16s">'
'class="reveal" href="https://instagram.com/zhahenzar" target="_blank" rel="noopener noreferrer" style="--delay:.08s"'
'class="reveal" href="https://github.com/zhahenza44" target="_blank" rel="noopener noreferrer" style="--delay:.16s"'
'class="reveal" href="mailto:zhahenza666@proton.me" style="--delay:.24s"'
'<a class="btn btn--ghost magnetic" id="send-message"'
'<a class="btn btn--ghost magnetic" href="https://github.com/zhahenza44/otomasi-web"'
```

Also assert `HTML.count('<li class="process-step reveal">') == 5` and `HTML.count('<li class="process-step">') == 0`.

- [ ] **Step 2: Add the static CSS test**

Add `test_entrance_motion_rules_exist` to `ContentTest`. Assert these markers appear in `CSS`:

```python
'.real-case-list > li:hover {'
'background-color: var(--bg-soft);'
'.real-case-list > li > div {'
'transition: transform 0.3s var(--ease-out);'
'.real-case-list > li:hover > div {'
'transform: translateY(-2px);'
'.real-case-list > li:hover a span {'
'transform: translateX(3px);'
```

Split `CSS` on `@media (prefers-reduced-motion: reduce) {` and assert the tail contains `.real-case-list > li:hover > div` and `transform: none;`.

- [ ] **Step 3: Add rendered normal-motion checks**

In `NORMAL_SCRIPT_B` of `tests/browser_smoke.py`, after the existing `case groups are labeled and ordered` check, add checks with these names and assertions:

```javascript
check('fictional case cards carry reveal class',
  doc.querySelectorAll('.project-card.reveal').length === 3,
  'cards=' + doc.querySelectorAll('.project-card.reveal').length);
check('fictional case cards use reveal transition',
  Array.from(doc.querySelectorAll('.project-card.reveal')).every((el) =>
    win.getComputedStyle(el).transitionProperty.includes('opacity')),
  Array.from(doc.querySelectorAll('.project-card.reveal')).map((el) =>
    win.getComputedStyle(el).transitionProperty).join(' | '));
check('process steps carry reveal class',
  doc.querySelectorAll('.process-step.reveal').length === 5,
  'steps=' + doc.querySelectorAll('.process-step.reveal').length);
check('CV contact links carry reveal class',
  doc.querySelectorAll('.cv-contact a.reveal').length === 3,
  'links=' + doc.querySelectorAll('.cv-contact a.reveal').length);
check('CV contact links use reveal transition',
  Array.from(doc.querySelectorAll('.cv-contact a.reveal')).every((el) =>
    win.getComputedStyle(el).transitionProperty.includes('transform')),
  Array.from(doc.querySelectorAll('.cv-contact a.reveal')).map((el) =>
    win.getComputedStyle(el).transitionProperty).join(' | '));
check('all three contact actions are magnetic',
  doc.querySelectorAll('.contact-actions .magnetic').length === 3,
  'magnetic=' + doc.querySelectorAll('.contact-actions .magnetic').length);
check('magnetic setup applies to all three',
  Array.from(doc.querySelectorAll('.contact-actions .magnetic')).every((el) =>
    el.style.transition.includes('transform')),
  Array.from(doc.querySelectorAll('.contact-actions .magnetic')).map((el) =>
    el.style.transition || 'none').join(' | '));
check('real case rows expose hover transform',
  Array.from(doc.querySelectorAll('.real-case-list > li > div')).every((el) =>
    win.getComputedStyle(el).transitionProperty.includes('transform')),
  Array.from(doc.querySelectorAll('.real-case-list > li > div')).map((el) =>
    win.getComputedStyle(el).transitionProperty).join(' | '));
```

- [ ] **Step 4: Add the reduced-motion check**

In `REDUCED_SCRIPT` of `tests/browser_smoke.py`, before the `reduced motion keeps content visible` check, add:

```javascript
check('reduced motion leaves contact magnets inert',
  Array.from(doc.querySelectorAll('.contact-actions .magnetic')).every((el) =>
    !el.style.transition),
  Array.from(doc.querySelectorAll('.contact-actions .magnetic')).map((el) =>
    el.style.transition || 'none').join(' | '));
```

- [ ] **Step 5: Verify RED**

Run:

```bash
python3 -m unittest discover -s tests
python3 tests/browser_smoke.py | tail -1
```

Expected: static suite `FAILED (failures=2)`, and rendered `checks=157 failed=8`. The eight rendered failures are the seven new normal-motion checks plus `real case rows expose hover transform`. No other check fails.

- [ ] **Step 6: Commit the tests**

```bash
git add tests/test_portfolio.py tests/browser_smoke.py
git commit -m "test: pin entrance motion gaps"
```

### Task 2: Add entrance motion in source

**Files:**
- Modify: `index.html:343-407`, `index.html:473-497`, `index.html:218-221`, `index.html:518-520`
- Modify: `css/styles.css:3515-3548`, `css/styles.css:3575-3621`

**Interfaces:**
- Consumes: the failing markers from Task 1.
- Produces: the DOM and CSS that make all Task 1 checks pass.

- [ ] **Step 1: Add reveal classes and delays in `index.html`**

Change the three `.project-card` articles to the exact markers pinned in Task 1. Change all five `<li class="process-step">` to `<li class="process-step reveal">`. Add `class="reveal"` and the pinned `--delay` values to the three `.cv-contact a` links without changing href, target, or rel. Add `magnetic` to the `Send message` and `GITHUB` anchor classes.

- [ ] **Step 2: Add hover rules and reduced-motion override in `css/styles.css`**

Give `.real-case-list > li > div` a `transition: transform 0.3s var(--ease-out);`. Add `.real-case-list > li:hover` with `background-color: var(--bg-soft);`, `.real-case-list > li:hover > div` with `transform: translateY(-2px);`, and `.real-case-list > li:hover a span` with `transform: translateX(3px);`. In the existing `prefers-reduced-motion` block, override the two new hover transforms to `transform: none;`. Do not put a transform on the `li` itself.

- [ ] **Step 3: Verify GREEN**

Run:

```bash
python3 -m unittest discover -s tests
python3 tests/browser_smoke.py | tail -1
git diff --stat -- demos
git diff --check
```

Expected: `Ran 38 tests ... OK`, `checks=157 failed=0`, empty `demos` diff, and no `git diff --check` output.

- [ ] **Step 4: Commit the source change**

```bash
git add index.html css/styles.css
git commit -m "feat: add entrance motion to remaining sections"
```

### Task 3: Record the motion in owner docs

**Files:**
- Modify: `PRODUCT.md`
- Modify: `README.md`

**Interfaces:**
- Consumes: the final DOM and CSS from Task 2.
- Produces: owner-facing docs that match the shipped motion.

- [ ] **Step 1: Update `PRODUCT.md`**

In the Capabilities and Constraints area, state that fictional case cards, CV contact links, and process steps use the existing reveal system; real-case rows have a hover lift; all three contact actions are magnetic; and reduced motion removes the new transforms. Keep the dials line unchanged.

- [ ] **Step 2: Update `README.md`**

In the page description or feature list, name the new entrance motion in one sentence. Keep the real and fictional separation and contact copy unchanged.

- [ ] **Step 3: Verify GREEN**

Run:

```bash
python3 -m unittest discover -s tests
python3 tests/browser_smoke.py | tail -1
git diff --stat -- demos
git diff --check
git status --short --branch
```

Expected: `OK`, `checks=157 failed=0`, empty `demos` diff, clean `git diff --check`, and a clean working tree after the commit.

- [ ] **Step 4: Commit the docs**

```bash
git add PRODUCT.md README.md
git commit -m "docs: record entrance motion additions"
```
