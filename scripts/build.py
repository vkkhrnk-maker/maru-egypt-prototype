#!/usr/bin/env python3
"""Собирает docs/index.html (то, что публикует GitHub Pages) из prototype/index.html.

Исходник prototype/index.html — фрагмент страницы без <head> (так его принимает
Claude Artifacts). Для обычного хостинга оборачиваем его в полноценный документ:
doctype, кодировка, viewport, noindex.
"""
import pathlib
import re

root = pathlib.Path(__file__).resolve().parent.parent
src = (root / "prototype" / "index.html").read_text(encoding="utf-8")

title = re.search(r"<title>.*?</title>", src, re.S).group(0)
body = src.replace(title, "", 1)
links = re.findall(r"<link[^>]*>", body)
body = re.sub(r"<link[^>]*>\s*", "", body)
style = re.search(r"<style>.*?</style>", body, re.S).group(0)
body = body.replace(style, "", 1)

reset = (
    "<style>html{color-scheme:light}"
    ":root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}"
    "body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>"
)
html = (
    '<!doctype html>\n<html lang="ru">\n<head>\n<meta charset="utf-8">\n'
    '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
    '<meta name="robots" content="noindex, nofollow">\n'
    '<link rel="icon" href="data:,">\n'
    + reset + "\n" + title + "\n" + "\n".join(links) + "\n" + style
    + "\n</head>\n<body>\n" + body.strip() + "\n</body>\n</html>\n"
)

out = root / "docs" / "index.html"
out.write_text(html, encoding="utf-8")
(root / "docs" / ".nojekyll").write_text("", encoding="utf-8")
print(f"Собрано {out.relative_to(root)} ({len(html):,} символов)")
