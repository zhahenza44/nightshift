# Contact Actions Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the contact `Copy email` box with `Send message` opening the owner's Instagram DM, move `GITHUB` into the action row as a box, and remove the `EMAIL` text link and unused copy path.

**Architecture:** The existing `.btn` system already supplies the box, hover states, focus states, and 50px tap target. Add two external anchors to `.contact-actions`, delete the empty `.contact-links` row and the unused clipboard/toast path, then give the narrow breakpoint its own two-column arrangement for the compact actions. The rest of the page stays untouched.

**Tech Stack:** Static HTML, CSS, vanilla JavaScript, Python `unittest`, Firefox BiDi rendered smoke script.

**Spec:** `docs/superpowers/specs/2026-11-27-contact-actions-design.md`

**Design read:** Incumbent NIGHT//SHIFT demo world, dial ENERGY 3 / RHYTHM 3 / MOTION 2. The change extends that world by reusing its existing button language, with no new color, icon, or motion.

## Global Constraints

- All visitor-facing copy stays English.
- Keep the NIGHT//SHIFT brand, real CV section, fictional showcase disclosures, and every file in `demos/` unchanged.
- Keep `Response <24h`, the terminal line, and the `contact-copy` paragraph exactly as they are.
- Keep `Send brief` at `mailto:zhahenza666@proton.me`.
- Use `https://ig.me/m/zhahenzar` exactly for `Send message`, with `target="_blank"` and `rel="noopener"`.
- Keep `GITHUB` at `https://github.com/zhahenza44/otomasi-web`, with `target="_blank"` and `rel="noopener"`.
- Work inline on `master`. Create no branch, merge, or pull request.
- TDD red, then green, then docs. Commit each phase separately. RED commits may use `--no-verify` because they intentionally fail the hook; GREEN commits must pass it.
- Firefox rendered smoke must stay green at 390px, 320px, reduced motion, and 1366px. `git diff --stat -- demos` must stay empty.
- Do not push until the owner confirms they want this version live.

## Review Focus

- A visitor expects a direct message, not the public profile: NORMAL_SCRIPT pins the exact `ig.me/m/` href plus new-tab and `noopener` attributes.
- Removing `EMAIL` must not leave a bordered empty row: NORMAL_SCRIPT pins `.contact-links` absent and exactly one `mailto:` anchor left in `.contact-main`.
- `GITHUB` must read as part of one action row on desktop: WIDE_SCRIPT pins all three `.contact-actions .btn` elements on the same top edge at 1366px.
- A narrow phone must not squeeze the compact boxes into overflow or tiny targets: NORMAL_SCRIPT and NARROW_SCRIPT pin the two ghost buttons side by side, above 44px tall, and inside the viewport at 390px and 320px.
- Removing the copy path must not leave stale code or runtime errors: the unit test pins no `navigator.clipboard.writeText`, `showToast`, or `copy-email` strings, and the rendered smoke console gate must stay clean.

---

### Task 1: Contact action markup and obsolete copy path

**Files:**
- Modify: `index.html:505-512`, `index.html:548`
- Modify: `js/main.js:486-492`, `js/main.js:732-783`
- Modify: `css/styles.css:2586-2617`, `css/styles.css:3117-3147`, `css/styles.css:3467-3470`
- Test: `tests/test_portfolio.py:38-48`, `tests/test_portfolio.py:116-126`, `tests/test_portfolio.py:356-364`
- Test: `tests/browser_smoke.py:208-219`, `tests/browser_smoke.py:276-281`, `tests/browser_smoke.py:342-358`, `tests/browser_smoke.py:368-385`, `tests/browser_smoke.py:444-453`, `tests/browser_smoke.py:560-578`

**Interfaces:**
- Consumes: existing `.btn`, `.btn--primary`, `.btn--ghost`, `.contact-actions`, and the existing rendered smoke harness.
- Produces: `#send-message` anchor, `.contact-actions a[href="https://github.com/zhahenza44/otomasi-web"]` box, and `.contact-actions .btn--primary`. Task 2 selects these exact three nodes.
- Produces: no `#copy-email`, no `#toast`, no `.contact-links`.

- [ ] **Step 1: Write the failing unit tests**

In `tests/test_portfolio.py`, remove `'id="toast"'` from `test_nightshift_sections_exist`, remove `"<span>Copy email</span>"` from the homepage copy markers. In `test_menu_dialog_copy_clock_and_nav_markers`, remove the three markers that assert clipboard, toast, and `Copied` behavior. Add:

