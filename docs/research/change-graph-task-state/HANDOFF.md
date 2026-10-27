---
title: Agent 接手入口与当前执行状态
status: active
created: 2026-10-23
updated: 2026-10-27
tags: [research, operation-selection]
---

# Agent 接手入口与当前执行状态

先读[人类主成果](dsh-work-history.md)、[现行候选v0.5](work-operation-candidates-v0.5.md)，操作输入见[工具说明](../../../tools/work-operation-checks/README.md)。研究分支codex/task-state-activity-research，首阶段提交05c1f84；最新HEAD用Git核对。

2026-10-27已实现四个基本入口上的八类组合、全部16段DSH逐步表达、83条来源事实与16条研究缺口、七条跨过程关系与两组内部包含（共14条可查询关系）。五个存储阶段和两个聊天承接范围有独立身份。固定truth v1未改。

工具在Agent任务状态管理/tools/work-operation-checks/。在仓库根运行 python -m unittest discover -s Agent任务状态管理/tools/work-operation-checks -v；37项当前通过。workbench.py提供build、case及--object/--revision/--scope/--step，输出目录必须新建。当前阅读器位于本工作树 artifacts/agent-task-state/maintenance/dsh-workbench-2026-10-27/delivery-v4/index.html；完整状态、展开和16段Markdown在同目录。图与16段交互已本机渲染，桌面/窄屏、对象历史与事实跳转通过。

来源裁定：记录修订、产品发布和运行修订分开；采用说明与adoption分身份，scope含工作域；旧状态/当前状态分开，未知/未完成/未分配/持续约束分别说明。四入口create/revise/statement/select不变，新增的是可执行组合，不按函数数证明最小。32个候选编号和去向保留。

CodeBuddy起稿包1/2/4并审查Sol起稿包3。任务c0282143首包及e32075a6首次读回为needs_attention，原因是主Agent改同Git根其他文件；工具证据已核对，实际模型允许输入哈希未变、读回只读input.json，原稿/结果/修正保留。包2=829b5c5e、包4及包3审阅=94ccb24c均completed。后续CodeBuddy使用独立工作树artifacts/worktrees/task-state-codebuddy-round1（HEAD2861b59），冻结期间不修改该Git根。

首次24条独立上下文读回发现Loader旧字段、聊天实施状态及unknown/residual误读；已修正。当前定向四问任务 bf697373-1461-40cd-8e1a-aaebd944b28b，输入在CodeBuddy工作树的Agent任务状态管理/tools/work-operation-checks/readback-targeted/input.json，禁止重复提交或改其输入。它复查四个具体语义问题，原24答案保留；取回后源对照裁定。另一项收尾是固定提交CodeBuddy集中审查，需review_commit并且不把待完成写为完成。

本批原始与分析资料在 artifacts/agent-task-state/maintenance/dsh-workbench-2026-10-27/。semantic-rubric-before-full-encoding.json为Sol源参考，probes-pack1.json为8项实际合成更新，ordinary-documents-frozen-baseline.md为已维护普通文档对照。readback-v1未派单，readback-v2为首次实际24答案，模型输出和来源评分分开。delivery-v1至v4保留，不覆盖。

本轮剩余：处理定向读回与固定提交审查，完成链接/锚点/Git差异收尾，保存最后提交并报告。下一研究轮围绕工作视图和压缩后接续。成本默认Sol加本地脚本，仅已授权CodeBuddy流水线，无Codex三并发；禁止自动重试失败任务，不切换付费服务，不运行DSH或SWE-Milestone。本轮CodeBuddy服务经用户明确授权，token/费用无回执时保持未知。

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
