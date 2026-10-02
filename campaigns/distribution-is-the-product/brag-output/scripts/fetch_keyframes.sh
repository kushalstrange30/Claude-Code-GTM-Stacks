#!/usr/bin/env bash
# Pull the Higgsfield key frames (Nano Banana 2, 16:9, 1376x768) into the composition.
# Needs d8j0ntlcm91z4.cloudfront.net reachable from this environment.
set -euo pipefail
cd "$(dirname "$0")/../composition/assets/img"
mkdir -p hf
base=https://d8j0ntlcm91z4.cloudfront.net/user_3JrUAwIbjln1sRjAjcUuEoszBpU
while read -r name file; do
  curl -fsS -o "hf/$name.png" "$base/$file.png" && echo "ok $name"
done <<'LIST'
open-1-rooftop    hf_20261002_210920_180dc519-f29b-4cfc-903c-e164812760c6
open-2-spark      hf_20261002_210932_be964bda-24e4-4bf1-a471-e4c3a1fcfa6f
open-3-city-grid  hf_20261002_210931_19ad36ef-b31f-486f-986a-939ab4ec404d
end-1-agent-hall  hf_20261002_210931_900f816d-4eac-4b8e-babb-e08052cf9711
end-2-orbit       hf_20261002_210932_7553d743-0fea-420c-bb54-37a6a276743f
end-3-monolith    hf_20261002_210934_c3900145-1d7c-4f72-8c6e-4f85686aff47
LIST
