# BB369TECH — Stable Company Architecture

Purpose: keep the company structure and visual foundation stable over the long term. New products and merchants extend the existing catalog and case templates; they do not trigger another homepage redesign. Product facts and necessary accessibility, compatibility and security maintenance can still be updated.

## Fixed responsibilities

| Area | Stable responsibility |
|---|---|
| Home / 首页 | Company value, three core capabilities, selected real work, consultation. Five main sections; no automatic product-card accumulation. |
| Services / 服务 | Delivery scope, retained business explanations, original workflow illustration and consultation links. |
| Products / 产品 | Approved bilingual public product/service directory with truthful availability states and official entry URLs. |
| Projects / 案例 | Approved real case directory. Homepage selects at most three; full directory grows independently. |
| Industries, Resources, FAQ | Retain their own URLs and directly readable HTML business information. |
| Independent platforms | Run actual products; their accounts, payment and customer-data boundaries remain independent. |
| CRM | Internal customer management, separate from the public corporate site. |
| Privacy, Terms, Security | Stable legal/security pages and original substantive text. |

Navigation remains Home, Services, Products, Projects, About, Contact and the matching Chinese pages. Secondary pages remain linked in the footer. Do not rename public URLs, collapse distinct topics, or replace business HTML with image-only or JavaScript-only content.

## Sources of truth

- `public/` is the shipping website. Root HTML/assets are a compatibility mirror; use `scripts/sync-public-mirror.py`. Historical `data/organization.json` and `public/data/organization.json` intentionally remain separate preserved assets.
- `public/assets/site.css` is the existing base system; `public/assets/premium-polish.css` is the single organized enterprise visual layer. Do not append more page-specific override files.
- `public/product-catalog.json` generates the static catalog regions in EN/ZH Products with `scripts/render-product-catalog.py`.
- Original `products.json` and other historical SEO/identity data remain preserved; do not overwrite them with the new catalog data.
- `public/projects.json` and `scripts/render-projects.py` generate static EN/ZH case cards. Preserve actual URLs, real screenshot files and publication permission.

## Add a product without redesigning Home

1. Confirm the real offering, official URL, release state and permission to display it.
2. Add one complete EN/ZH record to `public/product-catalog.json` using `docs/stable-architecture/PRODUCT-TEMPLATE.json`.
3. Use `service`, `public_unconfirmed`, `pilot` or verified `available` truthfully. `available` software requires `release_verified: true`. Public display approval and publication evidence are mandatory.
4. Do not put private, internal or unfinished products in the public JSON, even as hidden records. Drafts belong outside public deployment and public repositories.
5. Run the generator, mirror and preservation checks. Home structure remains unchanged.

New merchant cases use the existing case data/template and real screenshots. Do not fabricate customers, reviews, sales figures or delivery claims. Setting featured never creates more than three homepage cards. Updating the selected set is deliberate, never an automatic count of every new merchant.

## Verification and release

Run the commands in `docs/stable-architecture/MAINTENANCE.md`. Check real browsers and isolated preview. Classify every old asset PRESERVED / RELOCATED / IMPROVED; REMOVED requires separate human approval. If preservation cannot be proved, keep RELEASE HOLD.

Main, DNS, production traffic, payment, CRM and customer data are outside routine visual/catalog changes. This work authorizes design-branch development and isolated preview only; production requires explicit human approval.
