# Portfolio Cybertron Liveness Design

**Status:** approved
**Supersedes:** the restrained motion section of `2026-11-25-portfolio-cybertron-design.md`
**Owner request:** make the shell feel as alive as the NIGHT//SHIFT demo while keeping Alan Nawa's real CV.

## Intent

The owner compared the portfolio shell with `demo-portfolio-cyberpunk/index.html` and said that demo is what cyberpunk and TRON should feel like. The gap is not palette, it is energy: an orbital motif, repeated motion, a ticker, a larger typographic voice, and visible interface feedback. The shell must gain that energy without becoming a different person's fictional studio.

## Goals

- Raise ENERGY from 2 to 3 and MOTION from 2 to 3. RHYTHM stays 2.
- Give the hero one orbital SVG motif, a thin horizon grid, a scanline, and a finite entrance.
- Add a short ticker of real service labels, a scroll progress rule, and magnetic feedback on buttons.
- Add one finite reveal moment when the project grid first enters the viewport.
- Put the Instagram action row closer to the intro copy by removing the extra `margin-top` on `.hero-actions`. Both buttons stay on one baseline.
- Keep every visitor string in English and every fact true.

## Non-goals

- No boot overlay, loading theatre, or fake `SYSTEM ONLINE` state.
- No ghost cursor or scan-box cursor follower.
- No invented statistics, availability status, customer names, or fake studio identity.
- No Google Fonts or any external asset. System sans and system monospace stay.
- No Indonesian visitor copy. The six demos stay untouched and may keep their own language.
- No copying the demo's CSS or JS wholesale.

## Constraints

- Static HTML, CSS, and vanilla JS. No build step, package, or network asset.
- One hidden `<h1>Alan Nawa</h1>`, six cards, three real contact channels.
- Every loop stops under `prefers-reduced-motion: reduce` and content stays visible.
- Anything moving longer than five seconds needs a real pause control with `aria-pressed`.
- Interactive targets stay at least 44px, focus rings stay visible, text stays AA contrast.
- Palette stays cyan `#00e5ff`, magenta `#ff3d8d`, and near-black neutrals.
- Existing static and rendered tests are updated to pin the new contracts, not removed.

## Approaches considered

1. **Transplant the demo's visual language, keep Alan's data.** Rebuild the hero with an orb and grid, add restrained loops, magnetic buttons, a real-label ticker, and a progress rule. Copy stays English, facts stay real, fonts stay system. Chosen because it answers the owner's "lebih hidup" request without turning a CV into a fictional studio.
2. **Clone NIGHT//SHIFT as the shell.** Highest visual match, but it imports Indonesian copy, invented numbers, a fake availability status, external fonts, boot theatre, and ghost cursors. Rejected: it replaces the owner's identity and breaks the no-fabrication rule.
3. **Keep the current shell and link more prominently to the demo.** Cheap and safe, but it does not make the shell itself feel alive. Rejected against the explicit request.

## Decided parts

- **Hero orb:** inline SVG with concentric circles and a textPath using only real facts (`ALAN NAWA / WEB & AI AUTOMATION / SIX LIVE DEMOS`). Rings rotate in one loop. Reason: gives the page a specific TRON identity motif instead of a generic glow.
- **Ticker:** one `aria-hidden` row repeating the real service words `WEB DEVELOPMENT`, `LANDING PAGES`, `AI AUTOMATION`, `N8N`. Loop is governed by the same motion toggle as the orb. Reason: it carries the demo's pulse without inventing a slogan.
- **Motion pause:** one header button with the stable English label `Pause motion` and `aria-pressed`. Pressed means motion is paused and every loop is stopped. The label stays fixed so assistive technology announces one name plus its pressed state instead of `Resume motion, pressed`. Reason: loops exceed five seconds, so people need a real stop with an unambiguous toggle state.
- **Magnetic buttons:** pointer movement shifts a button at most 2px, pointer leave resets, keyboard focus never moves the button, disabled under reduced motion. Reason: direct response to the user's hand.
- **Scroll progress:** one cyan rule under the header, width reflects scroll position, no transition under reduced motion. Reason: orientation on a long CV, not decoration.
- **Project reveal:** the grid fades and rises once when it first enters view, through `IntersectionObserver`, with CSS fallback that leaves cards visible if JS is absent. This is the page's one dealt moment. Reason: directs attention to the real work.
- **Instagram spacing:** remove the added `margin-top` on `.hero-actions` and tighten the grid gap so the action row sits close to the intro, keeping both buttons aligned. Reason: closes the gap the owner reported.
- **Glow dose:** glow stays on the primary action and the orb rings only. Cards, badges, and section borders stay matte. Reason: keeps one focal point.

## Left to the builder

- Write the implementation plan and get it approved.
- Update `tests/test_portfolio.py` for the new loop, pause, ticker, orb, and motion rules. Keep the tests that pin contacts, six demos, English copy, hidden h1, and reduced motion.
- Update `tests/browser_smoke.py` to check the new controls at 390px, including the pause state, loop stop under reduced motion, and the action row spacing.
- Verify with unittest, the Firefox smoke script, HTML validation, local HTTP paths, and contrast checks.
- Run the antislop Delivery Gate and report it with the deliverable.
