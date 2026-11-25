# Portfolio Cybertron Liveness Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Make the static portfolio shell feel as alive as the NIGHT//SHIFT demo while keeping Alan Nawa's real identity, English copy, six local demos, and three real contact channels.

**Architecture:** Add one inline SVG orb, one aria-hidden ticker, one motion pause button, one scroll progress rule, and one finite project reveal. CSS owns the two governed loops and the pause switch. Vanilla JS owns toggle state, pointer feedback, progress width, and IntersectionObserver. Static tests pin markup, CSS, and JS contracts. The Firefox smoke script checks rendered behavior at 390px and 320px.

**Tech Stack:** Static HTML, CSS, vanilla JavaScript, Python `unittest`, Firefox WebDriver BiDi smoke script.

**Spec:** `docs/superpowers/specs/2026-11-25-portfolio-cybertron-liveness-design.md`

## Global Constraints

- Static HTML/CSS/JS only. No build step, dependency, external font, or external image on the shell.
- One `<h1 class="sr-only">Alan Nawa</h1>`, six project cards, and the three approved contact destinations stay byte-identical.
- Six demos under `demos/` stay unchanged.
- No boot overlay, ghost cursor, marquee slogan, fake availability status, invented statistic, customer name, testimonial, or Indonesian visitor copy.
- No em dash in visitor-facing copy or new documentation text.
- Motion budget is four `@keyframes` total: `hero-in`, `project-reveal`, `orb-spin`, and `ticker-scroll`. Only the last two use `infinite`.
- The two infinite loops stop under `.motion-paused` and under `prefers-reduced-motion: reduce`. All content stays visible with JavaScript absent and with reduced motion enabled.
- Interactive targets stay at least 44px, focus rings stay visible, text stays AA contrast, and no element overflows at 320px or 390px.
- Glow stays on the primary button and the orb rings only. Cards, badges, section borders, and the ticker stay matte.
- Every new design decision gets a one-line reason in `PRODUCT.md`.

## Review Focus

- A visitor on a phone: the action row must sit close to the intro, both hero buttons must share one baseline, and the header must fit at 390px and 320px with the new pause control.
- A visitor with reduced motion: loops, magnetic feedback, reveal movement, and progress transitions must stop while all copy and cards stay visible.
- A visitor who uses a keyboard: the pause button must be native, focusable, named in English, and its state must be exposed through `aria-pressed`. Focus must never trigger magnetic movement.
- A visitor on a long page: the scroll progress rule must reflect actual position, and the project grid must reveal once, not on every scroll.
- A reader of the source: no fabricated numbers or status may be introduced. `SIX LIVE DEMOS` is allowed because six real cards exist.

---

### Task 1: Page structure for the liveness motif

**Files:**
- Modify: `index.html`
- Modify: `tests/test_portfolio.py`

**Interfaces:**
- Consumes: existing header, `.hero-copy`, `.hero-panel`, and section boundaries from the current shell.
- Produces: `.hero-orb`, `.ticker`, `#motion-toggle`, and `#scroll-progress-bar`. No existing ID, URL, `data-track`, or demo path changes.

- [x] **Step 1: Write failing markup tests**

Add to `ContentTest`:

```python
def test_liveness_markup(self):
    for marker in ('class="hero-orb"', '<textPath', 'ALAN NAWA / WEB &amp; AI AUTOMATION / SIX LIVE DEMOS',
                   'class="ticker" aria-hidden="true"', 'id="motion-toggle"',
                   '>Pause motion<', 'aria-pressed="false"', 'class="scroll-progress"',
                   'id="scroll-progress-bar"'):
        with self.subTest(marker=marker):
            self.assertIn(marker, HTML)

def test_ticker_uses_real_service_labels(self):
    for label in ('WEB DEVELOPMENT', 'LANDING PAGES', 'AI AUTOMATION', 'N8N'):
        with self.subTest(label=label):
            self.assertIn(label, HTML)
    self.assertEqual(HTML.count('WEB DEVELOPMENT'), 2)
    self.assertEqual(HTML.count('LANDING PAGES'), 2)

def test_no_invented_liveness_claims(self):
    for phrase in ('40+', '98.2%', '6+ thn', 'OPEN FOR Q1 2027', 'SYSTEM ONLINE',
                   'BOOT SEQUENCE', 'ghost-cursor'):
        with self.subTest(phrase=phrase):
            self.assertNotIn(phrase, HTML)
```

