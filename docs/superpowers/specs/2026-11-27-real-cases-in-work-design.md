# Design: move the six real demos into Work & Services

## Intent

The owner said the demos from AI Lead Capture through NIGHT//SHIFT are real work, so they belong in Work & Services. The section also has to make the difference between a real case and a fictional case obvious at a glance.

## Goals

- The six demo items live inside `#work`, ahead of the three fictional case studies and ahead of CAPABILITIES.
- Two labeled groups appear inside `#work`: `REAL CASES / LIVE DEMOS` and `FICTIONAL CASE STUDIES`.
- The CV keeps identity, contact channels, and two services. It no longer holds a demo list.
- Every demo title, description, tag, href, `target="_blank"`, and `rel="noopener noreferrer"` stays exactly as it is.
- Static tests and rendered checks pin the new group labels, their order, and all six working links.
- README.md and PRODUCT.md describe the new structure.

## Non-goals

- Do not change any file inside `demos/`.
- Do not remove the fictional showcase, its case-file dialog, or its fictional disclosure.
- Do not change the hero, contact actions, location labels, process, or footer.
- Do not rename or translate the demo titles.

## Constraints

Static HTML, CSS, and vanilla JavaScript. Visitor copy stays English. The Firefox smoke suite covers 390px, 320px, 1366px, and reduced motion. `git diff --stat -- demos` must stay empty.

## Approaches

1. **Move and label (chosen).** Take the six items out of the CV and put them in a new block inside Work & Services. Give both case groups their own label so nobody has to guess which cases are real. One copy of each link, one source of truth. The owner chose real cases first, then fictional cases, then CAPABILITIES.
2. **Mirror the list.** Keep the six items in the CV and repeat them in Work & Services. Rejected: the same links appear twice, which duplicates content and gives the reader two places to look.
3. **Replace the fictional cases.** Turn the three fictional case studies into the six real demos. Rejected: it removes the disclosed fictional showcase the owner asked to keep.

## Implementation sketch

- Move the six `<li>` items out of `.cv-demo-list` in the CV and into a new `.real-case-list` in `#work`, directly after `.work-intro`.
- Add a `.section-head` before that list: label `REAL CASES / LIVE DEMOS`, meta `06 DEMOS / REAL WORK`.
- Add a `.section-head` before `.project-stack`: label `FICTIONAL CASE STUDIES`, meta `03 FILES / SHOWCASE`.
- Change the `#work` section meta from `03 FILES / 04 MODULES` to `06 REAL / 03 FICTIONAL / 04 MODULES`.
- Change the work intro copy so it names both groups. Keep the existing fictional disclosure in the CV and in the case-file dialog.
- Change the CV panel head from `CV / SIX DEMOS` to `CV / PROFILE`. Keep the `PROJECTS / Six live demos` row because it is still true.
- Rename the `.cv-demo-list` CSS rules to `.real-case-list`, including the 860px rule, and keep their declarations. Reuse `.section-head` for the two new group heads and add only the spacing needed in the Work block.
- Update `tests/test_portfolio.py` and `tests/browser_smoke.py` so the six-link checks look inside `#work`; pin the two group labels, their order, and the absence of a demo list in the CV. Keep the fictional disclosure checks.
- Update README.md and PRODUCT.md: the CV no longer lists demos, Work & Services holds both real and fictional cases, and the real cases come first.

## Verification

Run the unit suite, the rendered smoke suite, `git diff --stat -- demos`, and `git diff --check`. Expected: all unit tests pass, the smoke report ends with `failed=0`, `demos/` stays unchanged, and there are no whitespace errors.
