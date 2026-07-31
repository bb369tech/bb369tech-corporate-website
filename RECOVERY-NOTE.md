# Emergency Recovery

This package keeps the website files in both the repository root and `public/`.

- GitHub Pages can continue serving the root files immediately.
- Cloudflare Workers can continue deploying from `public/` through `wrangler.jsonc`.

After the custom domain is fully moved to Cloudflare Workers, the duplicated root website files may be removed in a later maintenance release.
