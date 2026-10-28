---
name: poe2-bd-standardizer
description: Standardize Path of Exile 2 (PoE2 / 流放之路 2 / 流亡黯道 2) builds into verified HUD cheatsheets and multi-language trade matrices. Trigger when user mentions PoE2 builds, BD 整理, 配装解析, 技能连线, 术语对齐, 黑话破译, or /poe2-bd.
---

# POE2 术语对齐中枢与实战 HUD 备忘单系统 (PoE2 Rosetta Stone & HUD Assistant)

本 Skill 是将所有非结构化、黑话混杂的 PoE2 攻略转化为**高保真、零臆测、可直接用于市集搜索与打游戏副屏查阅的实战 HUD 备忘单**的执行路由器。

---

## 路由工作流与完成标准 (Pipeline & Hard Completion Criteria)

每次处理 PoE2 BD 时，严格按顺序执行以下 4 步流程。每一个步骤只有在其 **完成判定 (Completion Criteria)** 100% 满足后，方可推进至下一步：

### Step 1: 规模研判与分支路由 (Triage & Route)
* **短文本/单点破译分支 (Instant Query)**：若输入为单个技能、装备或片段黑话咨询（< 300 字），直接在主上下文中执行 Step 3 输出多维对照卡片。
* **长文/视频稿/天梯快照分支 (Full HUD Cheatsheet)**：若输入为完整攻略或文档，触发完整多 Agent 协同流水线（Step 2 $\to$ 5）。

### Step 2: 降维解构与脱水 (Demystification)
* **执行角色**：[`agents/ingestion_demystifier.md`](agents/ingestion_demystifier.md)
* **核心动作**：剥除作者生活琐事、引流废话与夸张情绪词，提炼“触发源 $\to$ 介质 $\to$ 承伤 $\to$ 猝死点”四大机制因果链。
* **完成判定 (Completion Criterion)**：
  - [x] 四联机制链完整提取；
  - [x] 原文未提及的抗性、精魂或连招已明确标记为 `[⚠️ 原文未提及/缺项]`，无任何先行脑补。

### Step 3: 权威术语对齐与连线表格化 (Rosetta Alignment)
* **执行角色**：[`agents/rosetta_normalizer.md`](agents/rosetta_normalizer.md)
* **参考依据**：单一天理数据源 [`data/poe2_terms.json`](data/poe2_terms.json) 与 [`templates/poe2_hud_cheatsheet_template.md`](templates/poe2_hud_cheatsheet_template.md)
* **核心动作**：将所有民间黑话与国服简中强制清洗为 **【官方繁中】(poe2db)** 与 **【官方英文】(PoE Trade 搜索词)**，并强制以 Markdown 表格输出技能连线。
* **完成判定 (Completion Criterion)**：
  - [x] 技能连线必须采用 5 列表格标准（技能、插槽颜色/孔数、辅助宝石、NPC与购买章节、手感与联动）；
  - [x] 市集淘装表包含英文基底与英文筛选词（Item Type / Stat）。

### Step 4: 红队反幻觉审查与测试门禁 (Adversarial Audit Gate)
* **执行角色**：[`agents/zero_hallucination_auditor.md`](agents/zero_hallucination_auditor.md)
* **工具执行**：`python3 scripts/verify_bd.py <产物路径>` 与 `python3 scripts/run_adversarial_eval.py <产物路径>`
* **完成判定 (Completion Criterion)**：
  - [x] `verify_bd.py` 执行退出码为 0（所有 5 项门禁全部 PASS）；
  - [x] 0 伪繁体黑名单命中（无“十字弩”、“雇佣兵”、“女巫猎手”等遗留）；
  - [x] 0 非法占位符（无 TODO / FIXME / 待补充）；
  - [x] 产物与原文严格保真，凡原文缺项必有 `[⚠️ 原文未提及/缺项]`。未满足此条直接打回重做。

### Step 5: 规范归档与知识库交付 (Delivery & Notion Sync)
* **执行角色**：[`agents/porter_publisher.md`](agents/porter_publisher.md)
* **核心动作**：按四段式公式 `[游戏版本/赛季]_[基础职业+昇華]_[核心机制/技能]_[BD正式名称].md` 归档至 `output/` 目录。
* **完成判定 (Completion Criterion)**：
  - [x] 顶部 YAML Frontmatter 包含 `version`, `class`, `ascendancy`, `stage`, `budget`, `core_uniques` 六大字段；
  - [x] 若用户开启 Notion MCP，一键直传对应页面并验证排版。

---

## 零臆测铁律与负向约束 (Ironclad Negative Constraints)

1. **绝对零脑补数值**：原作者未明确指明抗性阈值、精魂预算分配或属性门槛时，**严禁自行推算或填满数值**，必须严格输出 `[⚠️ 原文未提及/缺项]`。
2. **严禁填空式虚构辅助石**：作者只写了 3 连就只写 3 连，绝不允许为了美观在表格中自行脑补 5 连或 6 连。
3. **黑名单硬性拦截**：严禁出现“十字弩”（必须为【十字弓】）、“雇佣兵”（必须为【傭兵】）、“女巫猎手”（必须为【女巫獵人】）等任何国服特供或伪繁体名称。
4. **语言双轨规范**：解析、指引与说明一律使用**简体中文**；所有游戏实体专有名词必须使用**官方繁中 + 官方英文**。

---

## 核心资产指针 (Disclosed References)

* **领域词典 (SSOT)**: [`data/poe2_terms.json`](data/poe2_terms.json)
* **HUD 模板**: [`templates/poe2_hud_cheatsheet_template.md`](templates/poe2_hud_cheatsheet_template.md)
* **质量门禁**: [`scripts/verify_bd.py`](scripts/verify_bd.py)
* **红队评测**: [`scripts/run_adversarial_eval.py`](scripts/run_adversarial_eval.py)
* **Agent SOP 目录**: [`agents/`](agents/)
