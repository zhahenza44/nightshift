# Portfolio Cyberpunk x TRON Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Restyle the static portfolio shell as cyberpunk x TRON with finite motion and translate all shell copy into English, while keeping six local demos and the three approved contact channels.

**Architecture:** Edit `index.html` for English strings, `css/styles.css` for tokens, angular surfaces, horizon grid, and finite motion, and `js/main.js` only if a class hook is needed. Static tests in `tests/test_portfolio.py` pin every contract. No build step and no external asset.

**Tech Stack:** Static HTML, CSS, vanilla JavaScript, Python `unittest` static assertions.

**Spec:** `docs/superpowers/specs/2026-11-25-portfolio-cybertron-design.md`

## Global Constraints

- Static HTML/CSS/JS only. No build step, no dependency, no external font or image on the shell.
- One `h1`, visually hidden via `.sr-only`; no skipped heading levels.
- Six project cards, all linking to existing local `demos/.../index.html` files.
- Contact channels only: Instagram `https://instagram.com/zhahenzar`, GitHub `https://github.com/zhahenza44`, email `mailto:zhahenza666@proton.me`.
- No WhatsApp, no projects.co.id, no fabricated availability claim.
- Text contrast at least 4.5:1; tap targets at least 44px; visible `:focus-visible`; keyboard-operable controls; `prefers-reduced-motion` disables motion.
- No infinite animation. At most two finite `@keyframes` blocks.
- Demo files under `demos/` are copied content and stay unchanged.

## Review Focus

- A phone at 390px: the horizon grid and clipped corners must not cause horizontal overflow or hide focus outlines. Task 2 pins the responsive guards; Task 4 checks the rendered geometry.
- A visitor with reduced motion enabled: all entrance and hover movement must stop while copy stays readable. Task 3 pins the reduced-motion rule.
- A screen reader: the hidden `h1`, English `aria-label`s, and `lang="en"` must all agree. Task 1 pins these strings.
- A keyboard-only visitor: filter buttons, menu toggle, and demo links must remain focusable after the visual changes. Task 3 pins focus and active states.
- A visitor with JavaScript disabled: entrance motion must not leave content invisible. Task 3 uses CSS-only finite animation, pinned by tests.

---

### Task 1: English shell copy

**Files:**
- Modify: `index.html`
- Modify: `tests/test_portfolio.py`

**Interfaces:**
- Consumes: existing IDs, classes, `data-track` values, and local demo hrefs from the current page.
- Produces: English strings and `lang="en"`; no class or ID renames.

- [ ] **Step 1: Write failing tests for English copy**

Add to `ContentTest`:

```python
def test_shell_copy_is_english(self):
    self.assertIn('<html lang="en">', HTML)
    self.assertIn('>Skip to content</a>', HTML)
    self.assertIn('Hi, I\'m Alan Nawa, not-a-dev :)', HTML)
    self.assertIn('>View projects<', HTML)
    self.assertIn('>View demo<', HTML)
    for phrase in ('Halo, saya', 'JASA', 'KONTAK', 'Yang sudah saya bangun',
                   'Punya project', 'Lihat project', 'Lihat demo', '3 kanal',
                   '>6 project<'):
        with self.subTest(phrase=phrase):
            self.assertNotIn(phrase, HTML)
```

Update `test_identity_and_copy` so the opening line assertion uses the English sentence.

- [ ] **Step 2: Run the tests and watch them fail**

Run: `python3 -m unittest discover -s tests -v`
Expected: FAIL on the new English assertions.

- [ ] **Step 3: Translate `index.html`**

Use these exact visitor-facing strings:
- `lang="en"`; title `Alan Nawa: Web & AI Automation`.
- Meta description: `Portfolio of Alan Nawa: websites, landing pages, and AI workflow automation. Explore six demos or reach out on Instagram, GitHub, or email.`
- Skip link: `Skip to content`. Brand aria-label: `Alan Nawa, back to top`. Brand subline: `Web & AI Automation`. Nav aria-label: `Main contact`. Menu button aria-label: `Open menu`. Mobile nav aria-label: `Mobile menu`; links `Projects`, `Contact`, plus the three contact names.
- Hero: eyebrow `PORTFOLIO`; hidden `h1` unchanged; role `Web development & AI automation`; intro `Hi, I'm Alan Nawa, not-a-dev :) I build clean websites and automated workflows so your business can respond to customers faster.`; buttons `View projects` and `Instagram`.
- Panel: label `SYS / PORTFOLIO`; rows `web / 6 projects`, `automation / n8n + AI`, `contact / 3 channels`.
- Services: `01 / SERVICES`, `Two ways I can help`, then:
  - `AI & workflow automation`: `Leads arrive, data is cleaned, AI classifies priority, then your team gets a notification and a follow-up draft. The flow runs in n8n and connects to the tools you already use.` Bullets: `Webhooks & API integrations`, `Google Sheets / CRM`, `AI classification and reply drafts`.
  - `Websites & landing pages`: `Pages that explain your offer clearly, load fast, and guide visitors to the next step. From a single landing page to a multi-page site.` Bullets: `Company profiles & catalogs`, `Filters, search, and detail pages`, `Responsive and easy to maintain`.
