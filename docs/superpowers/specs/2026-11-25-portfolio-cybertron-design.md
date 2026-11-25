# Portfolio cyberpunk x TRON design

## Intent

The owner wants the one-page CV at `index.html` to look and feel like the `NIGHT//SHIFT` demo: cyberpunk crossed with TRON, with motion. All visitor-facing copy must be in English.

Audience: someone opening the link from the owner's Instagram bio on a phone, scanning six demos and three contact channels.

## Goals

- Keep the current structure: hidden `h1`, intro, two services, six demo cards, contact, footer.
- Rebuild the visual language around cyan, magenta, clipped corners, a thin horizon grid, and mono system labels.
- Add a short entrance motion plus hover and press feedback, all finite.
- Translate every string on the shell into English.

## Non-goals

- No boot overlay, no fake availability status, no ghost cursors, no marquee, no endless loops.
- No external fonts or images. The shell stays static and dependency-free.
- No changes to the copied demo pages; they stay as they are.

## Constraints

- Static HTML/CSS/JS only, no build step.
- WCAG AA text contrast, 44px tap targets, visible focus, keyboard-operable controls, reduced-motion fallback.
- Counts must stay true: six projects, three contact channels.
- Contact channels remain Instagram, GitHub, and email. No WhatsApp or marketplace link.

## Approaches

- **A. Portfolio version (chosen).** Borrow the demo's palette, clipped panels, grid horizon, and finite motion, but leave out the demo's fabricated status and endless effects. Keeps the page honest and light.
- **B. Full demo clone.** Would copy the boot overlay, `OPEN FOR Q1` status, ghost cursors, marquee, and infinite loops. Rejected: it restores claims and motion the owner previously asked to remove, and adds external fonts.
- **C. Copy demo CSS then strip.** Same endpoint as A with more inherited code. Rejected: unnecessary surface area.

## Visual decisions and reasons

- Near-black `#05070c` base and `#090e17` panels: inherited TRON identity from the approved design.
- Cyan `#00e5ff` stays primary: it marks the one action and links, so the accent means something.
- Orange token becomes magenta `#ff3d8d`: it reads as cyberpunk and still clears 5.8:1 on panels. It marks indexes and technical labels only.
- Clipped corners on panels and cards: echoes the demo's angular frames without adding a fake interface.
- Thin perspective horizon grid in the opening section: gives the TRON world depth while staying CSS-only and static.
- One finite entrance transition of about 700ms with a small stagger: gives the page a deliberate opening without a loop.
- Hover lift on cards and step/press on controls: tells visitors what can be clicked.
- System sans for body, system mono for labels: no network font, and mono remains a technical voice.

## Copy decisions

Translate shell strings to English, including `aria-label`, filter labels, card descriptions, tags, panel labels, meta description, and footer. Keep names, handles, URLs, the `not-a-dev :)` phrase, and the six demo folder paths unchanged.

## Verification

Update static tests for the new token name, the finite keyframe budget, and the English strings. Keep guards for six cards, local demo links, forbidden contact channels, and accessibility markers. Run the suite, HTML validation, local HTTP checks for all six demos, contrast checks, and the antislop Delivery Gate.
