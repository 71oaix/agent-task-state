# Agent 任务状态管理论文项目

本项目处于问题发现阶段。已有工作大多把 Agent 的状态和工作轨迹保存下来；本项目要在其上建立一个更小的抽象语义层，用少量维护对象记录会分叉、回退、改版的软件开发历史，再从同一套记录生长出 Human view 与 Agent view。贡献不落在「任务状态离开模型上下文」，而落在这层语义比轨迹或普通文档多出的可检验约束。

现行意图见 [Intention Brief](docs/intention/intention.md)；已有记录的整理见 [recorded-work-review.md](docs/intention/recorded-work-review.md)；规格入口见 [Specification](docs/specification/specification.md)；实现入口见 [Implementation](docs/implementation/implementation.md)。[架构 v0.4](docs/specification/change-graph-task-state/design-v0.4.md) 仍是双视图的架构底稿，文内标明系统尚未实现。

[现行对象方案](docs/specification/change-graph-task-state/design-hypothesis.md#记录方案与验证边界)区分目标、计划、尝试、成果和依据，用 Change 保存每次变化。这个划分来自 T12 对象研究，五类是否最小仍开放。工作操作 v0.5 保存的是早期记录器接口，供追溯操作组合的演进。

[离线检查器](tools/work-operation-checks/README.md)已支持版本查询、部分更新规则检查和实验性接手数据导出。[DSH 历史地图](experiments/dsh-process/dsh-work-history.html)展示固定案例，两种视图尚未接到同一套日常使用入口。文档记载了 2026-11-01 针对 T12 记录机制的 180 项回归，本次未重跑，且对应归档目录在当前工作区尚未找到，不能当作已复核的实验数字。**真实 Agent 小任务的接续仍待验证**，重点是从快照恢复工作并登记新进展时，该语义层能否比普通文档或原始轨迹更好地沿用计划版本，并保留旧成果、报告和验收依据。详见[归档交接](history/handoffs/handoff-2026-11-01.md#2026-11-01-研究记录t12-对象比较已保存)。

## 研究证据与资料

Django 和 VS Code 对照尚未核验。压缩轨迹、全量 CI 重跑和行业频率样本仍缺。付费实验未获授权，工具使用范围见[项目规则](AGENTS.md)。
