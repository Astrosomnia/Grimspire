#!/usr/bin/env python3
"""Grimspire build helper.

The game lives in one HTML file, and index.html on main is the source of truth: edit it directly.
The source is the page from <title> on; this tool wraps it with the <head> and writes:

  index.html        - the live game, with OpenGraph tags
  debug/index.html  - the test build: noindex, GS_DEBUG=1 (TEST panel), title "Grimspire Test"

The Forge also writes both files when it releases art; it only replaces the LAB_PAYLOAD block.

Usage
  python3 tools/build.py debug                                   # rebuild index.html and debug/ from index.html (run after every edit)
  python3 tools/build.py build src.html                          # write index.html and debug/index.html from a bare source
  python3 tools/build.py src > src.html                          # print the bare source of the current index.html
  python3 tools/build.py extract <artifact-read.html> src.html   # legacy: strip claude.ai's wrapper from an Artifact read
"""
import re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
DESC = "A dark prophecy of war and woe. The spire will stand. Its defenders will not."
URL = "https://astrosomnia.github.io/Grimspire/"

HEAD = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#06070a">
<meta name="description" content="{DESC}">
<meta property="og:type" content="website">
<meta property="og:title" content="Grimspire">
<meta property="og:description" content="{DESC}">
{{OGURL}}
<meta property="og:image" content="{URL}og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{URL}og.jpg">
<style>body{{margin:0}}</style>
"""


def extract(page: str) -> str:
    """Take an Artifact 'read' (claude.ai skeleton + source) and return the source alone."""
    i = page.index("<title>")
    j = page.rfind("</body></html>")
    return page[i:j if j > i else None].rstrip() + "\n"


def from_index(page: str) -> str:
    i = page.index("<title>")
    j = page.rfind("</html>")
    return page[i:j].rstrip() + "\n"


def build(src: str):
    if not src.startswith("<title>Grimspire</title>"):
        sys.exit("source should start with <title>Grimspire</title>")
    live = HEAD.replace("{OGURL}", f'<meta property="og:url" content="{URL}">') + src + "\n</html>\n"
    dbg = (HEAD.replace("{OGURL}", '<meta name="robots" content="noindex">')
           + "<script>window.GS_DEBUG=1</script>\n"
           + src.replace("<title>Grimspire</title>", "<title>Grimspire Test</title>", 1)
           + "\n</html>\n")
    (ROOT / "index.html").write_text(live)
    (ROOT / "debug").mkdir(exist_ok=True)
    (ROOT / "debug" / "index.html").write_text(dbg)
    gv = re.search(r"const GV=(\d+)", src)
    print(f"built index.html and debug/index.html (GV={gv.group(1) if gv else '?'})")


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[:1] == ["extract"] and len(a) == 3:
        pathlib.Path(a[2]).write_text(extract(pathlib.Path(a[1]).read_text()))
    elif a[:1] == ["build"] and len(a) == 2:
        build(pathlib.Path(a[1]).read_text())
    elif a[:1] == ["debug"]:
        build(from_index((ROOT / "index.html").read_text()))
    elif a[:1] == ["src"]:
        sys.stdout.write(from_index((ROOT / "index.html").read_text()))
    else:
        sys.exit(__doc__)
