---
title: Change Graph 任务状态研究来源清单
status: active
created: 2026-10-09
updated: 2026-10-09
tags: [research, sources, verification, change-graph]
supersedes:
---

# Change Graph 任务状态研究来源清单

## 证据口径

本清单属于[论文研究项目](README.md)，负责外部来源身份、版本、发表状态、阅读范围和结果可信边界。初始化时只登记前序讨论提及的检索线索，**未将它们认定为已核实论文或已证明机制**。

每项核实记录应补齐官方标题、作者、官方 URL、年份、venue 与类别（主会 / Findings / Workshop / 期刊 / 预印本 / 待核实）、固定版本及核对日期。分别记录“找到入口 / 摘要阅读 / 全文阅读 / 代码静态核验 / 项目复现”；发表状态与效果证据分别判断。不能从聊天中的数字恢复论文结论。

已在[原课题来源清单](../../../../工具反馈管理/docs/research/cache-aware-tool-observation-management/source-inventory.md)登记的资料应先复用其证据，再检查是否适用于本项目；不得机械沿用旧日期和结论。

## 第一批核验队列

以下为初始化时的历史队列。已核验条目以文末 2026-10-09 首轮记录为准；尚未覆盖的工程项目继续待核。

以下名称保留为搜索线索，尚无本项目核实的官方链接、venue 或实验结论。排序依直接近邻优先，不表示重要性排名。

| 顺序 | 讨论中的名称 | 希望核对的具体问题 | 当前状态 |
|---|---|---|---|
| 1 | InfiAgent | 状态如何重建 Context？如何处理失败历史与当前有效方案？ | 身份、原文与发表状态待核实 |
| 1 | MAGE / Memory as Execution State Management | 是否已有与动态工作视图相同的状态修订和选择机制？ | 身份、原文与发表状态待核实 |
| 1 | Context as a Tool | 其 Context 选择变量、固定意图与压缩机制覆盖到哪里？ | 先查原课题清单，再核验本项目所需机制 |
| 1 | State-Aware Runtime for Long-Horizon LLM Agents | 所称权威状态、事务和视图机制是否已有实现及验证？ | 身份、原文与发表状态待核实 |
| 2 | StateMemBench | 怎样评测状态变化与过期事实，能否用于有效约束检验？ | 身份、原文与发表状态待核实 |
| 2 | ContinuityBench / Do Not Restart | 恢复与剩余工作评估是否覆盖我们的失败场景？ | 身份、原文与发表状态待核实 |
| 2 | Graph of Trace | 演化图用于可视化还是实际指导行动？人类评估怎样进行？ | 身份、原文与发表状态待核实 |
| 3 | Pi Durable | 持久化的是执行轨迹、业务状态还是语义任务状态？ | 工程项目身份及固定版本待核实 |
| 3 | DeepSeek Harness（基于 Cordis）/ Cordis | 框架生命周期与业务恢复分别保证什么？ | 分别核验项目，不能直接等同 |
| 3 | Jujutsu（JJ） | Change ID、Revision、操作历史的官方语义及借鉴边界 | 官方文档与版本待核实；不是论文效果依据 |
| 3 | pi-context | 与 Context as a Tool 的关系，按需 Context 的实际接口 | 工程项目身份及版本待核实 |

## 本地讨论来源

- [阶段性总结与设计假设](../change-graph-task-state-design-hypothesis.md)：用户直接提供的设计结论，未经过实证验证。
- 用户复制的前序讨论：2026-10-09 已可读取包括助手回复的文本；参考链接与复制范围不完整。原始个人文本不提交、不作为实验数据。
- 本轮项目初始化指令：授权建立研究项目并寻找论文问题，不证明创新成立。

## 核验后的逐项记录模板

每项新增记录保留：名称与官方入口；固定版本；年份、venue 和类别；核对日期；实际阅读深度；作者声称的结论及支持范围；项目是否复现；与候选问题的重叠或差异；下一步。

初始化核对日期：2026-10-09。当前仅完成队列登记，尚无本项目新核实的外部文献结果。

## 2026-10-09 首轮核验记录

核对日期均为 **2026-10-09**；责任为助手官方来源核验。没有项目复现或效果测量。“预印本已定位，正式发表未核实”不等于断言未发表。方法覆盖判断唯一见[近邻核验](neighbor-review.md)；问题建议唯一见[问题卡](problem-card.md)。

