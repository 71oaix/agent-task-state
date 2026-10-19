---
title: 本地资料分类与定位
status: active
created: 2026-10-15
updated: 2026-10-16
tags: [assets, organization, provenance]
---

# 本地资料分类与定位

研究资料从工作树中移出，统一放到**主工作区** `artifacts/agent-task-state/`。主工作区是 `C:/Users/10636/Desktop/Xiao-Notes/论文/`；不是当前独立研究工作树。主工作区总导航为 `artifacts/README.md`，本项目资料入口为 `artifacts/agent-task-state/README.md`。这两份本机导航及原始资料被 Git 忽略，分类规则和来源指引由本文及项目来源清单保存。

本轮解决实际资料混放和入口不清问题，不更改研究结论。2026-10-15 从研究工作树的两批资料中迁移 41 个文件，迁移前后大小及 SHA256 一致。工作树目录本身未移动，其他项目运行证据和依赖路径保留。

## 当前分类

下表全部为主工作区根目录相对路径；各类内部保留原批次名称，不抹去采集历史。

| 位置 | 资料性质 | 本轮文件数 |
|---|---|---:|
| `artifacts/agent-task-state/source-files/` | 原样保存的 ATMS PDF、固定 JJ 仓库 Markdown | 4 |
| `artifacts/agent-task-state/paper-extracts/` | 论文正文提取；不冒充原始 PDF 或原始网页响应 | 10 |
| `artifacts/agent-task-state/reference-extracts/` | Datomic、PROV、事件溯源页面提取 | 4 |
| `artifacts/agent-task-state/repository-snapshots/` | 仓库说明、静态协议、代码片段与任务规格快照；不是实际运行轨迹 | 13 |
| `artifacts/agent-task-state/publication-metadata/` | 发表身份与索引页面快照 | 3 |
| `artifacts/agent-task-state/acquisition-records/` | 原始获取清单、失败、重试和固定版本记录 | 7 |
| `artifacts/agent-task-state/maintenance/2026-10-15-classification/` | 新生成的迁移与校验记录；不计入上述 41 个原文件 | 按实际生成 |

两批原名为 `task-state-round1-2026-10-13` 和 `task-state-primitives-2026-10-14`。逐文件旧址、新址、类别、大小及保存文件哈希由 `artifacts/agent-task-state/maintenance/2026-10-15-classification/relocation-map.json` 保存。原获取清单内容未改，里面的旧文件名通过迁移表定位；`sha256_response` 与当前保存文件哈希分别解释，不能把提取文本和提取前响应当作同一字节对象。

原工作树两个批次目录仅保留 README 迁移指引。恢复原布局时依据迁移表逐文件处理，先校验新位置的 hash，并确认原位置没有同名文件；目标存在时停止，不能覆盖。迁移不涉及删除数据、重写来源清单或压缩历史。

## 原位保留但已经归类的资产

| 类别 | 主工作区位置 | 原位保留的原因与核验边界 |
|---|---|---|
| 本项目早期静态材料 | `artifacts/worktrees/change-graph-paper/artifacts/research-evidence/change-graph-neighbors-2026-10-09/` | 历史工作树中的六个 InterruptBench 快照，入口登记，不复制或迁移 |
| 本项目背景诊断 | `artifacts/diagnostics/chatgpt-content-reference-2026-10-09/` | 聊天引用故障诊断，不能进入实验样本；只核对目录角色，不重新读取私有内容 |
| 另一项目实验 | `artifacts/experiments/` | 每批运行有既定引用和原始数据，原位保留；有效结论查工具反馈管理的资产索引 |
| 另一项目工程证据 | `artifacts/verification/`、`artifacts/test-runs/`、`artifacts/acceptance-d02-20260927/`、`artifacts/er-01-sandbox-failed-test-20261009/`、`artifacts/er-01-validation-20261009/` | 按现有登记归类，未逐项复核全部输出；verification 内 UUID 目录保持未逐项判定 |
| 另一项目依赖与准备 | `artifacts/dependencies/`、`artifacts/provisioning/` | 现行执行依赖及历史准备证据，移动会影响脚本或解释路径 |
| 旧审计产物 | `artifacts/pi-jsonl-audit-2026-09-16/`、`artifacts/pi-jsonl-audit-2026-09-16-v2/`、`artifacts/pi-jsonl-audit-2026-09-16-v3/` | 前两版读取被系统权限拒绝，未核验内容、不更改权限；v3 仅列出清单和报告文件，未作为研究样本读取 |
| 运维、审阅和 Git 检出 | `artifacts/operations/`、`artifacts/review/`、`artifacts/worktrees/` | 工作区维护和隔离开发用途，不能当作论文证据库整体收录 |

