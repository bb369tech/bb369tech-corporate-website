# BB369TECH corporate website working rules

Read ARCHITECTURE-LOCK.md before changing this site. This is the existing corporate website; preserve its public identity and digital assets.

- Work in the existing authorized design/development branch. Never merge main, deploy production, alter DNS, payment, CRM or customer data without explicit user approval.
- public/ is authoritative. Mirror public HTML/assets with scripts/sync-public-mirror.py. Preserve the intentionally separate historical data/organization.json files.
- Keep the fixed company navigation and page responsibilities. New products use public/product-catalog.json and the static bilingual catalog generator; new real cases use public/projects.json. Do not redesign Home for every product or merchant. Featured cases are capped at three.
- Public JSON is publicly readable. Do not put internal, unfinished or unapproved products/clients there, even if the renderer would hide them. Preserve truthful pilot/unconfirmed states and public-release evidence.
- Preserve original URLs, business HTML, head metadata, JSON-LD, language relationships, Sitemap, Robots, FAQ, legal text, links, forms, mail/backend entry paths, real screenshots and old public records. Do not reduce important content to images, collapsed-only content or JavaScript-only rendering.
- Use the existing organized CSS system, not accumulating new override stylesheets. Keep desktop/mobile and English/Chinese consistent.
- Run product/case generation checks, mirror checks, tests/stable-asset-lock.py and tests/final-visual-regression.py. A new approved record may extend a catalog without changing the shell; do not delete an old record or weaken preservation tests to obtain PASS. If an approved factual correction requires updating a pinned preservation baseline, provide the exact Before/After and retain historical evidence.
- Do not send real inquiry emails or execute real payments in QA. Use the isolated non-delivery fixtures. Label PASS / FAIL / NOT VERIFIED honestly and keep RELEASE HOLD when preservation cannot be proved.
