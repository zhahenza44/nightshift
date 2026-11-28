# Web Scraping Real Case Design

Short design for the owner's request on 2026-11-28 to bring the five scraper examples from `web-scraping-portfolio/README.md` onto the NIGHT//SHIFT landing page. The owner chose one real case row with one link, not five rows and not a separate group.

## Intent

A visitor should see the scraper work as one more piece of real work beside the six existing demos. The row must point to real code and explain who the work serves without inventing facts.

## Goals

- Add one `<li>` to `#work .real-case-list`, after the six existing demo rows.
- Title it `Web Scraping Portfolio` and link once to `https://github.com/zhahenza44/web-scraping-portfolio` with the label `View code`, `target="_blank"`, and `rel="noopener noreferrer"`.
- Describe the five examples from the reference README: static HTML quotes, paginated books, a JSON API, Playwright rendering, and a 1,000 row catalog CSV.
- Add the owner's suitability sentence in English, with the "dll" filled only from the reference README: small businesses and companies can track competitor prices, watch job and property listings, follow public headlines, and export CSV, Excel, or JSON.
- Change the real case counts from six to seven in the page, tests, rendered checks, `PRODUCT.md`, and `README.md`.

## Non-goals

- No fifth demo file and no change to anything inside `demos/`.
- No JavaScript change, no new control, no new motion, and no new visual system.
- No separate "Web Scraping" group and no five individual scraper rows.
- No Indonesian visitor copy and no em dash in new copy.

## Constraints

- Every fact and number comes from `~/Projects/web-scraping-portfolio/README.md` and its committed `buku.csv`. The reference clone stays unchanged.
- The existing six demo links, three fictional cases, and four CAPABILITIES modules stay as they are.
- The GitHub link is a real destination, so it follows the existing new-tab pattern used by demo links.
- The static suite and Firefox smoke must stay green at 390px, 320px, reduced motion, and 1366px.

## Approaches

1. **Five scraper rows inside the real case list.** Rejected by the owner.
2. **A separate scraper group with its own head.** Rejected by the owner.
3. **One real case row with one code link.** Chosen. It keeps the existing list rhythm, makes the five examples one portfolio item, and adds only one destination to verify.

## Builder decisions

- Row description: `Five working scrapers cover static HTML, pagination, a JSON API, JavaScript rendering, and a 1,000 row catalog export. Built for small businesses and companies that need to track competitor prices, watch job and property listings, follow public headlines, and export clean CSV, Excel, or JSON files.`
- Tags: `Scrapy`, `Playwright`, `CSV`. These come from the reference README stack.
- The row uses the existing `.reveal` class and the existing `.real-case-list` markup. No CSS change is needed.
- Section meta becomes `07 REAL / 03 FICTIONAL / 04 MODULES` and the group meta becomes `07 CASES / REAL WORK`. The work intro says `Seven real cases`.
- The spec and plan are committed together so the final working tree stays clean.

## Left to the builder

Write the failing tests first, then add the row and copy, then update docs and rendered checks. Verify with the full unittest suite and browser smoke, then push to `origin/master` as approved by the owner.
