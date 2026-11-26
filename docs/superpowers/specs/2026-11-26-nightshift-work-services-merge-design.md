# Work and Services merge design

## Intent

The owner wants the main landing page to feel less fragmented. `Work` and `Services` become one section, the studio location becomes Surabaya, the contact link labelled `SOURCE` becomes `GITHUB`, and the hero stats drop the invented experience number.

## Decisions from the conversation

- Keep `NIGHT//SHIFT` as the brand and keep the fictional showcase.
- Merge `Work` and `Services` into one section using approach A below.
- Set every visitor-facing Jakarta or JKT location to `Surabaya, ID`.
- Keep `Response <24h` exactly as it is, including the terminal line and the contact copy.
- Change the hero `Projects` stat to `1` and remove the `Experience` stat.
- Change the visible contact link text `SOURCE` to `GITHUB`. Keep its href at `https://github.com/zhahenza44/otomasi-web`.
- Keep the real CV section, its six demo links, and its three contacts untouched.

## Goals

- One combined section that still shows the three fictional case files and the four capability cards.
- Navigation that matches the real section order.
- Location text that says Surabaya everywhere it is shown.
- Hero stats without the invented years of experience.
- All visitor copy stays English.

## Non-goals

- No new animation, pause control, or visual system.
- No change to the fictional case studies, metrics, status, email address, phone number, or disclosure.
- No change to `demos/`.
- No push or merge.

## Constraints

- The page is static HTML, CSS, and vanilla JavaScript.
- CSS changes must reuse existing tokens and avoid new decorative rules.
- The existing rendered checks cover 390px, 320px, and reduced motion. They must stay green.
- `Response <24h` stays as an accepted fictional-demo claim, already disclosed by the page.

## Approaches

A, chosen by the owner. One `<section class="section work" id="work">` holds the case files and a `CAPABILITIES` sub-block with the service cards. The nav item becomes `03 WORK &amp; SERVICES`; `Process` becomes `04` and `Contact` becomes `05`. The `#work` anchor keeps working, so `View work` and any existing link to `#work` still land on real content. This touches the least markup and CSS.

B, not chosen. The combined section would use `id="services"` and retarget every `#work` link. It reads worse because `work` would lose its own anchor.

C, not chosen. The combined section would use `id="work-services"` and remove both old anchors. It is the clearest name but breaks existing links.

## How it gets built

- Replace the two section bodies with the single section from approach A. Keep the current `work-intro`, `project-stack`, `services-intro`, and `service-grid` markup. Keep the `CAPABILITIES` label and the sentence about the four things the studio takes seriously inside the sub-block.
- Remove the `Services` nav item from both navs. Renumber the remaining section heads and nav items to `01` through `05`.
- Set the combined section head label to `WORK &amp; SERVICES` and its meta to `03 FILES / 04 MODULES`.
- Replace `JKT — ID`, `JAKARTA, ID`, `Jakarta, ID`, `jakarta, id`, and `JKT, ID` with Surabaya equivalents in the same visual casing. Replace the hero coordinate line with the text `SURABAYA, ID`; no new coordinate numbers are introduced.
- In the hero stats, set `Projects` to `1`, remove the `Experience` item, and leave `Response <24h` untouched.
- In the contact links, change only the visible label `SOURCE` to `GITHUB`.
- Update the static and rendered tests to pin the new section order, nav labels, location text, stats, and `GITHUB` label. Keep the fictional disclosure and CV checks.
- Update `README.md` and `PRODUCT.md` to describe the merged section and the owner's new decisions.
- Run the unit suite, rendered smoke suite, pre-commit hook, HTML validation, and a diff check on `demos/`.

## Known check issue

The rendered smoke check currently counts failed Google Fonts downloads as page console errors. In this environment `fonts.gstatic.com` requests fail with `downloadable font: download failed`, so the pre-commit hook fails before any page change. The fonts are an owner-approved part of the copied design and local fallbacks are expected. The implementation must filter only those font download failures from the console check, while keeping all other console errors as failures. This is a harness fix, not a page change.

## Left to the builder

Exact class names for the small services subhead, exact test names, and the smallest CSS change needed to keep the combined section readable at 320px. Use existing tokens and no new class that can be avoided.
