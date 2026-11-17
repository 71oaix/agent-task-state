# Implementation（现行实现说明）

本目录说明**现在已有什么实现入口**，以及它覆盖 Intention / 规格到哪一步。代码与检查器本体仍在 `tools/`，实验证据在 `experiments/`，不把仓库代码搬进 docs。

## 与意图的对应关系

| 意图块 | 当前实现落点 | 状态 |
|---|---|---|
| 最小语义层 / 开发历史记录 | [`tools/work-operation-checks/`](../../tools/work-operation-checks/README.md)（含 T12 相关脚本与离线检查） | 离线可跑；面向记录自洽与合成接续 |
| Human view | [DSH 历史地图](../../experiments/dsh-process/dsh-work-history.html) 等固定案例展示 | 有示例，未接日常入口 |
| Agent view / 接手导出 | 检查器中的实验性接手数据导出 | 有导出能力；**真实 Agent 接续未验证** |
| 相对轨迹或普通文档的对照证据 | 尚未建立有/无该语义层的 Agent 对照协议 | 缺口 |

已有实验记录的分析见 [recorded-work-review.md](../intention/recorded-work-review.md)。

## 主要入口

- 工具与约束：[`tools/AGENTS.md`](../../tools/AGENTS.md)、[`tools/work-operation-checks/README.md`](../../tools/work-operation-checks/README.md)
- 按次实验：[`experiments/`](../../experiments/)（如 `t12-objects`、`operation-composition`、`activity-survey`；`dsh-process` 是外部材料上的过程编码与展示）
- 被替代的旧设计与交接：[`history/`](../../history/)

## 实现边界（现行）

- 检查器用于**离线研究**，不自动等于线上 Agent 运行时。
- T12 的离线规则与合成接续，证明的是记录/查询能否自洽，不证明真实接续收益。文内记载的 180 项回归，对应归档目录在当前工作区尚未找到，不能当作已复核数字。
- 付费实验未授权；扩展验证须单独批准。

下一步实现工作应优先服务 Intention 中的真实接续对照，而不是继续扩大离线对象修订面。
