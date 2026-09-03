#!/usr/bin/env bash
# Détecteur d'anti-patterns impeccable, sans LLM et sans clé API.
# Usage: bash scripts/detect.sh "Prospect-demo.html"
set -u
D="$HOME/.claude/plugins/marketplaces/impeccable/plugin/skills/impeccable/scripts/detect.mjs"
if [ ! -f "$D" ]; then
  echo "detect.sh: plugin impeccable absent. Ignorer cette passe." >&2
  exit 0
fi
if [ ! -d "$HOME/.claude/plugins/marketplaces/impeccable/node_modules" ]; then
  echo "detect.sh: dépendances manquantes, passe DÉGRADÉE (pas de contraste calculé)." >&2
  echo "  cd ~/.claude/plugins/marketplaces/impeccable && npm install --omit=dev --omit=optional" >&2
fi
node "$D" "$@"
