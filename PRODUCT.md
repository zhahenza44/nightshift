# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

Static HTML, CSS, and vanilla JavaScript. No build step, no dependency, and no external font or image on the portfolio shell.

## Users

Someone opening the owner's link from an Instagram bio, usually on a phone, scanning six work samples and looking for a way to get in touch.

## Product Purpose

A one-page CV that introduces Alan Nawa's web development and AI automation work, proves it with six local demos, and gives visitors three real contact channels.

## Positioning

An honest, dependency-free portfolio: real work samples, real contact links, no fabricated availability or status claims.

## Operating Context

The shell is a single static page that can be opened from disk or any static host. The six demo pages live in `demos/` as local copies and open directly from project cards.

## Capabilities and Constraints

- Six project cards link to existing local demo files.
- Three contact channels: Instagram `@zhahenzar`, GitHub `zhahenza44`, and `zhahenza666@proton.me`.
- All shell copy is English; names, handles, URLs, and demo paths stay unchanged.
- Demo contents are out of scope and stay unchanged.
- No WhatsApp or marketplace link; no made-up response-time or availability claim.
- WCAG AA text contrast, 44px tap targets, visible focus, keyboard-operable controls, and reduced-motion support.

## Brand Commitments

Name: Alan Nawa. The owner pinned a cyberpunk x TRON direction inspired by the `NIGHT//SHIFT` demo: cyan primary, magenta technical accent, clipped corners, a thin horizon grid, and finite motion.

Design dials: ENERGY 2 / RHYTHM 2 / MOTION 2. The page is direct rather than shouting. It keeps a consistent CV rhythm with a distinct hero panel, paired services, card grid, and contact row. Motion is one 700ms entrance plus hover and press feedback, with no loop.

Visual reasons: cyan marks the single primary action and links. Magenta marks only indexes and technical labels. Gradients and the thin grid are the approved TRON identity, not decoration by default. System monospace gives the technical labels their voice without a network font. The two service cards share weight because they are two equal ways to help. The arrow on the footer source link is the only arrow; it marks an off-site GitHub destination. Near-black is the approved TRON base, not a deferred light theme.

## Evidence on Hand

Six demo folders under `demos/`, three live contact destinations, and the existing one-page CV at `index.html`. No customer logos, testimonials, benchmarks, or pricing are available; none may be invented.

## Product Principles

- Show real work before making claims.
- Keep the shell static, local, and dependency-free.
- Make the next action obvious: open a demo or contact the owner.
- Design for the phone first without losing the desktop composition.
- Use motion once, briefly, and never loop it.

## Accessibility & Inclusion

The page must meet WCAG AA contrast, keep all controls keyboard reachable with visible focus, retain a visually hidden `h1` for screen readers, and stop motion under `prefers-reduced-motion`.
