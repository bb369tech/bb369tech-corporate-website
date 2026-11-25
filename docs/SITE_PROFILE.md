# SITE PROFILE — BB369TECH Corporate Website (isolated Draft, not production approval)
## Identity and current scope
- Repository: `bb369tech/bb369tech-corporate-website`; domain: `bb369tech.com`
- Site type: D — corporate brand/product/case catalog
- Supported language target: en/zh
- Business model: Company site: public/ authoritative, projects capped to three featured, SEO/FAQ/contact.
- Primary customer journey: Understand company → service/product/project detail → approved company contact or platform referral
- Explicitly excluded from this release: No invented products, fake projects, merchant order checkout or customer data migration. No redesign of company shell.
- Source branch: Draft PR #16
- Live hosting/revision evidence: Existing corporate site; do not infer site published SHA from documentation PR; preserve ARCHITECTURE-LOCK.md and public mirror.

## Rules and safety
- Candidate corporate baseline: `bb369tech/bb369tech-tools@2391484995b04e01c09dc7d6b70fecd0e052d295:standards/engineering/v2.0/SITE_DELIVERY.md` (Draft PR #7, not merged).
- Use this repository's `AGENTS.md` and `docs/验收.md` for specific business functions. A corporate common rule must never replace this site's industry constraints.
- Current factual/rights blockers: Only approved public/product-catalog.json and public/projects.json entries, photo/identity/legal approval.
- Autonomous scope: isolated repo edits, minimal changes, synthetic checks, desktop/mobile preview, evidence and Draft PR; no real emails or third-party link submissions.
- Costs: **new $0**. Never create charged/free-trial-to-bill resources, upgrade plan, use billable CI without confirmed no-cost cap.
- Release: **NOT APPROVED**. No `main` merge, production DNS/hosting changes, production database/secrets/payments or published external URLs without a specific separate human approval. Keep rollback.
- Search promotion: technical indexability and useful pages can be validated; actual Google/Bing indexing, AI recommendations and third-party backlinks require real evidence. No link farm/mirror/auto-exchange; research and drafts only until approved.
- Existing baseline commands: scripts/sync-public-mirror.py, tests/stable-asset-lock.py, tests/final-visual-regression.py and existing tests subject to site instructions.
- Result levels: source/readback ≠ local tests ≠ preview ≠ remote CI ≠ live deployed SHA ≠ third-party indexing ≠ business conversions. Report GO/NO-GO separately.
