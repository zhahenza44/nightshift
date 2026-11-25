# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

Static HTML, CSS, and vanilla JavaScript. No build step. The page loads Google Fonts from the network and keeps local fallbacks.

## Users

Someone opening the owner's link, usually on a phone, who wants a full visual and interaction statement instead of a list of résumé entries.

## Product Purpose

A literal English copy of the `NIGHT//SHIFT` demo as the owner's main landing page. It shows the studio's art direction, layout rhythm, and browser behavior, then offers a fictional contact path that is disclosed on the page.

## Positioning

Demo fidelity over claim making. The page presents a fictional studio, fictional work, and fictional metrics as a visual demo. It does not present them as real client results.

## Operating Context

The page is one static document that can be opened from disk or any static host. `demos/` remains on disk with all six demos unchanged. The landing page does not link to them. External fonts are part of the copied design.

## Owner-directed decisions

- Use the NightShift demo literally, not the previous Alan Nawa CV shell.
- Translate every visitor-facing string into English and set `lang="en"`.
- Keep the fictional studio, case studies, metrics, status, email address, and phone number. Disclose them in the contact section.
- Keep the Google Fonts requests.
- Keep the boot sequence, ghost cursor, ticker, magnetic buttons, and other demo motion with no pause control.
- Leave every file inside `demos/` unchanged.
- Keep the demo stylesheet byte-for-byte, including its low-contrast `muted-2` technical labels. The contrast shortfall is an accepted consequence of the literal-copy decision.

## Capabilities and Constraints

- Root `index.html`, `css/styles.css`, `js/main.js`, and `assets/favicon.svg` come from `demos/nightshift/`. The only differences are translated visitor strings and the document language.
- The stylesheet is byte-for-byte identical to the demo stylesheet.
- All visitor copy is English. Brand tokens such as `NIGHT//SHIFT`, `N//S`, technical labels, and code-like strings stay as designed.
- Fictional data stays visible and is labeled as fictional on the page.
- The `demos/` folder is kept intact and is not linked from the landing page.
- Motion loops run without a pause control. Reduced-motion users get static content, a hidden cursor and ghost layer, and a skipped boot overlay.
- Keyboard controls keep visible focus. Header controls use the demo's 38px and 40px sizes, above the WCAG 2.2 AA 24px minimum; that is an accepted override of the 44px preference.

## Brand Commitments

Name: NIGHT//SHIFT. The demo supplies the visual direction. Dark near-black is the base, cyan marks the primary actions and links, magenta marks technical accents, and the grid, horizon line, orb, and ticker are the studio's identity motifs. The copied stylesheet carries those decisions without revision.

Design dials: ENERGY 3 / RHYTHM 3 / MOTION 3. That describes the shipped demo, not a new proposal. The page leads with a full-height hero, shifts between manifesto, work, services, process, and contact compositions, and uses motion to guide attention through each section.

Visual reasons: cyan carries the main action because it is the highest-contrast accent on the dark base. Magenta stays on technical labels so it never competes with the primary action. The grid and horizon belong to the NightShift identity copied from the demo. The orb repeats real studio facts as the hero motif. The ticker repeats service labels. The disclosure sits with the contact details so fictional data is never mistaken for a real offer.

Motion reasons: the boot sequence frames the page as a NightShift system, the ghost cursor follows the pointer, the ticker and marquee carry labels, the process fill tracks reading position, and magnetic buttons answer the pointer within the demo's cap. Reduced motion removes the pointer layers and loop animations while keeping all content visible.

## Evidence on Hand

The source of truth is `demos/nightshift/`. There are no real customers, testimonials, benchmarks, or contact records for the fictional studio. The page labels its data as fictional and makes no further claim.

## Product Principles

- Copy the demo exactly, then translate the copy.
- Keep the fictional disclosure where visitors can read it.
- Preserve layout, motion, and interaction behavior instead of rebuilding them from a description.
- Keep the demo archive unchanged and out of the main navigation.
- Verify the shipped page in a real browser at phone widths and with reduced motion.

## Accessibility & Inclusion

The document uses English, landmarks, a unique title, and labelled controls. Focus stays visible, dialogs close with Escape, and the mobile menu returns focus to its trigger. Text using `ink`, `ink-soft`, `muted`, `cyan`, `magenta`, `amber`, `green`, and `violet` meets WCAG AA on the shipped dark backgrounds. The `muted-2` technical labels measure between 3.20:1 and 3.70:1, below the 4.5:1 AA threshold for normal text. That shortfall stays because the stylesheet is a literal copy. Reduced motion disables the loops, cursor, and ghost layer while keeping content readable. Fictional contact details are disclosed and must not be treated as a real support channel.
