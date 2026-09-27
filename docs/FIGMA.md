# Getting the screens into Figma

Nothing to install, nothing to run. Every screen is already on the web.

## Do this

**1.** In Figma: **Resources → Plugins**, search **html.to.design**, install it.

**2.** Run the plugin, paste an address from the table, set the width, click import. One
screen at a time.

| Screen | Paste this | Width |
|---|---|---|
| Elder app | `https://jessai2026.github.io/AI-companion-for-elder/demo/html/en/01-elder-start.html` | 390 |
| Elder app, talking | `https://jessai2026.github.io/AI-companion-for-elder/demo/html/en/02-elder-chat.html` | 390 |
| Today | `https://jessai2026.github.io/AI-companion-for-elder/demo/html/en/03-today.html` | 390 |
| Alerts | `https://jessai2026.github.io/AI-companion-for-elder/demo/html/en/04-alerts.html` | 390 |
| Care | `https://jessai2026.github.io/AI-companion-for-elder/demo/html/en/05-care.html` | 390 |
| Camera | `https://jessai2026.github.io/AI-companion-for-elder/demo/html/en/06-camera.html` | 390 |
| Chat | `https://jessai2026.github.io/AI-companion-for-elder/demo/html/en/07-chat.html` | 390 |
| Weekly report | `https://jessai2026.github.io/AI-companion-for-elder/demo/html/en/08-weekly.html` | 900 |
| Doctor one-pager | `https://jessai2026.github.io/AI-companion-for-elder/demo/html/en/09-doctor.html` | 900 |
| Her stories | `https://jessai2026.github.io/AI-companion-for-elder/demo/html/en/10-memoir.html` | 900 |
| Dashboard, wide | `https://jessai2026.github.io/AI-companion-for-elder/demo/html/en/11-dashboard-wide.html` | 1280 |

That is all of it.

**For the Chinese interface**, change `/en/` to `/zh/` in any of those addresses.

Open any of them in a browser first if you want to see what you are importing.

## If something is odd

**A heading looks wrong after import.** Install **Atkinson Hyperlegible Next** and
**Fraunces** locally, both free from Google Fonts, and Figma will pick them up.

**A screen looks out of date.** These are snapshots taken from the running app. After a UI
change, regenerate and push them:

```bash
./scripts/demo_up.sh
uv run --with playwright python scripts/export_html.py --lang en
uv run --with playwright python scripts/export_html.py --lang zh
git add demo/html && git commit -m "chore: refresh exported screens" && git push
```

GitHub Pages serves the `merge/upstream-dev` branch, so a push updates the addresses
within a minute or two.

**You want to import from the app as it runs**, rather than from a snapshot — for a state
these files do not cover, say. Start it and use the local addresses instead:

```bash
./scripts/demo_up.sh
```

Then `http://127.0.0.1:8000/elder`, `http://127.0.0.1:8000/family?tab=care`, and so on.
Some builds of the plugin fetch through their own server and cannot reach `127.0.0.1`; if
that happens, `./scripts/share.sh` prints a public address to use instead.

## What the import gives you

Real layers: frames, text, colours, images. Pull colours and type off them, rearrange,
annotate, build slides.

Not a working prototype. The live camera becomes a still, hold-to-talk becomes a shape,
and an alert arriving becomes a screenshot of one that already has. To show how it
behaves, the app on a phone does that better than Figma will.