Keep `test_counts_match_cards` and add `self.assertIn("SIX LIVE DEMOS", HTML)` to it so the orb text is tied to six real cards.

- [x] **Step 2: Run the tests and watch them fail**

Run: `python3 -m unittest discover -s tests -v`

Expected: FAIL on `test_liveness_markup`, `test_ticker_uses_real_service_labels`, and the extended count test.

- [x] **Step 3: Add the structure to `index.html`**

Inside `.site-header`, place this button between the `.header-links` nav and `.menu-toggle`:

```html
<button class="motion-toggle" id="motion-toggle" type="button" aria-pressed="false" aria-label="Pause motion">
  <span class="motion-toggle-icon" aria-hidden="true"></span>
  <span class="motion-toggle-label">Pause motion</span>
</button>
```

Place this rule after `.mobile-menu` and before the closing `</header>`:

```html
<div class="scroll-progress" aria-hidden="true"><i id="scroll-progress-bar"></i></div>
```

Replace the five `.panel-bars` children with this SVG, keeping `.hero-panel` `aria-hidden="true"`:

```html
<svg class="hero-orb" viewBox="0 0 240 240" aria-hidden="true" focusable="false">
  <defs>
    <path id="orb-path" d="M120,120 m-88,0 a88,88 0 1,1 176,0 a88,88 0 1,1 -176,0"></path>
  </defs>
  <g class="orb-rings">
    <circle class="orb-ring orb-ring--outer" cx="120" cy="120" r="106"></circle>
    <circle class="orb-ring orb-ring--text" cx="120" cy="120" r="88"></circle>
    <circle class="orb-ring orb-ring--inner" cx="120" cy="120" r="68"></circle>
    <text class="orb-text" textLength="540" lengthAdjust="spacingAndGlyphs">
      <textPath href="#orb-path">ALAN NAWA / WEB &amp; AI AUTOMATION / SIX LIVE DEMOS / </textPath>
    </text>
  </g>
  <circle class="orb-core" cx="120" cy="120" r="38"></circle>
  <path class="orb-axis" d="M12 120 H228 M120 12 V228"></path>
</svg>
```

Place this ticker immediately after the closing `</section>` of `.hero` and before `<section class="services">`:

```html
<div class="ticker" aria-hidden="true">
  <div class="ticker-track">
    <div class="ticker-group">
      <span>WEB DEVELOPMENT</span><span>LANDING PAGES</span><span>AI AUTOMATION</span><span>N8N</span>
    </div>
    <div class="ticker-group">
      <span>WEB DEVELOPMENT</span><span>LANDING PAGES</span><span>AI AUTOMATION</span><span>N8N</span>
    </div>
  </div>
</div>
```

Do not change any existing text, link, card, ID, or demo path.

- [x] **Step 4: Run the tests and watch them pass**

Run: `python3 -m unittest discover -s tests -v`

Expected: all static tests PASS. The rendered smoke script still passes because its checks do not yet exercise the new controls.

- [x] **Step 5: Commit**

```bash
git add index.html tests/test_portfolio.py
git commit -m "feat: add cybertron liveness structure"
```

### Task 2: CSS for the orb, ticker, pause, and tighter actions

**Files:**
- Modify: `css/styles.css`
- Modify: `tests/test_portfolio.py`

**Interfaces:**
- Consumes: the new classes from Task 1 and the existing cyan, magenta, focus, hover, active, and reduced-motion blocks.
- Produces: four named keyframes, two governed infinite loops, a pause class, magnetic custom properties, and the tightened action row.

- [x] **Step 1: Write failing CSS tests**

Replace `test_motion_is_finite_and_capped` with:

