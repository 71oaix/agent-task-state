---
title: Change Graph 任务状态研究来源清单
status: active
created: 2026-10-09
updated: 2026-10-15
tags: [research, sources, verification, change-graph]
supersedes:
---

# Change Graph 任务状态研究来源清单

## 证据口径

本清单属于[论文研究项目](README.md)，负责外部来源身份、版本、发表状态、阅读范围和结果可信边界。初始化时只登记前序讨论提及的检索线索，**未将它们认定为已核实论文或已证明机制**。

每项核实记录应补齐官方标题、作者、官方 URL、年份、venue 与类别（主会 / Findings / Workshop / 期刊 / 预印本 / 待核实）、固定版本及核对日期。分别记录“找到入口 / 摘要阅读 / 全文阅读 / 代码静态核验 / 项目复现”；发表状态与效果证据分别判断。不能从聊天中的数字恢复论文结论。

已在[原课题来源清单](../../../../工具反馈管理/docs/research/cache-aware-tool-observation-management/source-inventory.md)登记的资料应先复用其证据，再检查是否适用于本项目；不得机械沿用旧日期和结论。

## 第一批核验队列

2026-10-10 新来源队列及读取纠错：用户指定[数据库韧性设计对话](database-resilience-discussion.md)，接口仅返回五轮；随后用户复制文本可辨认七轮，本次连续读到末尾，补回开头两轮。对话提及 ESAA: Event Sourcing for Autonomous Agents in LLM-Based Software Engineering、Agent Trajectory Interchange Format（ATIF）、AgentOps: Enabling Observability of LLM Agents、From Agent Traces to Trust: A Survey of Evidence Tracing and Execution Provenance in LLM Agents、Experience Memory Graph: One-Shot Error Correction for Agents、Zep: A Temporal Knowledge Graph Architecture for Agent Memory。遗漏段还引入 Pi Durable、LangGraph、Temporal、Phoenix、Letta、AMBER、NeMo Agent Toolkit 等来源线索；中段还有 SAMem、ExpeL、Reflexion、Agent Zero Memory、OpenTelemetry。这里只补齐线索，不把它们全部列为系统必须采用的机制。责任为助手后续官方来源核验；当前标题、作者、年份、发表 venue/类别、固定版本、机制与缺陷均待核实，未复现。下一关按问题价值、机制依据、实验证据和局限核查，不以对话内引用编号或“六篇”表述作正式文献证据。

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

