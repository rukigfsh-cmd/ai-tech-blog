#!/usr/bin/env bash
# Jekyll ビルド確認（GitHub Pages と同じ github-pages gem を使う）。
# 公開前に必ず実行し、"BUILD OK" が出ない変更は公開しない。
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"

export BUNDLE_PATH="${BUNDLE_PATH:-$HOME/.cache/kasegi-bundle}"
export BUNDLE_SILENCE_ROOT_WARNING=1

bundle install --jobs 4 --quiet
OUT="$(mktemp -d)"
trap 'rm -rf "$OUT"' EXIT
bundle exec jekyll build --quiet -d "$OUT"
echo "BUILD OK: $(find "$OUT" -name '*.html' | wc -l) pages"
