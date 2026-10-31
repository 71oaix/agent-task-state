---
title: Agent 任务状态管理论文项目
status: active
created: 2026-10-09
updated: 2026-10-31
tags: [research, task-state, entrypoint]
---

# Agent 任务状态管理论文项目

2026-10-31：五类逻辑角色 Goal/Plan/Attempt/Product/Evidence 保留，本轮对象新增 0、合并 0。独立存放便于维护，强内嵌也能保留身份。近期变化集中在计划归属与显式采用、成果 part 与整体分离、依据范围纠正与多假说分别纠正、精确依赖，以及无 changes 视图的版本查询和空成果状态；这些是记录与查询规则，不构成第六类对象。Kimi 冻结 3369 的两项缺陷已修复，本次独立上下文完整测试通过；GLM 第二次读回能恢复计划版本、报告指向与局部动作，依据选择由主调度补正。下一步用真实 Agent 小任务接续，不继续完善固定 T12。详见[T12对象研究](docs/research/change-graph-task-state/t12-object-study.md)与[当前接手入口](docs/research/change-graph-task-state/HANDOFF.md)。

2026-10-30（上一轮）：当前推荐 Goal/Plan/Attempt/Product/Evidence 五类逻辑角色，Change 记录变更；不声称五个顶层表最小或最优。四身份对照修正了“内嵌不能复用”的旧判断；独立 Plan/Product 存放的当前理由是减少宿主版本耦合、维护位置直接。T12 两图说明“调整安排”后的三路状态与对象联系；T03/T13/T15 补足计划阶段、判断修正与准确依赖；15 段的逐条覆盖为静态语义回查，其中这三点另有可执行片段。操作按当前代码入口组织到对象，底层 apply 只做事务。详见[T12对象研究](docs/research/change-graph-task-state/t12-object-study.md)与[组合研究本轮节](docs/research/change-graph-task-state/operation-composition-review.md#2026-10-30五类对象推荐与操作组合)。旧 v0.5 四入口保留为历史记录器，当前对象设计以 T12 研究页为准。

2026-10-29（更早）：[T12首轮对象与责任比较](docs/research/change-graph-task-state/operation-composition-review.md#2026-10-29t12对象方案与可执行比较)已完成，但范围限于三种责任布局和两种Plan存放；五类对象的共同身份边界当时尚未比较。当时保留Goal/Plan/Attempt/Product/Evidence为起点，责任先用父表，计划保留身份与版本；旧结果继续有效，但不再作为五对象边界已成立的证据。已测故障与下一轮单变量协议见`artifacts/agent-task-state/maintenance/t12-continuous-validation-2026-10-29/protocol.md`和`stage-1-review.md`。研究依据与独立读回差异见[组合研究](docs/research/change-graph-task-state/operation-composition-review.md)。

2026-10-28：当前从开发对象及连续变化重新检验工作操作。四模型独立构思与来源裁定已完成，见[综合分析](docs/research/change-graph-task-state/operation-composition-review.md#2026-10-28对象与变化的四模型构思及裁定)。下列工作台继续承担历史查证；四入口定位为记录层接口，局部保留与连续拆分缺口进入下一轮检验。

2026-10-27：已有[可运行工作台](tools/work-operation-checks/README.md)与[工作操作v0.5](docs/research/change-graph-task-state/work-operation-candidates-v0.5.md)。四个基本入口组合出八类工作功能，完整表达既有16段DSH过程，并提供逐步重放、历史查询和来源入口。[先看图与实际效果](docs/research/change-graph-task-state/dsh-work-history.md)。

**Agent 接手只从[当前状态与执行入口](docs/research/change-graph-task-state/HANDOFF.md)开始。**不需要聊天历史。该入口说明目前做到哪一步、下一项工作、验收办法和权限边界。

先读[DSH 工程全景](docs/research/change-graph-task-state/dsh-work-history.md)，了解八个方向及其演化与接续。查证用[过程底稿 v1](docs/research/change-graph-task-state/dsh-process-truth-v1.md)，机制结论见[三种记录方式比较](docs/research/change-graph-task-state/dsh-representation-comparison-v1.md)。全链接逐句清理已停止。

[十段细读案例](docs/research/change-graph-task-state/dsh-truth-v0.1.md)、[深度演化分析](docs/research/change-graph-task-state/dsh-development-analysis.md)和[40 版时间线](docs/research/change-graph-task-state/dsh-project-history.html)保留供深入查阅。

人类审阅读[研究计划 v1.1](docs/research/change-graph-task-state/research-plan-v1.1.md)：先调查真实软件开发活动，再确定持久记录和 Agent 工作，最后检验元操作如何组合。阶段成果与验收方式已列明。

本轮已完成首批来源筛选、[活动地图](docs/research/change-graph-task-state/software-development-activity-map.md)和[记录/Agent 工作映射](docs/research/change-graph-task-state/activity-record-agent-mapping.md)。[元操作推演](docs/research/change-graph-task-state/operation-composition-review.md)现含本轮覆盖与删减依据；当前可执行规则与原型见v0.5，历史推演保留。

- [资料分类与位置](docs/reference/artifact-organization.md)：本地材料按性质保存；原始资料不等于研究结论。
- [来源清单](docs/research/change-graph-task-state/source-inventory.md)：官方出处、版本、发表身份及核验范围。
- [文档索引](docs/INDEX.md)：查前版计划、候选设计和历史讨论。
- [资产登记](docs/reference/project-asset-register.md)：资料职责及状态。
- 用户六论文笔记：本机未跟踪文件，当前检出没有；不是接手前置条件，论文判断以来源清单为准。

2026-10-15 的历史交接曾从独立研究分支固定提交 `404a4ab` 接入本工作区的交接修订分支，原分支保留。本轮活动执行位于主工作区 artifacts/worktrees/task-state-activities/ 的 codex/task-state-activity-research，因共享工作区被另一任务切换，当前成果以此独立检出为准；不能混用不同工作树进度。另一项目[工具反馈管理](../工具反馈管理/README.md)的模型、任务、预算与工程批准不继承。
