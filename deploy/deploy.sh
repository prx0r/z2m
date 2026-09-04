#!/bin/bash
set -e

# Star at Night - Cloudflare Deployment Script
# Usage: ./deploy.sh [project] [branch]
# Requires: CLOUDFLARE_API_TOKEN and CLOUDFLARE_ACCOUNT_ID environment variables

PROJECT=${1:-star-at-night}
BRANCH=${2:-main}
DEPLOY_DIR="/root/z2m/deploy/star-at-night"

# Check for required environment variables
if [ -z "$CLOUDFLARE_API_TOKEN" ] || [ -z "$CLOUDFLARE_ACCOUNT_ID" ]; then
    echo "❌ Error: Set CLOUDFLARE_API_TOKEN and CLOUDFLARE_ACCOUNT_ID"
    echo "   export CLOUDFLARE_API_TOKEN=your_token"
    echo "   export CLOUDFLARE_ACCOUNT_ID=your_account_id"
    exit 1
fi

echo "🚀 Deploying $PROJECT to Cloudflare Pages..."

# Ensure we're in the deploy directory
cd "$DEPLOY_DIR"

# Deploy to Cloudflare Pages
wrangler pages deploy . --project-name="$PROJECT" --branch="$BRANCH" --commit-dirty=true

echo "✅ Deployment complete!"
echo "🌐 Site: https://$PROJECT.pages.dev"
