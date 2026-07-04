<a id="chinese"></a>

<div align="center">

**中文** · [English](#english)

# 🧭 Skill Scout Builder（Skill 寻构师）

#### 帮 Agent 找 Skill、比 Skill、改 Skill；没有合适的，就安全地造一个。

![License](https://img.shields.io/badge/license-MIT-blue)
![Skills](https://img.shields.io/badge/skills-1-10b981)
![AgentSkills](https://img.shields.io/badge/AgentSkills-standard-8b5cf6)

![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-f97316)
![Codex](https://img.shields.io/badge/Codex-Skill-22c55e)
![OpenCode](https://img.shields.io/badge/OpenCode-Skill-3b82f6)
![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-8b5cf6)

</div>

都是在真实 Agent 工作流里跑通后，才整理出来开源的。这个仓库目前收录了一个可移植的 Agent Skill：**Skill Scout Builder（Skill 寻构师）**。

它遵循开放的 Agent Skills 目录格式，让 Codex、Claude Code、OpenCode、OpenClaw 等支持 Skill 的 Agent 可以读取、安装和使用。不同 Agent 的搜索、安装器、市场和审批机制会不一样，但这个 Skill 的核心流程保持可移植。

---

## 目录

| 名字 | 一句话 | 入口 |
| --- | --- | --- |
| `skill-scout-builder`（Skill 寻构师） | 通过对话澄清需求，搜索并比较已有 Skill，最后安全安装、定制或创建新的可复用 Skill | [SKILL.md](skill-scout-builder/SKILL.md) |

---

## 安装方式

在 Codex、Claude Code、OpenClaw 等支持从 GitHub URL 安装 Skill 的 Agent 里，直接说：

```text
帮我安装这个 skill: https://github.com/BingheTalk/AI-Related-Repositories/tree/main/skill-scout-builder
```

Agent 会自己下载到对应 Skill 目录，不用你操心路径。

如果当前 Agent 不支持 URL 安装，可以手动复制到对应目录。

### Codex 手动安装

用户级安装：

```bash
git clone https://github.com/BingheTalk/AI-Related-Repositories.git
mkdir -p ~/.agents/skills
cp -R AI-Related-Repositories/skill-scout-builder ~/.agents/skills/
```

项目级安装：

```bash
git clone https://github.com/BingheTalk/AI-Related-Repositories.git
mkdir -p .agents/skills
cp -R AI-Related-Repositories/skill-scout-builder .agents/skills/
```

### Claude Code 手动安装

用户级安装：

```bash
git clone https://github.com/BingheTalk/AI-Related-Repositories.git
mkdir -p ~/.claude/skills
cp -R AI-Related-Repositories/skill-scout-builder ~/.claude/skills/
```

项目级安装：

```bash
git clone https://github.com/BingheTalk/AI-Related-Repositories.git
mkdir -p .claude/skills
cp -R AI-Related-Repositories/skill-scout-builder .claude/skills/
```

---

## ✨ Skill Scout Builder（Skill 寻构师）

> “先别急着造轮子。让 Agent 先帮你找一圈：有没有现成 Skill、哪个最接近、能不能安全改；实在没有，再造一个。”

这个 Skill 解决的是一个很常见的问题：你知道自己想让 Agent 多一种能力，但不知道应该找现成 Skill、改别人的 Skill，还是从零写一个。

它会先用自然对话把模糊想法整理成需求简报，然后自动搜索当前会话、本地目录、宿主市场、Git 仓库和公开来源中的候选 Skill。找到候选后，它会按需求匹配、环境兼容、依赖、安全性和可维护性做比较，最后让你选择：直接使用、定制候选、看另一个候选，或创建新 Skill。

### 它能做什么

- 把“我想要一个能做某事的 Skill”整理成可验收的需求
- 支持中文和英文关键词扩展，避免只按 Skill 名称搜索
- 搜索本地 Skill、项目 Skill、宿主市场、GitHub 和公开网页
- 对候选 Skill 做需求匹配、依赖检查和安全预审
- 安装或修改前等待用户确认
- 没有合适候选时，按确认后的需求创建新 Skill
- 对最终产物执行结构校验、安全审计和验收测试

### 适合

- 想找一个已有 Skill，但中文或模糊关键词搜不到
- 想比较几个 Skill，看哪个更适合当前任务
- 想把一个相近的 Skill 改造成自己的工作流
- 想先确认有没有现成方案，再决定是否新建 Skill
- 想让 Agent 按更安全的流程安装、审查和交付 Skill

### 不适合

- 只是让 Agent 完成一次普通任务，而不是沉淀成可复用 Skill
- 不关心候选来源、依赖、安全边界和验收测试
- 希望跳过确认，直接安装或执行第三方脚本

### 怎么触发

```text
$skill-scout-builder 帮我找一个能整理访谈录音并生成选题的 Skill
```

```text
帮我找一个符合需求的 Skill
中文关键词搜不到合适的 Skill，帮我扩展搜索
对比这几个 Skill，看看哪个更适合
先搜索是否有现成 Skill，没有就创建一个
检查并安全安装这个 Skill
```

### 工作流程

```text
宿主能力识别 → 需求澄清 → 简报确认 → 多渠道搜索
→ 候选对比与预审 → 用户选择 → 使用 / 定制 / 新建
→ 完整审计与验收 → 交付
```

---

## 仓库结构

```text
.
├── skill-scout-builder/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   ├── references/
│   └── scripts/
└── validation/
    ├── test_skill_scout_builder.py
    └── test-report.md
```

`agents/openai.yaml` 是 Codex 的可选界面增强；核心 Skill 不依赖它。

---

## 验证与安全

本地验证命令：

```bash
PYTHONPYCACHEPREFIX=/tmp/skill-scout-builder-pycache \
python3 -m unittest -v validation/test_skill_scout_builder.py

python3 skill-scout-builder/scripts/audit_skill.py \
  skill-scout-builder --format text
```

当前结果：

- 回归测试：`9/9` 通过
- Critical / High / Medium 风险：`0`
- 已知低风险提示：扫描脚本会只读检查 `/etc/codex/skills`，这是标准的系统级 Skill 搜索路径

完整验证记录见 [validation/test-report.md](validation/test-report.md)。

---

## 关于

这个 Skill 的目标不是“自动安装一切”，而是让 Agent 在找 Skill、改 Skill、造 Skill 的过程中更稳一点：先澄清，再搜索；先审查，再安装；先测试，再交付。

如果它帮你少造了一次轮子，或者帮你把一个模糊想法沉淀成可复用 Skill，欢迎给这个仓库一个 ⭐。

[MIT License](LICENSE) · 自由使用 / 修改 / 再分发

Made by [@BingheTalk](https://github.com/BingheTalk)

---

<a id="english"></a>

<div align="center">

[中文](#chinese) · **English**

# 🧭 Skill Scout Builder

#### Help your agent find, compare, adapt, or safely create reusable Skills.

![License](https://img.shields.io/badge/license-MIT-blue)
![Skills](https://img.shields.io/badge/skills-1-10b981)
![AgentSkills](https://img.shields.io/badge/AgentSkills-standard-8b5cf6)

![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-f97316)
![Codex](https://img.shields.io/badge/Codex-Skill-22c55e)
![OpenCode](https://img.shields.io/badge/OpenCode-Skill-3b82f6)
![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-8b5cf6)

</div>

This repository contains **Skill Scout Builder**, a portable Agent Skill that has been shaped through real agent workflows.

It follows the open Agent Skills directory format so compatible hosts such as Codex, Claude Code, OpenCode, and OpenClaw can read, install, and use it. Host-specific search, installation, marketplace, and approval capabilities may differ, but the core workflow is designed to stay portable.

---

## Directory

| Name | One-liner | Entry |
| --- | --- | --- |
| `skill-scout-builder` | Clarify a need, search and compare existing Skills, then safely install, adapt, or create a reusable Skill | [SKILL.md](skill-scout-builder/SKILL.md) |

---

## Installation

In Codex, Claude Code, OpenClaw, or any Agent that supports installing Skills from a GitHub URL, just say:

```text
Install this skill: https://github.com/BingheTalk/AI-Related-Repositories/tree/main/skill-scout-builder
```

The Agent should clone or copy it into the right Skill directory for its host.

If your current Agent does not support URL-based installation, install it manually.

### Manual install for Codex

User-level install:

```bash
git clone https://github.com/BingheTalk/AI-Related-Repositories.git
mkdir -p ~/.agents/skills
cp -R AI-Related-Repositories/skill-scout-builder ~/.agents/skills/
```

Project-level install:

```bash
git clone https://github.com/BingheTalk/AI-Related-Repositories.git
mkdir -p .agents/skills
cp -R AI-Related-Repositories/skill-scout-builder .agents/skills/
```

### Manual install for Claude Code

User-level install:

```bash
git clone https://github.com/BingheTalk/AI-Related-Repositories.git
mkdir -p ~/.claude/skills
cp -R AI-Related-Repositories/skill-scout-builder ~/.claude/skills/
```

Project-level install:

```bash
git clone https://github.com/BingheTalk/AI-Related-Repositories.git
mkdir -p .claude/skills
cp -R AI-Related-Repositories/skill-scout-builder .claude/skills/
```

---

## ✨ Skill Scout Builder

> “Before building a new wheel, ask the agent to search: is there an existing Skill, which one is closest, can it be adapted safely, or should we create a new one?”

Skill Scout Builder helps when you know what capability you want your agent to gain, but you do not yet know whether to find an existing Skill, adapt a close match, or create a new one.

It first turns a vague idea into a concise requirement brief through a lightweight conversation. Then it searches visible Skills, local Skill directories, host-native catalogs, Git repositories, and public sources. For serious candidates, it compares fit, dependencies, environment compatibility, maintainability, and safety before asking you to choose: use directly, adapt, inspect another candidate, or create a new Skill.

### What it does

- Turns fuzzy Skill ideas into testable requirement briefs
- Expands Chinese and English search terms beyond Skill names
- Searches local Skills, project Skills, host catalogs, GitHub, and public web sources
- Compares candidates by requirement fit, dependencies, and safety
- Waits for user approval before installing or modifying anything
- Creates a new Skill when no viable candidate exists
- Runs structural checks, safety review, and acceptance tests before delivery

### Good for

- Finding a Skill when Chinese or imprecise keywords fail
- Comparing several Skills for a specific workflow
- Adapting a near-match Skill to your own process
- Checking for existing reusable work before creating a new Skill
- Installing and reviewing third-party Skills with safer guardrails

### Not for

- One-off tasks that do not need to become reusable Skills
- Workflows that do not care about source, dependencies, safety, or validation
- Blindly installing or executing third-party scripts without review

### How to trigger

```text
$skill-scout-builder Find me a Skill that can summarize interview recordings into content ideas.
```

```text
Find a Skill that matches my requirements
Chinese keywords are not finding the right Skill; expand the search
Compare these Skills and tell me which one fits best
Search for an existing Skill first; create one only if none fits
Review and safely install this Skill
```

### Workflow

```text
Host profiling → requirement clarification → brief confirmation → multi-channel search
→ candidate comparison and pre-screening → user decision → use / adapt / create
→ full audit and acceptance testing → delivery
```

---

## Repository structure

```text
.
├── skill-scout-builder/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   ├── references/
│   └── scripts/
└── validation/
    ├── test_skill_scout_builder.py
    └── test-report.md
```

`agents/openai.yaml` is an optional Codex UI enhancement. The portable core does not depend on it.

---

## Validation and safety

Local validation commands:

```bash
PYTHONPYCACHEPREFIX=/tmp/skill-scout-builder-pycache \
python3 -m unittest -v validation/test_skill_scout_builder.py

python3 skill-scout-builder/scripts/audit_skill.py \
  skill-scout-builder --format text
```

Current result:

- Regression tests: `9/9` passed
- Critical / High / Medium findings: `0`
- Known low-level signal: the scanner read-only checks `/etc/codex/skills`, a standard system Skill search path

See [validation/test-report.md](validation/test-report.md) for the full validation record.

---

## About

Skill Scout Builder is not meant to blindly install everything. It is meant to make Skill discovery, adaptation, and creation steadier: clarify first, search broadly, review before installing, test before delivery.

If it saves you from rebuilding a wheel or helps turn a vague workflow idea into a reusable Skill, a ⭐ would be appreciated.

[MIT License](LICENSE) · free to use, modify, and redistribute

Made by [@BingheTalk](https://github.com/BingheTalk)
