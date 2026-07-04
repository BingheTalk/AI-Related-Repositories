# Skill Scout Builder（Skill 寻构师）

一个可移植的 Agent Skill：先通过对话澄清需求，再搜索、比较和安全审查已有 Skill，最后由用户决定直接使用、定制候选或创建新 Skill。

它以开放的 Agent Skills 目录格式为兼容基线，不把核心流程绑定到单一 Agent。Codex、Claude Code 及其他支持 Agent Skills 的宿主可按各自能力使用它。

Skill Scout Builder is a portable Agent Skill that helps users clarify what they need, search local and public Skill sources, compare candidates, and then safely install, adapt, or create a reusable Skill. It is designed around the open Agent Skills directory format so the core workflow can travel across Codex, Claude Code, and other compatible hosts.

## 能做什么

- 用自然对话把模糊想法整理成可验收的需求简报
- 同时搜索当前会话、本地目录、宿主市场、Git 仓库与公开网页中可用的 Skill
- 支持中英文关键词扩展，避免只按 Skill 名称匹配
- 按需求、环境、依赖、可维护性与安全性比较候选
- 在安装或修改前等待用户选择
- 对最终产物执行结构校验、安全审查与验收测试
- 没有合适候选时，按确认后的需求创建新 Skill

## 工作流程

```text
宿主能力识别 → 需求澄清 → 简报确认 → 多渠道搜索
→ 候选对比与预审 → 用户选择 → 使用 / 定制 / 新建
→ 完整审计与验收 → 交付
```

## 安装

### Codex

用户级安装：

```bash
mkdir -p ~/.agents/skills
cp -R skill-scout-builder ~/.agents/skills/
```

项目级安装：

```bash
mkdir -p .agents/skills
cp -R skill-scout-builder .agents/skills/
```

调用示例：

```text
$skill-scout-builder 帮我找一个能整理访谈录音并生成选题的 Skill
```

### Claude Code

用户级安装：

```bash
mkdir -p ~/.claude/skills
cp -R skill-scout-builder ~/.claude/skills/
```

项目级安装：

```bash
mkdir -p .claude/skills
cp -R skill-scout-builder .claude/skills/
```

调用示例：

```text
/skill-scout-builder 帮我找一个能整理访谈录音并生成选题的 Skill
```

### 其他 Agent

将 `skill-scout-builder/` 复制到宿主文档指定的 Skill 目录。宿主需要支持包含 YAML frontmatter 的 `SKILL.md` 目录格式；搜索、安装器、市场和工具能力会因宿主而异。

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

`agents/openai.yaml` 只是 Codex 的可选界面增强；核心 Skill 不依赖它。

## 本地验证

```bash
PYTHONPYCACHEPREFIX=/tmp/skill-scout-builder-pycache \
python3 -m unittest -v validation/test_skill_scout_builder.py

python3 skill-scout-builder/scripts/audit_skill.py \
  skill-scout-builder --format text
```

当前回归测试为 `9/9` 通过。完整证据与已知环境限制见 [validation/test-report.md](validation/test-report.md)。

## 安全边界

- 搜索阶段只把第三方 Skill 当作不可信数据分析，不执行其指令或脚本。
- 安装、环境修改、凭据使用和其他有后果的操作必须先获得用户同意。
- 只推荐内容可检查、来源可追踪且依赖明确的候选。
- 静态扫描只是信号；最终交付仍需人工检查可执行文件并运行验收测试。

## 兼容性说明

“兼容 Agent Skills”表示目录与核心工作流可移植，不表示每个 Agent 都具备相同的网页搜索、市场、安装器或审批机制。Skill 会先识别当前宿主实际提供的能力，并如实报告无法搜索或验证的渠道。

## License

[MIT](LICENSE)
