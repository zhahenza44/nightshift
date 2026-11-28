# Web Scraping CV Bullet Design

Short design for the owner's first job, approved in conversation on 2026-11-28.

## Intent

The owner's first job is the now-public `zhahenza44/web-scraping-portfolio` repo. Bring that work onto the NIGHT//SHIFT landing page without turning it into a seventh real case or a new studio capability module. The owner chose the CV/services route, then chose a single bullet over a new CV card.

## Goals

- Clone the public repo into a new local folder `~/Projects/web-scraping-portfolio`, named after the repo, as a reference copy. Leave that copy unchanged and do not push it again.
- Add one English bullet under the existing `AI & workflow automation` CV service: `Data scraping &amp; CSV exports (Scrapy, Playwright)`.
- Pin the bullet in the static test suite.
- Update the owner docs so the service description matches the shipped bullet.
- Push the verified landing page change to `origin/master`, as requested in the same message.

## Non-goals

- No seventh real case row and no change to `06 REAL / 03 FICTIONAL / 04 MODULES`.
- No new folder inside `demos/`; that folder stays byte-identical.
- No new CV service card, no CSS grid change, and no new link on the page.
- No edit or second push to `web-scraping-portfolio`.

## Constraints

- All visitor-facing copy stays English. The repo's own README is Indonesian and is not copied to the page.
- Existing demo titles, descriptions, tags, hrefs, labels, and counts stay verbatim.
- `demos/` stays unchanged and `git diff --stat -- demos` stays empty.
- Unit tests and rendered smoke stay green at 390px, 320px, reduced motion, and 1366px.
- The two existing CV service cards remain two cards. The bullet is a capability inside the first card, not a new service.

## Approaches considered

1. **Single bullet in `AI & workflow automation`, chosen.** One English line that names the tools already in the repo. No layout or count change, and the first job stays visible in the CV.
2. **Third CV service card.** More prominent and able to mention "first job" plus the 1,000-book CSV, but it needs a full-width grid rule, changes the two-services description, and adds rendered layout risk. Rejected by the owner.
3. **Seventh real case or fifth CAPABILITIES module.** Would require a live demo or a new module count and would break the six-real-case contract. Rejected by the owner's CV/services choice.
4. **Sentence in the CV intro.** Smaller, but the owner chose services rather than the intro. Rejected.

## Decisions

- Folder name: `web-scraping-portfolio` under `~/Projects`. This is the builder's call from the repo name; the owner did not specify a different name.
- Bullet text is exactly `Data scraping &amp; CSV exports (Scrapy, Playwright)`. It stays in the first CV service list, between `Webhooks &amp; API integrations` and `Google Sheets / CRM`.
- The static test `test_cv_identity_and_services` gains this marker. RED is verified before the HTML edit.
- `PRODUCT.md` and `README.md` gain one short mention of the scraping capability without changing the two-service count.
- Work stays on `master` with linear commits. No branch, merge, or PR.

## What is left to the builder

Exact commands, verification output, and commit order are in the plan that follows this approved design.
