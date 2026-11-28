# CV Third Service Card Design

Short design for the owner's follow-up request on 2026-11-28, approved in conversation after the earlier scraping bullet shipped, then revised when the owner rejected the slider in favour of a card below the existing two.

## Intent

The owner rejected the scraping bullet as the home for the first job. Web scraping is its own service, alongside AI and workflow automation and websites and landing pages. The third service gets its own CV card placed below the two existing cards. No slider, no new controls, and no new motion.

## Goals

- Give each service its own CV card: `AI & workflow automation`, `Websites & landing pages`, and `Web Scraping`.
- Keep the first two cards side by side on wide screens and stacked on narrow screens, as they are today.
- Place the `Web Scraping` card below them, spanning the full CV grid width.
- Update the static tests, rendered smoke, and owner docs to match the three-card structure.
- Push the verified change to `origin/master`, as requested for the earlier change and confirmed again here.

## Non-goals

- No slider, no scroll-snap, no carousel controls, and no change to `js/main.js`.
- No seventh real case, no fifth capability module, and no change to `06 REAL / 03 FICTIONAL / 04 MODULES`.
- No new link on the page and no new folder or file inside `demos/`.
- No new section boundary between the CV and the fictional case studies.
- No edit or second push to `web-scraping-portfolio`; that clone stays a reference copy.
- No branch, merge, or pull request.

## Constraints

- Visitor-facing copy stays English. The Indonesian README in the reference repo is a source of facts, not page copy.
- Existing demo titles, descriptions, tags, hrefs, labels, and counts stay verbatim.
- `demos/` stays byte-identical and `git diff --stat -- demos` stays empty.
- Unit tests and rendered smoke stay green at 390px, 320px, reduced motion, and 1366px.
- The two existing cards keep their current wording, except that the scraping bullet is removed from the first card.
- Design dials stay ENERGY 3 / RHYTHM 3 / MOTION 3 from `PRODUCT.md`. No new animation is added.
- No em dash in any new copy.

## Approaches considered

1. **Scraping bullet inside `AI & workflow automation`, the shipped version.** Smallest change, but the owner now wants a separate service. Replaced.
2. **Three-card horizontal slider, proposed then rejected by the owner.** Keeps cards side by side at every width, but adds controls, JS state, and motion that the owner does not want. Rejected.
3. **Static three-column grid.** No controls, but narrow screens squeeze the cards. Rejected.
4. **Third card below the first two, chosen.** One CSS span rule, no JS, no new interactive element, and the existing narrow-screen stacking already works.

## Decisions

- The `.cv-grid` keeps its two-column layout for the intro and spec panel. The two existing service cards stay in their current positions.
- A third `<article class="cv-service cv-service--wide reveal">` is added after the second card. One rule, `.cv-service--wide { grid-column: 1 / -1; }`, makes it span both columns on wide screens. Below 860px the grid is already one column, so no extra breakpoint is needed.
- Purpose, written down per R-31: the full-width span keeps the third card readable without shrinking the two cards above it, and avoids adding a carousel to a CV section that has no browsing task.
- First card loses the scraping bullet and keeps its original four bullets. Second card is unchanged. Third card is `Web Scraping` with index `03`.
- Third card description: `E-commerce price and catalog scraping, job and property listings, and scheduled monitoring. Data is cleaned and saved as CSV, Excel, or JSON.` Bullets: `Scrapy and Playwright`, `CSS and XPath selectors`, `JSON APIs and data pipelines`. All three bullets come from the reference repo README.
- Static tests pin three cards, the order of bullets inside each card, and the full-width CSS hook. The rendered smoke keeps its existing viewport, overflow, and reduced-motion checks, plus one check that the third card fits the grid at 320px.
- `PRODUCT.md` and `README.md` change from two services to three, and move the scraping mention from the automation service to the new card. Counts and contact details stay unchanged.
- Work stays on `master` with linear commits. Push happens only after the full suite and smoke are green.

## What is left to the builder

Exact commands, verification output, and commit order are in the plan that follows this approved design.
