# Getting the screens into Figma

Two ways. Pick by whether the app happens to be running.

## The short way: from a live URL

This is the one the plugin is built for, and it gives the cleanest layers.

1. In Figma, open **Resources → Plugins**, search **html.to.design**, install it.
2. Start the app and put it on a public address:

   ```bash
   ./scripts/demo_up.sh
   ./scripts/share.sh          # prints an https://… address
   ```

3. Run the plugin, paste an address from the list below, set the width, click import.

| Screen | Address | Width |
|---|---|---|
| Elder app | `<base>/elder` | 390 |
| Today | `<base>/family?tab=today` | 390 |
| Alerts | `<base>/family?tab=alerts` | 390 |
| Care | `<base>/family?tab=care` | 390 |
| Camera | `<base>/family?tab=monitor` | 390 |
| Chat | `<base>/family?tab=chat` | 390 |
| Weekly report | `<base>/family/report/weekly` | 900 |
| Doctor one-pager | `<base>/family/doctor` | 900 |
| Her stories | `<base>/family/memoir` | 900 |
| Dashboard, wide | `<base>/family` | 1280 |

Add `&lang=zh` (or `?lang=zh` where there is no `?` yet) for the Chinese interface.

The dashboard shows one tab at a time, so each tab needs its own import — that is what
`?tab=` is for.

**The tunnel address changes every time `share.sh` runs.** Import in one sitting.

## The other way: from files

Already exported, in the repo, and they open with nothing running:

```
demo/html/en/    11 screens, English
demo/html/zh/    11 screens, Chinese
```

Each file carries its own styling, so it opens correctly by double-clicking. In the
plugin, switch from **URL** to **Code** and paste the file's contents.

Regenerate them after a UI change:

```bash
./scripts/demo_up.sh
uv run --with playwright python scripts/export_html.py --lang en
uv run --with playwright python scripts/export_html.py --lang zh
```

## What you get, and what you don't

You get real layers: frames, text, colours, images. You can pull colours and type off
them, rearrange, annotate, and build slides.

You do not get a working prototype. The live camera becomes a still, hold-to-talk becomes
a shape, and an alert arriving becomes a screenshot of one that already has. For showing
how it behaves, the app on a phone is more convincing than anything Figma will produce
from this.

Webfonts come from Google Fonts. If a heading looks wrong after import, install
**Atkinson Hyperlegible Next** and **Fraunces** locally and Figma will pick them up.
