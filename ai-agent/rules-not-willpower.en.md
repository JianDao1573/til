---
date: 2026-08-15
type: methodology
tags: [ai-agent, automation, file-management, pitfall]
slug: rules-not-willpower-en
---

> 📌 **Disclaimer**: Personal experience with AI / automation tools. Written with AI assistance, reviewed by a human. Skip if you mind.
> 💬 Comments or feedback? Open a discussion on GitHub.

# Make AI Follow the Rules: Declare, Execute, Verify, Automate

> **One-liner**: When an AI agent keeps repeating the same mistake, don't rely on "reminding it" — rely on rule engines + validators + scheduled tasks.

## The Problem

When using an AI agent (or any automation) to manage files, it often breaks the rules:

- Files go into the wrong directories
- Stale files never get archived
- Rules are written in docs, but every new session "forgets" or "bypasses" them

## The Root Cause: Wrong Direction

The intuitive fix is "make the AI more obedient" — write more detailed rules, keep reminding it. **This is wrong.**

AI agents are stateless per session: they forget, and they bypass rules. If rule adherence depends on the "executor's self-discipline", it will fail repeatedly.

## The Solution: Four-Part Framework

| # | Action | Carrier | Example |
|---|--------|---------|---------|
| 1 | **Declare rules** | config / JSON | `sort_rules.json` (filename → directory) |
| 2 | **Execute forward** | a tool | a rule engine auto-archives files |
| 3 | **Verify backward** | an audit script | scans for misplaced files, read-only |
| 4 | **Automate on schedule** | cron | archive daily at 07:30 / audit at 08:00 |

## Case Study: File Management

```
Rules declared (machine-readable, not a doc convention)
   ├─ sort_rules.json      → routing rules (filename → directory)
   └─ organize-config.yaml → archiving rules (>7 days → history/)
        ↓
Forward execution: organize (a rule-based file organizer CLI) auto-archives stale snapshots
        ↓
Backward verification: audit script scans for stray/misplaced files, reports only
        ↓
Scheduling: cron runs daily, zero tokens
```

## Three Counterintuitive Takeaways

1. The root cause of "messy files" is often a **bug in the rules**, not a willful executor — check the rules first, don't blame the executor.
2. **"Stale" must be defined explicitly** — in this case it means "superseded by a newer version" (daily inventory snapshots), not "untouched for 30 days".
3. **Routing rules ≠ audit rules** — forward routing keywords can be broad; backward audits must be high-confidence, or false positives drown out real problems.

## Generalizing

Whenever an AI / program repeatedly makes the same type of mistake, apply this formula:

> **Declare rules + Execute with tools + Verify with audits + Automate on schedule**

This is isomorphic to what managers already know: "rely on SOPs, not on self-discipline." You've known this all along — this is just the first time you apply it to AI.

---

*Tags: `ai-agent` `methodology` `file-management` `pitfall`*
