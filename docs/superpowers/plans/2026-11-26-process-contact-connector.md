# Process contact connector implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Extend the neon process rail into the contact panel border and change the five process step numbers to Roman numerals.

**Architecture:** The process section already stops with zero bottom padding exactly where the contact panel starts. The scroll handler writes a percentage height to `#process-fill`; a pseudo-element on that fill spans the remaining seam, so the existing progress math and the existing smoke contract stay intact. The step numbers are static HTML text, so they change in `index.html` only.

**Tech Stack:** Static HTML, CSS, vanilla JavaScript, Python unit tests, Firefox BiDi rendered smoke script.

**Spec:** `docs/superpowers/specs/2026-11-26-process-contact-connector-design.md`

## Global Constraints

- All visitor-facing copy stays English and unchanged apart from the five step markers.
- The rail stays one straight vertical line. No bend, no diamond, no new label.
- Section indices `04` and `05`, both navigation lists, the CV section, contact copy, and `demos/` stay unchanged.
- `#process-fill.style.height` stays a percentage from the existing `progress * 100` calculation; `tests/browser_smoke.py` parses it with `Number.parseFloat`.
- `#process.section` and `#contact.section` keep zero vertical padding, so the list bottom meets the panel top.
- The rail keeps its x position at every breakpoint. Smoke runs at 390px, 320px, and 1366px; the process grid changes at 980px.
- Reduced motion behavior stays as it is; the existing reduced-motion smoke pass must remain green.
- Work stays inline on `master`, RED to GREEN to docs, one commit per task. `demos/` diff stays empty.
- The pre-commit hook requires green tests, so RED commits use `git commit --no-verify`. GREEN and docs commits run the hook normally.

## Review Focus

- Full scroll progress could still leave a one-pixel break at the seam. The connector rendered check scrolls past the 100% point and compares the connector bottom with `.contact-panel` top at 390px, 320px, and 1366px.
- A CSS change could alter the progress output that existing smoke reads. The connector rendered check keeps `Number.parseFloat(fill.style.height)` and adds a full-progress assertion beside the existing `process fill advances` check.
- The 980px grid change could move the rail outside the panel. The connector rendered check asserts the fill x sits between the panel left and right at all three smoke widths.
- The contact panel could paint over the seam. The connector rendered check asserts `.process-fill` has `z-index: 1`.
- Roman numerals could leak into the section or navigation numbers. The unit test reads only `.step-no` inside `.process-list`; the existing navigation test still pins two `04` links and two `05` links.

---

### Task 1: Fail on Arabic step markers

**Files:**
- Modify: `tests/test_portfolio.py`
- Modify: `tests/browser_smoke.py` at `NORMAL_SCRIPT_A`, after the `process steps activate on scroll` check

**Interfaces:**
- Consumes: the five existing `<span class="step-no">` elements inside `#process-list`.
- Produces: failing assertions named `test_process_step_numbers_are_roman` and `process step numbers are roman`. No production code changes in this task.

- [x] **Step 1: Write the failing tests**

In `tests/test_portfolio.py`, add:

```python
class ProcessContactTest(unittest.TestCase):
    def test_process_step_numbers_are_roman(self):
        block = re.search(r'<ol class="process-list" id="process-list">.*?</ol>', HTML, re.S)
        self.assertIsNotNone(block)
        numbers = re.findall(r'<span class="step-no">([^<]+)</span>', block.group(0))
        self.assertEqual(numbers, ["I", "II", "III", "IV", "V"])
        nav_numbers = re.findall(r'<a href="#(?:process|contact)"><span>(\d+)</span>', HTML)
        self.assertEqual(nav_numbers, ["04", "05", "04", "05"])
```

In `NORMAL_SCRIPT_A`, add:

```javascript
      const stepNumbers = Array.from(doc.querySelectorAll('.step-no'))
        .map((el) => el.textContent.trim()).join(',');
      check('process step numbers are roman', stepNumbers === 'I,II,III,IV,V', stepNumbers);
```

- [x] **Step 2: Run the tests and verify they fail**

Run: `python3 -m unittest tests.test_portfolio.ProcessContactTest.test_process_step_numbers_are_roman -v`
Expected: FAIL on `['01', '02', '03', '04', '05'] != ['I', 'II', 'III', 'IV', 'V']`.

Run: `python3 tests/browser_smoke.py`
Expected: FAIL on `process step numbers are roman :: 01,02,03,04,05`.

- [x] **Step 3: Commit the RED test**

```bash
git add tests/test_portfolio.py tests/browser_smoke.py
git commit --no-verify -m "test: pin roman process step numbers"
```

### Task 2: Switch step markers to Roman numerals

**Files:**
- Modify: `index.html:459-486`

**Interfaces:**
- Consumes: the two failing assertions from Task 1.
- Produces: `.step-no` text `I`, `II`, `III`, `IV`, `V` in document order. No other number changes.

- [x] **Step 1: Change the five step markers**

Replace only the five `.step-no` values in order: `01` to `I`, `02` to `II`, `03` to `III`, `04` to `IV`, `05` to `V`. Leave the `<ol>`, step copy, step times, section indices, and navigation untouched.

