# Rollback

No production or preview deployment occurred for this revision.

The preserved baseline is 49c4bf9ce734b44694d1f33fcf85973cbe8b60d8. Undo the isolated candidate with a normal revert of the candidate commit, never a force reset of main. Moving a remote branch must follow the user's preview-deployment authorization because the design branch automatically generates a Cloudflare preview.

No DNS, payment or CRM rollback is needed. Old public paths and frozen historical data records remain. A later approved production release must retain its preceding deployed version for recovery and re-check the URL map and inquiry contract after rollback.