```python
def test_motion_budget_is_explicit(self):
    self.assertEqual(CSS.count('@keyframes'), 4)
    for name in ('hero-in', 'project-reveal', 'orb-spin', 'ticker-scroll'):
        with self.subTest(name=name):
            self.assertIn('@keyframes ' + name, CSS)
    self.assertEqual(CSS.count('infinite'), 2)
    for selector in ('.orb-rings', '.ticker-track'):
        block = CSS.split(selector + ' {')[1].split('}')[0]
        with self.subTest(selector=selector):
            self.assertIn('infinite', block)
```

Add to `CssContractTest`:

```python
def test_liveness_styles(self):
    for marker in ('.hero-orb', '.orb-rings', '.orb-ring--text', '.orb-core',
                   '.ticker', '.ticker-track', '.ticker-group', '.scroll-progress',
                   'transform-box: view-box', 'drop-shadow'):
        with self.subTest(marker=marker):
            self.assertIn(marker, CSS)

def test_pause_and_reduced_motion_rules(self):
    self.assertIn('.motion-paused .orb-rings', CSS)
    self.assertIn('.motion-paused .ticker-track', CSS)
    self.assertIn('animation-play-state: paused', CSS)
    block = CSS.split('@media (prefers-reduced-motion: reduce)')[1]
    for marker in ('.orb-rings', '.ticker-track', '.project-grid.reveal-pending',
                   '.scroll-progress i'):
        with self.subTest(marker=marker):
            self.assertIn(marker, block)

def test_instagram_actions_are_tight(self):
    actions = CSS.split('.hero-actions {')[1].split('}')[0]
    copy = CSS.split('.hero-copy {')[1].split('}')[0]
    self.assertNotIn('margin-top', actions)
    self.assertIn('gap: 0.9rem', copy)

def test_no_dead_panel_bars(self):
    self.assertNotIn('panel-bars', CSS)
```

- [x] **Step 2: Run the tests and watch them fail**

Run: `python3 -m unittest discover -s tests -v`

Expected: FAIL on the new motion budget, liveness style, pause, spacing, and dead-bar assertions.

- [x] **Step 3: Update `css/styles.css`**