- [x] **Step 2: Run the tests and verify they pass**

Run: `python3 -m unittest tests.test_portfolio.ProcessContactTest.test_process_step_numbers_are_roman -v`
Expected: PASS.

Run: `python3 tests/browser_smoke.py | tail -3`
Expected: the `process step numbers are roman` check PASS and `failed=0`.

- [x] **Step 3: Commit the GREEN change**

```bash
git add index.html
git commit -m "feat: use roman process step numbers"
```

### Task 3: Fail on the missing seam connector

**Files:**
- Modify: `tests/browser_smoke.py` (add `CONNECTOR_SCRIPT`, add three entries to the main check loop)

**Interfaces:**
- Consumes: the inline height that `js/main.js:181-193` writes to `#process-fill`, and the top border of `.contact-panel`.
- Produces: failing rendered checks named with the viewport prefix. No production code changes in this task.

- [x] **Step 1: Add the rendered contract**

Add this `CONNECTOR_SCRIPT` beside the other script constants:

```javascript
CONNECTOR_SCRIPT = r"""
new Promise((resolve) => {
  const frame = document.getElementById('frame');
  const checks = [];
  const check = (name, pass, detail) => checks.push({name, pass: Boolean(pass), detail});
  const wait = (ms) => new Promise((done) => setTimeout(done, ms));
  let label = '';
  (async () => {
    try {
      if (!(frame.contentDocument && frame.contentDocument.readyState === 'complete')) {
        await new Promise((done) => frame.addEventListener('load', done, {once: true}));
      }
      await wait(2400);
      const win = frame.contentWindow;
      const doc = win.document;
      const list = doc.getElementById('process-list');
      const fill = doc.getElementById('process-fill');
      const panel = doc.querySelector('.contact-panel');
      win.scrollTo({top: 0, behavior: 'instant'});
      win.dispatchEvent(new win.Event('scroll'));
      await wait(80);
      const initialComplete = fill.classList.contains('is-complete');
      const initialClass = fill.className;
      fill.style.transition = 'none';
      const scrollTarget = list.getBoundingClientRect().bottom + win.scrollY -
        win.innerHeight * 0.58 + 2;
      win.scrollTo({top: scrollTarget, behavior: 'instant'});
      win.dispatchEvent(new win.Event('scroll'));
      for (let i = 0; i < 50; i += 1) {
        if (Number.parseFloat(fill.style.height) > 99.9) break;
        await wait(20);
      }

      label = win.innerWidth + 'px ';
      const progress = Number.parseFloat(fill.style.height);
      const fillRect = fill.getBoundingClientRect();
      const panelRect = panel.getBoundingClientRect();
      const after = win.getComputedStyle(fill, '::after');
      const afterHeight = Number.parseFloat(after.height);
      const afterBottom = Number.parseFloat(after.bottom);
      const exists = after.content !== 'none' && Number.isFinite(afterHeight) && Number.isFinite(afterBottom);
      const connectorBottom = fillRect.bottom - afterBottom;
      const fillStyle = win.getComputedStyle(fill);

      check(label + 'process connector class absent before rail completes', !initialComplete,
        'class=' + initialClass);
      check(label + 'process fill reaches full progress', progress > 99.9, 'height=' + fill.style.height);
      check(label + 'process connector waits for rail completion',
        fill.classList.contains('is-complete') && exists, 'class=' + fill.className);
      check(label + 'process connector exists', exists, 'content=' + after.content);
      check(label + 'process connector spans seam', exists && afterHeight === 2 && afterBottom === -1,
        'height=' + afterHeight + ' bottom=' + afterBottom);
      check(label + 'process connector lands on panel top',
        exists && Math.abs(connectorBottom - panelRect.top) <= 1.01,
        'connector=' + connectorBottom.toFixed(3) + ' panel=' + panelRect.top.toFixed(3));
      check(label + 'process connector stays inside panel width',
        fillRect.left > panelRect.left && fillRect.left < panelRect.right,
        'x=' + Math.round(fillRect.left) + ' panel=' + Math.round(panelRect.left) + '..' + Math.round(panelRect.right));
      check(label + 'process fill paints above contact panel', fillStyle.zIndex === '1', fillStyle.zIndex);
      const gradientColors = fillStyle.backgroundImage.match(/rgba?\([^)]+\)/g) || [];
      const endColor = gradientColors[gradientColors.length - 1] || '';
      check(label + 'process connector keeps terminal color',
        exists && after.backgroundImage === 'none' && after.backgroundColor === endColor,
        'seam=' + after.backgroundColor + ' gradientEnd=' + endColor + ' image=' + after.backgroundImage);

      resolve(checks);
    } catch (error) {
      resolve([{name: label + 'connector pass runs', pass: false,
        detail: String((error && error.stack) || error)}]);
    }
  })();
})
"""
```

Execution ruling: a fixed 250ms wait sampled the 0.15s height transition and an exact 1px float compare flaked at 1366px. The test disables the transition inside the iframe, polls the inline height, and allows 1.01px for floating-point rounding. A later review added the completion gate: the test scrolls back to the top before sampling, and checks the `is-complete` class because Firefox reports `content: none` and `display: none` unreliably on a non-generated pseudo-element.

