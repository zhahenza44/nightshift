# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

Static HTML, CSS, and vanilla JavaScript. No build step. The page loads Google Fonts from the network and keeps local fallbacks.

## Users

Someone opening the owner's link, usually on a phone, who wants a visual statement and a way to reach Alan Nawa. The visitor can also open six working demos from the Work & Services section.

## Product Purpose

The `NIGHT//SHIFT` demo as the main landing page, with Alan Nawa's real CV inserted after the manifesto. The NightShift part is a design showcase with disclosed fictional data. The CV part carries the owner's real identity, services, and contact channels. Work & Services carries the six real demos first, then the disclosed fictional case studies, then the CAPABILITIES modules.

## Positioning

One page, two clearly labeled truths. The fictional studio stays intact as a design demo. The real CV stays in its own section with a note that separates it from the case studies below. Work & Services labels the six real demos and the three fictional case studies separately, with the real demos first.

## Operating Context

The page is one static document that can be opened from disk or any static host. `demos/` remains on disk with all six demos unchanged, and the Work & Services section links to them. External fonts are part of the copied design.

## Owner-directed decisions

- Use the NightShift demo literally, not the previous Alan Nawa CV shell as the page design.
- Translate every visitor-facing string into English and set `lang="en"`.
- Keep the fictional studio, case studies, metrics, and status. Label the case studies as fictional in the case-file dialog and CV note.
- Use the owner's real contact channels and remove the fictional WhatsApp link.
- Remove the `DEMO CONCEPT / FICTIONAL STUDIO` label from the footer.
- Keep the Google Fonts requests.
- Keep the boot sequence, ghost cursor, ticker, magnetic buttons, and other demo motion with no pause control.
- Keep the brand as NIGHT//SHIFT and the hero headline copy unchanged.
- Merge Work and Services into one `03 WORK & SERVICES` section with a CAPABILITIES sub-block. Remove the separate `#services` anchor and renumber Process and Contact.
- Treat the demos from AI Lead Capture through NIGHT//SHIFT as real work. Move them out of the CV and into Work & Services ahead of the fictional case studies.
- Set visitor-facing location labels to Surabaya, ID in the mobile menu, CV base, and terminal; do not show a location label in the header or hero foot.
- Remove the `SURABAYA, ID` label from the header brand block and the hero foot row, keeping `DIGITAL STUDIO`, `SIGNAL 98.2%`, and `SCROLL TO EXPLORE` in place.
- Set the hero stat to `Projects 1`, remove Experience, and keep `Response <24h` with its terminal line and contact copy.
- Label the GitHub contact link `GITHUB` and keep its href at `https://github.com/zhahenza44/otomasi-web`.
- Ignore only blocked Google Fonts downloads in the rendered console check. Every other console error still fails the run.
- Remove the contact-section note naming fictional names, metrics, email, and phone number.
- Replace the demo email with `zhahenza666@proton.me` in the mobile menu and the `Email` button.
- Set the hero tag to `EST. 2026`.
- Remove the vertical section padding on `#cv.section` so the CV block does not create a wide empty band at 1366px.
- Reduce the bottom padding on `#work.section` to `clamp(32px, 4vw, 48px)` so CAPABILITIES does not leave a wide empty band before the Process section.
- Remove the bottom padding on `#process.section` so the last process step meets the contact panel without an empty band.
- Remove the vertical padding on `#contact.section` and the top margin on `.site-footer` so the contact panel meets the footer without an empty band.
- Keep the process rail straight and extend it into the contact panel top border without a bend or marker.
- Turn all four sides of the contact frame magenta once the process rail completes, so the rail reads as one connected gesture instead of stopping at a grey border. Keep the corner brackets magenta with it.
- Show the five process step numbers as Roman numerals I through V and leave section indices 04 and 05 unchanged.
- Add Alan Nawa's CV after the manifesto, using the data in the old shell at `bbebb12:index.html`.
- Allow additive CSS for the CV section that uses the demo tokens.
- Leave every file inside `demos/` unchanged.
- Keep the demo stylesheet's low-contrast `muted-2` technical labels. The contrast shortfall is an accepted consequence of the literal-copy decision.
- Publish the static page on GitHub Pages from `zhahenza44/nightshift`. Use `nightshift.is-not-a.dev` as the custom domain and point its DNS CNAME record to `zhahenza44.github.io`.
- Replace the Copy email action with Send message opening `https://ig.me/m/zhahenzar` in a new tab, because the conversation happens in Instagram DM.
- Rename the primary action from Send brief to Email, because the channel name is clearer than a verb phrase. Keep its `mailto:zhahenza666@proton.me` href, class, and behavior unchanged.
- Remove the unused copy-email toast path.
- Box GITHUB beside Send message and remove the EMAIL text link and the empty `.contact-links` row, so the action row has one conversation path and one code path.
- At phone widths, keep Email full width and place Send message and GITHUB side by side, using the existing ghost button style so the compact actions stay readable without overflow.
- Keep the `↗` glyph on the external action anchors to mark a new tab, following the existing NIGHT//SHIFT button language.

## Capabilities and Constraints

