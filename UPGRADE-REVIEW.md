# Corporate website additive upgrade — review draft

Production base: `7f3ee14594726fa7d7ca2794efeddaeb7e24e857`.
The official website version remains `v2.0.0`. This change creates no release or tag.

## Result

- Retains production English body content, original product cards and the public tools link. Adds three public service choices and the draft presentation styles.
- Integrates the public metadata changes from PR #3 without merging PR #3 or #4. Adds truthful Service nodes for ongoing support and custom business consultations.
- Generates the existing referenced 512px PNG from the existing SVG logo. No new brand design.
- Adds five separate Simplified Chinese pages with reciprocal language links. Other English-only destinations are clearly labelled. Chinese contact fields retain the same endpoint and select values. A follow-up correction supplies the backend-required inquiryType and explicit privacyConsent fields in both languages, while async submissions also retain topic as a compatibility alias.
- Mirrors changed website files into `public/`. Existing historical differences in `data/organization.json` versus `public/data/organization.json` are retained; neither data file is modified here.
- Leaves existing scripts, robots, legal/security pages, CNAME, backend endpoints and production version metadata unchanged. Adds a separate corporate-contact script and consent/status styles; only corporate contact forms use them. Public copy adds no private matching rules, decision logic, operational architecture or customer information.

## Validation

- `python tests/regression_public_site.py`: 10 tests, including baseline file retention, English body word/link retention, protected files, corrected contact contract, JSON-LD, local paths/fragments, reciprocal languages, changed-file mirrors and sitemap preservation.
- `node tests/browser_public_site.cjs` with Playwright available: 14 pages at widths 320, 390, 768, 1024 and 1440 (70 combinations), menu toggles, language navigation, FAQ interaction, form validation and two intercepted synthetic POSTs. No real POST or email is sent. Optionally set `BB369_CHROMIUM_EXECUTABLE` and `BB369_QA_ARTIFACT_DIR` for the local test environment.
- Main public offering, monthly support, merchant intake and tools URLs returned HTTP 200 during review. The monthly-support anchor was present.
- Production email delivery, indexing and AI recommendations are not established by these tests. A visual preview is not a production deployment.

## Review boundaries

No merge, deployment, release, payment or production submission is included.
PR #3 and #4 remain unchanged. This draft incorporates their relevant public improvements against the verified production base.

Follow-up contact fix: the previous topic-only form omitted backend-required inquiryType and privacyConsent. The pinned backend handler fixture reproduces rejection of the former payload and acceptance of the corrected payload with mail intercepted. Run `node --test tests/corporate-contact-contract.test.cjs` with Playwright available. It also checks explicit consent, provider failures, false success and retention of inputs on failure. Actual Render recipient configuration and inbox delivery remain unverified until the workspace selection and production verification are completed.