- Projects: `02 / PROJECTS`, `Things I've built`, filters `All`, `AI Automation`, `Web`; card labels `AUTOMATION` and `WEB`; card link `View demo`. Exact card descriptions:
  - `AI Lead Capture`: `An n8n webhook receives a lead, saves it to Google Sheets, classifies priority with AI, then sends a notification and automated follow-up.`
  - `Servis AC`: `A landing page for AC repair services with a list of services, price estimates, FAQ, and a clear consultation path.`
  - `Ruang Rapi`: `A company profile for an interior studio with a portfolio filter, before/after slider, and consultation form.`
  - `Kedai Kopi Oak`: `A coffee shop landing page with a menu, brand story, venue atmosphere, and a reason to visit.`
  - `Rental Mobil`: `A multi-page site with a catalog, filters, vehicle details, and automatic booking calculation.`
  - `NIGHT//SHIFT`: `A cyberpunk portfolio experiment with interface animation and technical typography.`
  - Tags: `Landing page`, `Responsive`, `FAQ`, `Company profile`, `Gallery`, `Form`, `Multi-page`, `Catalog`, `Booking`, `Experiment`, `Animation`, `Visual`, plus the existing `n8n`, `OpenAI`, `Sheets`, `Slack`.
- Contact: `03 / CONTACT`, `Have a project in mind?`, `Tell me what you need through any channel below. Pick whichever is most comfortable for you.`
- Footer: `Alan Nawa, web & AI automation.` and `View source` with the existing external arrow.

Keep all URLs, handles, `data-project` values, `data-track` values, IDs, and `demos/...` hrefs byte-identical.

- [ ] **Step 4: Run the tests and watch them pass**

Run: `python3 -m unittest discover -s tests -v`
Expected: all tests PASS.

- [ ] **Step 5: Commit**

```bash
git add index.html tests/test_portfolio.py
git commit -m "feat: translate portfolio shell to English"
```

### Task 2: Cyberpunk x TRON visual system

**Files:**
- Modify: `css/styles.css`
- Modify: `tests/test_portfolio.py`

**Interfaces:**
- Consumes: existing class names from `index.html`: `.tron-grid`, `.scanline`, `.site-header`, `.hero`, `.hero-panel`, `.service`, `.project-card`, `.filter-bar`, `.contact-links`, `.site-footer`.
- Produces: `--magenta` token, horizon layer, angular corner treatment, magenta technical accents.

- [ ] **Step 1: Write failing tests for the visual tokens**

Add to `CssContractTest`:

```python
def test_cybertron_tokens(self):
    self.assertIn('--magenta: #ff3d8d', CSS)
    self.assertNotIn('--orange', CSS)
    self.assertIn('.hero::before', CSS)
    self.assertIn('perspective(', CSS)
    self.assertIn('clip-path: polygon(', CSS)

def test_technical_accent_uses_magenta(self):
    self.assertGreaterEqual(CSS.count('var(--magenta)'), 3)
```

- [ ] **Step 2: Run the tests and watch them fail**

Run: `python3 -m unittest discover -s tests -v`
Expected: FAIL on the missing magenta and horizon markers.

- [ ] **Step 3: Update `css/styles.css`**

- Replace `--orange: #ff7a1a;` with `--magenta: #ff3d8d;`. Replace all three `var(--orange)` uses with `var(--magenta)`.
- Add a static horizon layer via `.hero::before`: `pointer-events: none`, `perspective(240px) rotateX(62deg)`, `transform-origin: bottom`, `background: repeating-linear-gradient(90deg, rgba(0, 229, 255, 0.10) 0 1px, transparent 1px 72px), repeating-linear-gradient(0deg, rgba(0, 229, 255, 0.10) 0 1px, transparent 1px 48px)`, anchored to the bottom of `.hero`.
- Give `.hero-panel` a clipped top-right and bottom-left corner with `clip-path: polygon(0 0, calc(100% - 14px) 0, 100% 14px, 100% 100%, 14px 100%, 0 calc(100% - 14px))` on a background pseudo-element, keeping the box itself unclipped so focus rings survive.
- Give `.project-card` a drawn corner notch with a pseudo-element rather than clipping the card box itself, so keyboard focus remains visible.
- Keep cyan as the primary action color and magenta only on indexes, section indexes, and the panel label.

