#!/usr/bin/env bash
# install_fonts.sh — make bundled Persian fonts visible to LibreOffice/Chrome/weasyprint.
# Run BEFORE any docx→PDF or pptx→PDF conversion, or Persian silently renders in DejaVu.
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC="$SKILL_DIR/assets/fonts"
DEST="$HOME/.fonts"

count=$(find "$SRC" -maxdepth 2 \( -iname '*.ttf' -o -iname '*.otf' \) 2>/dev/null | wc -l)
if [ "$count" -eq 0 ]; then
  echo "ERROR: no font files in $SRC" >&2
  echo "Bundled fonts are missing. Ask the user for the TTFs or run scripts/download_fonts.py (needs GitHub access)." >&2
  exit 1
fi

mkdir -p "$DEST"
find "$SRC" -maxdepth 2 \( -iname '*.ttf' -o -iname '*.otf' \) -exec cp -f {} "$DEST/" \;
fc-cache -f "$DEST" >/dev/null 2>&1 || fc-cache -f >/dev/null 2>&1

echo "installed $count font file(s) to $DEST:"
fc-list :lang=fa family 2>/dev/null | sort -u | sed 's/^/  /'
