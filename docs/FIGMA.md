# Getting the screens into Figma

You do not need anyone else's machine. Clone the repo, run one command, import.

## Do this

**1. Install the plugin.** In Figma: **Resources → Plugins**, search
**html.to.design**, install.

**2. Start the app.** In a terminal:

```bash
git clone https://github.com/SeroGoingCrazy/AI-companion-for-elder.git
cd AI-companion-for-elder
./scripts/demo_up.sh
```

Needs [uv](https://docs.astral.sh/uv/) and Python 3.12. No API key. Leave that terminal
open; Ctrl-C there stops the app.

**3. Import each screen.** Run the plugin, paste an address, set the width, click import.
One at a time.

| Screen | Paste this | Width |
|---|---|---|
| Elder app | `http://127.0.0.1:8000/elder` | 390 |
| Today | `http://127.0.0.1:8000/family?tab=today` | 390 |
| Alerts | `http://127.0.0.1:8000/family?tab=alerts` | 390 |
| Care | `http://127.0.0.1:8000/family?tab=care` | 390 |
| Camera | `http://127.0.0.1:8000/family?tab=monitor` | 390 |
| Chat | `http://127.0.0.1:8000/family?tab=chat` | 390 |
| Weekly report | `http://127.0.0.1:8000/family/report/weekly` | 900 |
| Doctor one-pager | `http://127.0.0.1:8000/family/doctor` | 900 |
| Her stories | `http://127.0.0.1:8000/family/memoir` | 900 |
| Dashboard, wide | `http://127.0.0.1:8000/family` | 1280 |

That is the whole thing.

## If something is odd

**The plugin cannot reach the address.** Some versions of html.to.design fetch through
their own server, which cannot see `127.0.0.1`. Put the app on a public address instead:

```bash
./scripts/share.sh
```

It prints an `https://…` address. Use that in place of `http://127.0.0.1:8000` in the
table above. The address changes every run, so import in one sitting.

**A heading looks wrong.** Install **Atkinson Hyperlegible Next** and **Fraunces**
locally; both are free from Google Fonts.

**Only one tab shows up.** The dashboard shows one tab at a time on purpose. Each tab is
its own import — that is what `?tab=` is doing.

**Nothing is running and you just want the files.** They are committed:
`demo/html/en/` and `demo/html/zh/`, eleven screens each. Open one to look at it. In the
plugin, switch from **URL** to **Code** and paste the file's contents. Regenerate them
after a UI change with `uv run --with playwright python scripts/export_html.py`.

**You want the Chinese interface.** Add `&lang=zh` to any address, or `?lang=zh` where
there is no `?` yet.

## What the import gives you

Real layers: frames, text, colours, images. Pull colours and type off them, rearrange,
annotate, build slides.

Not a working prototype. The live camera becomes a still, hold-to-talk becomes a shape,
and an alert arriving becomes a screenshot of one that already has. To show how it
behaves, the app on a phone does that better than Figma will.
