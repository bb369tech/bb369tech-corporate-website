# Deployment

## GitHub Pages

Publish from the repository root. Keep `CNAME`, `index.html`, and the public website files in the root directory.

## Cloudflare Workers

Deploy with:

```bash
npx wrangler deploy
```

Wrangler publishes only the files inside `public/`.
