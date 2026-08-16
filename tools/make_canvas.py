# -*- coding: utf-8 -*-
"""生成四象限写作 Canvas（jsoncanvas 格式，Obsidian 原生打开）

四象限（人的思想主权设计）：
  左上 话题        右上 AI 草稿（迭代物，可被覆盖）
  左下 碎片        右下 我的想法/批注（累积物，AI 不碰）

用法:
  py -3.12 make_canvas.py --config canvas.json --out 输出.canvas

config.json 结构:
  {
    "topic": "话题标题",
    "topic_desc": "一句话描述（可选）",
    "fragments": [{"title": "碎片标题", "content": "碎片摘要"}],
    "draft": "AI 草稿全文（Markdown）",
    "notes": "我的想法与批注（Markdown）"
  }

边界：只生成 .canvas 文件，不碰其他文件、不新建目录（--out 的父目录除外）。
"""
import argparse
import json
from pathlib import Path

# 布局常量（像素）
CELL_W, CELL_H = 720, 560
GAP = 60
POS = {
    "topic":     (0, 0),
    "draft":     (CELL_W + GAP, 0),
    "fragments": (0, CELL_H + GAP),
    "notes":     (CELL_W + GAP, CELL_H + GAP),
}
COLOR = {"topic": "1", "draft": "3", "fragments": "2", "notes": "5"}


def text_node(nid, text, x, y, w, h, color=None):
    node = {"id": nid, "type": "text", "text": text,
            "x": x, "y": y, "width": w, "height": h}
    if color:
        node["color"] = color
    return node


def build_canvas(cfg):
    nodes, edges = [], []

    # 左上：话题
    topic_text = f"# 🎯 话题：{cfg['topic']}"
    if cfg.get("topic_desc"):
        topic_text += f"\n\n> {cfg['topic_desc']}"
    nodes.append(text_node("topic", topic_text, *POS["topic"],
                           CELL_W, 160, COLOR["topic"]))

    # 右上：AI 草稿
    nodes.append(text_node("draft", cfg["draft"], *POS["draft"],
                           CELL_W, CELL_H, COLOR["draft"]))

    # 左下：碎片（垂直堆叠）
    frags = cfg.get("fragments", [])
    fx, fy = POS["fragments"]
    frag_h = max(120, min(180, CELL_H // max(len(frags), 1)))
    for i, f in enumerate(frags):
        body = f"### {f['title']}\n\n{f.get('content', '')}"
        y = fy + i * (frag_h + 20)
        nodes.append(text_node(f"frag{i}", body, fx, y,
                               CELL_W, frag_h, COLOR["fragments"]))

    # 右下：我的想法/批注
    notes = cfg.get("notes", "")
    notes_text = f"# ✍️ 我的想法与批注\n\n{notes}"
    nodes.append(text_node("notes", notes_text, *POS["notes"],
                           CELL_W, CELL_H, COLOR["notes"]))

    # 边：话题→草稿→批注 的迭代环
    edges.append({"id": "e1", "fromNode": "draft", "fromSide": "bottom",
                  "toNode": "notes", "toSide": "top"})
    edges.append({"id": "e2", "fromNode": "notes", "fromSide": "left",
                  "toNode": "draft", "toSide": "right"})
    edges.append({"id": "e3", "fromNode": "frag0", "fromSide": "top",
                  "toNode": "draft", "toSide": "bottom"})
    return {"nodes": nodes, "edges": edges}


def main():
    ap = argparse.ArgumentParser(description="生成四象限写作 Canvas")
    ap.add_argument("--config", required=True, help="JSON 配置文件路径")
    ap.add_argument("--out", required=True, help="输出 .canvas 路径")
    a = ap.parse_args()

    cfg = json.loads(Path(a.config).read_text(encoding="utf-8"))
    canvas = build_canvas(cfg)

    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(canvas, ensure_ascii=False, indent=2),
                   encoding="utf-8")
    print(f"✓ 已生成四象限 Canvas: {out}")
    print(f"  节点 {len(canvas['nodes'])} 个 | 边 {len(canvas['edges'])} 条")


if __name__ == "__main__":
    main()
