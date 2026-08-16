# 出海项目 MAP（内容海外分发）

> 版本: v1.1 | 更新: 2026-08-16
> 项目目标: 验证海外读者 + 建立 PayPal 打赏渠道
> 本质: 试水——先验证"有没有海外读者"，打赏是结果不是目标
> 定位: 「简道内容体系」的海外子项目（总蓝图见 MANUAL.md，平台规则见 overseas-content-distribution 技能）

## 一、项目全景

```
【资产】13 篇 TIL（12中+1英）@ D:\til → GitHub 母库（公开+Discussion+PayPal）
                                        ↓ 分发
【渠道】GitHub ✅ → r/ControlProblem ⏳ → X ⏳ → HN ⏳
                                        ↓ 反馈
【回收】GitHub Discussion（cron 每周日抓）→ AI 筛精华 → 反哺选题
```

## 二、资产现状（已就绪的）

| 资产 | 状态 | 说明 |
|------|------|------|
| TIL 母库 | ✅ | 13 篇（12 中文 + 1 英文），`D:\til` |
| GitHub repo | ✅ | `github.com/JianDao1573/til`（公开 + Discussion + PayPal 入口） |
| 英文版 | ✅ | 《Make AI Follow the Rules》`ai-agent/rules-not-willpower.en.md` |
| 内容流水线 | ✅ | til-pipeline 技能（选题→草稿→评分→素材→入库→分发→反馈） |
| 打赏入口 | ✅ | README badge + 英文版文末 `paypal.me/RENWEJ` |
| 反馈回收 | ✅ | 每周日 cron 抓 Discussion → AI 筛 → 推微信 |

## 三、海外渠道状态

> ⚠️ 状态截至 2026-08-15，最新进展待确认。

| 渠道 | 状态 | 阻塞 | 下一步 |
|------|------|------|--------|
| GitHub | ✅ 已上线 | 无 | 等自然流量 + 反馈 cron 观察 |
| Reddit r/ControlProblem | ⏳ ModMail 已发 | 等 mods 人工审核 | 24h 无回复 → 先参与社区再重发 |
| X @wRaven395064 | ⏳ 申诉已提交 | 账号因长期未用被锁 | 等审核邮件（1-5 天，查垃圾箱） |
| HN | ⏳ 未开始 | karma 1（需 20+ 才能提交 github.com） | 评论热门帖攒 karma |

## 四、待完成项目

### P0（本周，多为等待中）

- [ ] **r/ControlProblem 跟进**：ModMail 已发（8-15），24h 无回复 → 在社区先评论 2-3 条建立信誉 → 重发帖子
- [ ] **X 账号恢复**：等审核邮件（留意 gmail 垃圾箱）→ 恢复后立刻：改密码 + bio 加 PayPal + 发首条英文推文（草稿已备）
- [ ] **HN 攒 karma**：评论首页热门帖 2-3 条（需起草高质量评论）→ karma 20+ 后提交英文版

### P1（近两周）

- [ ] **英文版扩充**：决定是否翻译其他 11 篇（或挑 2-3 篇对口的：费曼/靠制度/LLM评分偏松）
- [ ] **海外反馈观察**：Discussion 是否出现海外留言 → 反馈 cron 是否筛出优质建议

### P2（中期）

- [ ] **Quartz 数字花园**：独立站点（不受平台政策限制，可放打赏+搜索+双链）
- [ ] **X 长期运营**：定期发英文内容（AI 圈子），攒关注
- [ ] **打赏转化观察**：PayPal 入口已就位，观察是否有海外读者打赏

## 五、平台规则与经验（沉淀在技能，此处只引用）

平台规则 / 踩坑 / 申诉模板（Reddit / HN / X / PayPal）已沉淀到 `overseas-content-distribution` 技能，此处不重复。出海实操前先读该技能。

## 六、核心判断

1. **打赏是结果不是目标**——先验证海外有没有读者，打赏自然来
2. **别伪装人工**——内容标注 AI-assisted + 人工审核，诚实是品牌
3. **等待期做能主动推进的**——HN 攒 karma 是唯一不依赖等待的线
