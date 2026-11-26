# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

Static HTML, CSS, and vanilla JavaScript. No build step. The page loads Google Fonts from the network and keeps local fallbacks.

## Users

Someone opening the owner's link, usually on a phone, who wants a visual statement and a way to reach Alan Nawa. The visitor can also open six working demos from the CV section.

## Product Purpose

The `NIGHT//SHIFT` demo as the main landing page, with Alan Nawa's real CV inserted after the manifesto. The NightShift part is a design showcase with disclosed fictional data. The CV part carries the owner's real identity, services, demo links, and contact channels.

## Positioning

One page, two clearly labeled truths. The fictional studio stays intact as a design demo. The real CV stays in its own section with a note that separates it from the case studies below.

## Operating Context

The page is one static document that can be opened from disk or any static host. `demos/` remains on disk with all six demos unchanged, and the CV section links to them. External fonts are part of the copied design.

## Owner-directed decisions

- Use the NightShift demo literally, not the previous Alan Nawa CV shell as the page design.
- Translate every visitor-facing string into English and set `lang="en"`.
- Keep the fictional studio, case studies, metrics, status, email address, and phone number. Label them in the footer and case-file dialogs.
- Keep the Google Fonts requests.
- Keep the boot sequence, ghost cursor, ticker, magnetic buttons, and other demo motion with no pause control.
- Keep the brand as NIGHT//SHIFT and the hero headline copy unchanged.
- Merge Work and Services into one `03 WORK & SERVICES` section with a CAPABILITIES sub-block. Remove the separate `#services` anchor and renumber Process and Contact.
- Set every visitor-facing location to Surabaya, ID, including the hero foot and the terminal line.
- Set the hero stat to `Projects 1`, remove Experience, and keep `Response <24h` with its terminal line and contact copy.
- Label the GitHub contact link `GITHUB` and keep its href at `https://github.com/zhahenza44/otomasi-web`.
- Ignore only blocked Google Fonts downloads in the rendered console check. Every other console error still fails the run.
- Remove the contact-section note naming fictional names, metrics, email, and phone number.
- Set the hero tag to `EST. 2026`.
- Remove the vertical section padding on `#cv.section` so the CV block does not create a wide empty band at 1366px.
- Add Alan Nawa's CV after the manifesto, using the data in the old shell at `bbebb12:index.html`.
- Allow additive CSS for the CV section that uses the demo tokens.
- Leave every file inside `demos/` unchanged.
- Keep the demo stylesheet's low-contrast `muted-2` technical labels. The contrast shortfall is an accepted consequence of the literal-copy decision.

## Capabilities and Constraints

- Root `index.html`, `js/main.js`, and the favicon come from `demos/nightshift/`. Their differences are translated visitor strings, the document language, the CV section, the merged Work & Services section, the Surabaya location, the hero stats and year, the removed contact note, and the `GITHUB` label.
- `css/styles.css` keeps every demo selector and keyframe, then appends a CV block, a `#cv.section` padding reset, and a `services-block` spacing rule before the reduced-motion rules.
- All visitor copy is English. Brand tokens such as `NIGHT//SHIFT`, `N//S`, technical labels, and code-like strings stay as designed.
- Fictional data stays visible. The footer and case-file dialogs label the showcase as fictional, and the CV section has its own note naming the real data.
- The CV lists two services, six demo links, and three real contact channels.
- The `demos/` folder is intact and linked from the CV section only.
- Motion loops run without a pause control. Reduced-motion users get static content, a hidden cursor and ghost layer, and a skipped boot overlay.
- Keyboard controls keep visible focus. Header controls use the demo's 38px and 40px sizes, above the WCAG 2.2 AA 24px minimum; that is an accepted override of the 44px preference.

## Brand Commitments

Name: NIGHT//SHIFT. The demo supplies the visual direction. Dark near-black is the base, cyan marks the primary actions and links, magenta marks technical accents, and the grid, horizon line, orb, and ticker are the studio's identity motifs. The CV block reuses these tokens instead of introducing a second visual system.

Design dials: ENERGY 3 / RHYTHM 3 / MOTION 3. That describes the shipped demo, not a new proposal. The page leads with a full-height hero, shifts between manifesto, CV, a combined work and services composition, process, and contact, and uses motion to guide attention through each section.

Visual reasons: cyan carries the main action because it is the highest-contrast accent on the dark base. Magenta stays on technical labels so it never competes with the primary action. The grid and horizon belong to the NightShift identity copied from the demo. The orb repeats studio facts as the hero motif. The ticker repeats service labels. The CV section uses the same section head and panel patterns so it reads as part of the page, and its note sits next to the real contact details.

Motion reasons: the boot sequence frames the page as a NightShift system, the ghost cursor follows the pointer, the ticker and marquee carry labels, the process fill tracks reading position, and magnetic buttons answer the pointer within the demo's cap. The CV section adds no animation. Reduced motion removes the pointer layers and loop animations while keeping all content visible.

## Evidence on Hand

NightShift source: `demos/nightshift/`. There are no real customers, testimonials, benchmarks, or contact records for the fictional studio. The footer and case-file dialogs label the showcase as fictional and make no further claim.

CV source: `bbebb12:index.html`. It supplies the owner's name, role, bio, two service descriptions, six demo paths, and three contact channels. No new claim was added to the CV section.

## Product Principles

- Copy the demo exactly, then translate the copy.
- Keep the fictional disclosure in the footer and case-file dialogs.
- Put real CV data in its own section with a note that separates it from the fictional showcase.
- Preserve layout, motion, and interaction behavior instead of rebuilding them from a description.
- Keep the demo archive unchanged and link it only from the CV list.
- Verify the shipped page in a real browser at phone widths and with reduced motion.

## Accessibility & Inclusion

The document uses English, landmarks, a unique title, and labelled controls. Focus stays visible, dialogs close with Escape, and the mobile menu returns focus to its trigger. Text using `ink`, `ink-soft`, `muted`, `cyan`, `magenta`, `amber`, `green`, and `violet` meets WCAG AA on the shipped dark backgrounds. The `muted-2` technical labels measure between 3.20:1 and 3.70:1, below the 4.5:1 AA threshold for normal text. That shortfall stays because the stylesheet is a literal copy. Reduced motion disables the loops, cursor, and ghost layer while keeping content readable. The fictional studio is labeled as fictional, and its contact details must not be treated as a real support channel. The three CV contact links are the real channels.
