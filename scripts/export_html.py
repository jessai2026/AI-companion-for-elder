"""Freeze each screen as a standalone HTML file.

    uv run elder-web                                       # the app must be running
    uv run --with playwright python scripts/export_html.py

Saving the server's HTML directly is not enough: the pages link a stylesheet, four
scripts and a webfont, and the dashboard renders its content from the API after load. So
each file is captured from a real browser *after* the page has settled, with the
stylesheet inlined and the scripts dropped — what is left is the finished DOM with its
styling, which opens with no server and imports into a design tool.

Fonts are left as the Google Fonts link. A design tool resolves it; offline the page
falls back to the same stack the app declares.

Output: demo/html/<lang>/NN-name.html
"""

from __future__ import annotations

import argparse
import sys
import time
import urllib.request
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
BASE = "http://127.0.0.1:8000"

# name -> (path, tab, viewport width)
SCREENS: list[tuple[str, str, str | None, int]] = [
    ("01-elder-start", "/elder", None, 390),
    ("02-elder-chat", "/elder", "chat", 390),
    ("03-today", "/family", "today", 390),
    ("04-alerts", "/family", "alerts", 390),
    ("05-care", "/family", "care", 390),
    ("06-camera", "/family", "monitor", 390),
    ("07-chat", "/family", "chat", 390),
    ("08-weekly", "/family/report/weekly", None, 900),
    ("09-doctor", "/family/doctor", None, 900),
    ("10-memoir", "/family/memoir", None, 900),
    ("11-dashboard-wide", "/family", "today", 1280),
]

FREEZE = """() => {
  // Inline every same-origin stylesheet, so the file carries its own styling.
  for (const link of [...document.querySelectorAll('link[rel="stylesheet"]')]) {
    const href = link.getAttribute('href') || '';
    if (!href.startsWith('/')) continue;          // leave the webfont link alone
    const sheet = [...document.styleSheets].find(s => s.href && s.href.endsWith(href));
    if (!sheet) continue;
    // @import pulls in the design tokens; cssText keeps the @import line rather than
    // its contents, so following it is what stops the exported file losing every
    // custom property and falling back to Times on a transparent background.
    const dump = (sh) => {
      let out = '';
      let rules;
      try {
        rules = [...sh.cssRules];
      } catch {
        return '';
      }
      for (const r of rules) {
        if (r.type === CSSRule.IMPORT_RULE) {
          out += r.styleSheet ? dump(r.styleSheet) + '\\n' : '';
        } else {
          out += r.cssText + '\\n';
        }
      }
      return out;
    };
    const css = dump(sheet);
    if (!css) continue;
    const style = document.createElement('style');
    style.setAttribute('data-from', href);
    style.textContent = css;
    link.replaceWith(style);
  }
  // Scripts have already done their work; keeping them would re-run against no server.
  for (const s of [...document.querySelectorAll('script')]) s.remove();
  for (const l of [...document.querySelectorAll('link[rel="manifest"]')]) l.remove();
  // The camera is a live stream; freeze the frame that is on screen.
  for (const img of [...document.querySelectorAll('img')]) {
    if ((img.getAttribute('src') || '').startsWith('/fall/stream')) {
      try {
        const c = document.createElement('canvas');
        c.width = img.naturalWidth || img.width;
        c.height = img.naturalHeight || img.height;
        c.getContext('2d').drawImage(img, 0, 0);
        img.setAttribute('src', c.toDataURL('image/jpeg', 0.85));
      } catch { /* tainted canvas; leave the src */ }
    }
  }
  return '<!doctype html>\\n' + document.documentElement.outerHTML;
}"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lang", default="en", choices=["en", "zh"])
    args = ap.parse_args()

    try:
        urllib.request.urlopen(f"{BASE}/healthz", timeout=3)
    except Exception:
        print(f"No server at {BASE} — start it with ./scripts/demo_up.sh first.", file=sys.stderr)
        return 1

    out = ROOT / "demo" / "html" / args.lang
    out.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome")
        for name, path, tab, width in SCREENS:
            ctx = browser.new_context(
                viewport={"width": width, "height": 900},
                device_scale_factor=2,
                is_mobile=width < 500,
                permissions=["microphone"],
                locale="zh-CN" if args.lang == "zh" else "en-US",
            )
            page = ctx.new_page()
            url = f"{BASE}{path}?lang={args.lang}"
            if tab and path == "/family":
                url += f"&tab={tab}"
            page.goto(url, wait_until="networkidle")

            if name == "02-elder-chat":
                page.click("#start-btn")
                page.wait_for_selector(".conversation .bubble", timeout=20_000)
                page.click("summary")
            time.sleep(6 if tab == "monitor" else 3)

            html = page.evaluate(FREEZE)
            (out / f"{name}.html").write_text(html, encoding="utf-8")
            print(f"  {name}.html  ({len(html) // 1024} KB)")
            ctx.close()
        browser.close()

    print(f"\n{out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
