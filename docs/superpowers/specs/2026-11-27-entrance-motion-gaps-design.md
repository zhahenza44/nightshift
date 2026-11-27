# Entrance Motion Gaps Design

Short design for a small change, approved by the owner on 2026-11-27 when they chose option 1.

## Intent

The page already choreographs the hero, boot, manifesto, process rail, terminal, and footer. Six later elements still arrive without the same cue: the three fictional case cards, the six real-case rows on hover, the three CV contact links, the five process steps, the two non-primary contact buttons, and the CV intro paragraph. Add entrance motion with the page's existing `.reveal` system so later sections guide attention in the same language as earlier ones.

## Goals

- Fictional case cards, CV contact links, and process steps use `.reveal`, with short delays where a group enters together.
- Real-case rows get a small hover lift and a short arrow shift, so the clickable row is obvious in a text-heavy list.
- `Send message` and `GITHUB` join `Email` in the existing magnetic behavior.
- The CV intro paragraph stays inside its parent fade. No new word-splitting script.
- Visitor copy, real and fictional labels, demo links, and all existing motion stay unchanged.

## Non-goals

- No new keyframe set, no bespoke case-file animation, and no `animation-timeline: view()`.
- No change to hero, boot, ghost cursor, manifesto word stagger, terminal typing, menu, dialog, or footer marquee.
- No change to any file inside `demos/`.
- No push without owner approval.

## Constraints

- All visitor-facing copy stays English.
- Real cases come first, then fictional cases, then CAPABILITIES.
- `This section is my real CV. The case studies below are fictional.` stays verbatim.
- `Response <24h`, the terminal line, and the contact copy stay verbatim.
- `demos/` stays byte-identical, and `git diff --stat -- demos` stays empty.
- `prefers-reduced-motion: reduce` keeps all new motion quiet. No-JS fallback stays visible.
- Design dials stay ENERGY 3 / RHYTHM 3 / MOTION 3 from `PRODUCT.md`.
- Unit tests and rendered smoke stay green at 390px, 320px, reduced motion, and 1366px.

## Approaches considered

1. **Reuse `.reveal` and the existing observer, chosen.** Add classes and `--delay` values, plus small CSS hover rules and two `magnetic` classes. The observer, reduced-motion override, and no-JS fallback already exist, so the change stays small and consistent. The motion uses the same language as the rest of the page rather than introducing a new effect.
2. **Bespoke group keyframes.** A dedicated slide and clip entrance for case cards would read more distinctly, but it adds CSS, needs its own reduced-motion handling, and risks colliding with the existing hover spotlight. Rejected for this small change.
3. **CSS `animation-timeline: view()`.** This avoids the observer, but Firefox does not support it and the rendered smoke suite runs in Firefox. Rejected.

## Decisions

- The three `.project-card` elements get `reveal`. The second and third get `style="--delay:.08s"` and `style="--delay:.16s"` so the three case files read in order. The first needs no delay.
- The five `.process-step` elements get `reveal`. Each enters on scroll, so no delay is needed.
- The three `.cv-contact a` links get `reveal` with delays `.08s`, `.16s`, and `.24s`. Href, target, and rel stay exactly as they are.
- `.real-case-list > li` keeps its existing reveal. A hover rule shifts the inner `div` up by 2px, changes the row background, and shifts the arrow by 3px. The inner `div` carries the transform so it cannot fight `.js .reveal.is-in` on the row.
- `Send message` and `GITHUB` get `class="btn btn--ghost magnetic"`. The existing `$$(".magnetic")` loop picks them up.
- The CV intro paragraph keeps only the fade from `.cv-intro`. The script uses a single `querySelector` for `data-words`, so word stagger there would need JS changes that this change does not make.
- The reduced-motion block gets an override that removes the two new hover transforms. Magnetic setup is already skipped under reduced motion.
- Reasons for each motion: reveal guides attention to content that previously arrived flat; delays order grouped items; the row lift marks the clickable area in a dense list; magnetic feedback covers all three contact channels equally.

## What is left to the builder

Exact test names, markers, commit order, and verification commands are in the plan.
