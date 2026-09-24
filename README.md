# POE2 术语对齐中枢与实战 HUD 备忘单助手 (Path of Exile 2 Rosetta Stone & HUD Assistant)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PoE2 Version](https://img.shields.io/badge/PoE2-0.5.x-blue.svg)](https://pathofexile2.com)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-brightgreen.svg)](https://www.python.org/)
[![0 External Dependencies](https://img.shields.io/badge/dependencies-0%20external-success.svg)](https://docs.python.org/3/)

专为《流放之路 2》（Path of Exile 2）玩家打造的**术语消歧与实战 HUD 备忘单工具**（支持 AI Agent Skill 与独立运行）。

彻底摆脱对第三方博主复杂乱序排版的盲目适配，聚焦解决最真实的玩家痛点：
**博主黑话、国服简中、国际服官方繁中与官方市集 (Trade) 英文混杂，导致游戏内找不到技能、市集搜不出装备。**

---

## ✨ 核心特性与设计原则

1. **多维术语对齐与市集搜索直达（Rosetta Stone）**：
   - 彻底理清：**`攻略黑话/简中 ➡️ 游戏内官方繁中 (NPC/背包) ➡️ 官方 Trade 英文 ➡️ 获取章节与筛选建议`** 四重映射。
   - 国际服官方繁中正名以 [poe2db.tw](https://poe2db.tw/tw/) 为唯一基准，官方英文以 [Path of Exile Trade](https://www.pathofexile.com/trade2) 为准。
2. **实战 HUD 备忘单（边玩边看单页卡片）**：
   - 剥除所有博主的生活碎碎念与无意义截图，浓缩为 5~10 KB 的超轻量纯文本速查卡。
   - 双屏打游戏或手机查阅一屏搞定，支持通过 Notion MCP 直接秒推至个人知识库。
3. **技能连线强制表格化（Table-First Gem Matrix）**：
   - 主动技能、孔色孔数、连线辅助（繁/英/俗称）、购买章节与 NPC、战斗联动机制全部以 Markdown 表格整齐收纳。
4. **官方市集 (Trade) 淘装指南**：
   - 关键基底（如 `Bombard Crossbow` 轟擊十字弓）与核心英文词缀一目了然，在 Trade 网站直接复制即可搜索。
5. **语言规范化**：
   - 对话、机制剖析与指引说明一律采用**简体中文**。
   - 游戏专有名词精准使用**官方繁中**与**官方英文**。

---

## 📁 项目目录结构

```text
.
├── SKILL.md                 # Antigravity / Claude Code 技能核心定义
├── CONTEXT.md               # 项目领域模型与规范说明 (含 ADR-019 战略转向)
├── data/
│   └── poe2_terms.json      # POE2 术语多维对照中枢 (职业、技能、辅助、基底、黑话)
├── templates/
│   └── poe2_hud_cheatsheet_template.md # 实战 HUD 备忘单标准模板 (表格化连线)
├── references/
│   └── poe2_terms_reference.md # 官方繁体中英名词消歧参考速查表
├── docs/adrs/               # 架构决策记录 (ADR-001 ~ ADR-019)
├── scripts/
│   └── verify_bd.py         # 自动化质量验证脚本 (验证表格行数与数值及格线)
├── input/                   # 原始文档或加点文件 (.build)
└── output/                  # 标准化 HUD 备忘单交付目录
```

---

## 🚀 使用方式

### 模式一：随问随查与黑话破译（对话直出）
看直播或攻略遇到看不懂的术语，随手发来一段：
> **用户输入**：“攻略说打散弹+火雷，副手拿狼头位移，这是啥意思？”  
> **AI 输出**：大白话机制分析 + 技能连线表格（爆炸擲彈 `Explosive Grenade` + 散射彈藥 `Scatter Ammo`）+ 市集搜索关键词。

### 模式二：生成边玩边看 HUD 备忘单
丢入一篇长文或链接，AI 自动生成单页极简备忘录并可直接通过 Notion MCP 发送到 Notion：
* 包含按章节 NPC 购买清单
* 包含装备市集筛选词缀
* 包含抗性与血量及格线
* 包含折叠的 BuildPlanner 纯文本模拟器配置串
