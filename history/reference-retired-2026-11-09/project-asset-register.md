
# Agent任务状态管理项目资产索引

本表只登记资产在哪里、来源和边界。现行设计从项目 [README](../../README.md) 进入。表下按日期留下的句子是当时的记录，不从这里产生下一步。2026-10-16 曾把实验 benchmark 锚在 SWE-Milestone，并暂停其他 benchmark 选型。2026-10-10 起，预算视图问题卡不再作为优先推荐。

| 资产 | 来源与版本 | 责任与边界 |
| --- | --- | --- |
| [T12五类对象推荐](../../experiments/t12-objects/t12-object-study.md)、[离线检验](../../tools/work-operation-checks/README.md) | 2026-10-31（currentrecommendation），2026-11-01 研究完成；identity-v2四身份对照、coverage-v2 15段静态回查、boundary-v2 T03/T13/T15边界、handoff-v2接续包、final-review-v1最终审查；T12六事实及同源补充；原底稿未改 | 五类逻辑角色与Change；独立存放是维护选择；最终审查修复两项Kimi缺陷，GLM第二次读回依据由主调度补正；详情在[组合研究最终审查节](../../experiments/operation-composition/operation-composition-review.md#最终审查与第二次接手读回2026-10-31) |
| [T12阶段成果本地存档入口](../../../artifacts/agent-task-state/archives/t12-object-stage-2026-11-01) | 2026-11-01；基线 `853d073`；`archive.py` 以本工作树根为输入，打包本项目自有文档/代码/图片与两批T12证据 | 只读打包，不删除、不覆盖、不读其他项目；排除 `__pycache__`、`.git`、第三方副本、PDF与重解析点；主调度已实际执行归档，该目录 `manifest.json` 与 `verification.json` 记录 200 文件 / 21782407 原始字节、ZIP 3712600 字节，SHA 与 CRC 全过；8 处缺失为 S022/S028/S029 第三方原文自身相对链接，不改冻结原文 |
| [final-review-v1 回执与验证](../../../artifacts/agent-task-state/maintenance/t12-continuous-validation-2026-10-29/final-review-v1/adjudication.md) | 2026-10-31；Kimi `9d11c98e` 冻结3369静态审查、GLM固定包与主调度纠正依据；[results.json](../../../artifacts/agent-task-state/maintenance/t12-continuous-validation-2026-10-29/final-review-v1/results.json)、[verification.md](../../../artifacts/agent-task-state/maintenance/t12-continuous-validation-2026-10-29/final-review-v1/verification.md) | 两项缺陷修正前后回执、180项新上下文回归、GLM语义裁定；验证不冒充Kimi修后复审，读回不写成GLM自主完全通过 |
| [四模型对象研究交接](../../history/object-operation-handoff-2026-10-28.md)、[综合裁定](../../experiments/operation-composition/operation-composition-review.md#2026-10-28对象与变化的四模型构思及裁定) | 2026-10-28；四模型固定e15f6f4、effort=max；均completed | 独立构思与主Agent裁定分开，三布局尚未运行比较；原答位于本工作树artifacts/agent-task-state/maintenance/object-review-2026-10-28/ |
| [工作操作工作台](../../tools/work-operation-checks/README.md) | 2026-10-27；原检查器与新增组合执行/历史查询/阅读器 | 16段、83来源事实与16研究缺口；模型原稿和Sol裁定分开；独立读回有明确输入范围 |
| [工作操作v0.5](../../experiments/operation-composition/work-operation-candidates-v0.5.md) | 2026-10-27；历史记录器接口；四入口与八类可执行组合 | 不再作为当前对象设计；旧实现与组合规则保留 |
| [工作操作v0.4](../../history/work-operation-candidates-v0.4.md) | 2026-10-25；历史筛选，由v0.5接替 | 四入口及两入口强对照的依据保留 |
| [元操作筛选](../../experiments/operation-composition/operation-selection-review.md) | 2026-10-25；逐步更新比较；新批次 dsh-operation-selection-2026-10-25 | 记录检查器与四组校准完成；跨过程独立/主 Agent 范围分开 |
| [工作操作 v0.3](../../history/work-operation-candidates-v0.3.md) | 2026-10-25；前轮工作接口清单；由 v0.4 接替 | 7 语义入口 / 11 组合 / 12 待补证；统一底座为原型建议 |
| [工作转换检验](../../experiments/operation-composition/transition-rule-review.md) | 2026-10-25；固定来源的逐步转换、规则与期待探针 | 主 Agent 离线走查；Qoder 已移除；独立检验已由新轮次接续；本批次 artifacts/agent-task-state/maintenance/dsh-transitions-2026-10-25/ |
| [DSH 工程全景](../../experiments/dsh-process/dsh-work-history.md)、[过程底稿 v1](../../experiments/dsh-process/dsh-process-truth-v1.md)、[机制比较](../../experiments/dsh-process/dsh-representation-comparison-v1.md) | 2026-10-20；固定86a4022；16过程/83事实/49来源对象 | 主Agent同作者离线表达、读回与删减；非独立盲测、数据库实现或长程任务效果 |
| [DSH truth v0.1](../../experiments/dsh-process/dsh-truth-v0.1.md)、[证据](../../experiments/dsh-process/dsh-truth-v0.1-evidence.md) | 2026-10-19；十过程/54事实/36来源；固定86a4022；阅读版与详细对照分工 | 编码前独立底稿；公开证据边界，非全项目完整事件流或独立复现 |
| [DSH深度演化分析](../../experiments/dsh-process/dsh-development-analysis.md) | 2026-10-18；沿用固定86a4022与五份历史正文 | 跨线解释、反例与承诺变化；非运行验证；首次迁移撤回原因未知 |
| [DSH全项目研究与图](../../experiments/dsh-process/dsh-project-history.md)、[版本证据](../../experiments/dsh-process/dsh-project-history-evidence.md) | 2026-10-16；固定86a4022；40版本/3954设计目录内容版本 | 用户要求先全景后分析；第三方材料本地忽略，未运行工程或付费实验 |
| [DSH 工程对象](../../experiments/dsh-process/engineering-study-dsh-session.md) | 2026-10-16；设计固定5e9f134 | 机制探索；PR访问缺口，未运行测试 |
| [活动来源筛选](../../experiments/activity-survey/activity-source-review.md)、[执行账本](../../history/research-execution-ledger.md) | 2026-10-15，交接基线31b6938；七份实证全文、四项目过程、一个官方Agent示例 | G1首批探索准入；非检索饱和、行业频率或长程效果证据；本地获取/分析批次保持忽略 |
| [活动地图](../../experiments/activity-survey/software-development-activity-map.md)、[记录映射](../../experiments/activity-survey/activity-record-agent-mapping.md) | G2提交f92101c，G3提交aaef635；27证据解释单元、12活动类、6工作点 | G2探索版、G3同一作者表示走查通过；强文档同样可支持问题；没有计时或独立模型试验 |
| [元操作首轮检查](../../experiments/operation-composition/operation-composition-review.md) | 同一六工作点，复核固定v1近邻方法；2026-10-15 | G4返工：事实/实际产物/采用及许可、验证、义务尚需统一协议；未实现或验证优越性 |
| [Agent 接手入口](../../history/handoff-2026-11-01.md) | 2026-11-06 起指向本项目目录；其中 2026-11-01 记录 T12 成果保存于 `853d073` | 阶段记录。项目目的和成果位置以项目 README 为准 |
| [研究计划 v1.1](../../history/research-plan-v1.1.md)、[执行说明](../../history/research-plan-v1.1-agent-notes.md) | 2026-10-15 用户纠正活动来源及整体流程 | 活动调查阶段的计划。其后已有活动地图、记录映射和操作检查；不批准付费实验 |
| [本地资料分类](artifact-organization.md) | 2026-10-15 实际盘点及 41 文件迁移哈希校验 | 主工作区 artifacts/agent-task-state 为当前资料根；其他项目与历史工作树原位分类；两个旧审计目录权限受限 |
| [元操作候选 v0.2](../../history/primitive-candidates-v0.2.md)、[协议与证据](../../history/primitive-candidates-v0.2-agent-notes.md) | 2026-10-14 用户审阅；继承 P 系列来源，复核 MAGE/StateMem/ESAA 方法及固定投影规范 | 当时的候选：明确身份、关系生命周期、整合及并发边界；十项近邻映射为原文分析，非真实轨迹重放或运行验证 |
| [元操作候选v0.1](../../history/primitive-candidates-v0.1.md)及[语义/证据](../../history/primitive-candidates-v0.1-agent-notes.md) | 2026-10-14，JJ固定提交、Datomic/PROV官方文档、ATMS原文相关章节、事件溯源 | 三类语义动作与事务统一接口候选；用户场景纸面推演，未实现或实验证明；原文现按性质存于主工作区 artifacts/agent-task-state/，原批次和迁移映射见分类入口 |
| [第一轮研究结论](../../history/research-round-1.md)及[证据说明](../../history/research-round-1-evidence.md) | 2026-10-13，v1.0执行首轮；官方条目、所读正文版本及固定仓库静态协议 | 助手核查；非完整综述、运行复现或效果实验。原文/静态资产现按性质存于主工作区 artifacts/agent-task-state/，获取批次保留 |
| [研究计划 v1.0](../../history/research-plan-v1.0.md)及[执行说明](../../history/research-plan-v1.0-agent-notes.md) | 2026-10-13用户确认定稿与准备执行；吸收三项批注及五项反思 | 前版研究执行基线，2026-10-15 由 v1.1 接替；第一轮结论已形成，非实现或付费实验授权 |
| [研究计划 v0.2](../../history/research-plan-v0.2.md)及[执行说明](../../history/research-plan-v0.2-agent-notes.md) | 2026-10-12用户三项批注；保留v0.1 | 相关广搜后归纳精读；优先软件开发；先明确语义模型再接入LLM。均为研究计划，未验证效果 |
| [研究计划 v0.1](../../history/research-plan-v0.1.md)及[执行说明](../../history/research-plan-v0.1-agent-notes.md) | 2026-10-12用户要求制定经验吸收、实验与收敛路线；官方入口核查见来源清单 | 研究提案，未运行实验；三组件和对象划分仍待验证 |
| [当前架构 v0.4](../research/change-graph-task-state/design-v0.4.md)及[查证约束](../research/change-graph-task-state/design-v0.4-agent-notes.md) | 2026-10-12用户确认简明历史图、证据核查、决策主体与执行清单入口 | 设计要求；尚无可操作图、数据接口或SDD执行器 |
| [架构审阅稿 v0.3](../../history/design-v0.3.md)及[Agent 接手说明](../../history/design-v0.3-agent-notes.md) | 2026-10-11用户要求按读者拆分，助手重构 v0.2 表达 | 同一架构的两类阅读入口；设计草案，非新增效果证据或实现批准 |
| [前版 v0.2](../../history/design-v0.2.md)及[对话吸取记录](../../history/database-resilience-discussion.md) | 2026-10-10指定对话接口返回五轮；用户复制全文七轮，后续分段读完并纠正遗漏，校验值见吸取记录 | 历史设计与来源记录，内容保留；非原文论文核验或效果证据 |
| [设计前版 v0.1](../../history/design-v0.1.md) | 2026-10-10用户要求初步设计；本地提交 b12d0f2 | 内容不覆盖，作为逐版讨论基线保留 |
| [研究项目与五份研究文档](../../history/research-directory-readme.md) | 原工作树固定提交 `0672238b3f96e01443997f9125d58249bcac29e5`，2026-10-09 纳入本目录；官方外部证据见[来源清单](../research/change-graph-task-state/source-inventory.md) | 助手维护，用户决定研究投入；近邻核验及手工实例，不是运行结果 |
| [阶段性总结与设计假设](../research/change-graph-task-state/design-hypothesis.md) | 原主工作区 `81ba115` 中已有文档，用户讨论总结，2026-10-09 | 现行设计假设。问题卡是当时的记录，在 history/ |
| 用户六论文总结（本机未跟踪；当前检出没有） | 分区前未跟踪的用户笔记，2026-10-09 原文迁移，内容不改；保持本地未跟踪，不随本次提交 | 用户已有比较笔记，未在本次重新核验论文事实 |
| 现行研究文档与离线检查器 | 2026-11-06 统一到本项目目录，来源为 `codex/task-state-activity-research` 的 `c26edbc`（2026-11-01） | 旧检出 `artifacts/worktrees/task-state-activities/` 保留供追溯，现行入口见[项目 README](../../README.md) |
| 原研究工作树 | 仓库根目录 `artifacts/worktrees/change-graph-paper/`，分支 `codex/change-graph-paper-init` | 历史开发位置，保持原路径及内容，不提交整个工作树 |

两个项目共用 Git 仓库、[共享资料中的通用指南](../../../共享资料/README.md)与原位置的 `artifacts/`。共享指南于2026-10-09从根目录原文迁入 `共享资料/`；该目录清单维护其来源、版本和使用边界。目录与来源身份已分开，研究模型、任务、评分方案、预算与样本数量仍须分别界定。技能操作留痕采用本项目文档、Git 和仓库忽略的 `.run-log.jsonl`；不写工作区外的全局技能日志。


## 2026-10-19 DSH 全量工作历史资料

- 当时的人类入口：[工作历史地图与全量盘点](../../experiments/dsh-process/dsh-work-history.md)；交互检索：[工作关系图](../../experiments/dsh-process/dsh-work-history.html)。图内保存可独立读取的主题、关系证据和提交检索元数据。
- 原始盘点位于主工作区 `artifacts/agent-task-state/repository-snapshots/dsh-exhaustive-2026-10-19/`；自有研究脚本位于 `artifacts/agent-task-state/maintenance/dsh-exhaustive-2026-10-19/`，不上传原始资料和运行产物。
- 责任状态：主 Agent 完成全量机器盘点与首批关系核对；截至 2026-10-19，全量正文审阅仍在进行。固定来源 86a4022，核对日期 2026-10-19。精确数量、范围与当时的后续核验 见[覆盖审计](../../experiments/dsh-process/dsh-project-history-evidence.md#2026-10-19-全量盘点与关系图审计)。

## 2026-10-20 DSH 引用与代码差异批次

主工作区 `artifacts/agent-task-state/repository-snapshots/dsh-exhaustive-2026-10-20/` 保存逐断言审阅、847 份完整补丁及文件树还原、部分撤回比较和新版图数据；自有脚本位于 `artifacts/agent-task-state/maintenance/dsh-exhaustive-2026-10-20/`。前批次保留。当时的人类入口为[工作地图](../../experiments/dsh-process/dsh-work-history.md)。当日的责任状态留在已结束的[交接日志](../../history/handoff-2026-11-01.md)。验证程度见[覆盖审计](../../experiments/dsh-process/dsh-project-history-evidence.md#2026-10-20-引用候选与无笔记变更核对)。

2026-10-20 扩围：同批次补入全部可达分支的 8,928 额外正文，保留完整英文文件事件、来源校验、181 文件名代表正文审阅、551 引用与 447 过程措辞审阅、45 文件名迁移对。地图 833 联系。责任为主 Agent；取消关键词后的引用已逐组读 1,248 组，与旧措辞复用去重覆盖 1,500 / 2,808 组。本批 1,399 原句和 3,985 来源位置校验通过。用户已叫停队列穷举，剩余材料按需查证；当日转入工程过程全景整理，验收与接手顺序写在后来结束的交接日志里。新解释尚未加入图，全文与代码语义审查未完成。


## 2026-10-20 纠偏计划离线闭环

本轮完成八方向工程全景、16段过程底稿、普通文档/语义显式/事务统一三份表示、静态读回和九项接口改写／删减检查。全部原始资料保持原位；新分析批次位于主工作区 `artifacts/agent-task-state/maintenance/dsh-composition-2026-10-20/v2/`，父目录保留初稿。底稿哈希、49来源元数据与36份正文对象、三份表示和未测量项见 manifest/metrics/verification。49来源中13个为提交记录，36个为正文版本。

共同自然语言负载由主Agent整理，读回器检查99条记录（83条来源事实与16条研究者缺口）的断言及其归属和来源、16条跨记录关联、27项政策投影的一致性。此结果不是独立语义正确率。G4仍需收敛工作身份、关系修订与选择范围；G5/G6/G7未启动。未运行上游、数据库或付费模型实验。


2026-10-20 阅读修订：工程全景的方向关系图改为[三条路径图](../../experiments/dsh-process/figures/dsh-evolution-paths.svg)，PNG用于正文，SVG为可编辑图源。该图是基于底稿的讲解图，箭头分别表示影响、保留／复用和机制共享，不扩展来源事实。浏览器渲染与几何检查保存在主工作区 `artifacts/agent-task-state/maintenance/dsh-doc-readability-2026-10-20/`。

2026-10-21：新增[八方向总图 SVG](../../experiments/dsh-process/figures/dsh-direction-overview.svg)及[显示版 PNG](../../experiments/dsh-process/figures/dsh-direction-overview.png)，来源为既有过程底稿与深度分析中的跨线连接；图按阅读分组，不表示版本顺序。三路径图的共享关系修正为分支汇聚。主文逐项提供证据入口，阅读效果待用户反馈。


2026-10-21：本轮[候选v0.3](../../history/primitive-candidates-v0.3.md)和[组合审查](../../experiments/operation-composition/operation-composition-review.md)负责定义及依据；[组合图源](../../experiments/dsh-process/figures/dsh-operation-composition.svg)及[PNG](../../experiments/dsh-process/figures/dsh-operation-composition.png)说明Loader局部撤回。新批次为artifacts/agent-task-state/maintenance/dsh-semantics-2026-10-21/v1/，保留三表示、原始对象补读、80项人工答案、时序与删减检查和manifest。83来源事实+16研究缺口保持原底稿；额外10条Loader细分不冒充新增独立任务。下一gate为离线检查器规格与授权；独立收益、并发及原型未完成。


2026-10-21 工作语言研究：当时的定义与取舍见[首轮推演](../../experiments/operation-composition/work-operation-study-v0.1.md)，[组合图](../../experiments/dsh-process/figures/dsh-work-operations.svg)解释 T12 拆分与目标接续。主 Agent 负责复核。三项 Qoder 的提示、完整结果与运行状态在主仓库 artifacts/agent-task-state/maintenance/dsh-work-operations-2026-10-21/，不上传。v0.3 转为记录层依据，当时安排先补 split/integrate/fork 转换契约及见证，暂缓原型。


2026-10-22：[候选覆盖与四份对照](../../experiments/operation-composition/work-operation-coverage-v0.1.md)负责本轮16段的变化编码、候选池及取舍。主 Agent 负责裁定，Qoder三路只读独立提交；83事实、68步、32同作者读回及结构/语义边界详见正文。原始输出、冻结初稿和裁定保存在主仓库 artifacts/agent-task-state/maintenance/dsh-operation-coverage-2026-10-22/，不上传。下一gate为候选规则组合/归约及未见证项定向取证，原型继续暂缓。


2026-10-22 阅读修订：[覆盖报告](../../experiments/operation-composition/work-operation-coverage-v0.1.md)改为简短审阅稿，说明结论及下一步比较；原16段推演、30候选与四份裁定转到[查证明细](../../experiments/operation-composition/work-operation-coverage-v0.1-evidence.md)，保留锚点和研究依据。原始分析批次不改，阅读修订检查存于主仓库 artifacts/agent-task-state/maintenance/dsh-coverage-reading-fix-2026-10-22/。

2026-10-22：[修订组合实验](../../experiments/operation-composition/revision-composition-experiment-v0.1.md)与[明细](../../experiments/operation-composition/revision-composition-experiment-v0.1-evidence.md)保存本轮收敛依据。12 个条款变化为研究编码，10 段来源、3 条补充过程；Qoder 三路有效结果与两轮失败均留在主仓库 artifacts/agent-task-state/maintenance/dsh-revision-experiment-2026-10-22/，保持忽略。责任人为主 Agent；当时拟继续归约修订规则及观察/判断/验证/采用，不据此批准数据库或付费实验。

2026-10-23：[修订判断](../../experiments/operation-composition/revision-composition-experiment-v0.1.md)已更新为全部16段的检验结论；[本轮明细](../../experiments/operation-composition/full-process-revision-check-v0.1-evidence.md)维护逐段裁定、80问评分和额外约定。冻结批次 artifacts/agent-task-state/maintenance/dsh-full-process-check-2026-10-22/ 保留原表示、失败及修正版，原始输出不上传。主Agent负责来源核对与评分；下一gate为对象/尝试身份、责任、上下文规则，不能把38个候选revise注释当实际执行。


2026-10-23 分轮收敛：[人类判断](../../experiments/operation-composition/work-operation-rounds-v0.1.md)、[工作候选 v0.2](../../history/work-operation-candidates-v0.2.md)、[裁定明细](../../experiments/operation-composition/work-operation-rounds-v0.1-evidence.md)。主Agent负责来源核验与评分；18项Qoder输出、冻结输入和裁定保留在主仓库 artifacts/agent-task-state/maintenance/dsh-primitives-2026-10-23/，原始资料不提交。新增组合图SVG/PNG解释T14/T12/T13。下一gate为T14完整转换规约，原型暂缓到可执行映射明确；前轮底稿和比较保持。


## 2026-11-01 T12 阶段成果本地存档

本轮 T12 研究完成，现行九份相关文档同步为研究已完成；HANDOFF 旧的“待主调度本地提交”状态改为成果已保存 `853d073`，本次存档同步的最终提交仍以 Git 记录为准。本地存档入口为 `artifacts/agent-task-state/archives/t12-object-stage-2026-11-01/`，主调度已实际执行归档并逐文件校验：200 文件 / 21782407 原始字节，ZIP 3712600 字节，SHA 与 CRC 全过；8 处缺失为 S022/S028/S029 第三方原文自身相对链接，不改冻结原文，详见该目录 `verification.json`。打包范围限于本项目自有文档、代码、图片，以及 `artifacts/agent-task-state/maintenance/t12-object-study-2026-10-29` 与 `t12-continuous-validation-2026-10-29` 两批证据；范围外历史资料保持原位，只保留原引用，不计入本包。打包清单、逐文件字节与 SHA256、ZIP 读回校验、文档本地链接核对结果，均以该目录 `manifest.json` 与 `verification.json` 为准。该 snapshot 保存执行归档时的源文件；本次最终状态同步由随后的本地 Git 提交及 `research.bundle` 保存，两者互补，快照不包含之后的修改。bundle 实际路径为归档目录内 `artifacts/agent-task-state/archives/t12-object-stage-2026-11-01/research.bundle`，存在情况以文件核验。
