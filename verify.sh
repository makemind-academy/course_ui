#!/bin/bash
# course-ui — each step is checked against what its article claims, in AppPlayer.
set -euo pipefail
cd "$(dirname "$0")"
echo "   [1/3] nothing in screens/ is code; the bundle carries the same files"
python3 - <<'PY' || exit 1
import json
for i in range(1, 6):
    a = json.load(open(f"screens/step{i}.json")); b = json.load(open(f"course_ui.mbd/ui/pages/step{i}.json"))
    assert a == b, f"step{i} differs between screens/ and the bundle"
alt = json.load(open("course_ui.mbd/ui/pages/step3_alt.json")); s3 = json.load(open("screens/step3.json"))
assert alt["content"] == s3["content"] and alt["initialState"] != s3["initialState"], "step3_alt must be the same screen with another state"
PY
grep -qE '"(42|7)"' screens/step3.json && { echo "   step3: the value is baked in"; exit 1; }
grep -q '{{now}}' screens/step3.json || { echo "   step3: nothing is bound"; exit 1; }
grep -qE '"(44|45|46)"' screens/step5.json && { echo "   step5: the rows are baked in"; exit 1; }
grep -q '"itemTemplate"' screens/step5.json || { echo "   step5: no row template"; exit 1; }
echo "   [2/3] open the bundle in AppPlayer and walk the steps"
rm -f captures/*.png
python3 verify.py
echo "   [3/3] captures"
COUNT=$(ls captures/*.png | wc -l | tr -d ' ')
[ "$COUNT" -eq 8 ] || { echo "   expected 8 captures, got $COUNT"; exit 1; }