- Change `.hero-copy` to `gap: 0.9rem` and remove the `margin-top` line from `.hero-actions`. Keep `display: flex`, `flex-wrap: wrap`, `gap: 0.85rem`, and the 560px `flex: 1` rule.
- Remove the `.panel-bars` and `.panel-bars i` rules. Add `.hero-orb` at `width: min(100%, 14rem)`, `aspect-ratio: 1`, `display: block`, and `margin-inline: auto`.
- Style `.orb-ring` with `fill: none`, `stroke: var(--line-strong)`, and `stroke-width: 1`. Style `.orb-ring--text` with `stroke: rgba(0, 229, 255, 0.65)`. Style `.orb-text` with `fill: var(--cyan)`, `font-family: var(--mono)`, `font-size: 8px`, and `letter-spacing: 1px`. Style `.orb-core` with `fill: rgba(0, 229, 255, 0.08)` and `stroke: var(--cyan)`. Style `.orb-axis` with `stroke: rgba(255, 61, 141, 0.35)`.
- Animate `.orb-rings` with `animation: orb-spin 18s linear infinite`, `transform-box: view-box`, and `transform-origin: 120px 120px`. Add one `filter: drop-shadow(0 0 8px rgba(0, 229, 255, 0.35))` on `.orb-rings` only.
- Add `@keyframes orb-spin` from `rotate(0deg)` to `rotate(360deg)`.
- Style `.ticker` with `overflow: hidden`, `border-block: 1px solid var(--line)`, and `background: rgba(9, 14, 23, 0.72)`. Style `.ticker-track` as `display: flex`, `width: max-content`, and `animation: ticker-scroll 24s linear infinite`. Style `.ticker-group` as `display: flex`, `flex: none`, `gap: 3rem`, `padding-right: 3rem`. Style `.ticker span` with mono type, `0.68rem`, `letter-spacing: 0.18em`, and `color: var(--muted)`.
- Add `@keyframes ticker-scroll` from `translateX(0)` to `translateX(-50%)`.
- Add `.scroll-progress` with `position: absolute`, `left: 0`, `right: 0`, `bottom: -1px`, `height: 2px`, and `pointer-events: none`. Add `.scroll-progress i` with `display: block`, `width: 0`, `height: 100%`, `background: var(--cyan)`, and `transition: width 120ms linear`.
- Add `.motion-toggle` beside the menu button: `min-height: 44px`, `display: inline-flex`, `align-items: center`, `gap: 0.45rem`, `padding: 0 0.7rem`, `border: 1px solid var(--line-strong)`, `background: transparent`, `color: var(--cyan)`, mono `0.62rem`, `letter-spacing: 0.1em`, `text-transform: uppercase`, and a 160ms hover and active transition. Style `.motion-toggle-icon` as a 6px cyan square. Add `.motion-toggle[aria-pressed="true"]` with magenta border and text. Add a visible focus state through the existing `:focus-visible` rule.
- Add magnetic variables to `.btn`: `transform: translate3d(var(--mag-x, 0px), var(--mag-y, 0px), 0)`. Update hover to `translate3d(var(--mag-x, 0px), calc(var(--mag-y, 0px) - 2px), 0)` and active to `translate3d(var(--mag-x, 0px), calc(var(--mag-y, 0px) + 1px), 0)`.
- Add `.project-grid.reveal-pending` with `opacity: 0` and `transform: translateY(10px)`. Add `.project-grid.reveal-pending.is-revealed` with `animation: project-reveal 600ms cubic-bezier(0.16, 1, 0.3, 1) forwards`. Add `@keyframes project-reveal` from that hidden state to `opacity: 1` and `transform: translateY(0)`.
- Add `.motion-paused .orb-rings, .motion-paused .ticker-track { animation-play-state: paused; }`.
- Change the nav breakpoint from `@media (max-width: 560px)` to `@media (max-width: 680px)` for `.header-links` and `.menu-toggle`. Keep the other 560px rules. Add `@media (max-width: 400px) { .brand-copy { display: none; } }`.
- In the reduced-motion block, set `.orb-rings`, `.ticker-track`, and `.project-grid` to `animation: none !important`, `transform: none !important`, and `opacity: 1 !important`. Add `.project-grid.reveal-pending` to that block. Set `.scroll-progress i { transition: none !important; }`, `.motion-toggle { display: none; }`, and keep the universal animation and transition kill switch.

- [x] **Step 4: Run the tests and watch them pass**

Run: `python3 -m unittest discover -s tests -v`

Expected: all static tests PASS.

- [x] **Step 5: Commit**

```bash
git add css/styles.css tests/test_portfolio.py
git commit -m "feat: style cybertron liveness"
```

### Task 3: JavaScript behavior for pause, progress, magnet, and reveal

**Files:**
- Modify: `js/main.js`
- Modify: `tests/test_portfolio.py`

**Interfaces:**
- Consumes: `#motion-toggle`, `#scroll-progress-bar`, `.btn`, and `#project-grid` from Task 1.
- Produces: one pause toggle, one scroll listener, one pointer-feedback listener set, and one finite IntersectionObserver reveal.

- [x] **Step 1: Write failing JS tests**

Add to `InteractionTest`:

```python
def test_motion_toggle_logic(self):
    for marker in ('const motionToggle', 'function setMotionPaused',
                   "classList.toggle('motion-paused'", 'Resume motion',
                   "setAttribute('aria-pressed'", "setAttribute('aria-label'"):
        with self.subTest(marker=marker):
            self.assertIn(marker, JS)

def test_scroll_progress_logic(self):
    for marker in ('#scroll-progress-bar', 'function updateProgress', 'scrollHeight',
                   'innerHeight', 'scrollY', 'passive: true'):
        with self.subTest(marker=marker):
            self.assertIn(marker, JS)

def test_magnetic_button_logic(self):
    for marker in ('--mag-x', '--mag-y', 'pointermove', 'pointerleave',
                   "matchMedia('(prefers-reduced-motion: reduce)')"):
        with self.subTest(marker=marker):
            self.assertIn(marker, JS)

def test_project_reveal_logic(self):
    for marker in ('IntersectionObserver', 'reveal-pending', 'is-revealed', 'threshold'):
        with self.subTest(marker=marker):
            self.assertIn(marker, JS)

def test_no_timers_or_forbidden_liveness_copy(self):
    self.assertNotIn('setInterval', JS)
    for phrase in ('Buka menu', 'Tutup menu', 'Jeda animasi', 'Lanjut animasi'):
        with self.subTest(phrase=phrase):
            self.assertNotIn(phrase, JS)
```

