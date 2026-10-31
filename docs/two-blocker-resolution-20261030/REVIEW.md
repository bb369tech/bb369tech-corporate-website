# Two-blocker resolution — 2026-10-30

Scope: candidate `367cf29f74425d0badee55bf58319510bed0bb0b`, main `5281d59c9d93e94d2862391060ffaae115f36008`. No visual, navigation, URL, HTML Schema, canonical, sitemap, payment, CRM, DNS or production deployment changes.

## Machine graph: exact restoration

Root cause: `public/` is the Cloudflare asset source. Its organization.json was a simplified single Organization; the historical root data/organization.json was the four-node graph still returned by production. Keeping the rich file in Git alone did not preserve the response at the public URL in preview.

`public/data/organization.json` is restored byte-for-byte from the freshly captured production response, which is also byte-identical to the unchanged historical root file. All four node IDs, relationships and fields remain intact. SHA-256: `391f76ae12888a73465ec31d7dd55bc67e7a8aa64dd044a8c4d195001e29c40a`.

The prior public variant is retained byte-for-byte as `organization-public-before-367cf29.json` in this review directory, SHA-256 `aae45df3a28b7d31aac7c5cc4472edf9939d4cbf475045fcf36d9d113f9285be`. The production graph also retains every URL/reference from that variant. No old file is silently discarded. Classification: public response IMPROVED/restored; prior variant RELOCATED to history; root historical file PRESERVED.

Four new restoration tests require exact production/root/public equality, the four original IDs, an exact old-public archive, no other runtime-byte changes, and retention of all prior machine references. Existing preservation tests now recognize only this precise authorized restoration, with the old archive and unchanged root required; no baseline reset or blanket JSON exclusion.

## Consultation: distinguish policy, validation and delivery

Verified LIVE source baseline: backend `1f4602b18e18da87af9a135fc36b0e55d9137cda`. Its CORS policy permits HTTPS bb369tech.com origins, but not this workers.dev preview. The CORS error then reaches the corporate parser's four-argument error handler, which labels every non-413 error as an invalid-body 400. This reproduces the actual preview OPTIONS response exactly: `Invalid or oversized inquiry. Please check the form.` It is not proof the frontend fields are malformed or the recipient email is wrong.

The current frontend provides required name/email/inquiryType/message/privacyConsent=accepted and preserves the topic alias. On an isolated loopback instance of exact live code, normal URL-encoded English/Chinese data returns 200 with synthetic mail capture. Missing fields/consent or invalid email correctly return 400. The confirmed campaign remains 403, rate limiting 429, oversize 413, duplicate requests do not repeat sends, and provider failure returns failure without automatic resending.

Only the existing isolated backend branch is adjusted: pass the recognized CORS error to the existing global CORS handler, preserving 403 instead of mislabeling it as a form 400. The prior exact-preview/path-scoped candidate exception remains unchanged. Other origins, other workers.dev sites and other routes remain denied. The full backend suite now passes 72 tests, including 10 new live-source/candidate contract tests. No production runtime source/configuration was changed.

Mail provider and CRM/AI/payment dependencies are replaced or fail closed in the isolated live-source harness. The durable-CRM candidate path is tested separately with local PGlite; passing a stubbed contract path is not represented as production persistence. Real SendGrid requests: 0. Production CRM writes: 0.

## Regression and release boundary

4 exact-restoration + 10 original-asset + 13 final static regression checks PASS; catalog and mirror checks PASS. All 205 files from the frontend parent remain; only one public runtime file changes. All HTML/CSS/JS/images and original form fields/path are byte-identical to `367cf29`, so the existing 105 responsive, 10 language, 30 filter and 8 browser-form simulation results are reused rather than rerunning unrelated visual changes. No test proof is substituted for real delivery.

Machine semantics require a final live preview hash comparison after the design branch update. Production backend must remain `1f4602b`; actual preview consultation will continue to be denied until a separately approved backend release. An intentional CORS denial is classified separately from a valid production-origin handler failure; it is still a limitation of the live preview.

Status: frontend asset repair can enter human review once the preview hash matches. Overall end-to-end production release remains NO-GO while actual consultation delivery/persistence is unverified and preview admission remains unavailable. No claim of full intake recovery, no main merge, no production deploy or backend rollout is authorized by this report.
