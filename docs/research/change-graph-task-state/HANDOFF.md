---
title: Agent 接手入口与当前执行状态
status: active
created: 2026-10-23
updated: 2026-10-27
tags: [research, operation-selection]
---

# Agent 接手入口与当前执行状态

先读[人类主成果](dsh-work-history.md)、[现行候选v0.5](work-operation-candidates-v0.5.md)，运行方式见[工具说明](../../../tools/work-operation-checks/README.md)。本轮已完成。实现阶段提交05c1f84、a44a401；收尾修正以当前研究分支HEAD为准。

## 当前可用成果

四个基本入口create/revise/statement/select，八类执行组合partial_revert、replace_parts、split、rework、close、reuse、adopt、correct。已完整表达固定16段、83条来源事实与16条研究缺口；七条跨过程联系与两组内部分解保存为14条可查询关系。五个存储阶段和两个聊天承接范围有独立身份。固定truth v1未改。

工具位于Agent任务状态管理/tools/work-operation-checks/。build生成完整工作台，case支持--object/--revision/--scope/--step；输出目录必须新建。当前本机阅读器：本工作树 artifacts/agent-task-state/maintenance/dsh-workbench-2026-10-27/delivery-final/index.html；同目录有bundle.json与16段逐步Markdown。本地程序回归41项通过，最终页面核验16段切换、指定版本、父子结构、精确端点/事实导航、报告性质、合成采用冲突，以及桌面/窄屏。

## 已经裁定的规则

记录修订、产品发布和运行修订分别保存。选择查询同时提供采用时快照和当前说明；视图取副本，不反写工作状态。未知不等于未完成，未分配不等于未完成，持续限制不自动生成待办。旧保证、旧问题与当前状态有范围；correct精确指向被修正命题，来源报告另存，不因推翻解释而否定报告曾发生。

32个候选编号和去向保留：4核心、14组合/便利、2合并、12待补证。本轮新增可执行实现和规则，核心候选新增0、移除0。v0.4归档，v0.5唯一现行。下一轮按用户指令推进工作视图与上下文压缩后接续，不再默认重枚举名称。

## 验证与来源边界

Sol负责实现、主来源走查和裁定；CodeBuddy起稿包1/2/4并审查Sol起稿包3。首次24条新上下文读回发现旧字段残留与unknown/residual误读；修正后只做四个问题的定向读回，关键区别恢复。定向任务bf697373 completed，JSON原文有孤立case-ID词元，另存仅格式规范化版本，答案文字未改；输入与原答卷保留。记录解释与阅读定义同时修改，不将结果单独归因于某接口。

CodeBuddy固定a44a401审查（c885e691，completed）提出六项实质问题；Sol逐项修复并完成本地回归，最后差异由Sol复查。模型没有运行测试，不把模型审查覆盖范围扩展到后来提交。源码语义判断与程序一致性、图和交互验证分别保存。

包1任务c0282143及初次读回e32075a6为needs_attention，原因是同Git根主Agent并行改文件；已核对路径/工具事件，读回允许输入哈希不变且仅观察到读取input。后续包2=829b5c5e、包4/包3审阅=94ccb24c以及定向/固定提交审查均completed。全部任务已终止，不重复派单。

## 本地复现与接续

本批根目录为本工作树 artifacts/agent-task-state/maintenance/dsh-workbench-2026-10-27/。四包模型原稿、source-walkthrough-final.json、readback-adjudication.json、code-review-adjudication.json、错误探针、普通文档基线与生成输出均保留。readback-v1未派单，v2为首次实际24答；delivery-v1至v4为历史生成物，delivery-final为现行。历史encode-pack3-sol.py、run-probes.py只作原始执行依据，不直接重跑覆盖当前文件；复现使用已提交fixtures与工具README命令并新建输出目录。

CodeBuddy独立工作树artifacts/worktrees/task-state-codebuddy-round1保留冻结输入（HEAD2861b59），不是现行成果入口。正式成果在codex/task-state-activity-research，Git状态实时核对，保护其他项目内容。原始资料截止2026-10-15。本轮未运行DSH和任务效果实验；后续SWE-Milestone与付费实验需另行授权。

成本继续采用Sol加本地脚本、必要的有界CodeBuddy任务；不默认Codex三并发，不重连Qoder，不自动重试失败任务或切换服务。无token/费用回执时记未知。

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