此次全局分类是角色导航，只有本项目当前两批资料做了物理迁移。没有将其他项目的活动数据重排，也不声称所有资产已逐文件核验。

## 后续存放规则

新资料先按项目，再按资料性质，再按来源或批次定位。外部原文和提取文本区分，固定链接、版本和获取记录一起保留。新增类别由实际产物触发，不预建案例、分析或实验的空目录。

人工标注和分析结果生成时，另建项目分析批次，引用来源文件及其版本，不写回原材料；正式验证运行按冻结协议保存完整新批次。临时文件也要声明用途，不能因为未分类就默认可删。新研究数据不再落入 `artifacts/worktrees/` 下的私有资料堆。

原始资料、个人日志和生成证据不提交。可提交的是设计结论、来源登记、分类规则和导航。2026-10-15 接手补全：研究文档已由固定提交 404a4ab 接入主工作区的独立交接分支。当前计划和状态从本项目 README → HANDOFF 进入；旧研究工作树保留为历史来源。尚未合并 main，也没有改变其他项目授权。

## 2026-10-15 活动研究执行新增批次

来源批次为主工作区 `artifacts/agent-task-state/` 下各性质目录的 `activity-research-2026-10-15/`；原始响应/正文提取与分析分开。新增分析分别为 `artifacts/agent-task-state/analysis/2026-10-15-G1-attempt-01/`、`artifacts/agent-task-state/analysis/2026-10-15-G2-attempt-01/`、`artifacts/agent-task-state/analysis/2026-10-15-G3-attempt-01/`。获取失败、重试和提取编码修正保留，正文读取与下载成功分开。G2 当前使用 activity-observations-v2.json，原 v1 及修订说明保留。

共享主工作区在执行中被其他任务切换，因此后续文档位于独立研究工作树 `artifacts/worktrees/task-state-activities/` 的 codex/task-state-activity-research，主工作区源资料保持唯一位置。G1 的位置纠正记录见执行账本；没有移动或清理其他任务文件。

## 2026-10-16 DSH 全项目研究批次

原始与派生资料均在主工作区 `artifacts/agent-task-state/repository-snapshots/dsh-full-history-2026-10-16/`：API与npm原始响应、固定源码归档和文档提取、版本目录、历史设计对象与派生图，manifest区分角色。完整Git历史在 `artifacts/agent-task-state/third-party/dsh-history-2026-10-16/`；自有临时研究生成/验证工具在 `artifacts/agent-task-state/maintenance/dsh-full-history-2026-10-16/`，均不提交。自有报告及HTML位于Agent任务状态管理研究目录，入口见[全项目报告](../research/change-graph-task-state/dsh-project-history.md)。


## DSH truth本地批次（2026-10-19）

`artifacts/agent-task-state/repository-snapshots/dsh-truth-2026-10-19/`保存固定来源元数据、逐事实派生清单、所选主题全部版本映射和核验结果。不同正文仍引用`artifacts/agent-task-state/repository-snapshots/dsh-full-history-2026-10-16/historical-note-objects/`，不重复复制第三方正文。`artifacts/agent-task-state/maintenance/dsh-truth-2026-10-19/`为自有提取辅助和本地运行记录。详细事实以dsh-truth-v0.1-evidence.md为对照，dsh-truth-v0.1.md提供阅读版。本轮JSON清单和审查记录见后续阅读修订批次。


## Truth阅读修订与Luna审查（2026-10-19）

`artifacts/agent-task-state/maintenance/dsh-truth-readable-2026-10-19/`保存阅读修订后的派生54条事实清单、原稿审查报告、事实保留核验与Luna试行记录。原稿及旧清单留在原批次和提交7fbdda6。原提取脚本build_truth.py属于原稿生成证据，现行阅读版由项目文档维护；重新执行旧脚本会重建旧稿。


## 2026-10-19 DSH 工作图盘点批次

主工作区 `artifacts/agent-task-state/repository-snapshots/dsh-exhaustive-2026-10-19/` 保存完整机器盘点、候选关系、审阅处置、审定图和覆盖账本；`artifacts/agent-task-state/maintenance/dsh-exhaustive-2026-10-19/` 保存自有静态分析与页面验证脚本。当前阅读入口为[DSH 工作地图](../research/change-graph-task-state/dsh-work-history.md)。原始正文沿用 dsh-full-history-2026-10-16，不重复采集。
