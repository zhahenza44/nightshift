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
            'id="studio"', 'id="cv"', 'id="work"', 'id="process"',
            'id="contact"', 'class="site-footer"', 'id="project-dialog"',
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, HTML)

    def test_english_navigation_and_actions(self):
        for marker in (
            '>Skip to content</a>',
            'aria-label="NIGHT SHIFT, back to top"',
            'aria-label="Main navigation"',
            'aria-label="Mobile navigation"',
            ">OPEN FOR Q1 2027</span>",
            "<span>Start a project</span>",
            'aria-label="Open menu"',
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, HTML)
        for marker in (
            '<a href="#cv"><span>02</span>CV</a>',
            '<a href="#work"><span>03</span>Work &amp; Services</a>',
            '<a href="#process"><span>04</span>Process</a>',
            '<a href="#contact"><span>05</span>Contact</a>',
        ):
            with self.subTest(nav=marker):
                self.assertEqual(HTML.count(marker), 2)

    def test_hero_copy_is_english(self):
        for marker in (
            'aria-label="Webs that cannot be ignored."',
            ">WEBS THAT</span>",
            ">CANNOT BE</span>",
            'id="hero-scramble">IGNORED.</span>',
            ">DIGITAL STUDIO</span>",
            ">EST. 2026</span>",
            "landing pages, company profiles, and AI automation systems",
            "<span>Start a project</span>",
            "<span>View work</span>",
            "<dt>Projects</dt>",
            "<dt>Response</dt>",
            "<span>h</span>",
            ">SCROLL TO EXPLORE</span>",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, HTML)
        self.assertNotIn("EST. 2020", HTML)

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
            ">WORK &amp; SERVICES</span>",
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
            "<span>Email</span>",
            'aria-label="Case file details"',
            'aria-label="Close case file"',
            ">CLOSE ×</button>",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, HTML)

    def test_contact_actions_use_instagram_dm_and_boxed_github(self):
        for marker in (
            '<a class="btn btn--primary magnetic" href="mailto:zhahenza666@proton.me"><span>Email</span><i>↗</i></a>',
            '<a class="btn btn--ghost" id="send-message" href="https://ig.me/m/zhahenzar" target="_blank" rel="noopener"><span>Send message</span><i>↗</i></a>',
            '<a class="btn btn--ghost" href="https://github.com/zhahenza44/otomasi-web" target="_blank" rel="noopener"><span>GITHUB</span><i>↗</i></a>',
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, HTML)
        for phrase in (
            'id="copy-email"', 'Copy email', 'Send brief', 'EMAIL <span>↗</span>',
            'class="contact-links', 'id="toast"',
        ):
            with self.subTest(absent=phrase):
                self.assertNotIn(phrase, HTML)
        for phrase in ('navigator.clipboard.writeText', 'showToast', 'copy-email', 'EMAIL COPIED'):
            with self.subTest(absent_js=phrase):
                self.assertNotIn(phrase, JS)

    def test_old_shell_contract_is_absent(self):
        for phrase in (
            "motion-toggle",
            "Pause motion",
            "id=\"project-grid\"",
            "id=\"filter-all\"",
            "class=\"sr-only\"",
            "data-track=",
            "filterButtons",
        ):
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, HTML)
        self.assertNotIn("data-track=", HTML)

    def test_section_numbering_and_nav(self):
        for marker in (
            '<span class="section-index">02</span>',
            '>MANIFESTO</span>',
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, HTML)
        for marker in (
            '<a href="#cv"><span>02</span>CV</a>',
            '<a href="#work"><span>03</span>Work &amp; Services</a>',
            '<a href="#process"><span>04</span>Process</a>',
            '<a href="#contact"><span>05</span>Contact</a>',
        ):
            with self.subTest(nav=marker):
                self.assertEqual(HTML.count(marker), 2)
        for phrase in ('href="#services"', 'id="services"'):
            with self.subTest(absent=phrase):
                self.assertNotIn(phrase, HTML)
        studio = HTML.find('id="studio"')
        cv = HTML.find('id="cv"')
        work = HTML.find('id="work"')
        self.assertGreater(cv, -1)
        self.assertLess(studio, cv)
        self.assertLess(cv, work)

    def test_merged_work_and_services_contract(self):
        for marker in (
            '>WORK &amp; SERVICES</span>',
            '<span class="section-index">03</span>',
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, HTML)
        order = ('studio', 'cv', 'work', 'process', 'contact')
        positions = [HTML.find('id="' + section + '"') for section in order]
        self.assertTrue(all(position > -1 for position in positions), str(positions))
        self.assertEqual(positions, sorted(positions))

    def test_surabaya_and_github_label(self):
        for marker in (
            '<span class="brand-meta">DIGITAL STUDIO</span>',
            '<span>SURABAYA, ID</span>',
            '<dd>Surabaya, ID</dd>',
            '<span class="t-key">location</span>: surabaya, id',
            '<div class="terminal-foot"><span>SURABAYA, ID</span>',
            '<a class="btn btn--ghost" href="https://github.com/zhahenza44/otomasi-web" target="_blank" rel="noopener"><span>GITHUB</span><i>↗</i></a>',
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, HTML)
        for phrase in (
            'JKT', 'Jakarta', 'jakarta', 'SOURCE <span>↗</span>',
            'DIGITAL STUDIO<br>SURABAYA, ID',
            '<span class="mono">SURABAYA, ID</span>',
        ):
            with self.subTest(absent=phrase):
                self.assertNotIn(phrase, HTML)

    def test_hero_stats_contract(self):
        for marker in (
            '<div><dt>Projects</dt><dd><span class="count" data-count="1">1</span></dd></div>',
            '<div><dt>Response</dt><dd>&lt;24<span>h</span></dd></div>',
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, HTML)
        for phrase in ('<dt>Experience</dt>', 'data-count="40"', 'data-count="6"'):
            with self.subTest(absent=phrase):
                self.assertNotIn(phrase, HTML)

    def test_cv_identity_and_services(self):
        for marker in (
            "Alan Nawa",
            "Web &amp; AI Automation",
            "Hi, I'm Alan Nawa",
            "I build clean websites and automated workflows",
            "AI &amp; workflow automation",
            "Websites &amp; landing pages",
            "Webhooks &amp; API integrations",
            "Google Sheets / CRM",
            "Company profiles &amp; catalogs",
            "Responsive and easy to maintain",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, HTML)

    def test_cv_demo_links(self):
        paths = (
            "demos/ai-lead-capture/dashboard/index.html",
            "demos/servis-ac/index.html",
            "demos/ruang-rapi/index.html",
            "demos/kedai-kopi/index.html",
            "demos/rental-mobil/index.html",
            "demos/nightshift/index.html",
        )
        names = (
            "AI Lead Capture",
            "Servis AC",
            "Ruang Rapi",
            "Kedai Kopi Oak",
            "Rental Mobil",
            "NIGHT//SHIFT",
        )
        for path in paths:
            with self.subTest(path=path):
                self.assertIn('href="' + path + '"', HTML)
        for name in names:
            with self.subTest(name=name):
                self.assertIn(name, HTML)
        self.assertEqual(HTML.count('href="demos/'), len(paths))
        anchors = re.findall(r'<a[^>]+href="demos/[^"]+"[^>]*>', HTML)
        for anchor in anchors:
            with self.subTest(anchor=anchor):
                self.assertIn('target="_blank"', anchor)
                self.assertIn('rel="noopener noreferrer"', anchor)

    def test_cv_contacts(self):
        for marker in (
            'href="https://instagram.com/zhahenzar"',
            'href="https://github.com/zhahenza44"',
            'href="mailto:zhahenza666@proton.me"',
            "@zhahenzar",
            "zhahenza44",
            "zhahenza666@proton.me",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, HTML)

    def test_cv_note_and_fictional_disclosure(self):
        self.assertIn("This section is my real CV", HTML)
        self.assertNotIn("names, metrics, email, and phone number are fictional", HTML)
        self.assertNotIn('class="demo-note"', HTML)

    def test_fictional_contact_and_footer_label_are_gone(self):
        self.assertNotIn("hello@nightshift.studio", HTML)
        self.assertNotIn("HELLO@NIGHTSHIFT.STUDIO", HTML)
        self.assertNotIn("https://wa.me/6281234567890", HTML)
        self.assertNotIn(">WHATSAPP <", HTML)
        self.assertNotIn("DEMO CONCEPT / FICTIONAL STUDIO", HTML)

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


