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
    def test_document_shell_is_translated_nightshift(self):
        for marker in (
            '<html lang="en" class="no-js">',
            "<title>NIGHT//SHIFT — Digital Studio</title>",
            '<meta name="theme-color" content="#050609">',
            "https://fonts.googleapis.com/css2?family=Chakra+Petch",
            "https://fonts.gstatic.com",
            'document.documentElement.classList.remove("no-js")',
            'document.documentElement.classList.add("js")',
            '<script src="js/main.js" defer></script>',
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, HTML)

    def test_meta_copy_is_english(self):
        self.assertIn('name="description" content="NIGHT//SHIFT is a fictional digital studio', HTML)
        self.assertIn('property="og:title" content="NIGHT//SHIFT — Digital Studio"', HTML)
        self.assertIn('property="og:description" content="Webs that cannot be ignored.', HTML)

    def test_nightshift_sections_exist(self):
        for marker in (
            'id="boot"', 'class="boot-log"', 'class="boot-bar"', 'id="cursor"',
            'id="cursor-ring"', 'class="cursor-label"', 'class="fx-noise"',
            'class="fx-scan"', 'id="scroll-progress"', 'id="site-header"',
            'id="mobile-menu"', 'class="hero" id="top"', 'class="ticker"',
            'id="studio"', 'id="work"', 'id="services"', 'id="process"',
            'id="contact"', 'class="site-footer"', 'id="project-dialog"', 'id="toast"',
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, HTML)

    def test_english_navigation_and_actions(self):
        for marker in (
            '>Skip to content</a>',
            'aria-label="NIGHT SHIFT, back to top"',
            'aria-label="Main navigation"',
            'aria-label="Mobile navigation"',
            '<a href="#work"><span>01</span>Work</a>',
            '<a href="#services"><span>02</span>Services</a>',
            '<a href="#process"><span>03</span>Process</a>',
            '<a href="#contact"><span>04</span>Contact</a>',
            ">OPEN FOR Q1 2027</span>",
            "<span>Start a project</span>",
            'aria-label="Open menu"',
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, HTML)

    def test_hero_copy_is_english(self):
        for marker in (
            'aria-label="Webs that cannot be ignored."',
            ">WEBS THAT</span>",
            ">CANNOT BE</span>",
            'id="hero-scramble">IGNORED.</span>',
            ">DIGITAL STUDIO</span>",
            ">EST. 2020</span>",
            "landing pages, company profiles, and AI automation systems",
            "<span>Start a project</span>",
            "<span>View work</span>",
            "<dt>Projects</dt>",
            "<dt>Experience</dt>",
            "<dt>Response</dt>",
            "<span>h</span>",
            ">SCROLL TO EXPLORE</span>",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, HTML)

    def test_three_case_files_and_fictional_metrics(self):
        for title in ("HYPERMART", "AEGIS", "VOID HOTEL"):
            with self.subTest(title=title):
                self.assertIn("<h3>" + title + "</h3>", HTML)
        for metric in ("+38%", "120+", "2.4s", "-72%", "84%", "24/7",
                       "+54%", "-31%", "4.8/5"):
            with self.subTest(metric=metric):
                self.assertIn(metric, HTML)
        self.assertEqual(HTML.count('data-open-project='), 3)

    def test_sections_and_disclosure_are_english(self):
        for marker in (
            ">MANIFESTO</span>",
            ">SELECTED WORK</span>",
            ">CAPABILITIES</span>",
            ">PROCESS</span>",
            ">CONTACT</span>",
            "Three fictional case studies",
            "Four things we take seriously",
            "AVG. TIMELINE 2–4 WEEKS",
            "Brief &amp; discovery",
            "Structure &amp; visual direction",
            "Design &amp; development",
            "QA &amp; handover",
            "Maintenance",
            "HAVE AN IDEA?",
            "SEND A SIGNAL.",
            "Tell us about the project.",
            "<span>Send brief</span>",
            "<span>Copy email</span>",
            "names, metrics, email, and phone number are fictional",
            "fictional case study for portfolio use",
            'aria-label="Case file details"',
            'aria-label="Close case file"',
            ">CLOSE ×</button>",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, HTML)

    def test_old_shell_contract_is_absent(self):
        for phrase in (
            "Alan Nawa",
            "not-a-dev",
            "https://instagram.com/zhahenzar",
            "zhahenza666@proton.me",
            'href="https://github.com/zhahenza44"',
            'href="demos/',
            "motion-toggle",
            "Pause motion",
            "id=\"project-grid\"",
            "id=\"filter-all\"",
            "class=\"sr-only\"",
            "SIX LIVE DEMOS",
        ):
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, HTML)
        self.assertNotIn('class="project-card', HTML)

    def test_no_indonesian_visitor_copy_in_html(self):
        words = (
            "yang", "dan", "untuk", "dengan", "tidak", "bukan", "kami", "kamu",
            "lebih", "dari", "dalam", "tanpa", "sebelum", "setelah", "atau",
            "juga", "pada", "dapat", "membuat", "membangun", "merancang",
            "menjadi", "mereka", "proyek", "karya", "tampilan", "waktu",
            "fiktif", "metrik", "studi kasus", "nomor telepon", "tersalin",
            "buka menu", "tutup menu", "kirim brief", "lihat karya",
        )
        for word in words:
            with self.subTest(word=word):
                self.assertIsNone(re.search(r"\b" + re.escape(word) + r"\b", HTML, re.I))

    def test_favicon_is_copied_from_demo(self):
        self.assertEqual(read("assets/favicon.svg"), read("demos/nightshift/assets/favicon.svg"))


