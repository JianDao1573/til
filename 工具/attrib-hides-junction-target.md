---
date: 2026-08-16
type: pitfall
tags: [工具, Windows, junction, 路径迁移]
slug: attrib-hides-junction-target
---

> 📌 **声明**：本文为个人踩坑经验，面向使用 AI / 自动化工具的人；由 AI 生成、人工审核。介意可划走。
> 💬 对本话题有意见或建议，欢迎留言交流。
# attrib +h 会穿透 junction

> **一句话**：隐藏 junction，却把真实目录也藏了。

## 问题

想让 `D:\` 根目录干净，建了 junction 后想「隐藏链接」，执行 `attrib +h`。结果用户资源管理器里 F5 刷了 10 次，真实目录（`D:\tools\Ollama` 等 4 个）怎么都看不到。

## 根因

Windows 的 `attrib +h` 会**穿透 junction（reparse point）**，把隐藏属性写到链接指向的真实目录上。所以「隐藏链接」变成了「隐藏真实目录」。

## 解法

`attrib -h <真实目录>` 取消隐藏。排查时先 `attrib <目录>` 看有没有 H 标记，别急着重建链接。

## 反直觉判断（真正踩坑点）

1. 「隐藏链接」居然影响「真实目录」——链接和目标不是隔离的
2. 看不到文件不是缓存、不是没刷新，是**隐藏属性**
3. 系统目录（$RECYCLE.BIN）天生隐藏是正常的，别误判

## 通用迁移

> Windows 上对「链接」的属性操作可能穿透到「目标」，改属性后要验证目标目录本身。

---

*标签：`工具` `Windows` `junction` `路径迁移`*
