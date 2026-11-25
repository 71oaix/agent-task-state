# 项目语义状态管理研究来源清单

## 近期来源登记

2026-11-17：StateHarness、MemTrace、ProjectGuard / SLUMP、OpenWiki 已登记到[近期来源队列](../../survey/project-semantic-state/survey.md)。候选入口来自论文讨论交接，均待原始来源核验；本次不沿用聊天中的机制、发表身份或实验数字作为事实。下文保留既有调查及其核验日期。


## 证据口径

本清单属于[本项目](../../../README.md)，负责外部来源身份、版本、发表状态、阅读范围和结果可信边界。初始化时只登记前序讨论提及的检索线索，**未将它们认定为已核实论文或已证明机制**。

每项核实记录应补齐官方标题、作者、官方 URL、年份、venue 与类别（主会 / Findings / Workshop / 期刊 / 预印本 / 待核实）、固定版本及核对日期。分别记录“找到入口 / 摘要阅读 / 全文阅读 / 代码静态核验 / 项目复现”；发表状态与效果证据分别判断。不能从聊天中的数字恢复论文结论。

已在[原课题来源清单](../../../../工具反馈管理/docs/research/cache-aware-tool-observation-management/source-inventory.md)登记的资料应先复用其证据，再检查是否适用于本项目；不得机械沿用旧日期和结论。

## 第一批核验队列

2026-10-10 新来源队列及读取纠错：用户指定[数据库韧性设计对话](../../../history/paused-topics/database-resilience-discussion.md)，接口仅返回五轮；随后用户复制文本可辨认七轮，本次连续读到末尾，补回开头两轮。对话提及 ESAA: Event Sourcing for Autonomous Agents in LLM-Based Software Engineering、Agent Trajectory Interchange Format（ATIF）、AgentOps: Enabling Observability of LLM Agents、From Agent Traces to Trust: A Survey of Evidence Tracing and Execution Provenance in LLM Agents、Experience Memory Graph: One-Shot Error Correction for Agents、Zep: A Temporal Knowledge Graph Architecture for Agent Memory。遗漏段还引入 Pi Durable、LangGraph、Temporal、Phoenix、Letta、AMBER、NeMo Agent Toolkit 等来源线索；中段还有 SAMem、ExpeL、Reflexion、Agent Zero Memory、OpenTelemetry。这里只补齐线索，不把它们全部列为系统必须采用的机制。责任为助手后续官方来源核验；当前标题、作者、年份、发表 venue/类别、固定版本、机制与缺陷均待核实，未复现。下一关按问题价值、机制依据、实验证据和局限核查，不以对话内引用编号或“六篇”表述作正式文献证据。

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

- [阶段性总结与设计假设](../../../history/design/change-graph-task-state/design-hypothesis.md)：用户直接提供的设计结论，未经过实证验证。
- 用户复制的前序讨论：2026-10-09 已可读取包括助手回复的文本；参考链接与复制范围不完整。原始个人文本不提交、不作为实验数据。
- 本轮项目初始化指令：授权建立研究项目并寻找论文问题，不证明创新成立。

## 核验后的逐项记录模板

每项新增记录保留：名称与官方入口；固定版本；年份、venue 和类别；核对日期；实际阅读深度；作者声称的结论及支持范围；项目是否复现；与候选问题的重叠或差异；下一步。

初始化核对日期：2026-10-09。当前仅完成队列登记，尚无本项目新核实的外部文献结果。

## 2026-10-09 首轮核验记录

核对日期均为 **2026-10-09**；责任为助手官方来源核验。没有项目复现或效果测量。“预印本已定位，正式发表未核实”不等于断言未发表。方法覆盖判断唯一见[近邻核验](../../../history/paused-topics/neighbor-review.md)；问题建议唯一见[问题卡](../../../history/paused-topics/problem-card.md)。

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