- [x] **Step 2: Run the tests and watch them fail**

Run: `python3 -m unittest discover -s tests -v`

Expected: FAIL on the four new behavior tests.

- [x] **Step 3: Add behavior to `js/main.js`**

Append the following, keeping the existing filter and menu code unchanged. Use exact strings `Pause motion` and `Resume motion`.

```js
const motionToggle = document.querySelector('#motion-toggle');
const motionLabel = motionToggle.querySelector('.motion-toggle-label');

function setMotionPaused(isPaused) {
  document.documentElement.classList.toggle('motion-paused', isPaused);
  motionToggle.setAttribute('aria-pressed', String(isPaused));
  const label = isPaused ? 'Resume motion' : 'Pause motion';
  motionToggle.setAttribute('aria-label', label);
  motionLabel.textContent = label;
}

motionToggle.addEventListener('click', () => {
  setMotionPaused(motionToggle.getAttribute('aria-pressed') !== 'true');
});

const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
const clamp = (value, min, max) => Math.min(max, Math.max(min, value));

function resetMagnet(button) {
  button.style.setProperty('--mag-x', '0px');
  button.style.setProperty('--mag-y', '0px');
}

document.querySelectorAll('.btn').forEach((button) => {
  button.addEventListener('pointermove', (event) => {
    if (reduceMotion.matches || event.pointerType !== 'mouse') return;
    const rect = button.getBoundingClientRect();
    const x = clamp(((event.clientX - rect.left) / rect.width - 0.5) * 4, -2, 2);
    const y = clamp(((event.clientY - rect.top) / rect.height - 0.5) * 4, -2, 2);
    button.style.setProperty('--mag-x', x.toFixed(2) + 'px');
    button.style.setProperty('--mag-y', y.toFixed(2) + 'px');
  });
  ['pointerleave', 'pointercancel', 'blur'].forEach((type) => {
    button.addEventListener(type, () => resetMagnet(button));
  });
});

reduceMotion.addEventListener('change', () => {
  if (reduceMotion.matches) document.querySelectorAll('.btn').forEach(resetMagnet);
});

const progressBar = document.querySelector('#scroll-progress-bar');

function updateProgress() {
  const max = document.documentElement.scrollHeight - window.innerHeight;
  const ratio = max > 0 ? Math.min(1, Math.max(0, window.scrollY / max)) : 0;
  progressBar.style.width = (ratio * 100).toFixed(2) + '%';
}

updateProgress();
window.addEventListener('scroll', updateProgress, {passive: true});
window.addEventListener('resize', updateProgress);

const projectGrid = document.querySelector('#project-grid');
if (projectGrid && 'IntersectionObserver' in window) {
  projectGrid.classList.add('reveal-pending');
  const revealObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      projectGrid.classList.add('is-revealed');
      observer.disconnect();
    });
  }, {threshold: 0.12});
  revealObserver.observe(projectGrid);
}
```

- [x] **Step 4: Run the tests and watch them pass**

Run: `python3 -m unittest discover -s tests -v`

Expected: all static tests PASS.

- [x] **Step 5: Commit**

```bash
git add js/main.js tests/test_portfolio.py
git commit -m "feat: wire cybertron interactions"
```

### Task 4: Rendered Firefox checks at 390px and 320px

**Files:**
- Modify: `tests/browser_smoke.py`

**Interfaces:**
- Consumes: the running page from Tasks 1 to 3.
- Produces: rendered checks for loop state, pause state, action spacing, magnetic cap, progress width, reveal completion, and narrow-header fit.

- [x] **Step 1: Extend the harness to two widths**

