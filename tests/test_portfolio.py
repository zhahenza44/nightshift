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


if __name__ == "__main__":
    unittest.main()
