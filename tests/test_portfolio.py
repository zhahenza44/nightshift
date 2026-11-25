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
        self.assertIn("Halo, saya Alan Nawa, not-a-dev :)", HTML)
        self.assertIn("https://instagram.com/zhahenzar", HTML)
        self.assertIn("zhahenza666@proton.me", HTML)
        self.assertIn("https://github.com/zhahenza44", HTML)

    def test_seven_project_cards(self):
        self.assertEqual(HTML.count('class="project-card'), 7)
        for title in ("AI Lead Capture", "Servis AC", "Ruang Rapi", "Kedai Kopi Oak",
                      "Rental Mobil", "Omegamoto", "NIGHT//SHIFT"):
            with self.subTest(title=title):
                self.assertIn(title, HTML)

    def test_omegamoto_has_no_link(self):
        card = re.search(r'<article class="project-card"[^>]*data-project="omegamoto".*?</article>', HTML, re.S)
        self.assertIsNotNone(card)
        self.assertNotIn("href=", card.group(0))

    def test_link_targets(self):
        for path in (
            "job1-otomasi-ai-workflow/workspace/demo-ai-lead-capture",
            "job2-web-landing-maintenance/workspace/demo-landingpage-servis-ac",
            "job2-web-landing-maintenance/workspace/demo-company-profile-ruang-rapi",
            "job2-web-landing-maintenance/workspace/demo-landingpage-kedai-kopi",
            "job2-web-landing-maintenance/workspace/demo-rental-mobil-multipage",
            "job2-web-landing-maintenance/workspace/demo-portfolio-cyberpunk",
        ):
            with self.subTest(path=path):
                self.assertIn(f"https://github.com/zhahenza44/otomasi-web/tree/main/{path}", HTML)

    def test_forbidden_contact(self):
        for phrase in ("wa.me", "whatsapp", "projects.co.id"):
            self.assertNotIn(phrase, HTML.lower())

    def test_sections_and_controls(self):
        for marker in ('class="skip-link"', 'id="project-grid"', 'id="filter-all"',
                       'id="filter-job1"', 'id="filter-job2"', 'id="menu-toggle"',
                       'id="mobile-menu"', 'id="contact"', "<main", "<footer"):
            self.assertIn(marker, HTML)


if __name__ == "__main__":
    unittest.main()