Replace the fixed `HARNESS` string with a `HARNESS_TEMPLATE` that formats `{width}` into the iframe style. Keep `HARNESS_PATH = "/__portfolio_browser_check__.html"` and add `NARROW_PATH = "/__portfolio_browser_check__320.html"`.

Update `Handler.do_GET` to match both paths:

```python
match = re.fullmatch(r"/__portfolio_browser_check__(\d*)\.html", self.path.split("?", 1)[0])
if match:
    width = int(match.group(1) or 390)
    body = HARNESS_TEMPLATE.format(width=width).encode()
```

Import `re` at the top of the file. The digit group has no leading underscore because both harness paths use a double underscore before the width.

- [x] **Step 2: Add normal-motion checks to `NORMAL_SCRIPT`**

Add these checks after the existing hero visibility check:

```javascript
const orb = doc.querySelector('.orb-rings');
const ticker = doc.querySelector('.ticker-track');
check('orb loop is running', win.getComputedStyle(orb).animationName === 'orb-spin',
  win.getComputedStyle(orb).animationName);
check('ticker loop is running', win.getComputedStyle(ticker).animationName === 'ticker-scroll',
  win.getComputedStyle(ticker).animationName);

const introRect = doc.querySelector('.hero-intro').getBoundingClientRect();
const actionsRect = doc.querySelector('.hero-actions').getBoundingClientRect();
const actionGap = Math.round(actionsRect.top - introRect.bottom);
check('Instagram action row sits close to intro', actionGap <= 16, 'gap=' + actionGap + 'px');

const primaryRect = doc.querySelector('.btn--primary').getBoundingClientRect();
const ghostRect = doc.querySelector('.btn--ghost').getBoundingClientRect();
check('Instagram button aligns with View projects', primaryRect.top === ghostRect.top,
  'primary=' + Math.round(primaryRect.top) + ' ghost=' + Math.round(ghostRect.top));
```

Add these checks after the menu checks and before the all-links click loop:

```javascript
const motionToggle = doc.getElementById('motion-toggle');
check('pause control starts English and unpaused',
  motionToggle.getAttribute('aria-label') === 'Pause motion' &&
  motionToggle.getAttribute('aria-pressed') === 'false',
  motionToggle.getAttribute('aria-label') + ' pressed=' + motionToggle.getAttribute('aria-pressed'));
motionToggle.click();
check('pause control pauses both loops',
  doc.documentElement.classList.contains('motion-paused') &&
  motionToggle.getAttribute('aria-label') === 'Resume motion' &&
  motionToggle.getAttribute('aria-pressed') === 'true' &&
  win.getComputedStyle(orb).animationPlayState === 'paused' &&
  win.getComputedStyle(ticker).animationPlayState === 'paused',
  win.getComputedStyle(orb).animationPlayState + ' / ' + win.getComputedStyle(ticker).animationPlayState);
motionToggle.click();
check('pause control resumes both loops',
  !doc.documentElement.classList.contains('motion-paused') &&
  win.getComputedStyle(orb).animationPlayState === 'running' &&
  win.getComputedStyle(ticker).animationPlayState === 'running',
  win.getComputedStyle(orb).animationPlayState + ' / ' + win.getComputedStyle(ticker).animationPlayState);

const magnetic = doc.querySelector('.btn--primary');
const magneticRect = magnetic.getBoundingClientRect();
magnetic.dispatchEvent(new win.PointerEvent('pointermove', {
  bubbles: true, pointerType: 'mouse',
  clientX: magneticRect.right - 1, clientY: magneticRect.top + 1
}));
const magX = Math.abs(Number.parseFloat(magnetic.style.getPropertyValue('--mag-x')) || 0);
const magY = Math.abs(Number.parseFloat(magnetic.style.getPropertyValue('--mag-y')) || 0);
check('magnetic offset is capped at 2px', magX <= 2.01 && magY <= 2.01,
  'x=' + magX.toFixed(2) + ' y=' + magY.toFixed(2));
magnetic.dispatchEvent(new win.PointerEvent('pointerleave', {bubbles: true}));
magnetic.focus();
const focusMagX = magnetic.style.getPropertyValue('--mag-x');
check('keyboard focus does not move button', focusMagX === '0px', focusMagX);
```

