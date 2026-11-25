import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    file = ROOT / path
    return file.read_text(encoding="utf-8") if file.exists() else ""


HTML = read("index.html")
CSS = read("css/styles.css")
JS = read("js/main.js")


class ContentTest(unittest.TestCase):
    def test_identity_and_copy(self):
        self.assertIn("Alan Nawa", HTML)
        self.assertIn("Hi, I'm Alan Nawa, not-a-dev :)", HTML)
        self.assertIn("https://instagram.com/zhahenzar", HTML)
        self.assertIn("zhahenza666@proton.me", HTML)
        self.assertIn("https://github.com/zhahenza44", HTML)

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

    def test_six_project_cards(self):
        self.assertEqual(HTML.count('class="project-card'), 6)
        for title in ("AI Lead Capture", "Servis AC", "Ruang Rapi", "Kedai Kopi Oak",
                      "Rental Mobil", "NIGHT//SHIFT"):
            with self.subTest(title=title):
                self.assertIn(title, HTML)
        self.assertNotIn("Omegamoto", HTML)

    def test_local_demo_links(self):
        expected = {
            "ai-lead-capture": "demos/ai-lead-capture/dashboard/index.html",
            "servis-ac": "demos/servis-ac/index.html",
            "ruang-rapi": "demos/ruang-rapi/index.html",
            "kedai-kopi": "demos/kedai-kopi/index.html",
            "rental-mobil": "demos/rental-mobil/index.html",
            "nightshift": "demos/nightshift/index.html",
        }
        for project, path in expected.items():
            with self.subTest(project=project):
                card = re.search(
                    rf'<article class="project-card"[^>]*data-project="{project}".*?</article>',
                    HTML, re.S)
                self.assertIsNotNone(card)
                self.assertIn(f'href="{path}"', card.group(0))
                self.assertTrue((ROOT / path).is_file(), f"missing {path}")
        self.assertNotIn("github.com/zhahenza44/otomasi-web/tree/main", HTML)

    def test_counts_match_cards(self):
        self.assertIn("6 project", HTML)
        self.assertNotIn("7 project", HTML)
        self.assertIn("SIX LIVE DEMOS", HTML)

    def test_job_prefixes_removed_and_heading_hidden(self):
        self.assertNotIn("JOB 1 /", HTML)
        self.assertNotIn("JOB 2 /", HTML)
        self.assertIn('<h1 class="sr-only">Alan Nawa</h1>', HTML)
        self.assertIn(".sr-only", CSS)

    def test_footer_source_label(self):
        self.assertIn("View source", HTML)
        self.assertNotIn("View source &amp; demo", HTML)

    def test_forbidden_contact(self):
        self.assertTrue(HTML)
        for phrase in ("wa.me", "whatsapp", "projects.co.id"):
            self.assertNotIn(phrase, HTML.lower())

    def test_sections_and_controls(self):
        for marker in ('class="skip-link"', 'id="project-grid"', 'id="filter-all"',
                       'id="filter-job1"', 'id="filter-job2"', 'id="menu-toggle"',
                       'id="mobile-menu"', 'id="contact"', "<main", "<footer"):
            self.assertIn(marker, HTML)

    def test_honest_copy_and_no_em_dash(self):
        self.assertTrue(HTML)
        self.assertNotIn("\u2014", HTML)
        self.assertNotIn("TERSEDIA UNTUK PROJECT", HTML)
        self.assertNotIn("status-dot", HTML)
        self.assertNotIn("<b>online</b>", HTML)
        self.assertNotIn("satu hari kerja", HTML)


