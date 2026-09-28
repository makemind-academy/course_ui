#!/usr/bin/env python3
"""course-ui: five screens, five files. The player draws each one; the same file drawn from another state shows another screen."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "tools"))
from appplayer import AppPlayer  # noqa: E402
from mcpclient import Server  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
CAP = os.path.join(HERE, "captures")

ap = AppPlayer()
bid = ap.install_bundle(os.path.join(HERE, "course_ui.mbd"))
ap.restart()
ap.open_bundle(bid)
ap.wait_text("Five screens, five files")
for label, key, shot in (
    ("Step 1 · the screen is the file", "The whole screen is this file", "step1"),
    ("Step 2 · layout is a direction and a gap", "", "step2"),
    ("Step 3 · the number is not in the file", "", "step3"),
    ("Step 3 · same file, another state", "7", "step3_alt"),
    ("Step 4 · the button names a tool", "Call next", "step4"),
    ("Step 5 · one file, two shapes (empty)", "", "step5_empty"),
    ("Step 5 · one file, two shapes (filled)", "44", "step5_filled"),
):
    ap.tap(label)
    if key:
        ap.wait_text(key)
    else:
        import time
        time.sleep(1.5)
    ap.shot(f"{CAP}/{shot}.png")
    ap.tap_id("back") if False else None
    # Every step page pops back to the menu through the player's back gesture;
    # the menu is re-entered by restarting, which is cheaper than guessing a
    # host control from a script.
    ap.restart()
    ap.open_bundle(bid)
    ap.wait_text("Five screens, five files")
# The last claim of part 5: a screen this track never wrote, drawn by the same
# player. It comes from the server track's finished server, over MCP, at run time.
DESK = os.path.join(HERE, "course-server")
# The server keeps its count on disk (part 5 of that track). Start from the seed
# so the number in this article is the number a reader gets.
state = os.path.join(DESK, "desk-state.json")
if os.path.exists(state):
    os.remove(state)
with Server(["dart", "run", "bin/step6.dart"], cwd=DESK) as desk:
    served = desk.read("ui://desk")
    assert served["type"] == "page" and served["title"] == "Desk", served
    before = desk.read("desk://waiting")["waiting"]

ap.register_server("com.makemind.sample.course_desk", "Course desk", cwd=os.path.abspath(DESK),
                   args=["run", "bin/step6.dart"])
ap.restart()
ap.open_server("com.makemind.sample.course_desk")
ap.wait_text("Admit one")
ap.expect_text("Desk")
# The count stays blank on purpose: `{{waiting}}` is a slot, and nothing in this
# document asks anyone to fill it. That is the line between a document and an app.
assert not any(t == str(before) for t, _ in ap.texts(str(before))), "the slot was filled by somebody"
ap.shot(f"{CAP}/step5_live_desk.png")
print(f"   ui://desk arrived at run time — type={served['type']}, title={served['title']}, waiting was {before}")
print("course-ui: five files drawn, step3 drawn from two states, step5 in two shapes, and a screen from the server track drawn by the same player")