InterruptBench commit：`17da111e4858b93c0cab1d88f85e1735fbd1d423`（GitHub commits/main API 核对）。公开任务与代码链接固定到该 commit；局部文件及 SHA256 见[可追溯示例](../../../history/paused-topics/traceable-example.md)。本地第三方代码保存于研究工作树的忽略目录 `artifacts/research-evidence/change-graph-neighbors-2026-10-09/`，仅阅读，不上传、不运行。Eval/LICENSE 为 MIT 许可文本；这不代替网站镜像、数据或全仓逐文件许可复核。

本轮没把 ContinuityBench 的多个同名项目混作一个来源。B1 的代码入口/公开断点包仍是缺口，不能把“论文定义恢复协议”升级为“可直接下载并运行全部断点任务”。

### 下一项来源核验

2026-10-10 阅读补充：沿用 N1 的 Findings of ACL 正式 PDF、N2/N5 的 arXiv v1；重新核对官方入口。N1 扩展到 §4.2 串行层级调用和 §5.2 PDF 覆盖任务及消融；N2 扩展到 §4.4 表4及附录任务/基线协议；N5 扩展到 §4 合成任务构造、§6.2 表3消融和单次运行边界。N2/N5 的正式发表状态仍未核实。本次只核查作者报告，不验证其运行数字，不构成全文代码审计或项目复现。信息选择理由与实验代表性的判断唯一维护于[近邻核验补充](../../../history/paused-topics/neighbor-review.md#2026-10-10保留信息的理由与实验证据)。

进入实验前需要逐项核对拟用近邻的可运行官方代码、固定依赖、状态接口与预算核算。SKILL.state 的正式接收类别、ContinuityBench 的论坛 decision/代码发布、StateMemBench 的数据资产继续待核实。Pi Durable/Cordis/JJ/pi-context 仍是工程来源队列，未据其可用性裁定论文创新。


## 2026-10-12：研究计划候选来源核查

核对日期2026-10-12。以下为规划所需的官方入口核验，未执行复现；采用依据与下一步见[计划执行说明](../../../history/research-plans/research-plan-v0.1-agent-notes.md)。既有论文的前次全文阅读范围不因此扩大。

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

责任：助手。以下按2026-10-13核对；待核实venue不等于断言未发表。所读版本不自动代表正式发表版。未运行任何论文实验。SWE-EVO沿既有登记补查固定README，既有N/B编号保留。检索与选择理由见[证据说明](../../../history/research-plans/research-round-1-evidence.md)，面向人类的取舍见[研究结论](../../../history/research-plans/research-round-1.md)。

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

核对日期均为2026-10-14，责任为助手。本轮提供[元操作候选](../../../history/primitives-and-operations/primitive-candidates-v0.1.md)及[操作语义与阅读范围](../../../history/primitives-and-operations/primitive-candidates-v0.1-agent-notes.md)。没有复现或模型实验；我们的组合建议与来源原有接口分别标明。

| 编号 | 官方来源、作者与身份 | 固定版本或日期 | 阅读范围及设计用途 |
|---|---|---|---|
| P1 | [JJ Glossary](https://github.com/jj-vcs/jj/blob/02afa7cab7ab706ec05fc9e8aab7b4ff9a3cd11a/docs/glossary.md)、[Operation log](https://github.com/jj-vcs/jj/blob/02afa7cab7ab706ec05fc9e8aab7b4ff9a3cd11a/docs/operation-log.md)、[Conflicts](https://github.com/jj-vcs/jj/blob/02afa7cab7ab706ec05fc9e8aab7b4ff9a3cd11a/docs/conflicts.md)；jj-vcs维护者，软件官方文档，非学术发表 | commit `02afa7cab7ab706ec05fc9e8aab7b4ff9a3cd11a` | 身份、rewrite、divergence、view、operation及冲突概念；Change非独立实体；不声称无限保留或语义自动合并 |
| P2 | [Datomic Transaction Model](https://docs.datomic.com/transactions/model.html)、[Transaction Functions](https://docs.datomic.com/transactions/transaction-functions.html)；Cognitect官方软件文档，非论文 | 2026-10-14页面快照及SHA256，非产品版本冻结 | 不可变db value、with/transact、事务完整性、db/cas与纯函数约束；启发候选构造与原子登记，不等于选型 |
| P3 | [PROV-DM: The PROV Data Model](https://www.w3.org/TR/2013/REC-prov-dm-20130430/)；Luc Moreau、Paolo Missier编辑，W3C Recommendation，非会议论文 | 2013-04-30固定推荐标准 | §2、§5.2至§5.4来源、revision、责任、bundle；不把provenance当形式蕴含 |
| P4 | [An assumption-based TMS](https://dekleer.org/Publications/An%20Assumption-Based%20TMS.pdf)；Johan de Kleer；Artificial Intelligence期刊，28(2):127–162 | 1986；作者公开原文；[作者发表目录](https://dekleer.org/bib.htm)与[出版社条目](https://www.sciencedirect.com/science/article/pii/0004370286900809)核实身份 | §1与§4.3至§4.7相关段落，重点§4.6三个基本操作；非全文证明审计。假设环境不同于LLM Context，保证相对于给定依据 |
| P5 | [Event Sourcing Pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing)；Microsoft Azure Architecture Center官方工程文档，非论文 | 2026-10-14页面快照及SHA256 | 追加事件、投影、重放、一致性与事件演化；不是现成的工作语义模型 |

原文保存在忽略目录 `artifacts/research-evidence/task-state-primitives-2026-10-14/`，完整路径语义及manifest见Agent说明，不提交PDF或第三方原文。以上证据支持候选设计来源，不证明我们的组合已经最小、完备或提高任务质量。

## 2026-10-14：审阅后的近邻方法复核

用于[元操作候选 v0.2](../../../history/primitives-and-operations/primitive-candidates-v0.2.md)和[十项机制映射](../../../history/primitives-and-operations/primitive-candidates-v0.2-agent-notes.md)。继承原有作者、来源编号和发表身份登记；本轮没有找到新的正式接收证据，不能据此断言未发表。

| 来源 | 版本、类别与核对日期 | 本轮阅读范围与影响 |
|---|---|---|
| [MAGE](https://arxiv.org/html/2606.06090v1) | 2026 arXiv v1；正式 venue 待核实；2026-10-14 | §3.2–3.3：执行树、摘要、维护及分支修订；已有当前路径及替代分支，不因接口名不同否定选择能力 |
| [StateMem](https://arxiv.org/html/2608.19652v1) | 2026 arXiv v1；正式 venue 待核实；2026-10-14 | §5.1–5.3：来源、依赖、替代及 needs_recheck；适用性维护不是本项目独有机制 |
| [ESAA](https://arxiv.org/html/2602.23193v1) | 2026 arXiv v1；正式 venue 待核实；2026-10-14 | §3 及此前固定仓库提交 22e54a898ee4821a503caf2964e88ab7dee5eac1 的投影规范；已有任务动作、归属约束和投影，不能称为只有 append；仓库规范与论文版本分开 |

没有运行上述实现。映射中的“未核实”是证据边界，不是能力不存在的证明；本项目候选协议也没有实现保证。P 系列固定来源继续作为设计借鉴，不作为新协议正确性证明。

## 2026-10-15：本地分类迁移，不改变来源判断

当前两批共 41 个文件移至主工作区 `artifacts/agent-task-state/`，按原样文件、正文提取、参考提取、仓库快照、发表元数据和获取记录分类。迁移前后保存文件 SHA256 一致，获取清单内容不变；旧位置、现位置与逐文件 hash 查[分类说明](../../../history/reference-retired-2026-11-09/artifact-organization.md)。旧条目中的研究工作树路径保留为采集历史，不再是现存文件地址。2026-10-09 的六个 InterruptBench 快照仍在主工作区 `artifacts/worktrees/change-graph-paper/artifacts/research-evidence/change-graph-neighbors-2026-10-09/`。本轮没有重新核验论文发表状态或新增活动研究结论。

## 2026-10-15：开发活动调查来源

核查日期 2026-10-15。A 系列为本轮新增来源；来源性质与发表身份分开判断。正文存本地忽略批次 activity-research-2026-10-15，实际获取状态、文件哈希和提取路径查获取清单；未声称全文全部推导或代码复现。

| 编号 | 来源及官方证据 | 年份、venue / 类别 | 本轮范围 |
|---|---|---|---|
| A1 | André N. Meyer、Thomas Fritz、Gail C. Murphy、Thomas Zimmermann，[Software Developers’ Perceptions of Productivity](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/meyer-fse-2014.pdf) | 2014，ACM SIGSOFT FSE 主会论文；作者公开稿首页会议与版权信息 | 方法、任务/活动定义、结果与局限；全文已保存，不把感知生产力当任务质量 |
| A2 | Meyer、Earl T. Barr、Christian Bird、Zimmermann，[Today was a Good Day: The Daily Life of Software Developers](https://www.microsoft.com/en-us/research/wp-content/uploads/2019/04/devtime-preprint-TSE19.pdf)，[IEEE 条目](https://ieeexplore.ieee.org/abstract/document/8666786) | IEEE TSE 期刊；所读作者稿注明 2019-03-08 接受，DOI 10.1109/TSE.2019.2904957；正式卷期年本轮主站访问受限，未把接受年冒充卷期年 | 方法、项目阶段与活动感受、局限；全文保存；不能泛化“中断均有害” |
| A3 | Alberto Bacchelli、Christian Bird，[Expectations, Outcomes, and Challenges of Modern Code Review](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/ICSE202013-codereview.pdf)，[作者所在机构条目](https://research.tudelft.nl/en/publications/expectations-outcomes-and-challenges-of-modern-code-review/) | 2013，ICSE 主会论文，712–721，DOI 10.1109/ICSE.2013.6606617 | §III–VII 方法、动机、结果、理解困难及建议；全文保存；旧作者个人站链接 404，未用空页冒充原文 |
| A4 | Jonathan Sillito、Murphy、Kris De Volder，[Questions Programmers Ask During Software Evolution Tasks](https://www.cs.ubc.ca/~murphy/papers/other/asking-answering-fse06.pdf) | 2006，ACM SIGSOFT/FSE 主会论文；公开稿首页会议与版权信息 | §3–7 方法、问题与工具组合、局限；全文保存 |
| A5 | Danilo Silva、Nikolaos Tsantalis、Marco Tulio Valente，[Why We Refactor? Confessions of GitHub Contributors](https://homepages.dcc.ufmg.br/~mtov/pub/2016-fse-why-we-refactor.pdf) | 2016，ACM SIGSOFT FSE 主会论文，公开作者稿首页会议信息；[arXiv 作者稿](https://arxiv.org/abs/1607.02459)不是未发表的证据 | 方法、动机分类、开发者回答和工具限制；全文保存，不仅凭代码变化推断动机 |
| A6 | Chris Parnin、Spencer Rugaber，[Resumption Strategies for Interrupted Programming Tasks](https://chrisparnin.me/pdf/parnin-icpc09.pdf) | 所读为 2009 ICPC 会议版本，DOI 10.1109/ICPC.2009.5090030；IEEE 页面遇验证；不将同名 2011 期刊扩展版与本文件混用 | §3–5 数据、恢复策略、编辑延迟及威胁；全文保存，会议版本身份以文件和 DOI 对应，主会类别本轮未额外核定 |
| A7 | Amy J. Ko、Robert DeLine、Gina Venolia，[Information Needs in Collocated Software Development Teams](https://www.microsoft.com/en-us/research/publication/information-needs-in-collocated-software-development-teams/)，[全文](https://www.microsoft.com/en-us/research/wp-content/uploads/2007/05/icse07_ko.pdf) | 2007，ICSE 主会论文；机构条目及公开稿首页会议 | §3–6 方法、任务结构、信息需求和局限；全文保存 |
| A8 | Parnin、DeLine，[Evaluating Cues for Resuming Interrupted Programming Tasks](https://www.microsoft.com/en-us/research/publication/evaluating-cues-for-resuming-interrupted-programming-tasks/) | 2010，ACM CHI 会议论文；机构官方条目；主会类别本轮未额外核定 | 仅官方摘要/元数据，未全文精读，不迁移其效果到 Agent |
| A9 | [The Work Life of Developers 作者说明](https://andre-meyer.ch/the-work-life-of-developers-activities-switches-and-perceived-productivity/) | 2017 作者研究博客，称已接受 IEEE TSE；本轮没有取得所链全文，正式卷期未核实 | 背景和引用入口；不作本轮全文实证依据 |

| 过程编号 | 官方材料 | 性质、日期与阅读边界 |
|---|---|---|
| C1 Python | [PEP 703](https://peps.python.org/pep-0703/)、[SC 接受说明](https://discuss.python.org/t/pep-703-making-the-global-interpreter-lock-optional-in-cpython-acceptance/37075) | 2023-10-24 有主体的公开决定及之后讨论；PEP 当前页面另存，不能回填当时信息；无学术 venue |
| C2 Kubernetes | [Issue 753](https://github.com/kubernetes/enhancements/issues/753)、[KEP](https://github.com/kubernetes/enhancements/blob/master/keps/sig-node/753-sidecar-containers/README.md)、[v1.28 发布说明](https://kubernetes.io/blog/2023/08/25/native-sidecar-containers/)、[PR 120620](https://github.com/kubernetes/kubernetes/pull/120620) | 官方提案、跟踪、发布与实际审阅；读取当前快照及可见历史，未读取所有折叠内容；PR 本地下载 TLS 失败但网页读取成功，释义胶囊不冒充原文；无学术 venue |
| C3 curl | [CVE-2023-38545](https://curl.se/docs/CVE-2023-38545.html)、[修复提交](https://github.com/curl/curl/commit/fb4415d8aee6c1) | 官方 2023 公告及修复 patch，报告/修复/协调发布，未获得私下讨论；无学术 venue |
| C4 GitLab | [数据库事故复盘](https://about.gitlab.com/blog/postmortem-of-database-outage-of-january-31/) | 2017-02-10 一手事后报告；可分析活动，不能当实时日志或独立事实裁决；无学术 venue |
| C5 SWE-agent 示例 | [官方轨迹文档](https://swe-agent.com/latest/usage/trajectories/)、[原始示例文件](https://github.com/SWE-agent/SWE-agent/blob/main/trajectories/demonstrations/replay__marshmallow-code__marshmallow-1867__default__t-0.20__p-0.95__c-2.00__install-1___install_from_source/marshmallow-code__marshmallow-1867.traj) | 作者发布 v0.7.0 示例/回放，14 步；本地从已保存文档 HTML 提取 JSON，公开 raw 可读但本地直连失败；非本轮运行、非评分结果、无长程压缩证据；文档不附学术 venue |

本轮是时间标记与保存文件 hash 固定的网页快照，动态 URL 不等同于固定 Git 提交。查询、排除和源/提取对应查 activity-source-review.md 所列本地批次；原材料、分析派生与正式结论分别保存。Django、VS Code 仅为保留候选，仓库元数据请求失败，未启用验证。

2026-10-15 G4 初检补充：再次读取 ESAA v1 §3、MAGE v1 §3.2 至 §3.3、StateMem v1 §5 方法以比较六个工作点。来源身份及正式 venue 待核实状态沿用既有登记；本次没有运行它们的代码，不能把论文机制映射当成实际适配证据。

## 2026-10-16 工程来源 DSH-01

DeepSeek Harness 会话演化：开源工程资料，非学术发表；核对日2026-10-16。固定提交、读取范围和角色见[对象报告](../../../experiments/dsh-process/engineering-study-dsh-session.md)。六历史响应、四设计文本、四提交详情已保存。PR #3654 API404。未运行代码或完整核实CI。本批次为机制探索，非独立验证。

## 2026-10-16 工程来源 DSH-02：全项目版本历史

开源工程资料，非论文发表。固定HEAD 86a402200d95fecef4529d969836f1fe13c6cb0d。通过公开GitHub API、Git历史和npm registry核对40个可识别版本、28条Release、29标签、33npm版本；均已保存。详见[版本证据](../../../experiments/dsh-process/dsh-project-history-evidence.md)和[全景研究](../../../experiments/dsh-process/dsh-project-history.md)。40版设计目录的3954份不同内容已保存并按Git对象摘要核对；当前目录有1271项（1270普通文件及1符号链接），1266带日期主题。完整采集不代表全部精读；PR审阅和原工程测试未全量取得/运行。公开事件的确切时间未知，6月Git历史与8月公开入口分别说明。访问失败及角色见批次manifest。


### DSH-02 追加分析范围（2026-10-18）

[dsh-development-analysis.md](../../../experiments/dsh-process/dsh-development-analysis.md)在同一固定86a4022材料上深化跨线分析，并对读五份版本正文、核查主线合入日期。来源仍是公开工程设计记录与Git历史，非论文、无发表venue；未扩展截止日或声称独立运行验证。发现8月25日迁移合入与撤回、9月6日流式阶段合入；撤回原因缺口保留。详细固定链接与内容哈希见分析文末，验证记录见执行账本。


### DSH-02 truth提取（2026-10-19）

[dsh-truth-v0.1.md](../../../experiments/dsh-process/dsh-truth-v0.1.md)为编码前独立过程底稿；[证据表](../../../experiments/dsh-process/dsh-truth-v0.1-evidence.md)逐项列出来源版本、Git对象和局限。沿用原截止86a4022。36个直接来源（23正文、13提交），另保留447版本映射和91份不同正文的索引。来源是公开工程记录，不是论文，无发表venue。未刷新最新、未获取完整审阅、未运行复现；首次迁移撤回原因等缺口继续保留。


### DSH 全量工作关系盘点补充，2026-10-19

来源仍为前述固定 86a4022 历史和本地原始正文。本轮完成 1,358 个文件主题、3,954 个正文 blob、22,346 条完整提交消息及 DAG、2,172 次主线文件变化的机器盘点；当前结构补取 349 份 package.json 和 99 个官方服务登记。官方子系统共 66 个。图中关系核对覆盖 139 个候选位置及补查段落，合并 171 条边，非全量正文精读。研究入口为[dsh-work-history.md](../../../experiments/dsh-process/dsh-work-history.md)，精确范围与缺口见[dsh-project-history-evidence.md](../../../experiments/dsh-process/dsh-project-history-evidence.md#2026-10-19-全量盘点与关系图审计)。公开仓库固定元数据 has_issues=false、has_pull_requests=false；29 条撤回声明引用的目标 SHA 全部在可达历史外。讨论链与撤回目标继续补查。该来源是公开软件工程资料，不涉及论文发表身份。

## 2026-10-20 DSH 候选与差异复核

资料固定 86a4022。当前 1,074 个候选和全历史 4,041 个出现位置已归入审阅；图合并 563 条关系、971 份引文，原始 blob/路径匹配。847 次无 notes 变更保存完整补丁并逐次还原文件树，全部匹配；提交意图、文件清单和实现摘录已检查。29 条撤回含 24 条完整逆变换和 5 条已对读的部分逆变换。证据批次 dsh-exhaustive-2026-10-20，详细协议及阅读限制见[覆盖审计](../../../experiments/dsh-process/dsh-project-history-evidence.md#2026-10-20-引用候选与无笔记变更核对)。

当前继续穷尽正文内部过程；全文精读和完整代码语义审查未完成，公共 PR 和部分理由缺失。元操作编码、原型和模型实验未开始。

## 2026-10-20 全部可达提交补查

固定 86a4022，公开工程记录，无论文 venue。检查扩大至全部可达提交的 notes、早期 ADR/RFC，提取 12,882 不同英文正文、1,535 工作文件名及 4 结构文件；12,908 个提交/路径/blob 组合全部匹配。新增 181 文件名的代表正文、551 新引用语句和 447 演化措辞已读，41 处补读上下文。图更新为 833 联系，文件迁移与演化引用分别标记。完整数量与来源限制见[覆盖审计](../../../experiments/dsh-process/dsh-project-history-evidence.md#2026-10-20-全部可达提交补查)。

主 Agent 随后取消引用关键词筛选，补做所有链接检查：原始新增队列 3,263 句，按链接标题及 RFC/Agent Note 文案归一后，74 句与已读语句对应、6 句仅为语法性指针，其余合为 2,808 组待逐项审阅。该队列尚未完成，尚未进入图。G4 保持返工，元操作、原型和模型实验未开始。


## 2026-10-20 DSH 连续过程比较的来源复用

本轮复用固定 `86a402200d95fecef4529d969836f1fe13c6cb0d` 及其可达历史，沿用第三方仓库材料身份。新增整理范围为Shell执行两代协议、聊天迁移与架构、Windows诊断前后版本、反馈Web入口、共享Office转换、独立引擎与桌面运行时、tool角色协议。逐事实引用见[底稿v1](../../../experiments/dsh-process/dsh-process-truth-v1.md)。

本地比较批次 `artifacts/agent-task-state/maintenance/dsh-composition-2026-10-20/v2/sources.json` 登记49来源对象的固定提交、原路径、author/committer时间与署名；36份正文另核对Git blob，13项提交记录核对commit对象。原始决策主体未具名处保留未知。核对日期2026-10-20；没有新增论文发表状态主张，也未重新在线读取全部URL或运行来源代码。作者测试和性能数据保持报告归属。


## 2026-10-21 Loader定向补读

为区分机械撤回与适配，补读既有S046、S039、S048、S038提交对象及S025固定正文blob（d37539cb3e34c32cd026f330ce92a48baf4bcd0c）。来源仍为固定DSH仓库记录，非新论文或发表状态核验。S046明确机械中间态暴露不兼容，S039保存作者验证范围，S025保存回顾理由与保留范围。对象及指纹位于新批次source-checks.json。该补读不构成运行复验；完整决策者和准确决定时刻未知。第一轮复合断言按最早来源读入可能提前暴露回顾信息，本轮Loader拆分、其余复合记录保守等待全部支持来源，旧产物原样保留。


## 2026-10-23 元操作定向补查

以下为固定DSH提交内的项目作者笔记，非论文，venue不适用。本地Git对象核对日期2026-10-23，来源截止不变；在线可达性未另查。X1已归档，X2包含多时态修订，按陈述范围使用。

- [X1 2026-07-23-session-telemetry-otel-revival.md](https://github.com/deepseek-ai/deepseek-harness/blob/86a402200d95fecef4529d969836f1fe13c6cb0d/.agents/notes/archived/feature/2026-07-23-session-telemetry-otel-revival.md)：用于分轮证据的定向见证；正文保持本地批次，不提交第三方副本。
- [X2 2026-08-10-npm-release-sequences.md](https://github.com/deepseek-ai/deepseek-harness/blob/86a402200d95fecef4529d969836f1fe13c6cb0d/.agents/notes/implemented/process/2026-08-10-npm-release-sequences.md)：用于分轮证据的定向见证；正文保持本地批次，不提交第三方副本。
- [X3 2026-09-16-sidebar-browser.md](https://github.com/deepseek-ai/deepseek-harness/blob/86a402200d95fecef4529d969836f1fe13c6cb0d/.agents/notes/implemented/feature/2026-09-16-sidebar-browser.md)：用于分轮证据的定向见证；正文保持本地批次，不提交第三方副本。
