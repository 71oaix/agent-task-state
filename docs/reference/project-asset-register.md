---
title: Agent任务状态管理项目资产索引
status: active
created: 2026-10-09
updated: 2026-10-16
tags: [asset-register, task-state, preservation]
supersedes:
---

# Agent任务状态管理项目资产索引

2026-10-16 当前决定：实验 benchmark 锚定 SWE-Milestone，其他 benchmark 选型暂停；研究继续 G4 基本机制比较。实时记录与历史重构共用核心操作，重构为外围能力。下表历史阶段口径以 [HANDOFF](../research/change-graph-task-state/HANDOFF.md) 当前状态为准。

2026-10-10 研究口径更新：预算视图问题卡暂停优先推荐，保留历史候选；近邻核验补充了信息选择理由、消融与实验代表性，来源清单记录新增阅读范围。下一步为继续审查论文依据与工作生命周期覆盖，不以简单销量任务筛选掉复杂开发问题。下表原始来源与历史工作树身份保持不变。

| 资产 | 来源与版本 | 责任与边界 | 下一步 |
|---|---|---|---|
| [DSH全项目研究与图](../research/change-graph-task-state/dsh-project-history.md)、[版本证据](../research/change-graph-task-state/dsh-project-history-evidence.md) | 2026-10-16；固定86a4022；40版本/3954设计目录内容版本 | 用户要求先全景后分析；第三方材料本地忽略，未运行工程或付费实验 | 跨八主线核对连续变化，再比较基本机制 |
| [DSH 工程对象](../research/change-graph-task-state/engineering-study-dsh-session.md) | 2026-10-16；设计固定5e9f134 | 机制探索；PR访问缺口，未运行测试 | 连续编码锁替换、迁移、新约束 |
| [活动来源筛选](../research/change-graph-task-state/activity-source-review.md)、[执行账本](../research/change-graph-task-state/research-execution-ledger.md) | 2026-10-15，交接基线31b6938；七份实证全文、四项目过程、一个官方Agent示例 | G1首批探索准入；非检索饱和、行业频率或长程效果证据；本地获取/分析批次保持忽略 | 按缺口扩展来源，保留候选项目还需确认可用性 |
| [活动地图](../research/change-graph-task-state/software-development-activity-map.md)、[记录映射](../research/change-graph-task-state/activity-record-agent-mapping.md) | G2提交f92101c，G3提交aaef635；27证据解释单元、12活动类、6工作点 | G2探索版、G3同一作者表示走查通过；强文档同样可支持问题；没有计时或独立模型试验 | 不用当前分类作为最终最小模型，继续组合检验 |
| [元操作首轮检查](../research/change-graph-task-state/operation-composition-review.md) | 同一六工作点，复核固定v1近邻方法；2026-10-15 | G4返工：事实/实际产物/采用及许可、验证、义务尚需统一协议；未实现或验证优越性 | 比较两种完整编码并重验反例；G5规则未冻结 |
| [Agent 接手入口](../research/change-graph-task-state/HANDOFF.md) | 2026-10-15；研究文档从 404a4ab 固定版本接入主工作区交接分支 | 当前阶段、下一动作及七关验收入口；G1 尚未开始，交接文档检查不等于研究通过 | 按 G1 实际执行，逐关追加证据及更新状态 |
| [研究计划 v1.1](../research/change-graph-task-state/research-plan-v1.1.md)、[执行说明](../research/change-graph-task-state/research-plan-v1.1-agent-notes.md) | 2026-10-15 用户纠正活动来源及整体流程 | 当前计划：活动归纳、记录投影、Agent 工作、元操作检验；未完成新调研或批准原型和付费实验 | 先广搜并归纳真实开发活动，再形成记录映射 |
| [本地资料分类](artifact-organization.md) | 2026-10-15 实际盘点及 41 文件迁移哈希校验 | 主工作区 artifacts/agent-task-state 为当前资料根；其他项目与历史工作树原位分类；两个旧审计目录权限受限 | 新资料按项目、性质、批次保存；保持来源和分析分离 |
| [元操作候选 v0.2](../research/change-graph-task-state/primitive-candidates-v0.2.md)、[协议与证据](../research/change-graph-task-state/primitive-candidates-v0.2-agent-notes.md) | 2026-10-14 用户审阅；继承 P 系列来源，复核 MAGE/StateMem/ESAA 方法及固定投影规范 | 当前候选：明确身份、关系生命周期、整合及并发边界；十项近邻映射为原文分析，非真实轨迹重放或运行验证 | 取得真实开发修订与决策记录，检查组合规则；尚未证明最小性或优越性 |
| [元操作候选v0.1](../research/change-graph-task-state/primitive-candidates-v0.1.md)及[语义/证据](../research/change-graph-task-state/primitive-candidates-v0.1-agent-notes.md) | 2026-10-14，JJ固定提交、Datomic/PROV官方文档、ATMS原文相关章节、事件溯源 | 三类语义动作与事务统一接口候选；用户场景纸面推演，未实现或实验证明；原文现按性质存于主工作区 artifacts/agent-task-state/，原批次和迁移映射见分类入口 | 检验接口等价、工作身份、部分整合和关系修订；寻找不能表达的复杂工作变化 |
| [第一轮研究结论](../research/change-graph-task-state/research-round-1.md)及[证据说明](../research/change-graph-task-state/research-round-1-evidence.md) | 2026-10-13，v1.0执行首轮；官方条目、所读正文版本及固定仓库静态协议 | 助手核查；非完整综述、运行复现或效果实验。原文/静态资产现按性质存于主工作区 artifacts/agent-task-state/，获取批次保留 | 局部收窄与对应对照顺序已撤回；保留文献事实，转为基本操作及组合语义的设计依据 |
| [研究计划 v1.0](../research/change-graph-task-state/research-plan-v1.0.md)及[执行说明](../research/change-graph-task-state/research-plan-v1.0-agent-notes.md) | 2026-10-13用户确认定稿与准备执行；吸收三项批注及五项反思 | 前版研究执行基线，当前顺序由 v1.1 替代；第一轮结论已形成，非实现或付费实验授权 | 按主计划2026-10-13主线修正比较基本对象、操作及组合能力 |
| [研究计划 v0.2](../research/change-graph-task-state/research-plan-v0.2.md)及[执行说明](../research/change-graph-task-state/research-plan-v0.2-agent-notes.md) | 2026-10-12用户三项批注；保留v0.1 | 相关广搜后归纳精读；优先软件开发；先明确语义模型再接入LLM。均为研究计划，未验证效果 | 形成研究地图、精读依据及语义模型草案 |
| [研究计划 v0.1](../research/change-graph-task-state/research-plan-v0.1.md)及[执行说明](../research/change-graph-task-state/research-plan-v0.1-agent-notes.md) | 2026-10-12用户要求制定经验吸收、实验与收敛路线；官方入口核查见来源清单 | 研究提案，未运行实验；三组件和对象划分仍待验证 | 先完成机制比较、真实任务适配审查和数据模型操作检验 |
| [当前架构 v0.4](../research/change-graph-task-state/design-v0.4.md)及[查证约束](../research/change-graph-task-state/design-v0.4-agent-notes.md) | 2026-10-12用户确认简明历史图、证据核查、决策主体与执行清单入口 | 设计要求；尚无可操作图、数据接口或SDD执行器 | 检验图与详情同版本、证据与主体可追踪、清单可检查 |
| [当前架构审阅稿 v0.3](../research/change-graph-task-state/design-v0.3.md)及[Agent 接手说明](../research/change-graph-task-state/design-v0.3-agent-notes.md) | 2026-10-11用户要求按读者拆分，助手重构 v0.2 表达 | 同一架构的两类阅读入口；设计草案，非新增效果证据或实现批准 | 用户审阅架构，Agent按接手说明完成来源核验与下一轮迭代 |
| [前版 v0.2](../research/change-graph-task-state/design-v0.2.md)及[对话吸取记录](../research/change-graph-task-state/database-resilience-discussion.md) | 2026-10-10指定对话接口返回五轮；用户复制全文七轮，后续分段读完并纠正遗漏，校验值见吸取记录 | 历史设计与来源记录，内容保留；非原文论文核验或效果证据 | 与 v0.3 对照，按需追溯设计推理 |
| [设计前版 v0.1](../research/change-graph-task-state/design-v0.1.md) | 2026-10-10用户要求初步设计；本地提交 b12d0f2 | 内容不覆盖，作为逐版讨论基线保留 | 对照 v0.2 修改理由 |
| [研究项目与五份研究文档](../research/change-graph-task-state/README.md) | 原工作树固定提交 `0672238b3f96e01443997f9125d58249bcac29e5`，2026-10-09 纳入本目录；官方外部证据见[来源清单](../research/change-graph-task-state/source-inventory.md) | 助手维护，用户决定研究投入；近邻核验及手工实例，不是运行结果 | 寻找能区分简单状态表与候选视图的真实前缀 |
| [阶段性总结与设计假设](../research/change-graph-task-state-design-hypothesis.md) | 原主工作区 `81ba115` 中已有文档，用户讨论总结，2026-10-09 | 设计假设；初始化后的判断以研究入口和问题卡为准 | 随问题分析核验 |
| [六论文总结](../../六论文总结.md) | 分区前未跟踪的用户笔记，2026-10-09 原文迁移，内容不改；保持本地未跟踪，不随本次提交 | 用户已有比较笔记，未在本次重新核验论文事实 | 引用结论前对照来源清单 |
| [文档索引](../INDEX.md) | 本项目当前 Markdown 清单 | 只维护目录与生命周期，不批准研究或执行 | 新增或修订文档后更新 |
| 原研究工作树 | 仓库根目录 `artifacts/worktrees/change-graph-paper/`，分支 `codex/change-graph-paper-init` | 历史开发位置，保持原路径及内容，不提交整个工作树 | 后续维护优先进入本项目目录 |

两个项目共用 Git 仓库、[共享资料中的通用指南](../../../共享资料/README.md)与原位置的 `artifacts/`。共享指南于2026-10-09从根目录原文迁入 `共享资料/`；该目录清单维护其来源、版本和使用边界。目录与来源身份已分开，研究模型、任务、评分方案、预算与样本数量仍须分别界定。技能操作留痕采用本项目文档、Git 和仓库忽略的 `.run-log.jsonl`；不写工作区外的全局技能日志。