- Root `index.html`, `js/main.js`, and the favicon come from `demos/nightshift/`. Their differences are translated visitor strings, the document language, the CV section, the merged Work & Services section, the Surabaya location, the hero stats and year, the removed contact note, the real contact address, the removed WhatsApp link and footer label, the `GITHUB` label, reveal classes with delays on the case cards, CV contact links, and process steps, and magnetic classes on all three contact buttons.
- `css/styles.css` keeps the demo selectors and keyframes except for the narrow-width `.hero-foot .mono` rule, which replaces the demo's `.hero-foot .mono:nth-child(2)` selector after the hero-foot location label was removed, and a `margin-left: auto` rule that keeps the scroll cue right aligned on phone widths. It renames the CV demo-list rules to `.real-case-list` and adds a `.case-group-head` spacing rule. It overrides the demo `.work` padding with a compact `#work.section` rule in the Work block, then appends a CV block, padding resets for `#cv.section`, `#process.section`, and `#contact.section`, a zero footer top margin, and a `services-block` spacing rule before the reduced-motion rules. It adds hover lifts to `.real-case-list > li` without transforming the `li` itself and a reduced-motion override that cancels both new transforms.
- All visitor copy is English. Brand tokens such as `NIGHT//SHIFT`, `N//S`, technical labels, and code-like strings stay as designed.
- Fictional case studies and metrics stay visible. The case-file dialog and CV note label the showcase as fictional, and the contact actions use the owner's real channels.
- The CV lists two services and three real contact channels. The `AI & workflow automation` service lists e-commerce price and catalog scraping, job and property listings, scheduled monitoring, and CSV/Excel/JSON delivery from the owner's `web-scraping-portfolio` repo. Work & Services lists six real demo links and three fictional case studies.
- The `demos/` folder is intact and linked from the Work & Services section only.
- Motion loops run without a pause control. Reduced-motion users get static content, a hidden cursor and ghost layer, a skipped boot overlay, and no reveal, hover, or magnetic transforms.
- Keyboard controls keep visible focus. Header controls use the demo's 38px and 40px sizes, above the WCAG 2.2 AA 24px minimum; that is an accepted override of the 44px preference.

## Brand Commitments

Name: NIGHT//SHIFT. The demo supplies the visual direction. Dark near-black is the base, cyan marks the primary actions and links, magenta marks technical accents, and the grid, horizon line, orb, and ticker are the studio's identity motifs. The CV block reuses these tokens instead of introducing a second visual system.

Design dials: ENERGY 3 / RHYTHM 3 / MOTION 3. That describes the shipped demo, not a new proposal. The page leads with a full-height hero, shifts between manifesto, CV, a combined work and services composition, process, and contact, and uses motion to guide attention through each section.

Visual reasons: cyan carries the main action because it is the highest-contrast accent on the dark base. Magenta stays on technical labels so it never competes with the primary action. The grid and horizon belong to the NightShift identity copied from the demo. The orb repeats studio facts as the hero motif. The ticker repeats service labels. The CV section uses the same section head and panel patterns so it reads as part of the page, and its note sits next to the real contact details. The contact panel follows the last process step and meets the footer so the final screen ends on the call to action instead of an empty band.

Motion reasons: the boot sequence frames the page as a NightShift system, the ghost cursor follows the pointer, the ticker and marquee carry labels, the process fill tracks reading position, and magnetic buttons answer the pointer within the demo's cap. Fictional case cards, CV contact links, and process steps enter through the existing reveal system, with short delays that order each group. Real-case rows lift their content and arrow on hover so the clickable area is clear in a text-heavy list. All three contact actions are magnetic. The CV intro keeps only its parent fade, with no word stagger. Reduced motion removes the pointer layers, loop animations, and new hover transforms while keeping all content visible.

## Evidence on Hand

NightShift source: `demos/nightshift/`. There are no real customers, testimonials, benchmarks, or contact records for the fictional studio. The case-file dialog and CV note label the showcase as fictional and make no further claim. The contact actions carry the owner's real channels.

CV source: `bbebb12:index.html`. It supplies the owner's name, role, bio, two service descriptions, six demo paths, and three contact channels. No new claim was added to the CV section.

## Product Principles

- Copy the demo exactly, then translate the copy.
- Keep the fictional disclosure in the case-file dialog and CV note.
- Put real CV data in its own section with a note that separates it from the fictional showcase.
- Put the six real demo links in Work & Services and label them separately from the fictional case studies, with the real cases first.
- Preserve layout, motion, and interaction behavior instead of rebuilding them from a description.
- Keep the demo archive unchanged and link it only from the real case list in Work & Services.
- Verify the shipped page in a real browser at phone widths and with reduced motion.

## Accessibility & Inclusion

The document uses English, landmarks, a unique title, and labelled controls. Focus stays visible, dialogs close with Escape, and the mobile menu returns focus to its trigger. Text using `ink`, `ink-soft`, `muted`, `cyan`, `magenta`, `amber`, `green`, and `violet` meets WCAG AA on the shipped dark backgrounds. The `muted-2` technical labels measure between 3.20:1 and 3.70:1, below the 4.5:1 AA threshold for normal text. That shortfall stays because the stylesheet is a literal copy. Reduced motion disables the loops, cursor, and ghost layer while keeping content readable. The fictional showcase is labeled as fictional in the case-file dialog and CV note, and it no longer publishes invented contact details. The contact links and the three CV contact links use the owner's real channels.