class ProcessContactTest(unittest.TestCase):
    def test_process_step_numbers_are_roman(self):
        block = re.search(r'<ol class="process-list" id="process-list">.*?</ol>', HTML, re.S)
        self.assertIsNotNone(block)
        numbers = re.findall(r'<span class="step-no">([^<]+)</span>', block.group(0))
        self.assertEqual(numbers, ["I", "II", "III", "IV", "V"])
        nav_numbers = re.findall(r'<a href="#(?:process|contact)"><span>(\d+)</span>', HTML)
        self.assertEqual(nav_numbers, ["04", "05", "04", "05"])


class CssContractTest(unittest.TestCase):
    def test_stylesheet_is_copied_from_demo(self):
        demo_css = read("demos/nightshift/css/styles.css")
        self.assertTrue(CSS)
        self.assertTrue(demo_css)
        removed_from_demo = {".contact-links", ".is-visible", ".toast"}
        markers = sorted(set(re.findall(r"@keyframes\s+[\w-]+|[.#][A-Za-z][\w-]*", demo_css)) - removed_from_demo)
        for marker in markers:
            with self.subTest(marker=marker):
                self.assertIn(marker, CSS)
        for marker in (".cv-grid", ".cv-service", ".cv-demo-list"):
            with self.subTest(cv_marker=marker):
                self.assertIn(marker, CSS)

    def test_nightshift_visual_markers(self):
        for marker in (
            "@keyframes boot-line", "@keyframes orb-spin", "@keyframes ticker",
            "@keyframes footer-marquee", ".fx-scan", ".cursor-ring",
            ".project-dialog", ".hero-horizon", ".hero-rings",
            "@media (prefers-reduced-motion: reduce)", ":focus-visible",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, CSS)

    def test_cv_styles_use_existing_tokens(self):
        start = CSS.find(".cv-grid")
        self.assertGreater(start, -1)
        end = CSS.find("@media (prefers-reduced-motion", start)
        block = CSS[start:end] if end > start else CSS[start:]
        for token in ("var(--cyan)", "var(--muted)"):
            with self.subTest(token=token):
                self.assertIn(token, block)

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
            "dialog.showModal()", "dialog.close()",
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
            "fictional case study for portfolio use",
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

    def test_github_pages_cname_is_pinned(self):
        self.assertEqual(read("CNAME"), "nightshift.is-not-a.dev\n")

    def test_browser_smoke_ignores_only_font_download_errors(self):
        smoke = read("tests/browser_smoke.py")
        for marker in (
            "downloadable font: download failed",
            "fonts.gstatic.com",
            'event.get("params", {}).get("level") == "error"',
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, smoke)

    def test_nightshift_plan_exists(self):
        self.assertIn("NightShift becomes the main landing page",
                      read("docs/superpowers/plans/2026-11-25-nightshift-main-landing.md"))


if __name__ == "__main__":
    unittest.main()
