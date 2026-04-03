#!/usr/bin/env bash
set -e

if [ -z "$OVH_HOST" ] || [ -z "$OVH_USER" ] || [ -z "$OVH_PATH" ]; then
  echo "OVH_HOST, OVH_USER et OVH_PATH doivent être définies"
  exit 1
fi

rsync -avz --delete \
  --exclude '.git' \
  --exclude '__pycache__' \
  --exclude '.venv' \
  ./ "$OVH_USER@$OVH_HOST:$OVH_PATH"

echo "Déploiement OVH terminé"