class CssContractTest(unittest.TestCase):
    def test_tron_tokens(self):
        for token in ("--bg:", "--cyan:", "--magenta:", "--line:", "color-scheme: dark"):
            self.assertIn(token, CSS)

    def test_cybertron_tokens(self):
        self.assertIn('--magenta: #ff3d8d', CSS)
        self.assertNotIn('--orange', CSS)
        self.assertIn('.hero::before', CSS)
        self.assertIn('perspective(', CSS)
        self.assertIn('clip-path: polygon(', CSS)

    def test_technical_accent_uses_magenta(self):
        self.assertGreaterEqual(CSS.count('var(--magenta)'), 3)

    def test_grid_and_scanline(self):
        for marker in (".tron-grid", ".scanline", "mask-image"):
            self.assertIn(marker, CSS)

    def test_tap_targets_and_cursor(self):
        self.assertTrue(CSS)
        self.assertIn("cursor: pointer", CSS)
        self.assertIn("min-height: 44px", CSS)

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

    def test_motion_stops_under_reduced_motion(self):
        block = CSS.split('@media (prefers-reduced-motion: reduce)')[1]
        self.assertIn('animation: none', block)
        self.assertIn('transform: none', block)
        for selector in ('.hero-copy > *', '.btn--primary:active', '.card-link',
                         '.contact-links a:hover'):
            with self.subTest(selector=selector):
                self.assertIn(selector, block)

    def test_entrance_focus_is_visible(self):
        self.assertIn('.hero-actions:focus-within', CSS)
        focus_block = CSS.split('.hero-actions:focus-within')[1].split('}')[0]
        self.assertIn('animation: none', focus_block)
        self.assertIn('opacity: 1', focus_block)

    def test_interactive_states_and_boundaries(self):
        self.assertTrue(CSS)
        self.assertIn("--line-strong: rgba(0, 229, 255, 0.45)", CSS)
        self.assertIn(".filter-bar button:active", CSS)
        self.assertIn(".contact-links a:active", CSS)
        self.assertIn(".menu-toggle:active", CSS)

    def test_responsive_reflow(self):
        for marker in ("@media (max-width: 900px)", "@media (max-width: 560px)", "grid-template-columns"):
            self.assertIn(marker, CSS)
        self.assertIn(".project-grid {", CSS)

    def test_narrow_viewport_guard(self):
        self.assertIn("overflow-wrap: anywhere", CSS)
        self.assertIn("min-width: 0", CSS)

    def test_reduced_motion_and_focus(self):
        self.assertIn("@media (prefers-reduced-motion: reduce)", CSS)
        self.assertIn("animation: none", CSS)
        self.assertIn(":focus-visible", CSS)

    def test_no_external_assets(self):
        self.assertTrue(CSS)
        self.assertNotIn("http", CSS)

    def test_glow_dose_cap(self):
        self.assertTrue(CSS)
        self.assertNotIn("box-shadow: inset", CSS)
        self.assertEqual(CSS.count("text-shadow:"), 1)


class InteractionTest(unittest.TestCase):
    def test_filter_controls_semantics(self):
        for marker in ('aria-pressed="true"', 'data-filter="all"', 'data-filter="job1"',
                       'data-filter="job2"', 'role="group"'):
            self.assertIn(marker, HTML)

    def test_filter_logic_markers(self):
        for marker in ("function applyFilter", "card.dataset.track", "card.hidden",
                       "setAttribute('aria-pressed'", "filterButtons"):
            self.assertIn(marker, JS)

    def test_mobile_menu_markers(self):
        for marker in ("menuToggle", "aria-expanded", "event.key === 'Escape'", "inert"):
            self.assertIn(marker, JS)

    def test_no_whatsapp_in_js(self):
        self.assertTrue(JS)
        self.assertNotIn("whatsapp", JS.lower())

    def test_shell_js_copy_is_english(self):
        self.assertTrue(JS)
        self.assertIn('isOpen ? "Close menu" : "Open menu"', JS)
        for phrase in ("Buka menu", "Tutup menu"):
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, JS)

    def test_motion_toggle_logic(self):
        for marker in ('const motionToggle', 'function setMotionPaused',
                       "classList.toggle('motion-paused'", "setAttribute('aria-pressed'"):
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


class DeliveryTest(unittest.TestCase):
    def test_readme_has_no_forbidden_contacts(self):
        readme = read("README.md")
        self.assertTrue(readme, "README.md must exist")
        for phrase in ("wa.me", "whatsapp", "projects.co.id"):
            self.assertNotIn(phrase, readme.lower())
        self.assertIn("index.html", readme)

    def test_full_content(self):
        self.assertEqual(HTML.count('class="project-card'), 6)

    def test_readme_lists_local_demos(self):
        readme = read("README.md")
        self.assertIn("demos/", readme)
        self.assertNotIn("tujuh demo", readme)

    def test_readme_describes_english_cybertron_shell(self):
        readme = read("README.md")
        self.assertIn("English", readme)
        self.assertIn("cyberpunk", readme.lower())
        self.assertIn("demos/", readme)
        self.assertNotIn("Omegamoto", readme)

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


if __name__ == "__main__":
    unittest.main()