Add the script to `main()` with these three exact tuple entries:

```python
        (url, CONNECTOR_SCRIPT, False, None),
        (narrow_url, CONNECTOR_SCRIPT, False, None),
        (wide_url, CONNECTOR_SCRIPT, False, None),
```

- [x] **Step 2: Run the test and verify it fails**

Run: `python3 tests/browser_smoke.py`
Expected: FAIL on `390px process connector exists`, `390px process connector spans seam`, `320px process fill paints above contact panel`, `1366px process connector keeps neon gradient`, and their matching checks at the other two widths. The progress, lands-on-panel, and width checks may pass because the fill already reaches the panel top; the missing pseudo-element and z-index must still fail the run.

- [x] **Step 3: Commit the RED test**

```bash
git add tests/browser_smoke.py
git commit --no-verify -m "test: pin process rail seam connection"
```

### Task 4: Extend the rail into the contact frame

**Files:**
- Modify: `css/styles.css:2383-2392`
- Modify: `js/main.js:187` (final review fix)

**Interfaces:**
- Consumes: the failing checks from Task 3 and the unchanged inline height output.
- Produces: `.process-fill::after`, a 2px tall continuation whose bottom edge is 1px below the fill, plus `z-index: 1` on the fill. The final review fix toggles `is-complete` from `updateProcess()` so the 2px extension appears only when the rail reaches the contact panel.

- [x] **Step 1: Extend the rail in CSS**

In `css/styles.css`, add `z-index: 1;` to `.process-fill` immediately after `height: 0;`, then add this rule directly after the `.process-fill` block:

```css
.process-fill::after {
  content: "";
  display: none;
  position: absolute;
  left: 0;
  bottom: -1px;
  width: 1px;
  height: 2px;
  background: var(--magenta);
  box-shadow: inherit;
}

.process-fill.is-complete::after {
  display: block;
}
```

Keep the existing `top`, `left`, `width`, gradient, glow, and `transition` declarations unchanged. In `js/main.js`, add `processFill.classList.toggle("is-complete", progress >= 0.999);` immediately after the existing height assignment; the inline `progress * 100` output stays unchanged.

Execution ruling: a final review caught two side effects. `background: inherit` restarted the cyan-to-magenta gradient inside the 2px seam and flashed cyan at the magenta end, so the connector uses the gradient's terminal color via `var(--magenta)` and the test checks the rendered terminal color instead of identical declarations. The always-on pseudo also placed a 2px neon cap at the top of the empty rail, so the connector is gated by the completion class. Cost if wrong is a visible ornament and a broken seam; both are pinned by RED checks.

- [x] **Step 2: Run the tests and verify they pass**

Run: `python3 tests/browser_smoke.py`
Expected: every connector check PASS at 390px, 320px, and 1366px, `failed=0`, and the console-error check still passes.

Run: `python3 -m unittest discover -s tests`
Expected: all unit tests PASS.

- [x] **Step 3: Commit the GREEN change**

```bash
git add css/styles.css
git commit -m "feat: connect process rail to contact frame"
```

### Task 5: Docs and local artifact hygiene

**Files:**
- Modify: `.gitignore`
- Modify: `README.md`
- Modify: `PRODUCT.md`
- Commit: `docs/superpowers/specs/2026-11-26-process-contact-connector-design.md`
- Commit: `docs/superpowers/plans/2026-11-26-process-contact-connector.md`

**Interfaces:**
- Consumes: the green behaviour from Tasks 2 and 4.
- Produces: owner-facing docs that match the rendered page and a clean working tree.

- [x] **Step 1: Ignore brainstorm artifacts**

Add `.superpowers/` to `.gitignore` on a new line. Keep the existing two lines unchanged.

- [x] **Step 2: Update the README**

Add one sentence to the opening description: "Process steps use Roman numerals I through V, and the neon process rail continues into the top border of the contact panel." Leave the deployment, demo, and CV paragraphs unchanged.

- [x] **Step 3: Update the product decisions**

Add two bullets under `## Owner-directed decisions`, next to the existing process and contact padding decisions:

```markdown
- Keep the process rail straight and extend it into the contact panel top border without a bend or marker.
- Show the five process step numbers as Roman numerals I through V and leave section indices 04 and 05 unchanged.
```

- [x] **Step 4: Verify the final state**

Run: `python3 -m unittest discover -s tests`
Expected: all unit tests PASS.

Run: `python3 tests/browser_smoke.py | tail -3`
Expected: `failed=0`.

Run: `git diff --stat -- demos`
Expected: no output.

- [x] **Step 5: Commit the docs**

```bash
git add .gitignore README.md PRODUCT.md docs/superpowers/specs/2026-11-26-process-contact-connector-design.md docs/superpowers/plans/2026-11-26-process-contact-connector.md
git commit -m "docs: record process rail and roman step decisions"
```

Confirm the pre-commit hook exits 0 and `git status --short --branch` shows no uncommitted changes.
