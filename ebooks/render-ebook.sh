#!/usr/bin/env bash
# Render ebooks/ebook-seamwise.pdf from the Seamwise ebook deck.
# Assembles .build/head.html + act fragments + tail.html into
# prt-seamwise-ebook.html, then prints to PDF via headless Chrome at
# exactly 1440x900pt per page (one .page element per PDF page).
set -euo pipefail
cd "$(dirname "$0")"

OUT_HTML="prt-seamwise-ebook.html"
OUT_PDF="ebook-seamwise.pdf"
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# 1. assemble
cat .build/head.html > "$OUT_HTML"
for f in .build/act0.html .build/act1.html .build/act2.html .build/act3.html \
         .build/act4.html .build/act5.html .build/act6.html .build/act7.html \
         .build/act8.html .build/act9.html; do
  [ -f "$f" ] && cat "$f" >> "$OUT_HTML"
done
cat .build/tail.html >> "$OUT_HTML"
echo "assembled $OUT_HTML ($(wc -l < "$OUT_HTML" | tr -d ' ') lines)"

# 2. print to PDF
"$CHROME" --headless=new --disable-gpu --no-pdf-header-footer \
  --virtual-time-budget=45000 \
  --print-to-pdf="$OUT_PDF" "file://$PWD/$OUT_HTML" 2>/dev/null

# 3. report
pdfinfo "$OUT_PDF" | grep -E "Pages|Page size|File size"
