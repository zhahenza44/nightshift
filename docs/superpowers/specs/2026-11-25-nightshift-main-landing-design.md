# Design: NightShift as the main landing page

**Date:** 2026-11-25
**Status:** approved

## Intent

The owner wants the existing `NIGHT//SHIFT` demo to become the main landing page, not just an inspiration. The current Alan Nawa CV shell is replaced. The visitor-facing language becomes English.

## Goals

- Copy `demos/nightshift/index.html`, `demos/nightshift/css/styles.css`, `demos/nightshift/js/main.js`, and `demos/nightshift/assets/favicon.svg` into the repository root, replacing the current shell files.
- Translate every visitor-facing string to English, including document language, title, meta description, boot log, navigation, hero, labels, work, services, process, contact, dialog copy, toast copy, footer, and accessible names.
- Keep the NIGHT//SHIFT identity, layout, motion, effects, and interactions from the demo.

## Non-goals

- Keeping Alan Nawa's CV data, six demo cards, or real contact channels on the landing page.
- Adding the previously requested Instagram spacing change, pause control removal, or purple and neon pink running lines.
- Editing anything inside `demos/`.

## Constraints and accepted tradeoffs

- The demo uses Google Fonts and external font requests. This stays because the copy is literal.
- The demo contains fictional studio data, metrics, status, email, and phone number. These stay because the copy is literal. The fictional-note text is translated to English.
- The demo has no pause control. This stays because the copy is literal.
- The `demos/` folder stays intact but is no longer linked from the main landing page.
- Static and rendered tests are rewritten to pin the new contract. They are not simply removed.
- No push or merge unless asked.

## Approaches considered

1. **Copy the demo wholesale and translate visitor copy.** Chosen. This is the closest match to the owner's instruction.
2. **Copy the layout but replace the fictional data with Alan Nawa's CV.** Rejected because it is not a literal copy.
3. **Copy the demo but strip fictional data and external fonts.** Rejected because it changes the demo.

## Decided parts

- Root `index.html`, `css/styles.css`, `js/main.js`, and `assets/favicon.svg` become the NightShift demo files with English visitor copy.
- The HTML language becomes `en`. Brand tokens such as `NIGHT//SHIFT`, `N//S`, technical labels, and code-like strings stay as designed.
- The demo note in the contact section becomes an English disclosure that the names, metrics, email, and phone number are fictional.
- All demo behavior stays: boot sequence, ghost cursor, scanline, ticker, magnetic buttons, reveal, process fill, project dialogs, copy-email toast, clock, and mobile menu.
- Existing tests and documentation are updated for the new landing page contract.

## Left to the builder

- Write the implementation plan and get approval.
- Copy the four demo files into the root and translate visitor copy.
- Update static tests, rendered tests, `PRODUCT.md`, and `README.md`.
- Verify with unittest, the Firefox smoke script, HTML validation, local HTTP paths, and contrast checks.
- Run the antislop Delivery Gate and report it with the deliverable.
- Commit the work. Do not push or merge.