| ID / 完整标题 / 作者 | 年份、venue 与类别 | 固定来源 | 实际阅读与局限 |
|---|---|---|---|
| N1 — InfiAgent: An Infinite-Horizon Framework for General-Purpose Autonomous Agents；Chenglin Yu、Yuchen Wang、Songmiao Wang、Hongxia Yang、Li Ming | 2026，Findings of ACL；正式 Findings，非主会 | [Anthology 元数据](https://aclanthology.org/2026.findings-acl.1787/)、[正式 PDF](https://aclanthology.org/2026.findings-acl.1787.pdf)，pp.35884–35894 | 正式元数据、摘要、§3.2–3.3/4.1 相关方法；未完整代码审计、未复现。不能与同名 DABench 或 2025 pyramid 工作混同 |
| N2 — Beyond Semantic Organization: Memory as Execution State Management for Long-Horizon Agents（MAGE）；Yaoqi Chen 等 | 2026，预印本已定位，正式发表未核实 | [arXiv v1](https://arxiv.org/abs/2606.06090v1)、[HTML 方法](https://arxiv.org/html/2606.06090v1)，2026-06-04 | 元数据、§2–3 方法、§4 评估定义；论文已有兄弟分支 hints，不能视为本研究新增。未验证代码与作者数字 |
| N3 — Context as a Tool: Context Management for Long-Horizon SWE-Agents；Shukai Liu 等 | 2026，Findings of ACL；正式 Findings，非主会 | [元数据](https://aclanthology.org/2026.findings-acl.1032/)、[正式 PDF](https://aclanthology.org/2026.findings-acl.1032.pdf)，pp.20604–20617 | 正式元数据与§2.1–2.3；主动管理与稳定意图锚点已核实。未完整训练/协议核验，未使用作者 solved rate 作项目效果依据 |
| N4 — SKILL.state: Scalable Long-Horizon Agent Skills；Sanket Badhe、Priyanka Tiwari、Jonghyun Chung | 2026，预印本；作者 Comments 自述 accepted at EMNLP；正式 venue 类别与主会/Findings 待核实 | [arXiv v3](https://arxiv.org/abs/2608.26263v3)、[HTML](https://arxiv.org/html/2608.26263v3)，2026-09-02 | 元数据、§3 schema/更新机制、预算匹配表的存在；未正式接收证据核验、代码审查或复现。不可把 tested_hypotheses 省略而制造弱基线 |
| N5 — Can Agent Memory Systems Track Evolving State?（StateMem / StateMemBench）；Xinyi Fan、Miri Liu、Ruozhen Yang、Siru Ouyang、Jiawei Han | 2026，预印本已定位，正式发表未核实 | [arXiv v1](https://arxiv.org/abs/2608.19652v1)、[HTML](https://arxiv.org/html/2608.19652v1)，2026-08-20 | §4 类型、§5 依赖更新/渲染、§6 单次运行边界及匹配控制；未获取正式数据包/代码，未复现。它包含依赖传播和 needs_recheck，不可误报为空白 |
| N6 — Do Not Restart: Residual Completion for Stateful Agent Handoffs；Runzhi Deng、Yiming Zhong、Fang Zhao、Pan Zhou | 2026，预印本已定位，正式发表未核实 | [arXiv v4](https://arxiv.org/abs/2609.13800v4)、[HTML](https://arxiv.org/html/2609.13800v4)，2026-09-26 | §3.1–3.5 目标/合同/执行保障，§4 环境和评估定义；保证以完整合同构建为条件。未核实发布的可运行代码或重跑 |
| N7 — State-Aware Runtime for Long-Horizon LLM Agents: A Conceptual Framework and Research Agenda；Xiwei Chen | 2026，Cambridge Open Engage Working Paper；页面明确非 Cambridge 同行评审接收 | [v4 官方页](https://client.prod.orp.cambridge.org/engage/coe/article-details/6a80ae6b810b9dcc821646ae)，2026-08-17；DOI 10.33774/coe-2026-vt9t2 | 官方元数据、摘要与版本说明；未全文协议或代码审查，不声称实现/benchmark 已验证 |
| B1 — ContinuityBench: A Framework and Taxonomy for Evaluating Agent Recovery from Interrupted State；Aryan Gulati | 2026，官方 PDF 索引页脚标注 ICML CTB Workshop；非 ICML 主会。论坛 decision 未复核 | [官方 PDF ID](https://openreview.net/pdf?id=3N3BzvoLbG)、[内容哈希 PDF](https://openreview.net/pdf/93d0bd39f66f01a5565ae496208d39676dde78ec.pdf) | 官方搜索索引读取摘要/§3.4–3.6 与页脚；直接访问验证页/403、PDF下载失败。协议片段可确认 h0/h1/h2，代码与公共 snapshot 包未核实；不冒报全文读完 |
| B2 — When Users Change Their Mind: Evaluating Interruptible Agents in Long-Horizon Web Navigation（InterruptBench）；Henry Peng Zou 等 | 2026，预印本已定位，正式发表未核实 | [arXiv v1](https://arxiv.org/abs/2604.00892v1)、[HTML](https://arxiv.org/html/2604.00892v1)、[作者仓库](https://github.com/HenryPengZou/InterruptBench) | 论文§2 任务定义与§5 公开案例；固定仓库 task 0/raw updates/run.py/evaluator/multi-interrupt 文档静态核验。环境未启动、未重放真实轨迹 |

### 固定代码与本地证据边界

InterruptBench commit：`17da111e4858b93c0cab1d88f85e1735fbd1d423`（GitHub commits/main API 核对）。公开任务与代码链接固定到该 commit；局部文件及 SHA256 见[可追溯示例](traceable-example.md)。本地第三方代码保存于研究工作树的忽略目录 `artifacts/research-evidence/change-graph-neighbors-2026-10-09/`，仅阅读，不上传、不运行。Eval/LICENSE 为 MIT 许可文本；这不代替网站镜像、数据或全仓逐文件许可复核。

本轮没把 ContinuityBench 的多个同名项目混作一个来源。B1 的代码入口/公开断点包仍是缺口，不能把“论文定义恢复协议”升级为“可直接下载并运行全部断点任务”。

### 下一项来源核验

进入实验前需要逐项核对拟用近邻的可运行官方代码、固定依赖、状态接口与预算核算。SKILL.state 的正式接收类别、ContinuityBench 的论坛 decision/代码发布、StateMemBench 的数据资产继续待核实。Pi Durable/Cordis/JJ/pi-context 仍是工程来源队列，未据其可用性裁定论文创新。
