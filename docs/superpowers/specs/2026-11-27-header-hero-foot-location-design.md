# Design: remove the location label from header and hero foot

## Intent

The owner wants `SURABAYA, ID` gone from two visible spots: the brand block in the header and the foot row directly below the `Projects 1` hero stat. Everywhere else the location stays. This is a copy cleanup, not a redesign.

## Goals

- The header brand block shows only `DIGITAL STUDIO`.
- The hero foot row shows only `SIGNAL 98.2%` and `SCROLL TO EXPLORE`, with its existing padding, border, flex layout, and reveal timing.
- At 320px, `SIGNAL 98.2%` stays hidden exactly as it is today. No new overflow at 320px, 390px, or 1366px.
- Static tests, rendered checks, and product docs describe the new copy.

## Non-goals

- Keep `SURABAYA, ID` in the mobile menu, CV base row, terminal line, and terminal foot.
- Do not change NIGHT//SHIFT branding, the hero stats, contact actions, or the footer at the bottom of the page.
- Do not change any file inside `demos/`.

## Constraints

Static HTML, CSS, and vanilla JavaScript. All visitor-facing copy stays English. The existing Firefox smoke suite covers 390px, 320px, reduced motion, and 1366px.

## Approaches

1. Remove the two text nodes from `index.html` and fix the one selector that depends on their order. This leaves no dead DOM text and keeps the visible layout the same. Chosen.
2. Hide the two nodes with `display: none` in CSS. Rejected: the text would remain in the DOM, in accessibility output, and in source checks, which is worse than a real removal.

## Implementation sketch

- `index.html`: reduce the brand meta to `DIGITAL STUDIO`; delete the mono `SURABAYA, ID` span from `.hero-foot`.
- `css/styles.css`: in the narrow-width rule that currently says `.hero-foot .mono:nth-child(2)`, target the remaining mono span directly so `SIGNAL 98.2%` stays hidden at 320px.
- `tests/test_portfolio.py` and `tests/browser_smoke.py`: pin the new header and hero foot copy, assert the label is absent in those two spots, and keep the existing checks for the other Surabaya locations.
- `PRODUCT.md` and `README.md`: update the location decision and opening description so they no longer credit the header and hero foot with the label.

## Verification

Run the unit suite and the rendered smoke suite, then check that `git diff --stat -- demos` is empty and `git diff --check` is clean. Expected: all unit tests pass and the smoke report ends with `failed=0`.
