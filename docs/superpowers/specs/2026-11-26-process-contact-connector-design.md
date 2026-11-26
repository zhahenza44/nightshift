# Process to contact connector design

## Intent

The neon progress line in `04 PROCESS` should visibly continue into the frame of `05 CONTACT`, so the two sections read as one sequence. The five step markers beside Brief & discovery through Maintenance should use Roman numerals only.

## Goals

- The cyan to magenta rail ends on the top border of `.contact-panel` with no visible break.
- The rail keeps its existing scroll-driven progress and the same x position on every breakpoint.
- `.step-no` shows `I`, `II`, `III`, `IV`, `V`.
- All visitor-facing copy stays English and unchanged apart from those five markers.

## Non-goals

- No bend along the contact panel border, no extra junction ornament, and no new label.
- No change to section indices `04` / `05`, navigation numbers, the CV section, contact copy, or `demos/`.
- No new pause control or change to the reduced-motion contract.

## Constraints

- `#process-fill.style.height` is the current progress output and is read by `tests/browser_smoke.py`; keep that behaviour testable.
- `#process.section` and `#contact.section` have zero vertical padding, so the list bottom and panel top already meet. The rail must extend into that seam by about 1px rather than introducing a gap.
- Above 980px the process grid has two columns, so the rail lands on the panel's top border inside the panel width. At 980px and below the grid is one column, so it lands near the panel's top-left corner.
- The pre-commit hook runs unit tests and the rendered smoke check. Reduced motion disables the looping animations and must stay green.
- Work stays on `master`, RED to GREEN to docs, one commit per task.

## Approaches

- **A, chosen:** keep one straight vertical rail and extend it into the panel's top border at the same x. It preserves the single direction of the neon line and never crosses the `05 CONTACT` section head.
- **B, rejected:** turn the line right along the panel's top border toward the label. This adds a segment near the section head and changes the rail's direction.
- **C, rejected:** add a diamond marker at the junction. This adds decoration where a continuous line already communicates the connection.

## Builder decisions

- Extend the rail and its fill through the seam using the existing gradient and glow, with progress kept in sync with the existing scroll calculation.
- Replace only the five `.step-no` values with uppercase Roman numerals; leave `<ol>` semantics intact.
- Add `.superpowers/` to `.gitignore` so brainstorm artifacts stay local.
- Pin both outcomes with failing tests first, then implement, then update the docs.

## What is left to the builder

Decide the exact CSS mechanism for the one-pixel seam extension, provided the rendered result matches A and every existing check still passes.
