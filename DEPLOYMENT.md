# Deployment and source ownership

Cloudflare Worker: `bb369tech-corporate-website`.
Production branch: `main`. Static directory: `public/`.
Existing Wrangler settings and Worker Previews are preserved.

**v3.0 candidate is on release hold.** Do not run a production deploy or merge without approval of the final independent preview.

`public/` is the source of truth for HTML, CSS, JS, media and sitemap. Run `python scripts/sync-public-mirror.py` after editing it. Root files are compatibility mirrors for existing GitHub Pages paths. `--check` detects drift. No file is deleted by this script.

Exception: `data/` contains divergent historical machine-readable institution records. Both original root and public records remain frozen; the mirror script intentionally skips `data/`. Reconcile them only in a separately reviewed semantic change.

The local `.openai/hosting.json` and `public/__qa/` are ignored and serve only local browser QA. They are not Cloudflare configuration or shipping source. Do not publish the user-supplied visual reference.

Preview generation must use the existing Worker preview mechanism. A successful build alone does not establish a working URL. The candidate URL must be opened and verified before production approval.