class CssContractTest(unittest.TestCase):
    def test_stylesheet_is_copied_from_demo(self):
        self.assertTrue(CSS)
        self.assertEqual(CSS, read("demos/nightshift/css/styles.css"))

    def test_nightshift_visual_markers(self):
        for marker in (
            "@keyframes boot-line", "@keyframes orb-spin", "@keyframes ticker",
            "@keyframes footer-marquee", ".fx-scan", ".cursor-ring",
            ".project-dialog", ".hero-horizon", ".hero-rings",
            "@media (prefers-reduced-motion: reduce)", ":focus-visible",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, CSS)

    def test_external_font_request_is_present(self):
        self.assertIn("https://fonts.googleapis.com", HTML)


class InteractionTest(unittest.TestCase):
    def test_boot_and_hero_markers(self):
        for marker in (
            'has("noboot")', "function animateCount", "function startScramble",
            "requestAnimationFrame", "classList.add(\"is-ready\")",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, JS)

    def test_ghost_cursor_and_magnetic_markers(self):
        for marker in (
            "function ghostSequence", "showScanBox", "setGhost",
            "$$(\".magnetic\")", "mousemove", "mouseleave",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, JS)

    def test_menu_dialog_copy_clock_and_nav_markers(self):
        for marker in (
            'open ? "Close menu" : "Open menu"', 'event.key === "Escape"',
            "dialog.showModal()", "dialog.close()", "navigator.clipboard.writeText",
            'showToast(`EMAIL COPIED — ${email}`)', '"Copied"',
            'new Intl.DateTimeFormat("en-GB"', "IntersectionObserver",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, JS)

    def test_case_file_copy_is_english(self):
        for marker in (
            'kicker: "CASE FILE 01 / E-COMMERCE"',
            'kicker: "CASE FILE 02 / AI AUTOMATION"',
            'kicker: "CASE FILE 03 / HOSPITALITY"',
            '["YEAR", "2026"]', '["ROLE",', '["STACK",',
            "<h4>Challenge</h4>", "<h4>Approach</h4>",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, JS)

    def test_no_indonesian_visitor_copy_in_js(self):
        words = (
            "yang", "dan", "untuk", "dengan", "tidak", "bukan", "kami", "kamu",
            "lebih", "dari", "dalam", "tanpa", "sebelum", "setelah", "atau",
            "juga", "pada", "dapat", "membuat", "membangun", "merancang",
            "menjadi", "mereka", "proyek", "karya", "tampilan", "waktu",
            "fiktif", "metrik", "studi kasus", "nomor telepon", "tersalin",
            "buka menu", "tutup menu", "detail studi kasus",
        )
        for word in words:
            with self.subTest(word=word):
                self.assertIsNone(re.search(r"\b" + re.escape(word) + r"\b", JS, re.I))

    def test_old_shell_interaction_contract_is_absent(self):
        for marker in (
            "applyFilter", "setMotionPaused", "motion-paused", "--mag-x",
            "reveal-pending", "filterButtons",
        ):
            with self.subTest(marker=marker):
                self.assertNotIn(marker, JS)


class DeliveryTest(unittest.TestCase):
    def test_docs_exist(self):
        for path in ("README.md", "PRODUCT.md"):
            with self.subTest(path=path):
                self.assertTrue(read(path), path + " must exist")

    def test_nightshift_plan_exists(self):
        self.assertIn("NightShift becomes the main landing page",
                      read("docs/superpowers/plans/2026-11-25-nightshift-main-landing.md"))


if __name__ == "__main__":
    unittest.main()
