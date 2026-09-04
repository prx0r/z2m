# Star at Night - Cloudflare Deployment

## Quick Deploy

```bash
./deploy.sh
```

## Manual Deploy

```bash
cd /root/z2m/deploy/star-at-night
CLOUDFLARE_API_TOKEN="your_token" CLOUDFLARE_ACCOUNT_ID="your_account_id" \
wrangler pages deploy . --project-name=star-at-night --branch=main
```

## URLs

- **Production:** https://star-at-night.pages.dev
- **Preview:** https://<hash>.star-at-night.pages.dev

## R2 Storage

- **Bucket:** star-at-night
- **Endpoint:** https://954612afb5a97bb15dddcdc70176813d.r2.cloudflarestorage.com
- **Use:** Product images, generated PDFs, user uploads

## Credentials

Stored in `~/.agent-vault/vault.json`:
- `CLOUDFLARE_API_TOKEN`
- `CLOUDFLARE_ACCOUNT_ID`
- `CLOUDFLARE_R2_ACCESS_KEY`
- `CLOUDFLARE_R2_SECRET_KEY`
- `CLOUDFLARE_R2_ENDPOINT`

## Architecture

```
Cloudflare Pages (static site)
    ↓
Cloudflare R2 (assets, images, PDFs)
    ↓
Cloudflare Workers (API, checkout, webhooks)
    ↓
Prodigi (print fulfillment)
    ↓
Etsy (marketplace sales)
```

## Next Steps

1. [ ] Add custom domain (staratnight.com or similar)
2. [ ] Set up Cloudflare Workers for API endpoints
3. [ ] Configure R2 public access for product images
4. [ ] Add Cloudflare Analytics
5. [ ] Set up GitHub Actions for auto-deploy
