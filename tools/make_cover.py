# -*- coding: utf-8 -*-
"""封面 + 小红书卡片 固化脚本（TIL 内容加工层）

用法（py -3.12）：
  封面:  py -3.12 make_cover.py cover --title "让 AI 遵守规则" --subtitle "别靠提醒，靠制度" --type methodology --out "D:/项目/jiandao-til/分发/2026-08-15-xxx/封面"
  小红书: py -3.12 make_cover.py xhs --cards cards.json --out "D:/项目/jiandao-til/分发/2026-08-15-xxx/小红书"

--type 取值（对应宪法 PRINCIPLES.md 颜色分类）：
  pitfall 避坑 / methodology 方法论 / tool 工具 / efficiency 效率 / review 复盘 / alert 提醒
"""
import argparse
import json
import subprocess
from pathlib import Path

CHROME = r"C:/Program Files/Google/Chrome/Application/chrome.exe"

# 类型 → (主色, 亮色) —— 与 PRINCIPLES.md 宪法颜色分类一致
TYPE_COLORS = {
    "pitfall":     ("#ff4c4c", "#ffb6c1"),  # 避坑 · 活力橘
    "methodology": ("#155799", "#45c0e8"),  # 方法论 · 经典蓝
    "tool":        ("#45c0e8", "#155799"),  # 工具 · 天空蓝
    "efficiency":  ("#009975", "#45c0e8"),  # 效率 · 翡翠绿
    "review":      ("#8c6888", "#c97886"),  # 复盘 · 薰衣紫
    "alert":       ("#ffd300", "#ff4c4c"),  # 提醒 · 柠檬黄
}
TYPE_LABEL = {
    "pitfall": "避坑", "methodology": "方法论", "tool": "工具",
    "efficiency": "效率", "review": "复盘", "alert": "提醒",
}


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def shot(html_path: Path, png_path: Path, w: int, h: int):
    subprocess.run(
        [CHROME, "--headless", "--disable-gpu", "--hide-scrollbars",
         f"--screenshot={png_path}", f"--window-size={w},{h}",
         f"file:///{html_path}".replace("\\", "/")],
        capture_output=True, timeout=30, check=True)


def make_cover(title, subtitle, series, accent, accent_light, outdir: Path):
    outdir.mkdir(parents=True, exist_ok=True)
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
html,body {{ width:900px; height:383px; overflow:hidden; }}
body {{ font-family:"Microsoft YaHei","PingFang SC",sans-serif; background:#1a1a2e; }}
.cover {{ width:900px; height:383px; position:relative; overflow:hidden;
  background:
    linear-gradient(rgba(21,87,153,0.14) 1px, transparent 1px),
    linear-gradient(90deg, rgba(21,87,153,0.14) 1px, transparent 1px),
    #1a1a2e;
  background-size: 48px 48px; }}
.bar {{ position:absolute; left:0; top:0; width:10px; height:100%; background:{accent}; }}
.glow {{ position:absolute; right:-80px; top:-80px; width:340px; height:340px; border-radius:50%;
  background:radial-gradient(circle, {accent}, transparent 70%); opacity:0.55; }}
.tag {{ position:absolute; left:48px; top:40px; font-size:18px; color:{accent_light}; letter-spacing:3px; font-weight:600; }}
.title {{ position:absolute; left:46px; top:100px; font-size:52px; font-weight:800; color:#ffffff; line-height:1.3; }}
.sub {{ position:absolute; left:48px; top:230px; font-size:26px; color:{accent_light}; font-weight:600; }}
.foot {{ position:absolute; left:48px; bottom:28px; font-size:15px; color:#8a93a6; letter-spacing:2px; }}
</style></head><body><div class="cover">
<div class="bar"></div><div class="glow"></div>
<div class="tag">{esc(series)}</div>
<div class="title">{esc(title)}</div>
<div class="sub">{esc(subtitle)}</div>
<div class="foot">简道 · 个人知识分享 · 大道至简</div>
</div></body></html>"""
    hp = outdir / "cover.html"
    hp.write_text(html, encoding="utf-8")
    shot(hp, outdir / "cover.png", 900, 383)
    print(f"✓ 封面已生成: {outdir/'cover.png'}")


def make_xhs(cards, accent, accent_light, type_label, outdir: Path):
    outdir.mkdir(parents=True, exist_ok=True)
    for i, c in enumerate(cards, 1):
        kind = c.get("kind", "content")
        title = c["title"]
        subtitle = c.get("subtitle", "")
        points = c.get("points", [])
        dark = kind in ("cover", "dark")
        bg = "#1a1a2e" if dark else "#ffffff"
        fg = "#ffffff" if dark else "#1a1a2e"
        sub_html = f'<div class="sub">{esc(subtitle)}</div>' if subtitle else ""
        pts = "".join(f'<div class="pt"><span class="dot"></span>{esc(p)}</div>' for p in points)
        html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
html,body {{ width:1080px; height:1440px; overflow:hidden; }}
body {{ font-family:"Microsoft YaHei","PingFang SC",sans-serif; background:{bg}; color:{fg}; }}
.card {{ width:1080px; height:1440px; padding:110px 90px; display:flex; flex-direction:column; }}
.tag {{ font-size:30px; color:{accent_light if dark else accent}; letter-spacing:4px; font-weight:600; margin-bottom:40px; }}
h1 {{ font-size:82px; line-height:1.25; font-weight:800; margin-bottom:36px; }}
.sub {{ font-size:40px; color:{accent_light if dark else accent}; margin-bottom:60px; font-weight:600; }}
.pt {{ font-size:42px; line-height:1.6; margin:22px 0; display:flex; align-items:flex-start; }}
.dot {{ width:16px; height:16px; background:{accent}; border-radius:50%; margin:18px 22px 0 0; flex-shrink:0; }}
</style></head><body><div class="card">
<div class="tag">{'TIL · 今日一课' if kind == 'cover' else f'{type_label} · TIL'}</div>
<h1>{esc(title)}</h1>
{sub_html}
{pts}
</div></body></html>"""
        hp = outdir / f"{i}.html"
        hp.write_text(html, encoding="utf-8")
        shot(hp, outdir / f"{i}.png", 1080, 1440)
    print(f"✓ 小红书 {len(cards)} 张卡片已生成: {outdir}")


def main():
    ap = argparse.ArgumentParser(description="TIL 封面/小红书卡片固化脚本")
    sub = ap.add_subparsers(dest="cmd", required=True)

    cov = sub.add_parser("cover", help="生成公众号封面（共用：公众号/知乎/头条/掘金）")
    cov.add_argument("--title", required=True)
    cov.add_argument("--subtitle", default="")
    cov.add_argument("--series", default="TIL")
    cov.add_argument("--type", default="methodology", choices=TYPE_COLORS.keys())
    cov.add_argument("--out", required=True)

    xhs = sub.add_parser("xhs", help="生成小红书 6 卡片（多图）")
    xhs.add_argument("--cards", required=True, help="cards.json 路径")
    xhs.add_argument("--type", default="methodology", choices=TYPE_COLORS.keys())
    xhs.add_argument("--out", required=True)

    a = ap.parse_args()
    accent, accent_light = TYPE_COLORS[a.type]
    label = TYPE_LABEL[a.type]

    if a.cmd == "cover":
        make_cover(a.title, a.subtitle, a.series, accent, accent_light, Path(a.out))
    else:
        cards = json.loads(Path(a.cards).read_text(encoding="utf-8"))
        make_xhs(cards, accent, accent_light, label, Path(a.out))


if __name__ == "__main__":
    main()
