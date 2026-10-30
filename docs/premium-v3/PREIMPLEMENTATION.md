# v3.0 implementation scope — release hold

Baseline main: b553356528d097632f4f30da40258af4501f8212.
Design baseline: 86fa3c68c65c0fc722b1a176c9f64e094e04d782.
Design branch is 58 commits ahead, 0 behind; no main reconciliation required at inspection.

## Existing differences
See EXISTING-DIFF.txt (full file list). Current design changes 34 files, including public HTML, CSS, JS, bilingual additions, root mirrors and Wrangler previews.

## Planned changes
- Replace accumulated conflicting stylesheet overrides with one light enterprise system.
- Recompose both homepages with centered headline, two CTAs, large clearly labelled interface illustration, three services, selected verified work and available services.
- Preserve prior homepage business copy in supporting sections; keep other existing page bodies and legal terms.
- Recompose service, product, project, company and contact layouts consistently; preserve form fields, endpoint, scripts and privacy consent.
- Correct same-page language pairs, shared navigation and Chinese footer destinations; only real translations receive hreflang.
- Add one source-verified case with no business outcome claims. Existing project categories labelled as implementation areas, not named customers.
- Preserve all existing public paths, metadata, redirects and schema; add missing reciprocal hreflang and sitemap entries.
- Make public/ authoritative with a reproducible root mirror script, including tests to detect drift.
- Add content templates, preservation inventories, test records and rollback instructions.

## Constraints
No main merge, production deploy, DNS/traffic/payment/backend changes. No true customer submissions. Cloudflare preview and external service availability require live verification; local build success cannot establish those results.
