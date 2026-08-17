# -*- coding: utf-8 -*-
"""自动更新 README.md 目录索引（扫描分类目录 → 提取标题 → 生成索引）

用法（py -3.12）：
  预览（不写文件）: py -3.12 update_readme_index.py
  应用（备份后写）: py -3.12 update_readme_index.py --apply

边界：
- 只改 README.md 的「## 目录」章节（到下一个 ## 或文件尾）
- 只读分类目录下的 *.md（提取第一个 # 标题）
- 写前自动备份 README.md.bak
- 不碰其他文件、不新建目录
"""
import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent  # 仓库根目录
README = ROOT / "README.md"

# 非内容目录（排除）
EXCLUDE = {".git", ".github", "templates", "分发", "tools"}

# 分类目录 → 显示名（未来加分类时在此补一行）
CATEGORY_LABELS = {
    "ai-agent": "ai-agent（AI / 自动化）",
    "思维": "思维（思维 / 学习方法论）",
    "审美": "审美（审美 / 设计）",
    "工具": "工具（工具 / 效率）",
}


def extract_title(md_path: Path) -> str:
    """提取第一个 # 标题（frontmatter 之后的第一个一级标题）"""
    in_frontmatter = False
    for line in md_path.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if s == "---":
            in_frontmatter = not in_frontmatter
            continue
        if not in_frontmatter and s.startswith("# "):
            return s[2:].strip()
    return md_path.stem  # 兜底用文件名


def scan_categories() -> dict:
    """扫描分类目录 → {分类: [(标题, 相对路径)]}"""
    result = {}
    for d in sorted(ROOT.iterdir()):
        if not d.is_dir() or d.name in EXCLUDE or d.name.startswith("."):
            continue
        mds = sorted(d.glob("*.md"))
        if not mds:
            continue
        items = [(extract_title(m), f"{d.name}/{m.name}") for m in mds]
        result[d.name] = items
    return result


def build_index(categories: dict) -> str:
    lines = ["## 目录", ""]
    for cat, items in categories.items():
        label = CATEGORY_LABELS.get(cat, cat)
        lines.append(f"### {label}")
        for title, rel in items:
            lines.append(f"- [{title}]({rel})")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main():
    ap = argparse.ArgumentParser(description="自动更新 README 目录索引")
    ap.add_argument("--apply", action="store_true", help="实际写入（默认只预览）")
    a = ap.parse_args()

    cats = scan_categories()
    if not cats:
        print("⚠️ 未发现任何分类目录下的 *.md，请检查仓库目录结构")
        return

    new_index = build_index(cats)
    old = README.read_text(encoding="utf-8")

    # 定位「## 目录」章节（到下一个 ## 或文件尾）
    pattern = re.compile(r"## 目录\n(.*?)(?=\n## |\Z)", re.DOTALL)
    m = pattern.search(old)
    if not m:
        print("❌ 未找到「## 目录」章节，请确认 README 结构")
        return

    new_readme = old[:m.start()] + new_index + old[m.end():]

    print("=== 预览：新目录索引 ===")
    print(new_index)
    print(f"（分类 {len(cats)} 个，共 {sum(len(v) for v in cats.values())} 篇）")
    print()

    if not a.apply:
        print("（预览模式，未写入。确认无误后加 --apply 写入）")
        return

    backup = README.with_suffix(".md.bak")
    backup.write_text(old, encoding="utf-8")
    README.write_text(new_readme, encoding="utf-8")
    print(f"✓ 已更新 README.md（备份: {backup.name}）")


if __name__ == "__main__":
    main()
