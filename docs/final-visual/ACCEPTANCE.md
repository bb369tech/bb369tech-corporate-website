# Final visual and case-integration candidate

Date: October 30, 2026, Los Angeles. Base: `49c4bf9ce734b44694d1f33fcf85973cbe8b60d8`.

**Merge conclusion: HOLD. Do not merge main or release production.**

## Delivered candidate

- Exactly five homepage regions: Hero, Services, Solutions, Featured Projects, Contact.
- Clear websites/software positioning and free consultation entry in EN/ZH.
- One consolidated design system; no chain of appended visual hotfixes.
- Three verified existing public projects: SJ Home Improvement, Botánica de la Luz, Productos La Rosa. All use actual live-page screenshots and documented page-delivery scope.
- Full public Projects directory with English/Chinese industry filters. All case HTML is visible without JavaScript.
- `projects.json` is the extensible case source. Add approved public facts and an actual screenshot, run `scripts/render-projects.py`, then synchronize root mirrors. No homepage redesign is needed for each new merchant.
- Prior homepage and generic project-detail paragraphs migrated into existing business pages. Original public paths, search identity, legal copy, product links and inquiry contracts remain.

## Verification

| Check | Status | Evidence / limit |
|---|---|---|
| Existing branch contains latest main | PASS | 61 commits ahead, 0 behind at start; main b553356528d097632f4f30da40258af4501f8212 |
| Final integrity regression | PASS | 12 tests, now including formal main/live-production semantic preservation; public paths, exact metadata/schema/hreflang, paragraph retention/migration, legal bodies, forms, functional scripts, Wrangler, links, anchors, sitemap, static case generation and mirrors |
| Existing contact recovery tests | PASS | 3 unit tests |
| Existing backend fixture contract | PASS | 1 intercepted fixture test; no real delivery |
| Real browser responsive layouts | PASS | 20 pages × widths 320/390/768/1440 = 80 checks, plus 12 focused checks after restoring main semantics; one h1, no horizontal overflow, visible images decoded successfully |
| Menus, Escape and language round trips | PASS | 12 EN/ZH primary paths |
| Industry filters | PASS | EN/ZH: Retail=2, Home improvement=1, All=3; correct count and pressed state |
| Required fields/privacy consent | PASS | Two production-page copies blocked empty submission; zero real posts |
| Real browser mocked form success/failure | PASS | 8 isolated tests: success, HTTP 503, HTTP 200 with success=false, network exception, each EN/ZH; correct reset/preservation, recovery and topic alias |
| Test isolation | PASS | QA form action changed only in ignored fixture copies to a local non-delivery trap; fetch stub performs zero network requests; original shipping form untouched |
| JavaScript syntax | PASS | project-filter.js; existing site/contact scripts remain byte-identical |
| Website console | PASS, scoped | No recorded error matching local site origin in inspected browser log; browser-extension metadata errors were excluded and are not attributed to the site |
| Actual screenshots | PASS | Desktop homepage; complete three-project desktop directory in labelled reduced 1440px frame; 390px Chinese homepage and directory; SJ/La Rosa source screenshots |
| Client rights records | PARTIAL / HOLD for other records | Three existing public-release records support the selected public examples; no independent signed publicity agreements supplied. Other candidates excluded where evidence insufficient; referral/demo pages are not labelled commissioned client websites |
| Current candidate Cloudflare URL | NOT VERIFIED / NOT UPDATED | This request explicitly says not to auto-deploy. The existing branch triggers preview deployment on push, so its remote ref has not been moved for this revision |
| Real edge HTTP, redirects and missing-path 404 | NOT VERIFIED | Requires the new isolated Cloudflare preview |
| Real backend mail/CRM delivery | NOT VERIFIED | Intentionally no real inquiry, email, customer record or payment |
| Complete HTML standards validation and Lighthouse | NOT VERIFIED | Structural/content checks and byte budgets are not a full validator or performance score |

## Preview boundary

Existing Cloudflare branch URL (previous revision, not this new candidate):
https://design-premium-visual-baseline-2026-bb369tech-corporate-website.bb369-ai.workers.dev/

This task does not relabel that older deployed preview as the new revision. The complete new candidate was verified through the existing local preview at `http://terminal.local:4173/` and preserved in the current browser.

To finish remote preview acceptance, authorize moving only the existing design branch to the prepared candidate commit. This will trigger the already configured Cloudflare preview. Do not merge main or change production traffic. After the new preview is available, verify the deployed commit/content, HTTP/404 behavior and final user visual approval before production.

## Protected systems

No platform/customer repository changes; no CRM/database/permissions/Stripe/payment/customer-data/API/DNS/domain changes; no new hosting project. Current baseline contains no chatbot embed, and this task neither removes one nor claims to have integrated an unverified AI service.

See CASE-AUDIT.md, CONTENT-AND-URL-MAP.md, URL-MAP.csv, browser-results.json, FILES.txt and ROLLBACK.md.

## Strict main and production preservation addendum

See ../semantic-preservation/REPORT.md. The pinned formal main and 24 live production HTML entries were checked independently. The final ledger has 2,409 records (including mirror/navigation duplicates): 2,054 PRESERVED, 330 RELOCATED, 25 IMPROVED, 0 REMOVED. Fifteen main headline/quick-entry text units were restored in stable Services/Contact HTML after the earlier design-branch-only check missed them. No main, remote design ref or deployed preview was updated.
