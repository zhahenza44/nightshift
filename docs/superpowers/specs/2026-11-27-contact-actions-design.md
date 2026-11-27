# Contact action buttons design

Date: 2026-11-27

## Intent

In `05 CONTACT`, replace the `Copy email` box with a `Send message` box that opens the owner's Instagram direct message. Remove the `EMAIL` text link below the buttons and turn the `GITHUB` text link into a box beside `Send message`. The visitor should have one clear path to a conversation and a visible code link without a dangling text row.

## Goals

- `Copy email` becomes an anchor labeled `Send message` with `href="https://ig.me/m/zhahenzar"`, opening in a new tab with `rel="noopener"`.
- The `EMAIL ↗` link inside `.contact-links` is removed.
- `GITHUB ↗` moves from `.contact-links` into `.contact-actions` as a boxed anchor using the existing ghost button style.
- Desktop shows `Send brief`, `Send message`, and `GITHUB` in one row.
- At 320px and 390px, `Send brief` spans the row and `Send message` with `GITHUB` sit side by side below it, each at least 44px tall and inside the viewport.

## Non-goals

- Do not change `Send brief`, `mailto:zhahenza666@proton.me`, or the Instagram profile link elsewhere on the page.
- Do not remove the email in the CV section or the footer.
- Do not change `Response <24h`, the terminal line, or the contact copy.
- Do not touch `demos/`.

## Constraints

- All visitor-facing copy stays English.
- Keep the NIGHT//SHIFT brand, the fictional showcase disclosures, and the real CV section.
- Inline work on `master`, no branch, merge, or pull request.
- TDD red, green, then docs. One commit per task.
- Firefox rendered smoke must stay green at 390px, 320px, reduced motion, and 1366px.

## Approaches considered

1. Change only the existing button and leave the links row. Rejected: it leaves `EMAIL` text and a nearly empty bordered row behind.
2. Move `GITHUB` into `.contact-actions` and delete the now empty `.contact-links` container. Chosen: one action row, no orphaned markup, and the box style already exists.
3. Build new button styles for all three actions. Rejected: unnecessary change when `.btn` and `.btn--ghost` already match the design.

## Builder direction

Remove the copy-email JavaScript and toast path only if no other caller uses it. Update the unit and rendered tests that currently assert `Copy email`, the copied-email toast, and the plain `GITHUB` link. Add rendered checks for the DM href, the boxed GitHub link, the missing `EMAIL` link, and the 320px side-by-side layout. Keep the rest of the page untouched.
