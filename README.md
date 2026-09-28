# course-ui — one host, five screens

The third part of the course. The two before it built a server and a client;
this one is about what the client puts on the glass.

Every screen is a JSON file under `screens/`. There is one host, in
`host/test/capture_test.dart`, and it never learns what any of them contain —
it loads a file, renders it, and writes a PNG.

| step | file | what it adds |
| --- | --- | --- |
| 1 | `screens/step1.json` | the screen is the file |
| 2 | `screens/step2.json` | layout is a direction and a gap |
| 3 | `screens/step3.json` | the number comes from state, not from the file |
| 4 | `screens/step4.json` | a button names a tool and stops there |
| 5 | `screens/step5.json` | one file, two shapes, and rows it did not count |

```bash
bash verify.sh                     # renders all five, checks what each claims
cd host && flutter test test/capture_test.dart   # or just the captures
```

Captures land in `captures/`, alongside `run.log` — which is where the two
things a picture cannot show get written down: the tool name a button actually
sent, and how many rows the list actually built.

`vendor/flutter_mcp_ui_runtime` is vendored so the folder runs on its own.
