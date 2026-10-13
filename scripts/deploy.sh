#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
target="${BLOG_SSH_HOST:-hostinger}"
release="$(date -u +%Y%m%dT%H%M%SZ)-$(git rev-parse --short HEAD)"
npm ci
npm run build
archive="$(mktemp)"
trap 'rm -f "$archive"' EXIT
tar -czf "$archive" -C dist .
ssh "$target" "mkdir -p /opt/dev-universe-blog/site/releases/$release"
scp "$archive" "$target:/opt/dev-universe-blog/release.tgz"
scp deploy/compose.yaml deploy/nginx.conf "$target:/opt/dev-universe-blog/"
ssh "$target" bash -s -- "$release" <<'REMOTE'
set -euo pipefail
release="$1"
cd /opt/dev-universe-blog
tar -xzf release.tgz -C "site/releases/$release"
chmod -R a+rX "site/releases/$release"
if test -L site/current; then readlink site/current > previous-release.txt; fi
ln -s "releases/$release" site/next
mv -Tf site/next site/current
docker compose config --quiet
docker compose up -d
printf '%s\n' "$release" > deployed-release.txt
REMOTE
curl --fail --retry 5 --retry-delay 3 https://dev-universe.tech/ -o /dev/null
