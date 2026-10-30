# Content templates and publication states

Edit `public/` HTML directly; content remains readable without JavaScript. Use the existing `.card`, `.catalog-grid`, `.case-card`, `.page-hero`, `.grid-2` and `.section-head` components. Do not add a homepage card for every product.

## Product record (editorial template, not a runtime API)

| Field | Required content |
|---|---|
| name_en / name_zh | Approved public name |
| summary_en / summary_zh | Plain description of the actual deliverable |
| audience | Who can use it |
| functions | Verified functions only |
| state | Available, Pilot, In Development, Internal Only |
| evidence | Source commit, test result and verified official entry |
| entry | Official public URL, or consultation for scoped service |
| approval | Person authorizing public presentation and date |

Only approved Available offerings appear in the homepage Available Solutions section. Pilot entries must say consultation and cannot imply general availability. In Development and Internal Only remain outside sales directories. Existing public tools retain their historical links with availability to confirm until separately verified. Do not publish supermarket/antique products.

## Case record

Name, approved public identity, official URL, source repository/commit, screenshot date, delivered scope, languages, publication authorization. Use facts about delivery, never inferred outcomes or invented testimonials.

Verified example: `bb369tech/bb369-platform`, `clients/botanica-de-la-luz/index.html`, content blob `fc53f1b5180bd18ab6a081c6dfbd234d89f4bd48`. Live page and site footer visibly confirm BB369TECH technology services. Screenshot taken from the public page on 2026-10-30. No revenue, ranking or customer growth claims.

## Site ownership boundaries

Company site → service/product/case information and inquiry entry.
Platform → application runtime and existing account/payment routes.
CRM → existing private system; no new API, database or management UI is introduced.

When adding a translation, create an actual translated page before adding reciprocal hreflang; retain legal English labels if no approved legal translation exists.
