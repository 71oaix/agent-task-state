# 项目语义状态研究的现有实现

当前实验环境包含原生 Pi、作者版 StateHarness A4 和 StateSystem v0.1.0。后两组在同一 Pi 底座上比较状态维护方式。现行目标见[研究意图](../intention/intention.md)，待验证的行为见[规格入口](../specification/specification.md)。

## 可复用积累

| 已有入口 | 可支持的研究 | 当前证据边界 |
|---|---|---|
| [离线检查器](../../tools/work-operation-checks/README.md)与 T12 脚本 | 对象版本、部分更新规则、关系和历史查询 | 面向显式编码的自洽及合成接续；不证明真实语义正确 |
| [DSH 历史地图](../../experiments/dsh-process/dsh-work-history.html)与过程编码 | 固定案例展示、工程机制分析的材料 | 尚未接通日常双视图，也未将机制抽象为本轮系统 |
| 实验性接手数据导出 | 面向任务的状态投影候选 | 真实 Agent 接续收益待验证 |

已有材料的分析见[已有记录分析](../intention/recorded-work-review.md)。T12 文档记载的 180 项回归对应归档在此前盘点中未找到，暂缺可复核的原始记录。

## Pi 实验环境与材料

实验使用 Docker Desktop 的 Linux 容器，固定 Pi `1.5.2` 和 Node `22.22.1`。纯 Pi 组保留默认系统提示词，关闭自动扩展、MCP、技能、提示词模板和项目上下文，只开放 `read`、`bash`、`edit`、`write`。A4 和 StateSystem 分别显式加载自己的扩展。各组从同一冻结镜像和空会话开始，链内逐题揭示，评分材料位于独立容器。

Meltano 三题链用于环境和评分校准，已用上游参考补丁验证三个检查点。公开 ChainSWE 主样本和备用样本已[冻结](../../experiments/chainswe-baseline/sample-v1.json)，Dulwich 和 mpmath 已完成首轮 A0/A4 探查。作者版 A4 运行作者的原始 hook 与协议，通过 Pi 适配工具事件和诊断请求，详见[实验记录](../../experiments/chainswe-baseline/state-maintenance-pilot.md)。

本地 Qwen3.5-9B 已用于启动和工具校准。第一批逐题运行使用 DeepSeek 官方 API。为控制实验成本，当前复跑使用 Magpie 转发的 OpenCode Zen 免费模型 `opencode-zen/deepseek-v4.1-flash-free`。隔离运行器按线路记录结果，额度中断保留补丁和日志，评分与会话完成状态单独记录。

公开基准的本地材料、原始日志、补丁和冻结扩展存放于 `evidence/`。StateSystem 的本地操作入口位于 `evidence/pi-baseline/statesystem/README.md`，版本与运行输出独立存放。LHTB 已核对任务配置，Harbor 运行待验收。

## 多模型研究协作

研究方案争议可通过 Gemini MCP 与 Codex 进行多轮共同设计。先给研究目标和可共享证据，让双方独立判断，再补证、质疑和修正，通常五到六轮内收敛或说明残余分歧。送达以 MCP 确认会话绑定为准，已送达任务按原会话取答和续聊。此轮 ChainSWE 讨论取得 Gemini 首轮意见，追问送达后中断。通道和协作范式分别跟踪在 [MCP 会话恢复](https://github.com/71oaix/gemini-desktop-mcp/issues/4)与[多轮协作](https://github.com/71oaix/gemini-desktop-mcp/issues/6)。协作意见由本项目用原文与代码核验。

## 新方向的实现缺口

当前机制证据覆盖同一题里状态写入后能否读到最新内容。跨题维护、历史知识复用、Agent 是否主动沿链接读取以及额外读取开销，需要完整链对照。v0.1.0 的任务模板还有一条沿用自作者版的同步说明，应随下一版本更正。更广泛的构建和使用机制仍按[实验协议](../specification/specification.md#实施顺序与开放设计)逐步探索。

代码与操作约束见 [tools/AGENTS.md](../../tools/AGENTS.md)。研究记录在 [experiments/](../../experiments/)，历史设计与交接在 [history/](../../history/)。
