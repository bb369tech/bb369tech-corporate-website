# Content and URL preservation

No old public URL is renamed or removed. All 21 complete pages and existing historical alias files remain. No redirects are introduced.

| Previous location / behavior | Candidate location / behavior |
|---|---|
| Homepage Hero | Rewritten clear websites/software positioning and free consultation CTA, same homepage URLs |
| Homepage Services repeated blocks | One three-service region; prior detailed paragraphs retained on existing Services pages |
| Homepage Products / What We Do supporting blocks | Existing Products and Services pages retain the detailed business copy; industry material goes to existing Industries pages |
| Homepage one selected case | Three source-verified public projects, with real screenshots and external website links |
| Projects generic anonymous categories | Historical prose retained under Services delivery details; not presented as named customer work |
| Products | Existing URLs, product/service/pilot links, copy and status distinctions retained |
| Industries / Resources / FAQ | Original URLs/content retained, shared visual system |
| Contact forms | Original fields, values, required/consent logic, action, method and functional script retained |
| Privacy / Terms / Security | Original legal main text retained |
| Canonical / title / description / JSON-LD | Preserved on every existing page |
| Robots / Sitemap | Preserved, including previous 404 noindex correction and actual translation URLs |
| EN / Chinese navigation | Existing corresponding-language paths and reciprocal hreflang retained |
| Existing bot / CRM / payments | No new embed, backend or payment behavior introduced; no current bot embed was present in inspected baseline |
| New case workflow | `public/projects.json` + screenshots → `python scripts/render-projects.py` → static HTML EN/ZH homepage and directory |

The main index page has exactly five main sections: Hero, Services, Solutions, Featured Projects, Contact. Supporting content is migrated, not silently deleted. The migration is explicitly checked across the complete site.

Root mirrors are synchronized from public/; historical data/ records remain exempt/frozen. A runtime JavaScript failure does not hide the case content; filters are optional progressive enhancement.