```python
    def test_contact_actions_use_instagram_dm_and_boxed_github(self):
        for marker in (
            '<a class="btn btn--ghost" id="send-message" href="https://ig.me/m/zhahenzar" target="_blank" rel="noopener"><span>Send message</span><i>↗</i></a>',
            '<a class="btn btn--ghost" href="https://github.com/zhahenza44/otomasi-web" target="_blank" rel="noopener"><span>GITHUB</span><i>↗</i></a>',
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, HTML)
        for phrase in (
            'id="copy-email"', 'Copy email', 'EMAIL <span>↗</span>',
            'class="contact-links', 'id="toast"',
        ):
            with self.subTest(absent=phrase):
                self.assertNotIn(phrase, HTML)
        for phrase in ('navigator.clipboard.writeText', 'showToast', 'copy-email', 'EMAIL COPIED'):
            with self.subTest(absent_js=phrase):
                self.assertNotIn(phrase, JS)
```

- [ ] **Step 2: Write the failing rendered checks**

In `tests/browser_smoke.py`, replace the copy-button toast block at lines 208-219 with checks named `send message opens Instagram DM in a new tab` (exact href, target `_blank`, `rel` contains `noopener`, span reads `Send message`), `email link row is gone` (`.contact-links` absent and exactly one `mailto:` anchor inside `.contact-main`), and `github is a box beside send message` (GitHub anchor is inside `.contact-actions`, has `.btn`, span reads `GITHUB`, and top edge matches the DM anchor within 1px).

Replace the `github label replaced source` check with `github label stays GITHUB in the action row`, asserting the GitHub anchor text starts with `GITHUB` and no `.contact-links` node exists. Add `https://ig.me/m/zhahenzar` to the `required` href list. Delete the `copy email uses the real address` check. Replace `#copy-email` with `#send-message` in the focus loop and the 320px tap-target selector list, and rename the focus labels from `copy email button` to `send message button`.

In `WIDE_SCRIPT`, add a check named `1366px contact actions share one row` that collects all three `.contact-actions .btn` nodes and asserts their `getBoundingClientRect().top` values differ by at most 1px.

- [ ] **Step 3: Run the tests and verify RED**

Run: `python3 -m unittest discover -s tests && python3 tests/browser_smoke.py`

Expected: the new unit test fails on the missing DM anchor; the rendered smoke reports the new contact-action checks failing while the existing checks stay green. Confirm the failures are missing behavior, not syntax errors.

- [ ] **Step 4: Commit RED**

```bash
git add tests/test_portfolio.py tests/browser_smoke.py
git commit --no-verify -m "test: pin instagram dm and boxed github contact actions"
```

- [ ] **Step 5: Implement the markup change**

In `index.html`, replace the `Copy email` button with:

```html
<a class="btn btn--ghost" id="send-message" href="https://ig.me/m/zhahenzar" target="_blank" rel="noopener"><span>Send message</span><i>↗</i></a>
```

Move the GitHub anchor into `.contact-actions` after the DM anchor:

```html
<a class="btn btn--ghost" href="https://github.com/zhahenza44/otomasi-web" target="_blank" rel="noopener"><span>GITHUB</span><i>↗</i></a>
```

Delete the whole `.contact-links` div and the `#toast` div. Leave `Send brief` and the terminal untouched. The `↗` glyph keeps the existing button language and marks an external destination.

- [ ] **Step 6: Remove the unused copy path**

In `js/main.js`, change the ghost-cursor label branch to `text = "CLICK";` for buttons with no special case. Delete the `Copy email + toast` section, including `showToast`, `legacyCopy`, the clipboard call, the label swap, and the timer. In `css/styles.css`, delete the `.contact-links` rules, its 520px grid override, and the entire Toast section. Do not touch any other `.btn` or `.toast` reference.

- [ ] **Step 7: Run the tests and verify GREEN**

Run: `python3 -m unittest discover -s tests && python3 tests/browser_smoke.py`

Expected: unit tests all PASS and rendered smoke reports `failed=0` with no console errors. The 390px side-by-side checks belong to Task 2 and are not present yet.

- [ ] **Step 8: Commit GREEN**

```bash
git add index.html js/main.js css/styles.css
git commit -m "feat: send Instagram DM and box GitHub in contact actions"
```

### Task 2: Phone action row reflow

**Files:**
- Modify: `css/styles.css:3388-3390`
- Test: `tests/browser_smoke.py` in `NORMAL_SCRIPT_B` and `NARROW_SCRIPT`