- [ ] **Step 4: Run the tests and watch them pass**

Run: `python3 -m unittest discover -s tests -v`
Expected: all tests PASS.

- [ ] **Step 5: Commit**

```bash
git add css/styles.css tests/test_portfolio.py
git commit -m "feat: apply cyberpunk TRON visual system"
```

### Task 3: Finite entrance and interaction motion

**Files:**
- Modify: `css/styles.css`
- Modify: `tests/test_portfolio.py`

**Interfaces:**
- Consumes: the visual tokens from Task 2 and the existing `:focus-visible`, `:hover`, `:active`, and `prefers-reduced-motion` blocks.
- Produces: one finite keyframe animation, capped motion budget, stronger hover/press feedback.

- [ ] **Step 1: Write failing motion tests**

Replace `test_no_endless_motion` with:

```python
def test_motion_is_finite_and_capped(self):
    self.assertTrue(CSS)
    self.assertNotIn('infinite', CSS)
    self.assertLessEqual(CSS.count('@keyframes'), 2)
    self.assertIn('@keyframes hero-in', CSS)
    self.assertIn('animation: hero-in', CSS)

def test_motion_stops_under_reduced_motion(self):
    block = CSS.split('@media (prefers-reduced-motion: reduce)')[1]
    self.assertIn('animation: none', block)
    self.assertIn('transform: none', block)
```

- [ ] **Step 2: Run the tests and watch them fail**

Run: `python3 -m unittest discover -s tests -v`
Expected: FAIL because no `hero-in` keyframe exists.

- [ ] **Step 3: Add finite motion in `css/styles.css`**

- Define one `@keyframes hero-in` using opacity and a small `translateY` (at most 14px), duration 700ms, `both` fill mode.
- Apply it to `.hero-copy > *` with delays `0ms`, `80ms`, `160ms`, `240ms` for children 1 to 4 and `240ms` for child 5. No JavaScript class toggle, no loop.
- Add a 2px card hover lift and a 1px control press offset using `transform`, with transitions under 250ms.
- In the existing `@media (prefers-reduced-motion: reduce)` block, set `animation: none` and `transform: none` for the animated selectors.

- [ ] **Step 4: Run the tests and watch them pass**

Run: `python3 -m unittest discover -s tests -v`
Expected: all tests PASS.

- [ ] **Step 5: Commit**

```bash
git add css/styles.css tests/test_portfolio.py
git commit -m "feat: add finite cyberpunk entrance motion"
```

### Task 4: Documentation and delivery checks

**Files:**
- Modify: `README.md`
- No production code changes.

**Interfaces:**
- Consumes: English strings, `--magenta`, finite motion, and the six local demos from Tasks 1 to 3.
- Produces: README that matches the shipped page.

- [ ] **Step 1: Write a failing README test**

Add to `DeliveryTest`:

```python
def test_readme_describes_english_cybertron_shell(self):
    readme = read('README.md')
    self.assertIn('English', readme)
    self.assertIn('cyberpunk', readme.lower())
    self.assertIn('demos/', readme)
    self.assertNotIn('Omegamoto', readme)
```

- [ ] **Step 2: Run the tests and watch them fail**

Run: `python3 -m unittest discover -s tests -v`
Expected: FAIL on the missing README terms.

- [ ] **Step 3: Update `README.md`**

State that the shell copy is English, describe the cyberpunk x TRON palette and finite motion, keep the folder map and local demo table, and keep the note that demo contents are unchanged.

- [ ] **Step 4: Run the full verification set**

Run:

```bash
python3 -m unittest discover -s tests -v
xmllint --html --noout index.html
python3 -m http.server 8086 >/tmp/opencode/cybertron-http.log 2>&1 &
pid=$!
sleep 1
for path in / /css/styles.css /js/main.js /assets/favicon.svg \
  /demos/ai-lead-capture/dashboard/index.html \
  /demos/servis-ac/index.html \
  /demos/ruang-rapi/index.html \
  /demos/kedai-kopi/index.html \
  /demos/rental-mobil/index.html \
  /demos/nightshift/index.html; do
  curl -s -o /dev/null -w "%{http_code} $path\\n" "http://127.0.0.1:8086$path"
done
kill "$pid"
python3 /home/asnodt/.config/opencode/skills/antislop-human/contrast-check.py '#ff3d8d' '#05070c'
python3 /home/asnodt/.config/opencode/skills/antislop-human/contrast-check.py '#ff3d8d' '#090e17'
```

Expected: tests all PASS, `xmllint` exit 0, ten HTTP `200` lines, and both contrast ratios at least 4.5:1.

- [ ] **Step 5: Commit**

```bash
git add README.md
git commit -m "docs: describe English cyberpunk portfolio"
```
