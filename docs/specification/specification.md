# Specification（现行规格与架构取舍）

本目录放**系统必须满足什么**及已记录的架构判断。尚未完成 three-space-development 的 Gate 2 正式 Specification Package；下列材料是现行依据，不是已批准交接包。现行意图见 [Intention Brief](../intention/intention.md)。

## 本轮规格意图（从 Intention 落下的义务）

系统侧需要同时满足：

1. **最小语义层**：提供少量可维护对象和可组合操作，记录软件开发历史中的目标、安排、一次推进、产出与带出处的判断，以及每次变化的前后状态。这是对已有状态与轨迹的抽象，不是再存一份更全的日志。
2. **完整历史语义**：对象可独立变化（例如尝试结束而目标仍待验收；计划改版后旧成果仍指旧版）；身份、版本、关系与出处可查询。
3. **双视图生长面**：同一权威记录可投影 Human view（进度与依据可读）与 Agent view（接续所需的现状与证据入口）。
4. **可证伪的增量**：最终验证不只是记录器自洽，还包括真实 Agent 在受限 Context 下，该语义层是否比普通文档或原始轨迹更能支持正确接续。

失败时至少应能观察到：无法恢复当前工作边界、错误沿用计划版本、丢失仍有效的旧成果/报告/验收依据，或 Agent 视图无法阻止明显跑偏。

「状态独立于 Context」「执行图或树」「保留失败分支」「有效状态替换旧状态」已被近邻覆盖，不能单独作为规格目标或论文新意。

## 现行设计材料

| 文档 | 作用 |
|---|---|
| [架构 v0.4](change-graph-task-state/design-v0.4.md) | Change Graph / 任务状态与双视图架构（仍为草案） |
| [设计假设与对象方案](change-graph-task-state/design-hypothesis.md) | 2026-10-09 假设及五类对象 + Change；验证边界 |
| [来源清单](change-graph-task-state/source-inventory.md) | 外部证据与发表身份 |
| [design-v0.4 agent notes](change-graph-task-state/design-v0.4-agent-notes.md) | 架构讨论笔记 |
| [已有记录整理](../intention/recorded-work-review.md) | 对已完成记录工作的分析，不是新规格 |

## 已公开的开放点（不得假装已关闭）

- 五类是否最小、顶层是否拆成五张表：开放。
- 真实 Agent 小任务接续：仍待验证。
- 双视图日常入口：尚未接通。
- 主张句与可执行实验协议：尚未写下。

正式规格包（边界、输入输出、不变量、验收用例、SDD handoff）待 Intention 歧义收窄后再写；在此之前以本文与上表为现行阅读入口。
