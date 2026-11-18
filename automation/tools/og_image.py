#!/usr/bin/env python3
"""記事の OGP 画像（1200x630 PNG）を作り、front matter の image を設定する。

使い方:
    python3 automation/tools/og_image.py _posts/2026-11-20-example.md [他の記事 ...]
    python3 automation/tools/og_image.py --all          # image が無い/ファイルが無い記事すべて
    python3 automation/tools/og_image.py --all --force  # すべて作り直す

出力: assets/images/<slug>.png（slug はファイル名から日付と拡張子を除いたもの）
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
POSTS = ROOT / "_posts"
OUT_DIR = ROOT / "assets" / "images"

W, H = 1200, 630
BG = (24, 34, 60)          # 藍
BG_GRID = (34, 47, 80)
ACCENT = (226, 92, 64)     # 朱
TEXT = (245, 247, 250)
SUB = (170, 183, 205)

FONT_CANDIDATES = [
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
    "/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf",
    "/usr/share/fonts/truetype/fonts-japanese-gothic.ttf",
    "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
]

# 行頭に来てはいけない文字（簡易禁則）
NO_LINE_START = set("、。，．・：；？！）」』】〕〉》ー〜…ゃゅょっぁぃぅぇぉャュョッァィゥェォ,.:;?!)]}%")


def font_path() -> str:
    for p in FONT_CANDIDATES:
        if os.path.exists(p):
            return p
    raise SystemExit("日本語フォントが見つかりません")


def read_front_matter(text: str) -> tuple[dict, str, str]:
    m = re.match(r"^---\n(.*?)\n---\n?", text, re.S)
    if not m:
        return {}, "", text
    import yaml  # PyYAML

    try:
        data = yaml.safe_load(m.group(1)) or {}
    except Exception:
        data = {}
    return data, m.group(1), text[m.end():]


def wrap(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, max_w: int) -> list[str]:
    lines: list[str] = []
    cur = ""
    for ch in text:
        trial = cur + ch
        if draw.textlength(trial, font=font) <= max_w or not cur:
            cur = trial
            continue
        if ch in NO_LINE_START:  # 禁則: 前の行にぶら下げる
            cur = trial
            continue
        lines.append(cur)
        cur = ch
    if cur:
        lines.append(cur)
    return lines


def render(title: str, category: str, out: Path) -> None:
    fp = font_path()
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # 方眼（通帳・設計図のような細い罫線）
    for x in range(0, W, 40):
        d.line([(x, 0), (x, H)], fill=BG_GRID, width=1)
    for y in range(0, H, 40):
        d.line([(0, y), (W, y)], fill=BG_GRID, width=1)

    # 左の朱色の帯
    d.rectangle([(0, 0), (14, H)], fill=ACCENT)

    pad_x = 80
    site_font = ImageFont.truetype(fp, 34)
    d.text((pad_x, 56), "AIテックラボ", font=site_font, fill=TEXT, stroke_width=1, stroke_fill=TEXT)

    if category:
        cat_font = ImageFont.truetype(fp, 26)
        tw = d.textlength(category, font=cat_font)
        x0 = W - pad_x - tw - 36
        d.rounded_rectangle([(x0, 52), (W - pad_x, 98)], radius=23, outline=ACCENT, width=3)
        d.text((x0 + 18, 60), category, font=cat_font, fill=TEXT)

    # タイトル: 3行以内に収まるまで文字を小さくする
    max_w = W - pad_x * 2
    for size in (68, 62, 56, 50, 46, 42):
        f = ImageFont.truetype(fp, size)
        lines = wrap(d, title, f, max_w)
        if len(lines) <= 3:
            break
    else:
        lines = lines[:3]
        lines[-1] = lines[-1][:-1] + "…"
    line_h = int(size * 1.42)
    block_h = line_h * len(lines)
    y = (H - block_h) // 2 + 20
    for line in lines:
        d.text((pad_x, y), line, font=f, fill=TEXT, stroke_width=2, stroke_fill=TEXT)
        y += line_h

    foot_font = ImageFont.truetype(fp, 24)
    d.text((pad_x, H - 76), "rukigfsh-cmd.github.io/ai-tech-blog", font=foot_font, fill=SUB)

    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, "PNG", optimize=True)


def set_image_line(fm_raw: str, value: str) -> str:
    line = f'image: "{value}"'
    if re.search(r"^image:.*$", fm_raw, re.M):
        return re.sub(r"^image:.*$", line, fm_raw, count=1, flags=re.M)
    return fm_raw.rstrip("\n") + "\n" + line


def process(path: Path, force: bool) -> str:
    text = path.read_text(encoding="utf-8")
    data, fm_raw, body = read_front_matter(text)
    if not fm_raw:
        return f"skip (front matter なし): {path.name}"
    slug = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", path.stem)
    rel = f"/assets/images/{slug}.png"
    out = OUT_DIR / f"{slug}.png"
    if out.exists() and not force and data.get("image") == rel:
        return f"ok (既存): {path.name}"
    title = str(data.get("title") or slug)
    cats = data.get("categories") or []
    if isinstance(cats, str):
        cats = cats.split()
    category = str(cats[0]) if cats else ""
    render(title, category, out)
    new_fm = set_image_line(fm_raw, rel)
    path.write_text(f"---\n{new_fm}\n---\n{body}", encoding="utf-8")
    return f"made: {out.relative_to(ROOT)}"


def main(argv: list[str]) -> None:
    force = "--force" in argv
    files = [a for a in argv if not a.startswith("--")]
    if "--all" in argv:
        files = sorted(str(p) for p in POSTS.glob("*.md"))
    if not files:
        print(__doc__)
        raise SystemExit(1)
    for f in files:
        print(process(Path(f).resolve(), force))


if __name__ == "__main__":
    main(sys.argv[1:])