**Interfaces:**
- Consumes: `#send-message`, `.contact-actions .btn--primary`, and the GitHub box selector produced by Task 1.
- Produces: a phone state where the primary button spans the row and the two ghost buttons share a row.

- [ ] **Step 1: Write the failing rendered checks**

In `NORMAL_SCRIPT_B`, add `390px send brief spans the action row` and `390px send message and github sit side by side`. In `NARROW_SCRIPT`, add the same two checks with the `320px` prefix. Each side-by-side check must assert that the DM and GitHub boxes share a top edge within 1px, do not overlap horizontally (`dm.right <= github.left + 1`), are at least 44px tall, and end at or inside `viewport + 1`. Each primary check must assert the primary button's width is at least 200px at 320px (and 280px at 390px) and that its bottom is above the DM top.

- [ ] **Step 2: Run the smoke and verify RED**

Run: `python3 tests/browser_smoke.py`

Expected: the new 390px and 320px layout checks fail because the current `.contact-actions .btn { width: 100%; }` stacks all three buttons.

- [ ] **Step 3: Commit RED**

```bash
git add tests/browser_smoke.py
git commit --no-verify -m "test: pin phone action row reflow"
```

- [ ] **Step 4: Reflow the narrow action row**

In the `@media (max-width: 520px)` block, replace `.contact-actions .btn { width: 100%; }` with:

```css
  .contact-actions .btn--primary {
    width: 100%;
  }

  .contact-actions .btn--ghost {
    flex: 1 1 0;
    min-width: 0;
    gap: 8px;
    padding-inline: 10px;
  }
```

If the 320px check still reports overflow, reduce only `gap` and `padding-inline` inside this scoped rule until it passes. Do not change the base `.btn` size or any other breakpoint.

- [ ] **Step 5: Run the full suite and verify GREEN**

Run: `python3 -m unittest discover -s tests && python3 tests/browser_smoke.py && git diff --stat -- demos`

Expected: unit tests PASS, rendered smoke `failed=0`, and no `demos/` diff.

- [ ] **Step 6: Commit GREEN**

```bash
git add css/styles.css
git commit -m "feat: pair contact boxes on phone widths"
```

### Task 3: Record the decisions and verify the final state

**Files:**
- Modify: `README.md:5`, `README.md:8`
- Modify: `PRODUCT.md:34`, `PRODUCT.md:45`, after `PRODUCT.md:53`

**Interfaces:**
- Consumes: the final DOM and CSS from Tasks 1 and 2.
- Produces: owner-facing documentation of the new action row and the reason for each decision.

- [ ] **Step 1: Update the README**

In the showcase bullet, remove `copy-email toast`. In the opening description, replace `Copy email, and EMAIL link all use \`zhahenza666@proton.me\`` with `Send brief uses \`zhahenza666@proton.me\`; Send message opens \`https://ig.me/m/zhahenzar\``. Add one sentence: `GITHUB is now a boxed action beside Send message, and the EMAIL text link is gone.`

- [ ] **Step 2: Update the product decisions**

Add these bullets under `## Owner-directed decisions`:

```markdown
- Replace the Copy email action with Send message opening `https://ig.me/m/zhahenzar` in a new tab, because the conversation happens in Instagram DM.
- Keep Send brief at `mailto:zhahenza666@proton.me` and remove the unused copy-email toast path.
- Box GITHUB beside Send message and remove the EMAIL text link and the empty `.contact-links` row, so the action row has one conversation path and one code path.
- At phone widths, keep Send brief full width and place Send message and GITHUB side by side, using the existing ghost button style so the compact actions stay readable without overflow.
- Keep the `↗` glyph on the external action anchors to mark a new tab, following the existing NIGHT//SHIFT button language.
```

- [ ] **Step 3: Run the final verification**

Run: `python3 -m unittest discover -s tests`

Expected: all unit tests PASS.

Run: `python3 tests/browser_smoke.py | tail -1`

Expected: `checks=` line with `failed=0`.

Run: `git diff --stat -- demos && git diff --check && git status --short --branch`

Expected: no `demos/` diff, no whitespace errors, clean `master` except the intended new commits.

- [ ] **Step 4: Commit the docs**

```bash
git add README.md PRODUCT.md
git commit -m "docs: record contact action decisions"
```

- [ ] **Step 5: Ask before shipping**

Report the verification evidence and ask the owner whether to push `master` to `origin/master`. Do not push without that answer.