Add these checks after the all-links click loop:

```javascript
doc.getElementById('project-grid').scrollIntoView({block: 'center'});
setTimeout(() => {
  const gridOpacity = Number(win.getComputedStyle(doc.getElementById('project-grid')).opacity);
  check('project grid reveal completes', gridOpacity === 1, 'opacity=' + gridOpacity);

  win.scrollTo({top: doc.documentElement.scrollHeight, behavior: 'instant'});
  win.dispatchEvent(new win.Event('scroll'));
  const progressWidth = Number.parseFloat(doc.getElementById('scroll-progress-bar').style.width);
  check('scroll progress reaches bottom', progressWidth >= 99, 'width=' + progressWidth + '%');
  resolve(checks);
}, 700);
```

Move the existing final `resolve(checks)` into that timeout. Keep the outer 1200ms delay before the nested 700ms delay so the finite entrance has already ended.

- [x] **Step 3: Add `NARROW_SCRIPT` for 320px**

Define `NARROW_SCRIPT` using the same BiDi expression shape as `REDUCED_SCRIPT`. It must check:

```javascript
check('320px iframe viewport', win.innerWidth === 320, String(win.innerWidth));
check('320px has no horizontal overflow', doc.documentElement.scrollWidth <= 320,
  'scrollWidth=' + doc.documentElement.scrollWidth);
for (const selector of ['.brand', '.motion-toggle', '#menu-toggle', '.btn--primary', '.btn--ghost']) {
  const rect = doc.querySelector(selector).getBoundingClientRect();
  check(selector + ' fits 320px',
    rect.left >= -1 && rect.right <= 321 && rect.height >= 44,
    Math.round(rect.left) + '..' + Math.round(rect.right) + ' h=' + Math.round(rect.height));
}
```

- [x] **Step 4: Extend reduced-motion checks**

In `REDUCED_SCRIPT`, change the node selector to include the new animated elements:

```javascript
const nodes = Array.from(doc.querySelectorAll(
  '.hero-copy > *, .btn, .card-link, .project-card, .orb-rings, .ticker-track, .project-grid'
));
```

Add:

```javascript
check('reduced motion hides pause control',
  win.getComputedStyle(doc.getElementById('motion-toggle')).display === 'none',
  win.getComputedStyle(doc.getElementById('motion-toggle')).display);
const gridOpacity = Number(win.getComputedStyle(doc.getElementById('project-grid')).opacity);
check('reduced motion keeps project grid visible', gridOpacity === 1, 'opacity=' + gridOpacity);
```

- [x] **Step 5: Run the rendered check and fix any failure**

Run: `python3 tests/browser_smoke.py`

Expected: all checks PASS. The check count must be greater than the previous 27. Fix source or script assertions until there are zero failures. Do not weaken the pause, overflow, action spacing, magnetic cap, reveal, or reduced-motion checks.

- [x] **Step 6: Commit**

```bash
git add tests/browser_smoke.py
git commit -m "test: verify rendered cybertron liveness"
```

### Task 5: Product truth, README, full verification, and delivery gate

**Files:**
- Modify: `PRODUCT.md`
- Modify: `README.md`
- Modify: `docs/superpowers/specs/2026-11-25-portfolio-cybertron-liveness-design.md`
- Modify: `tests/test_portfolio.py`

**Interfaces:**
- Consumes: the shipped markup, CSS, and JS from Tasks 1 to 4.
- Produces: documentation that matches the live page and a complete verification report.

- [x] **Step 1: Write failing documentation tests**

Add to `DeliveryTest`:

```python
def test_product_records_liveness_dials_and_reasons(self):
    product = read('PRODUCT.md')
    for marker in ('ENERGY 3 / RHYTHM 2 / MOTION 3', 'orb', 'pause', 'ticker',
                   'scroll progress', 'magnetic', 'reveal'):
        with self.subTest(marker=marker):
            self.assertIn(marker, product.lower() if marker.islower() else product)
    self.assertNotIn('Use motion once, briefly, and never loop it', product)

def test_readme_describes_liveness(self):
    readme = read('README.md')
    for marker in ('orb', 'ticker', 'Pause motion', 'scroll progress', 'reduced motion'):
        with self.subTest(marker=marker):
            self.assertIn(marker, readme.lower() if marker.islower() else readme)
```

