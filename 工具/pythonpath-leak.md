---
date: 2026-08-15
type: pitfall
tags: [工具, 踩坑, Python]
slug: pythonpath-leak
---

> 📌 **声明**：本文为个人踩坑经验，面向使用 AI / 自动化工具的人；由 AI 生成、人工审核。介意可划走。
> 💬 对本话题有意见或建议，欢迎留言交流。

> **一句话**：脚本报 numpy 相关错误，但 numpy 明明正常——根因可能不是 numpy，是环境变量泄漏污染了 Python 环境。

## 问题

跑第三方 Python 脚本时报了一堆 numpy 错误，但单独 `python -c "import numpy"` 又完全正常。第一反应是"numpy 坏了"，重装、降级折腾半天，没用。

## 根因

Hermes Agent 的 terminal 里，`PYTHONPATH` 指向 Hermes 自己的 venv（Python 3.11 的 numpy 等）。当你在这个环境里跑第三方 CLI（用 `py -3.12`），Hermes venv 的包会"泄漏"进来，和你的 Python 3.12 环境冲突，报出莫名其妙的 numpy 错误。

**报错在 numpy，根因在环境变量——不是 numpy 坏了，是环境被污染了。**

## 解法：跑第三方 CLI 前清空环境

```bash
# 跑 pandas / organize 等第三方 CLI 前，先清掉 Hermes venv 的泄漏
env -u VIRTUAL_ENV -u PYTHONPATH -u PYTHONHOME py -3.12 your_script.py
```

更彻底的做法：用 `uv tool` 把第三方 CLI 隔离安装到独立环境，从根上避免冲突。

## 反直觉判断（真正的踩坑点）

1. **报错在哪，根因不一定在哪**——numpy 报错，可能是环境变量污染，别急着怪 numpy
2. **"能跑"和"环境干净"是两回事**——Hermes terminal 能跑，不代表第三方脚本能用同一套环境
3. **隔离比修复更快**——与其在污染环境里修，不如直接清空环境或 uv 隔离

## 通用迁移

> 遇到"报错和直觉对不上"的情况，先怀疑环境（变量/依赖/版本），再怀疑代码。**环境问题占了"莫名其妙报错"的一大半。**

---

*标签：`工具` `踩坑` `Python` `环境变量` `隔离`*
