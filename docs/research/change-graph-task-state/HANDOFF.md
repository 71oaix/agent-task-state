---
title: Agent 接手入口与当前执行状态
status: active
created: 2026-10-23
updated: 2026-10-27
tags: [research, operation-selection]
---

# Agent 接手入口与当前执行状态

2026-10-27 执行用户批准的“形成可用工作操作并完整表达 DSH”计划。使用当前独立分支，起始 HEAD 2861b5934e09a2002702309df67a86f6b2033071。当前四入口 create/revise/statement/select；本轮优先可用组合，不按函数数量压缩。

当前实现：tools/work-operation-checks/workbench.py、EXPRESSION.md、reader.html、test_workbench.py；组合含 partial_revert、replace_parts、split、rework、close、reuse、adopt、correct；新文件尚未提交。Loader 主 Agent 预分析和可运行示范位于本工作树 artifacts/agent-task-state/maintenance/dsh-workbench-2026-10-27/；图已渲染，移动/桌面及历史查询交互检查通过。

CodeBuddy 批次1任务 c0282143-6631-471f-8a7d-91b860d42ba5，deepseek-v4.1-flash/max，edit 仅允许 cases/pack1.json，包含 T01/T03/T12/T14。任务仍运行时不改其文件、不重复提交。此文件初稿四案可重放，主 Agent 来源复核已发现决定/落地时态、T12 用后续信息提前分配责任、unknown 被写成 not_started 等问题；裁定草稿在 sol-review-in-progress.json。待任务完成先保存原稿和原始 result，再修正、冻结包1。

下一动作：包1校准后依序派 CodeBuddy 包2(T02/T04/T06/T08)、包3(T05/T07/T09/T15)、包4(T10/T11/T13/T16)，只读取固定底稿、EXPRESSION、既有代码和包1示范，避免全资料扫描。每包仍用独立白名单 JSON，HEAD 变化前须确认无 edit 在排队。主 Agent 检验每步、覆盖和来源含义后继续。

随后全量 build 到新的 ignored 输出目录，建立83事实/16缺口对应、七条跨过程和两条内部包含关系，CodeBuddy 用新上下文对选定片段读回。source truth 不修改；模型编码和模型自检不计为独立检验。程序拒绝与语义来源审查分开。最终形成候选v0.5、更新dsh-work-history与operation-composition-review、索引/资产、固定提交集中审阅。计划未完成时不能报完成。

本轮已明确授权 CodeBuddy 服务分工，不使用 Qoder，不默认 Codex 子代理三并发。失败先取回状态/结果，禁止自动重发；用量无回执保持未知。控制成本优先主 Agent 与本地脚本。CodeBuddy interface contract_revision=2.0、串行队列；其工具白名单不是OS隔离。

<details><summary>2026-10-25 上轮接手记录</summary>

先读[本轮主结论](dsh-work-history.md)，现行规则只查[候选 v0.4](work-operation-candidates-v0.4.md)，依据与范围查[筛选实验](operation-selection-review.md)。v0.3 已归档，前轮资料保留。

本轮按批准计划实现检查器并完成四组校准。陈述/生命周期完成独立跨过程更新；关系/采用因用户成本指示及账户额度错误改为主 Agent 本地走查。共 36 独立更新、12 本地主 Agent 更新，来源语义评分与程序一致性检查分开。组合回归覆盖八个案例，其余八过程只作影响核对。

当前四个工作入口为 create/revise/statement/select。open/close 作为组合；observe/judge 合并到 statement；bind 作为有类型引用的组合，独立关系身份按需。32 个编号去向为 4 核心候选、14 组合/便利、2 合并、12 待补证。初始登记、对象类型、范围与效力规则都算入机制；四入口不是函数数量下界。两入口版本保留强对照。

代码在 Agent任务状态管理/tools/work-operation-checks/，使用 Python 标准库。验证：python -m unittest discover -s Agent任务状态管理/tools/work-operation-checks -v。18 项测试；原跨过程使用 freeze-v2，交付版在引用存留修正后另以 freeze-v3-delivery 和32步本地重放验证。它是记录检查器，不运行 DSH 或判断自由文字真伪。

原始批次在仓库根目录 artifacts/agent-task-state/maintenance/dsh-operation-selection-2026-10-25/：protocol-v1.json、episodes-private.json、freeze-v2.json；workers/results/submissions 是实际独立运行，manual 是主 Agent 走查，review/calibration 是独立评分；combined-replay.json 与 deletion-profiles.json 是本地变换重放。不要覆盖旧批次或把两入口变换计为独立实验。

本轮到此结束候选筛选。现有测试已覆盖同前驱分叉及冲突保留。下一阶段只在确需独立引用/修订一条关系时补最小反例，并把当前记录接到按版本查证/恢复工作视图的能力切片；复用现有检查器，不再重新枚举名称。长期工具使用与压缩后接续收益仍待 SWE-Milestone 阶段，付费实验继续需要单独授权。

用户已要求控制成本：禁止默认三并发；默认主 Agent 加确定性脚本。仅当一个具体争议会改变候选去向且主 Agent 无法可靠裁定时，调用一次最小材料的独立审阅；用量/费用未知不能写为零。Qoder 已移除，不重连、不改用付费服务、不重试额度错误。

研究工作树 artifacts/worktrees/task-state-activities，分支 codex/task-state-activity-research。提交状态从 Git 核对，保护其他项目未提交内容。固定资料截至 2026-10-15，底稿 v1 和前轮答卷不变；已知来源缺口保留未知。

</details>
