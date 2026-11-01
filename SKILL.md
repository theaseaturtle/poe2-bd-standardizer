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
* **短文本/单点破译分支 (Instant Query)**：若输入为单个技能、装备或片段黑话咨询（< 300 字），仅允许在回复首行做一次「提问词 $\to$ **官方繁中正名**」映射确认，下方机制解析与表格 100% 禁用黑话并直接执行 Step 3。
* **长文/视频稿/天梯快照分支 (Full HUD Cheatsheet)**：若输入为完整攻略或文档，触发完整多 Agent 协同流水线（Step 2 $\to$ 5）。

### Step 2: 降维解构与脱水 (Demystification)
* **执行角色**：[`agents/ingestion_demystifier.md`](agents/ingestion_demystifier.md)
* **核心动作**：剥除作者生活琐事、引流废话与夸张情绪词，提炼“触发源 $\to$ 介质 $\to$ 承伤 $\to$ 猝死点”四大机制因果链。
* **完成判定 (Completion Criterion)**：
  - [x] 四联机制链完整提取；
  - [x] 原文未提及的抗性、精魂或连招已明确标记为 `[⚠️ 原文未提及/缺项]`，无任何先行脑补。

### Step 3: 权威术语对齐与连线表格化 (Rosetta Alignment)
* **执行角色**：[`agents/rosetta_normalizer.md`](agents/rosetta_normalizer.md)
* **参考依据**：领域词汇表 [`GLOSSARY.md`](GLOSSARY.md)、单一天理数据源 [`data/poe2_terms.json`](data/poe2_terms.json) 与 [`templates/poe2_hud_cheatsheet_template.md`](templates/poe2_hud_cheatsheet_template.md)
* **核心动作**：执行简繁混合（麻花文）排版与零黑话转换——非游戏叙事用简体中文；游戏系统机制词（天賦、昇華、精魂、護甲、抗性、詞綴等）用不加粗官方繁中；专有实体名用 `**加粗官方繁中**`；装备词缀用 `poe2db.tw` 官方繁中原文模板 + 官方英文 Trade 检索词。
* **完成判定 (Completion Criterion)**：
  - [x] 技能连线采用 5 列表格标准（主动技能繁英、插槽顏色/孔數、連線輔助寶石繁英、开启/购买章节与 NPC、战斗手感与联动机制），表格与正文 0 攻略俗称残留；
  - [x] 市集淘装表 100% 采用 `poe2db.tw` 官方繁中詞綴原文模板 + 官方英文 Trade 检索词（严禁“物理点伤”、“攻速”等简体概括）。

### Step 4: 红队反幻觉审查与测试门禁 (Adversarial Audit Gate)
* **执行角色**：[`agents/zero_hallucination_auditor.md`](agents/zero_hallucination_auditor.md)
* **工具执行**：`python3 scripts/verify_bd.py <产物路径>` 与 `python3 scripts/run_adversarial_eval.py <产物路径>`
* **完成判定 (Completion Criterion)**：
  - [x] `verify_bd.py` 与 `run_adversarial_eval.py` 执行退出码均为 0；
  - [x] 0 伪繁体、0 攻略黑话、0 未转繁中的简体游戏系统词/词缀简写、0 `【】` 方头括号；
  - [x] 0 非法占位符（无 TODO / FIXME / 待补充）；
  - [x] 产物与原文严格保真，凡原文缺项必有 `[⚠️ 原文未提及/缺项]`。未满足此条直接打回重做。

### Step 5: 规范归档与知识库交付 (Delivery & Notion Sync)
* **执行角色**：[`agents/porter_publisher.md`](agents/porter_publisher.md)
* **核心动作**：文件名、H1 大标题与 YAML `title` 使用简体中文（按 `[游戏版本/赛季]_[基础职业+升华]_[核心机制/技能]_[BD正式名称].md` 归档至 `output/` 目录），以便简体输入法搜索。
* **完成判定 (Completion Criterion)**：
  - [x] 顶部 YAML Frontmatter 包含 `version`, `class`, `ascendancy`, `stage`, `budget`, `core_uniques` 六大字段（其中 `class`, `ascendancy`, `core_uniques` 使用官方繁中）；
  - [x] 若用户开启 Notion MCP，一键直传对应页面并验证排版。

---

## 零臆测铁律与负向约束 (Ironclad Negative Constraints)

1. **绝对零脑补数值**：原作者未明确指明抗性阈值、精魂预算分配或属性门槛时，**严禁自行推算或填满数值**，必须严格输出 `[⚠️ 原文未提及/缺项]`。
2. **严禁填空式虚构辅助石**：作者只写了 3 连就只写 3 连，绝不允许为了美观在表格中自行脑补 5 连或 6 连。
3. **正文与表格零黑话 & 零 `【】` 括号**：严禁出现“十字弩”、“雇佣兵”、“女巫猎手”、“散弹”、“火雷”、“物理点伤”、“攻速”等国服特供词、黑话或简体词缀概括；严禁使用 `【】` 包裹名词。
4. **简繁麻花文双轨层级 (ADR-021)**：
   - **叙事引导语**：一律使用**简体中文**；
   - **系统机制词**（天賦、昇華、精魂、盛怒、護甲、閃避、能量護盾、抗性、暴擊、擊暈、暈眩累積、詞綴、插槽、異界）：使用**不加粗的官方繁中**；
   - **专有实体名**（職業、昇華名、技能/輔助寶石、裝備基底/傳奇、天賦節點名、NPC、通貨、符文）：使用**加粗官方繁中 `**官方繁中**`**；
   - **装备词缀**：严格使用 **`poe2db.tw` 官方繁中詞綴原文模板 + 官方英文 Trade 检索词**。

---

## 核心资产指针 (Disclosed References)

* **领域词汇表**: [`GLOSSARY.md`](GLOSSARY.md)
* **领域词典 (SSOT)**: [`data/poe2_terms.json`](data/poe2_terms.json) & [`references/poe2_terms_reference.md`](references/poe2_terms_reference.md)
* **HUD 模板**: [`templates/poe2_hud_cheatsheet_template.md`](templates/poe2_hud_cheatsheet_template.md)
* **质量门禁**: [`scripts/verify_bd.py`](scripts/verify_bd.py)
* **红队评测**: [`scripts/run_adversarial_eval.py`](scripts/run_adversarial_eval.py)
* **Agent SOP 目录**: [`agents/`](agents/)