2026-10-10 阅读补充：沿用 N1 的 Findings of ACL 正式 PDF、N2/N5 的 arXiv v1；重新核对官方入口。N1 扩展到 §4.2 串行层级调用和 §5.2 PDF 覆盖任务及消融；N2 扩展到 §4.4 表4及附录任务/基线协议；N5 扩展到 §4 合成任务构造、§6.2 表3消融和单次运行边界。N2/N5 的正式发表状态仍未核实。本次只核查作者报告，不验证其运行数字，不构成全文代码审计或项目复现。信息选择理由与实验代表性的判断唯一维护于[近邻核验补充](neighbor-review.md#2026-10-10保留信息的理由与实验证据)。

进入实验前需要逐项核对拟用近邻的可运行官方代码、固定依赖、状态接口与预算核算。SKILL.state 的正式接收类别、ContinuityBench 的论坛 decision/代码发布、StateMemBench 的数据资产继续待核实。Pi Durable/Cordis/JJ/pi-context 仍是工程来源队列，未据其可用性裁定论文创新。


## 2026-10-12：研究计划候选来源核查

核对日期2026-10-12。以下为规划所需的官方入口核验，未执行复现；采用依据与下一步见[计划执行说明](research-plan-v0.1-agent-notes.md)。既有论文的前次全文阅读范围不因此扩大。

| 来源 | 类别、年份与官方证据 | 本次支持范围与未完成项 |
|---|---|---|
| JJ operation log | [官方软件文档](https://docs.jj-vcs.dev/latest/operation-log/)，持续更新 | 工作操作历史设计参考；采用前固定软件版本 |
| Event Sourcing | [Microsoft 官方架构文档](https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing)，非论文 | 事件与状态重建参考；不是效果实验 |
| PROV Primer | [W3C 2013 Working Group Note](https://www.w3.org/TR/prov-primer/) | 来源与主体建模参考；不要将 Primer 本身称为 Recommendation |
| Skyframe | [Bazel 官方文档](https://bazel.build/reference/skyframe)，非论文 | 增量依赖机制参考；不能保证语义推理正确 |
| Zep | [arXiv 2501.13956](https://arxiv.org/abs/2501.13956)，2025；正式 venue 待核实 | 论文入口和摘要核对；方法、消融及代码仍须查 |
| ATIF | [Harbor 官方 RFC](https://github.com/harbor-framework/harbor/blob/main/rfcs/0001-trajectory-format.md)，页面2026年4月、v1.8；非学术论文 | 轨迹格式候选；采用前固定 commit 与 schema |
| SWE-EVO | [arXiv 2512.18470](https://arxiv.org/abs/2512.18470)，2025；正式 venue 待核实；[官方仓库](https://github.com/SWE-EVO/SWE-EVO) | 软件演化执行底座候选；仅摘要和 README，环境、评分与在线变更协议未核验 |

未确认 ESAA、AgentOps、From Agent Traces to Trust、Experience Memory Graph 的具体版本与发表身份，本轮不据此得出机制结论。

## 2026-10-13：v1.0第一轮扩展与重点核查

责任：助手。以下按2026-10-13核对；待核实venue不等于断言未发表。所读版本不自动代表正式发表版。未运行任何论文实验。SWE-EVO沿既有登记补查固定README，既有N/B编号保留。检索与选择理由见[证据说明](research-round-1-evidence.md)，面向人类的取舍见[研究结论](research-round-1.md)。

| 编号/官方标题 | 作者 | 年份、venue类别与版本 | 官方证据 | 阅读与可信边界 |
|---|---|---|---|---|
| R1：ESAA: Event Sourcing for Autonomous Agents in LLM-Based Software Engineering | Elzo Brito dos Santos Filho | 2026；arXiv v1，2026-02-26；正式venue待核实 | [官方入口](https://arxiv.org/html/2602.23193v1) | 方法§3–4、案例§5、讨论§7–8；固定协议静态读取。可行性非因果验证 |
| R2：SlopCodeBench: Benchmarking How Coding Agents Degrade Over Long-Horizon Iterative Tasks | Gabriel Orlanski等 | 2026；arXiv v2，2026-05-07；正式venue待核实 | [官方入口](https://arxiv.org/html/2603.24755v2) | §2、主要实验及附录code_search阶段1–3；代码/任务仓库固定读取，未运行 |
| R3：SWE-Chain: Benchmarking Coding Agents on Chained Release-Level Package Upgrades | Man Ho Lam等 | 2026；arXiv v1，2026-05-14；正式venue待核实 | [官方入口](https://arxiv.org/html/2605.14415v1) | §2–3协议与实验口径；README/run.sh固定读取，未评分审计 |
| R4：SWE-CI: Evaluating Agent Capabilities in Maintaining Codebases via Continuous Integration | Jialong Chen等 | 2026；arXiv v3，2026-03-18；正式venue待核实 | [官方入口](https://arxiv.org/html/2603.03823v3) | 任务/Architect/Programmer/评估方法；固定README，未运行 |
| R5：SWE Context Bench: A Benchmark for Context Learning in Coding | Jared Zhu、Minhao Hu、Junde Wu | 2026；arXiv v1，2026-02-09；正式venue待核实 | [官方入口](https://arxiv.org/html/2602.08316v1) | §2–3及Table3；当前数据与v1不混用；Oracle不等于自由检索 |
| R6：Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents? | Thibaud Gloaguen等 | 2026；ICLR MemAgents Workshop；所读arXiv v2，2026-06-23 | [官方入口](https://arxiv.org/html/2602.11988v2) | §3–5；Workshop身份以ETH官方页核实，正式版与v2未逐项比对 |
| R7：Experience Memory Graph: One-Shot Error Correction for Agents | Wenjun Wang、Yuchen Fang等 | 2026；所读arXiv v1，2026-07-15；发现v2未补读；正式venue待核实 | [官方入口](https://arxiv.org/html/2607.13884v1) | §4–5及消融；环境非软件，成功轨迹参照。未来会议模板非接收证据 |
| R8：SWE-MeM: Learning Adaptive Memory Management for Long-Horizon Coding Agents | Shuzheng Gao等 | 2026；arXiv v1，2026-06-26；正式venue待核实 | [官方入口](https://arxiv.org/html/2606.28434v1) | 记忆工具/训练/§4.2消融；模型训练变化不归因于图存储 |
| R9：From Agent Traces to Trust: A Survey of Evidence Tracing and Execution Provenance in LLM Agents | Yiqi Wang等 | 2026；arXiv v2，2026-06-14；正式venue待核实 | [官方入口](https://arxiv.org/html/2606.04990v2) | 全文取得；本轮主要摘要/分类/引用线索，非全文精读或实验验证 |
| R10：SWE-Milestone: Evaluating AI Agents on Continuous Software Evolution | Gangda Deng、Zhaoling Chen等 | 2026；ICML主会，PMLR306:23853–23890；所读arXiv v4，2026-07-21 | [官方入口](https://proceedings.mlr.press/v306/deng26d.html) | 正式身份核实；v4§3–5、附录案例/局限与固定README。未运行、未与正式PDF逐项对照 |
| R11：A truth maintenance system | Jon Doyle | 1979；Artificial Intelligence期刊12(3):231–272 | [官方入口](https://www.sciencedirect.com/science/article/pii/0004370279900080) | 作者MIT目录与出版社身份/摘要核对；全文精读待办 |
| R12：Reflexion: Language Agents with Verbal Reinforcement Learning | Noah Shinn等 | 2023；NeurIPS主会 | [官方入口](https://proceedings.neurips.cc/paper_files/paper/2023/hash/1b44b878bb782e6954cd888628510e90-Abstract-Conference.html) | 本轮官方条目/摘要；不追加未读消融或数字 |
| R13：ExpeL: LLM Agents Are Experiential Learners | Andrew Zhao等 | 2024；AAAI主会技术轨道，38(17):19632–19642 | [官方入口](https://ojs.aaai.org/index.php/AAAI/article/view/29936) | 本轮官方条目/摘要；经验提炼方法入口，全文待选读 |
| R14：MetaGPT: Meta Programming for A Multi-Agent Collaborative Framework | Sirui Hong等 | 2024；ICLR Conference | [官方入口](https://proceedings.iclr.cc/paper_files/paper/2024/hash/6507b115562bb0a305f1958ccc87355a-Abstract-Conference.html) | 官方条目/摘要；角色SOP与交接相邻，非完整方案历史证据 |
| R15：ChatDev: Communicative Agents for Software Development | Chen Qian等 | 2024；ACL主会长文，15174–15186 | [官方入口](https://aclanthology.org/2024.acl-long.810/) | 官方条目/摘要；开发协作相邻，未补读完整实验 |
| R16：AgentOps: Enabling Observability of LLM Agents | Liming Dong、Qinghua Lu、Liming Zhu | 2024；所读官方摘要v2，2024-11-30；正式venue待核实 | [官方入口](https://arxiv.org/abs/2411.05285) | 官方入口/摘要；生命周期追踪线索，不当作语义维护实验证据 |

R6正式身份另见[ETH SRI官方发表页](https://www.sri.inf.ethz.ch/publications/gloaguen2026agentsmd)；R10所读[v4正文](https://arxiv.org/html/2603.13428v4)与正式PMLR页面分别固定。R11作者目录见[MIT MEDG](https://groups.csail.mit.edu/medg/ftp/doyle/)。所有条目本次核对日期为2026-10-13。原始下载不提交；固定仓库与读取范围见证据说明。MAGIS等在官方检索中作为协作线索发现，但本轮没有足够阅读范围支持机制判断，未提升为设计依据。

## 2026-10-14：基本操作与组合机制来源

核对日期均为2026-10-14，责任为助手。本轮提供[元操作候选](primitive-candidates-v0.1.md)及[操作语义与阅读范围](primitive-candidates-v0.1-agent-notes.md)。没有复现或模型实验；我们的组合建议与来源原有接口分别标明。

| 编号 | 官方来源、作者与身份 | 固定版本或日期 | 阅读范围及设计用途 |
|---|---|---|---|
| P1 | [JJ Glossary](https://github.com/jj-vcs/jj/blob/02afa7cab7ab706ec05fc9e8aab7b4ff9a3cd11a/docs/glossary.md)、[Operation log](https://github.com/jj-vcs/jj/blob/02afa7cab7ab706ec05fc9e8aab7b4ff9a3cd11a/docs/operation-log.md)、[Conflicts](https://github.com/jj-vcs/jj/blob/02afa7cab7ab706ec05fc9e8aab7b4ff9a3cd11a/docs/conflicts.md)；jj-vcs维护者，软件官方文档，非学术发表 | commit `02afa7cab7ab706ec05fc9e8aab7b4ff9a3cd11a` | 身份、rewrite、divergence、view、operation及冲突概念；Change非独立实体；不声称无限保留或语义自动合并 |
| P2 | [Datomic Transaction Model](https://docs.datomic.com/transactions/model.html)、[Transaction Functions](https://docs.datomic.com/transactions/transaction-functions.html)；Cognitect官方软件文档，非论文 | 2026-10-14页面快照及SHA256，非产品版本冻结 | 不可变db value、with/transact、事务完整性、db/cas与纯函数约束；启发候选构造与原子登记，不等于选型 |
| P3 | [PROV-DM: The PROV Data Model](https://www.w3.org/TR/2013/REC-prov-dm-20130430/)；Luc Moreau、Paolo Missier编辑，W3C Recommendation，非会议论文 | 2013-04-30固定推荐标准 | §2、§5.2至§5.4来源、revision、责任、bundle；不把provenance当形式蕴含 |
| P4 | [An assumption-based TMS](https://dekleer.org/Publications/An%20Assumption-Based%20TMS.pdf)；Johan de Kleer；Artificial Intelligence期刊，28(2):127–162 | 1986；作者公开原文；[作者发表目录](https://dekleer.org/bib.htm)与[出版社条目](https://www.sciencedirect.com/science/article/pii/0004370286900809)核实身份 | §1与§4.3至§4.7相关段落，重点§4.6三个基本操作；非全文证明审计。假设环境不同于LLM Context，保证相对于给定依据 |
| P5 | [Event Sourcing Pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing)；Microsoft Azure Architecture Center官方工程文档，非论文 | 2026-10-14页面快照及SHA256 | 追加事件、投影、重放、一致性与事件演化；不是现成的工作语义模型 |

原文保存在忽略目录 `artifacts/research-evidence/task-state-primitives-2026-10-14/`，完整路径语义及manifest见Agent说明，不提交PDF或第三方原文。以上证据支持候选设计来源，不证明我们的组合已经最小、完备或提高任务质量。

## 2026-10-14：审阅后的近邻方法复核

用于[元操作候选 v0.2](primitive-candidates-v0.2.md)和[十项机制映射](primitive-candidates-v0.2-agent-notes.md)。继承原有作者、来源编号和发表身份登记；本轮没有找到新的正式接收证据，不能据此断言未发表。

| 来源 | 版本、类别与核对日期 | 本轮阅读范围与影响 |
|---|---|---|
| [MAGE](https://arxiv.org/html/2606.06090v1) | 2026 arXiv v1；正式 venue 待核实；2026-10-14 | §3.2–3.3：执行树、摘要、维护及分支修订；已有当前路径及替代分支，不因接口名不同否定选择能力 |
| [StateMem](https://arxiv.org/html/2608.19652v1) | 2026 arXiv v1；正式 venue 待核实；2026-10-14 | §5.1–5.3：来源、依赖、替代及 needs_recheck；适用性维护不是本项目独有机制 |
| [ESAA](https://arxiv.org/html/2602.23193v1) | 2026 arXiv v1；正式 venue 待核实；2026-10-14 | §3 及此前固定仓库提交 22e54a898ee4821a503caf2964e88ab7dee5eac1 的投影规范；已有任务动作、归属约束和投影，不能称为只有 append；仓库规范与论文版本分开 |

没有运行上述实现。映射中的“未核实”是证据边界，不是能力不存在的证明；本项目候选协议也没有实现保证。P 系列固定来源继续作为设计借鉴，不作为新协议正确性证明。

## 2026-10-15：本地分类迁移，不改变来源判断

当前两批共 41 个文件移至主工作区 `artifacts/agent-task-state/`，按原样文件、正文提取、参考提取、仓库快照、发表元数据和获取记录分类。迁移前后保存文件 SHA256 一致，获取清单内容不变；旧位置、现位置与逐文件 hash 查[分类说明](../../reference/artifact-organization.md)。旧条目中的研究工作树路径保留为采集历史，不再是现存文件地址。2026-10-09 的六个 InterruptBench 快照仍在主工作区 `artifacts/worktrees/change-graph-paper/artifacts/research-evidence/change-graph-neighbors-2026-10-09/`。本轮没有重新核验论文发表状态或新增活动研究结论。