- [x] **Step 2: Run the tests and watch them fail**

Run: `python3 -m unittest discover -s tests -v`

Expected: FAIL on the two new documentation tests.

- [x] **Step 3: Update the documents**

In `PRODUCT.md`:

- Change `Design dials` to `ENERGY 3 / RHYTHM 2 / MOTION 3`.
- Replace the motion sentence with a statement that loops are governed by a real pause control and all motion stops under reduced motion.
- Add one-line reasons: the orb is the TRON identity motif, the ticker carries real service labels, the pause control gives visitors a real stop, the progress rule gives orientation on a long CV, magnetic feedback answers the pointer, the single reveal directs attention to real work, and the tighter action row closes the reported gap.
- Keep the no-fabrication, English, six-demo, and three-contact constraints unchanged.

In `README.md`:

- Replace the one short entrance motion sentence with the orb, real-label ticker, pause button, scroll progress, magnetic pointers, and one project reveal.
- State that both loops stop under reduced motion and that the pause button has `aria-pressed`.
- Update the tests paragraph to mention rendered checks at 390px and 320px.

In the spec file, change `Status:` from `drafted for approval` to `approved`.

- [x] **Step 4: Run the full verification set**

Run from the repository root:

```bash
python3 -m unittest discover -s tests -v
python3 tests/browser_smoke.py
xmllint --html --noout index.html
python3 -m http.server 8087 >/tmp/opencode/liveness-http.log 2>&1 &
pid=$!
sleep 1
for path in / /css/styles.css /js/main.js /assets/favicon.svg \
  /demos/ai-lead-capture/dashboard/index.html \
  /demos/servis-ac/index.html \
  /demos/ruang-rapi/index.html \
  /demos/kedai-kopi/index.html \
  /demos/rental-mobil/index.html \
  /demos/nightshift/index.html; do
  curl -s -o /dev/null -w "%{http_code} $path\\n" "http://127.0.0.1:8087$path"
done
kill "$pid"
python3 /home/asnodt/.config/opencode/skills/antislop-human/contrast-check.py '#00e5ff' '#05070c'
python3 /home/asnodt/.config/opencode/skills/antislop-human/contrast-check.py '#00e5ff' '#090e17'
python3 /home/asnodt/.config/opencode/skills/antislop-human/contrast-check.py '#ff3d8d' '#05070c'
python3 /home/asnodt/.config/opencode/skills/antislop-human/contrast-check.py '#93a9b6' '#05070c'
python3 /home/asnodt/.config/opencode/skills/antislop-human/contrast-check.py '#93a9b6' '#090e17'
git hook run pre-commit
```

Expected: all unit tests PASS, all rendered checks PASS, `xmllint` exit 0, ten HTTP `200` lines, all contrast ratios at least 4.5:1, and the pre-commit hook exit 0.

- [x] **Step 5: Run the antislop Delivery Gate**

Use the `antislop` core skill checklist. Report a PASS or FAIL line for every item with concrete evidence. If any item FAILS, fix it and rerun the gate before delivery. Record the final PASS or FAIL report in the delivery message, not in a new repo file.

- [x] **Step 6: Commit**

```bash
git add PRODUCT.md README.md docs/superpowers/specs/2026-11-25-portfolio-cybertron-liveness-design.md tests/test_portfolio.py
git commit -m "docs: record cybertron liveness decisions"
```

## Completion Checklist

- Working tree clean on `master`.
- All unit tests and rendered checks pass with zero failures.
- No external asset, no fake statistic, no fake status, no boot overlay, no ghost cursor, and no Indonesian shell copy.
- The reported gap above the Instagram action is closed and both hero buttons remain aligned.
- The finished page reads as cyberpunk x TRON because of the orb, horizon, ticker, and governed motion, not because of fabricated content.
