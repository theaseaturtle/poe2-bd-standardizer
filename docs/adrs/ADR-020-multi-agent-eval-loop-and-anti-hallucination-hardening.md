# ADR-020: 多 Agent 协同架构与红蓝对抗质检进化体系 (Multi-Agent Architecture & Adversarial Evaluation Loop)

## 状态 (Status)
**已通过 (Accepted)** - 2026-10-28

## 背景与痛点 (Context & Problem Statement)
在 ADR-019 中，项目确立了「实战 HUD 备忘单」与「POE2 多维术语对齐中枢」的双核心模式，大幅提升了交付效率与玩家体验。然而在实际落地时，单一 Agent 处理复杂长文本时仍面临以下瓶颈：
1. **长上下文注意力分散与疲劳**：主播 1~2 小时的视频听翻稿或万字长文输入时，单 Agent 容易在后半段丢失细节，或将生活琐事与核心机制混淆。
2. **“热心肠”脑补与隐蔽幻觉**：面对原文未提及的抗性、精魂消耗或未指明的辅助宝石时，单 Agent 容易“好心帮用户填满表格”，产生致命的机制臆测。
3. **词库与提示词迭代缺乏闭环验证**：每次修改 `SKILL.md` 或扩充 `poe2_terms.json` 后，缺乏自动化的“攻防测试”机制来验证抗幻觉能力是否真正提升。

## 核心架构决策 (Decisions)

### 1. 核心定位：Skill 为纲，Agent 为用
* **Skill 是唯一的规范核心 (SSOT SOP)**：`SKILL.md`、`data/poe2_terms.json` 和 `templates/` 是不可动摇的业务知识资产与格式标准。
* **Agent 是专业化执行与质检单元**：Agent 遵循 Skill 规范，按职责流水线分工，杜绝全能单体的认知过载。

### 2. 标准多 Agent 协同流水线 (Multi-Agent Pipeline)
将复杂任务解构为四大专职 Agent：
1. **Ingestion & Demystifier Agent (解构提取)**：前哨清洗，剥离情绪与口播废话，提炼触发源 $\to$ 介质 $\to$ 承伤 $\to$ 猝死点的机制链骨架。
2. **Rosetta Stone Normalizer Agent (术语对齐)**：领域专家，强制加载 `poe2_terms.json`，完成「黑话/简中 $\to$ 官方繁中 $\to$ Trade 英文」转换与表格连线矩阵生成。
3. **Zero-Hallucination Auditor Agent (红队质检)**：对抗性审查官，专查脑补、偷渡数值、伪繁体与未标明的缺失项，执行 `verify_bd.py` 自动化拦截。
4. **Porter & Publisher Agent (资产与发布)**：四段式版本命名归档，调用 Notion MCP 完成一键直传。

### 3. 红蓝对抗评测闭环 (Adversarial Eval Loop)
* 建立恶意与高难黑话测试用例库（包含国服特供译名、口播吹牛、精魂未算、断章取义等真实陷阱）。
* 蓝方 Agent 负责按照当前 Skill 执行转换，红方 Agent 负责挑刺找茬，输出《漏洞排查报告》，驱动 `SKILL.md` 负向约束与 `poe2_terms.json` 的针对性扩充。

### 4. 自动化校验器升级 (verify_bd.py 2.0)
* 新增国服特供/伪繁体黑名单拦截（如检测到“十字弩”、“女巫猎手”等未正名实体直接阻断）。
* 强化对未提及标记 `[⚠️ 原文未提及/缺项]` 的规范性检测，确保零无中生有。

## 收益与影响 (Consequences)
* **抗幻觉能力几何级提升**：通过红蓝对抗与 Auditor 机制，彻底斩断 AI 擅自脑补数值与连招的温床。
* **支持工业级批量与超长文本处理**：上下文有效隔离，轻松应对数万字主播口播稿与论坛复杂长贴。
* **Skill 具备自我演进能力**：构建了从“暴露漏洞 $\to$ 红方抓包 $\to$ 迭代规则与词库 $\to$ 绿灯发布”的良性工程闭环。
