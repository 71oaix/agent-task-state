# 项目语义状态管理近期研究来源队列

最后更新：2026-11-20

本队列登记[论文讨论交接](chatgpt-conversation://6afad74d-dce4-83e9-a1a7-59c848773dfa)提及的研究线索。名称和链接来自该讨论；文末记录本轮对 StateHarness、ChainSWE 与 LongHorizon-Harness 的原始来源核对。其余条目保持待核验。既有来源记录见[来源清单](../../specification/change-graph-task-state/source-inventory.md)。

| 讨论名称与候选入口 | 后续核验问题 | 状态 |
|---|---|---|
| [StateHarness](https://arxiv.org/abs/2610.17616) | 研究状态表达、组织、维护、查询、实验开销和归因 | 论文和源码已核对。Pi 上的作者版 A4 已用于本项目的逐题校准，论文原实验使用的旧样本和协议尚待复现。见[实验记录](../../../experiments/chainswe-baseline/state-maintenance-pilot.md)。 |
| [MemTrace](https://arxiv.org/abs/2610.04838)、[候选代码](https://github.com/Homy-Xu/MemTrace) | 核实论文与代码对应关系、状态一致性和信息失效机制及验证范围 | 待原始来源核验 |
| [ProjectGuard / SLUMP](https://aclanthology.org/2026.findings-emnlp.76/) | 核实论文、系统与评测名称关系，以及语义承诺和实现一致性的研究边界 | 待原始来源核验 |
| [OpenWiki](https://github.com/langchain-ai/openwiki) | 核实知识与代码证据关联、变更后的重新验证机制，以及讨论所称 LEDGER 的实际入口和评测范围 | 待原始来源核验 |

StateHarness 承担学术参考和候选基线角色；DSH 承担同等重要的工程参考和机制设计来源角色。后续需结合 DSH 的事实归属、替代、生命周期、权威、验证与同步线索作机制比较，不预设采用其中任何方案。

正式核验时记录官方身份、作者、版本、发表类别及核对日期，分别说明原文阅读、代码检查和复现范围；对有效性与可靠性结论保留适用条件，检查维护成本及实验归因。登记队列不代表已经证明相关研究的机制或我们的创新空间。

## StateHarness 对照组补充核验

作者源：[仓库入口](https://anonymous.4open.science/r/StateHarness)、[arms.py](https://anonymous.4open.science/api/repo/StateHarness/file/state_harness_skills/runner/arms.py)。以下对照定义已对照公开源码与作者说明。额外对照的可运行性和实验结果尚未核实。

| 编号 | 含义 |
|---|---|
| A0 | 原生 Agent |
| A1 | 协议提示，无 hooks；源码注明模板每实例新种子、不跨实例 |
| A2 | 开头带入状态，由 agent 自行维护，无中途注入 |
| A3 | 周期注入，关闭升级诊断与阻断校验 |
| A4 | 完整 StateHarness |
| R1 | 按 A4 实测预算供原生 Agent 重试 |
| R2 | LongHorizon-Harness 的管理、执行与审计流程 |

论文 v1 报告的 ChainSWE 对照和作者 README 的主实验命令均使用 A0、A4、R2。A1–A3、R1 可作为后续候选对照；构建、维护、使用的独立增益仍需分别设计实验。

ChainSWE 输入版本差异：作者从旧 100 链 304 问题 JSONL 版中选 37 链 114 问题，all-at-once；[现公开版 ChainSWE](https://huggingface.co/datasets/C-lister/ChainSWE)为四个 Parquet 分片，长度分片合计 376 个不同链 ID，与作者 37 个旧 ID 精确匹配 0 个。格式可转换；旧 ID 与载荷需旧快照，或依 repo、base commit、问题 ID 顺序和测试补丁映射。进一步按同一仓库和原始问题 ID 核对，114 个问题确认重合 20 个；37 条链中只有 `meltano/sdk` 的一条同时匹配有序问题清单与起始提交。该匹配尚未比较题面、镜像及补丁字节，其他未匹配项也可能存在不同的问题标识。公开版的 1,504 是题目在各条链中的出现次数，按仓库与问题 ID 去重为 661。因此原样复现须先重建旧版本，新实验可固定公开版与同一评分协议另立样本。

StateHarness 的 state 是任务相关的项目理解与进展，包含最初观察、任务意图、当前焦点、假设、发现、已做与待做工作、依赖及过程建议。Agent 编写四类持久记录，运行时生成工作简报，配合提醒、影响检索、格式校验和按需诊断。事件日志提炼开发经历，关系和当前状态还支持脱离原轨迹的查询。StateHarness v1 评测整套机制，单项收益未由主对照隔离。

论文报告相对原生 Claude Code，RefactorBench 完整链通过率从 29.4% 到 35.3%，关联清理从 87.0% 到 95.4%，调用点分项仍为 93.3%。ChainSWE 修复率从 35.1% 到 39.5%，原有测试回归从 16 到 23。RefactorBench 平均耗时从 383 到 529 秒，诊断用量未全部计入统一 token 账。以上是作者报告值。回归的增加无法归因于陈旧状态，状态记录也无法保证 Agent 行动，论文 §4.5 记录了记下缺口却未继续处理的案例。论文工作模型为 Sonnet 5，作者 README 的 Haiku 是示例参数。本项目各组统一使用自选工作模型。见[论文表 1–2 与附录 B](https://arxiv.org/html/2610.17616v1)。

## ChainSWE 评测协议

[原 ChainSWE](https://arxiv.org/html/2607.02606)逐题揭示并交补丁，后续题继承先前仓库改动。Seq 每题新会话，Seq+Mem 保留对话。StateHarness 将旧题按时间编号拼接，一次给齐，同会话交一个总补丁，评分端按题累积应用测试补丁。源码仅显示拼接和添加说明，题库差异的成因仍不明。作者评分器将日志中缺失的测试单列，判定要求至少一个已观测的修复测试通过、其余已观测的修复测试通过、没有观测到原有测试失败。该规则与原版正式评分的一致性未确认。

逐题揭示适合研究何时发现知识需要更新，整链给齐适合研究所有要求已知时的长任务协调。任务可见性、会话承接、交付和评分边界应分开控制。现行协议见[规格入口](../../specification/specification.md#首轮实验协议)。

## LongHorizon-Harness 的参照作用

[LongHorizon-Harness](https://arxiv.org/html/2608.01964v1)将规划、执行和只读审计分开，由管理者根据已核实状态与总目标决定下一步。可借鉴的是允许记录暂定判断，同时要求用于验收和后续推进的结论有相应证据。三角色架构仍属外部参照。
