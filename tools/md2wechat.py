#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""md2wechat.py — 本地 markdown → 微信排版 HTML（简道主题）

解决分发两个痛点：
1. 不用打开 md.doocs.org 网站来回复制（本地一次生成）
2. 排版用「简道主题」内联样式，比 doocs/md 默认输出美观，
   且符合微信 2026 算法（完读率权重最高 → 呼吸感排版）

用法：
  python tools/md2wechat.py <文章.md> [--type methodology] [--out 路径.html]

  --type : methodology|efficiency|pitfall|alert|review|tool（决定主题色）
  --out  : 输出路径（默认与源文件同目录同名 .html）

生成后：浏览器打开 .html → Ctrl+A 全选 → 复制 → 粘贴到公众号编辑器（保留格式）。
图片请手动上传到公众号（本地路径图片不会随粘贴带过去）。
"""

import argparse
import pathlib
import re

import markdown

# 主题色（复用 color-system.md 六色）
THEME = {
    "methodology": "#155799",  # 方法论 - 经典蓝
    "efficiency": "#009975",   # 效率 - 翡翠绿
    "pitfall": "#ff4c4c",      # 避坑 - 活力橘
    "alert": "#ffd300",        # 提醒 - 柠檬黄
    "review": "#8c6888",       # 复盘 - 薰衣紫
    "tool": "#45c0e8",         # 工具 - 天空蓝
}

# 正文基准（呼吸感排版核心：字号/行高/段距）
BODY_FONT = "15px"
BODY_COLOR = "#333333"
BODY_LINEHEIGHT = "1.75"
BODY_MARGIN = "0 0 1em 0"  # 段落间距 = 完读率关键


def strip_frontmatter(text: str) -> str:
    """剥离 YAML frontmatter（--- 包裹的头部）。"""
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            return parts[2].lstrip("\n")
    return text


def fix_tight_list(text: str) -> str:
    """段落紧跟列表（无空行）时，在列表前补空行。

    标准 markdown 要求列表前空行；TIL 文章常见「冒号结尾 + 紧跟列表」
    （如「...它经常不守规矩：\\n- 文件放到错误目录」），
    不加空行 Python markdown 会把列表当段落文本，`- ` 前缀残留。
    """
    # 非空行（段落）后紧跟列表项（-/*/+ 或 数字.）→ 在中间插空行
    return re.sub(r"(\S[^\n]*)\n(?=[-*+] |\d+\. )", r"\1\n\n", text)


def apply_inline_style(html: str, theme: str) -> str:
    """给 markdown 输出的 HTML 加内联样式。

    微信编辑器粘贴时只认内联 style，<style> 标签会被剥离，
    所以所有样式必须写成 inline style。
    """
    # 段落（正文基准）
    html = re.sub(
        r"<p>",
        f'<p style="font-size:{BODY_FONT};color:{BODY_COLOR};'
        f"line-height:{BODY_LINEHEIGHT};margin:{BODY_MARGIN};"
        f'letter-spacing:0.5px;">',
        html,
    )
    # 一级标题（带主题色下边框，作为章节分隔）
    html = re.sub(
        r"<h1>",
        f'<h1 style="font-size:19px;color:{theme};font-weight:bold;'
        f"line-height:1.4;margin:1.5em 0 0.8em;padding-bottom:0.3em;"
        f'border-bottom:2px solid {theme};">',
        html,
    )
    # 二级标题
    html = re.sub(
        r"<h2>",
        f'<h2 style="font-size:17px;color:{theme};font-weight:bold;'
        f'line-height:1.4;margin:1.2em 0 0.6em;">',
        html,
    )
    # 三级标题
    html = re.sub(
        r"<h3>",
        f'<h3 style="font-size:16px;color:#333;font-weight:bold;'
        f'line-height:1.4;margin:1em 0 0.5em;">',
        html,
    )
    # 引用块（声明/金句，左边框 + 浅灰底）
    html = re.sub(
        r"<blockquote>",
        f'<blockquote style="border-left:3px solid {theme};'
        f'background:#f5f7fa;padding:10px 15px;margin:1em 0;color:#555;'
        f'font-size:14px;line-height:1.6;border-radius:0 6px 6px 0;">',
        html,
    )
    # 加粗（重点强调用主题色）
    html = re.sub(
        r"<strong>",
        f'<strong style="color:{theme};font-weight:bold;">',
        html,
    )
    # 列表（3+ 并列项用列表 = 呼吸感铁律）
    html = re.sub(r"<ul>", '<ul style="margin:0.5em 0;padding-left:1.6em;">', html)
    html = re.sub(r"<ol>", '<ol style="margin:0.5em 0;padding-left:1.6em;">', html)
    html = re.sub(
        r"<li>",
        f'<li style="font-size:{BODY_FONT};color:{BODY_COLOR};'
        f"line-height:{BODY_LINEHEIGHT};margin:0.3em 0;\">",
        html,
    )
    # 分割线
    html = re.sub(
        r"<hr\s*/?>",
        '<hr style="border:none;border-top:1px solid #e0e0e0;margin:1.5em 0;">',
        html,
    )
    # 链接
    html = re.sub(
        r"<a ",
        f'<a style="color:{theme};text-decoration:underline;" ',
        html,
    )
    # 代码块容器（深色底，先处理，作为 code 分组的锚点）
    html = re.sub(
        r"<pre>",
        '<pre style="background:#282c34;color:#abb2bf;padding:12px 15px;'
        'border-radius:6px;overflow-x:auto;font-size:13px;line-height:1.5;'
        'font-family:Menlo,Consolas,monospace;white-space:pre-wrap;">',
        html,
    )
    # 代码块内的 code（紧跟 <pre>，含 fenced_code 的 class）：等宽字体，不加行内浅底
    html = re.sub(
        r"(<pre[^>]*>)\s*<code",
        r'\1<code style="font-family:Menlo,Consolas,monospace;"',
        html,
    )
    # 行内代码（剩余 <code>，不含 pre 包裹的）
    html = re.sub(
        r"<code>",
        '<code style="background:#f0f0f0;color:#c7254e;padding:2px 5px;'
        'border-radius:3px;font-size:13px;font-family:Menlo,Consolas,monospace;">',
        html,
    )
    # 表格
    html = re.sub(
        r"<table>",
        '<table style="border-collapse:collapse;margin:1em 0;width:100%;font-size:14px;">',
        html,
    )
    html = re.sub(
        r"<th>",
        f'<th style="background:{theme};color:#fff;padding:8px 10px;'
        f'border:1px solid #ddd;font-weight:bold;">',
        html,
    )
    html = re.sub(
        r"<td>",
        '<td style="padding:8px 10px;border:1px solid #ddd;color:#333;">',
        html,
    )
    # 图片（居中 + 圆角 + 留白）
    html = re.sub(
        r"<img ",
        '<img style="display:block;margin:1em auto;max-width:100%;border-radius:8px;" ',
        html,
    )
    # 列表项内的段落：去底部段距（li 自带 margin，避免 p 的 margin 叠加造成列表松散）
    html = re.sub(
        r'(<li[^>]*>)\s*<p style="([^"]*)margin:0 0 1em 0([^"]*)">',
        r'\1<p style="\2margin:0\3">',
        html,
    )
    return html


def main() -> None:
    ap = argparse.ArgumentParser(description="markdown → 微信排版 HTML（简道主题）")
    ap.add_argument("md", help="源 markdown 文件路径")
    ap.add_argument("--type", choices=THEME.keys(), default="methodology", help="文章类型（决定主题色）")
    ap.add_argument("--out", help="输出 HTML 路径（默认与源文件同目录同名）")
    args = ap.parse_args()

    src = pathlib.Path(args.md)
    if not src.exists():
        print(f"[错误] 文件不存在：{src}")
        raise SystemExit(1)

    text = src.read_text(encoding="utf-8")
    text = strip_frontmatter(text)
    text = fix_tight_list(text)
    body = markdown.markdown(text, extensions=["fenced_code", "tables", "sane_lists"])
    styled = apply_inline_style(body, THEME[args.type])

    out = pathlib.Path(args.out) if args.out else src.with_suffix(".html")
    out.write_text(styled, encoding="utf-8")
    print(f"[生成] {out}")
    print(f"[主题色] {THEME[args.type]} ({args.type})")
    print("[下一步] 浏览器打开 → Ctrl+A 全选 → 复制 → 粘贴到公众号编辑器（保留格式）")
    print("[提示] 正文里的本地图片需手动上传到公众号")


if __name__ == "__main__":
    main()
