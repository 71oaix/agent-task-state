# Agent 项目语义状态管理研究

本项目研究 Coding Agent 如何构建、维护和使用软件项目知识，以及这些能力能否改善开发正确率和效率。代码、测试和产物提供事实基础，目标、决策、依赖及有出处的判断提供决策依据。系统支持持久化、查询和核验，Agent 在开发中形成判断、采取行动并把新证据写回项目。

**当前主实验采用逐题揭示，首轮保留同一会话。** 同一仓库的后续要求按顺序出现，用每题边界的代码和知识快照观察知识起初是否写对、变更后是否更新、仍适用的知识是否影响行动。实验以原生 Pi 和 Pi 上的 StateHarness 参考版为对照，工作模型由本项目自选并在各组固定。整链一次给齐保留为论文对齐条件，逐题重开会话用于独立评估跨会话复用。见[研究意图](docs/intention/intention.md)和[实验协议与规格入口](docs/specification/specification.md)。

三组实验环境已经就绪。纯 Pi 和作者版 StateHarness A4 已在 Dulwich 与 mpmath 上做过逐题校准。第三组 **StateSystem（暂名）** 已冻结首版，在 mpmath #922 上验证了源文件写入和读取。使用相同 Magpie 免费线路复跑时，A4 与 StateSystem 的单题补丁都通过了独立评分，A4 的最终答复被额度限制中断。完整四题链的同线路三组对照仍待执行。见[实验记录](experiments/chainswe-baseline/state-maintenance-pilot.md)和[现有实现](docs/implementation/implementation.md)。

StateHarness 提供学术与实验参照，DSH 提供真实工程材料，LongHorizon-Harness 提供独立验收与目标推进的参照。原始来源与复现边界见[调研记录](docs/survey/project-semantic-state/survey.md)。

旧 Change Graph 和双视图设计已[归档](history/design/change-graph-task-state/)。T12 与[离线检查器](tools/work-operation-checks/README.md)保留为规则及案例积累，真实工程材料仍通过 [DSH 历史地图](experiments/dsh-process/dsh-work-history.html)和[已有记录分析](docs/intention/recorded-work-review.md)可查。
