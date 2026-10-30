---
title: Agent 接手入口与当前执行状态
status: active
created: 2026-10-23
updated: 2026-10-30
tags: [research, operation-selection]
---

# Agent 接手入口与当前执行状态

## 2026-10-30 当前状态：五类对象推荐待最终审阅

**当前结论：**T12 推荐 Goal/Plan/Attempt/Product/Evidence 五类逻辑角色，Change 记录变更；不声称五张表最小或最优。强内嵌 Plan 可被 A2 直接引用 A 的精确旧版 section，强内嵌 Product 可由 A2 继续更新原 slot 且 A 保持 ended，Evidence 可在 Change 内以稳定 statement locator 引用，合并 Work 仍需 attempt key/status。独立存放的当前理由是减少宿主版本耦合、维护位置直接，不是功能表达优越；整份删除宿主数据只证明存放依赖。

**规则与核对：**Plan 可关联 Goal 或 Attempt；Product 的 part 有稳定定位和局部状态，整体进展派生、整体验收单独判断；Evidence 是有来源报告，不是认证真理，纠正具体命题/范围并保留旧报告。T03 计划阶段、T13 判断修正、T15 准确版本依赖已进入可执行边界；15 段的逐条覆盖是静态语义回查，其中这三点另有可执行片段，没有证据迫使新增第六类。产品运行规则只作为成果内容，不实现 job/queue/Goal 授权。操作按当前代码入口组织到对象，`apply` 只做事务。对象加入 0、合并 0；改动是 Plan 归属、Product 局部状态、Evidence 纠正规则、关系版本。

**审阅状态：**主文、本页、组合记录、README、索引与资产登记是待最终审阅的本地文档草稿，未提交。代码研究 checkpoint `5ba5d1e` 保留待审实现；本任务未运行 Git，HEAD 以任务合同为准。独立 GLM 与一次 Kimi 审阅仍待执行，不能写研究全部完成或审阅已通过。回执差异（fd501936、0b1190ec、HY 0ecff39a/a0c6a83c）见[组合记录本轮节](operation-composition-review.md#2026-10-30五类对象推荐与操作组合)。

**待办：**

1. Astra 最终审阅本轮推荐、主文与操作组合，确认需审阅处。
2. 执行独立 GLM 与一次 Kimi 审阅；完成前不更新“已通过”。
3. 审阅通过后按仓库流程提交/PR；本任务不提交。
4. 下一阶段用真实 Agent 接续检验这批规则，不把本批固定材料结论外推。

<details><summary>2026-10-29 及更早接手记录（历史，保留当时口径）</summary>

以下为历史记录，日期与当时口径保留；文中的“当前”均指该条记录日期。

## 2026-10-29 历史状态：2a2核心裁定与core-v1

**本切片结论：**第2a2切片已完成：按Astra裁定修正Plan实际采用权威、显式采用后的scope要求、同Goal Evidence边界、Kimi审阅表述与模型调用口径；把S029 item状态、工作范围、部分复用和9context→8→Turn inputs依赖写入可查询状态；新增`t12_continuous.py`导出函数与`test_t12_export.py`实际调用，首次建立`artifacts/agent-task-state/maintenance/t12-continuous-validation-2026-10-29/core-v1`。四身份替代、其余15段和最终推荐未做，不能称研究全部完成。

**核心裁定：**见同目录`core-adjudication.md`。`product.plan_usage`是唯一实际采用权威；有显式采用后`produce`省略`plan_scope`必须拒绝，继续旧版须显式`adopt_plan(旧版本, scope)`；同Goal关联不等于Evidence语义充分，检查器不判自然语言真实性；`stage1-adjudication.md`的Kimi“只在未决争议时”表述不代表Astra裁定，批准要求是最终固定一次审阅冻结候选/对照/反例，旧稿保留；DS本身即模型调用，token/费用回执未知，按未知记录，不记为零。

**S029映射：**1-5与9 permission/system完成/写码/提交；6、7、8、9context、10、11未完成草稿且在turnstep；第5项保留原PR `latestCompletedParagraphFirstLine`；4A/4B分开可查。`draft-code::9_context_hiding`依赖`draft-code::8_trigger_notifications`，后者依赖`turnstep::Turn starts and Inbox claims`；端点、basis、nature可双向查询，关系不代表完成、转交或验收。

**证据与验证：**`python -m unittest discover -s Agent任务状态管理/tools/work-operation-checks -v`实际运行：首次97项中1 failure、1 error（测试查询形状与合成链readback），修正后97项全部通过；旧86项语义保持，新增11项。`core-v1`由`test_t12_export.py`实际调用`export_core`建立，含trace/checks/readback/operations/manifest；本切片未执行CLI，复现须另给新目录。首次运行已生成core-v1，后续运行只做内存重建一致性校验，不覆盖。

**基线与权限：**基线`4433b09490daf7ce05b344bfd8092982f9025fc8`，分支`codex/task-state-activity-research`；本切片未运行Git、目录shell或网络，未提交、推送或合并，只改任务白名单文件。

**模型与费用：**本切片由DeepSeek执行，DeepSeek本身就是模型调用；token与费用回执未知，按未知记录，不记为零；未运行付费效果实验。Astra独立核查fe00b704的原始工具事件为3次unittest、首次1失败1错误、之后86测试通过、无拒绝工具；该核查与本切片的97项运行是两份证据，不互相替代。

**范围限制：**四组身份替代、其余15段逐段核查和最终对象推荐仍未执行；`core-v1`只证明本切片的结构规则、S029映射和导出链可运行，不证明五类对象边界已最终成立。

### 2026-10-29 第2a1切片：公共引用/采用/生命周期/验收规则

本切片只实现`t12_study.py`的公共规则与`test_t12_continuous.py`控制链，未做四身份替代、图示、其余15段或大实验输出。`ref`只接受现存的正整数revision，拒绝None/bool/0/不存在版本；`version(state,id)`查询当前仍可用。`begin(plan)`兼容为全section初始采用；新增`adopt_plan`按section显式采用确切Plan版本并记录basis与Change号；`change_plan`不自动采用；`produce`的`plan_scope`记录实际使用的scope/版本，缺省时按begin版本解释，旧Product与旧报告不变（2a2已收紧：一旦存在显式采用，缺省`plan_scope`拒绝）。`end`要求`retained_unresolved`，新增`reopen`；三布局的assign/transfer/share新接收者必须active，从ended转出合法。`advance_product`值域受控但允许合法回退；`accept_goal`要求Evidence、非空scope且subject可追踪到同一Goal，拒绝Goal/Product自证与其他目标报告。完整控制链在两种Plan存放方式下运行，批次失败整体回退。

验证：`python -m unittest discover -s Agent任务状态管理/tools/work-operation-checks -v`，86项通过（原77+新9）。本切片由DS执行，DS本身即模型调用；token/费用回执未知，按未知记录，不记为零；未运行付费实验。实际变更与下一缺口见同目录`core-rules-review.md`；失败任务记录见同目录`failed-bc01f64e.json`。

### 上一阶段：T12对象方案首轮比较（2026-10-29）

上一轮批准计划已完成到完整路径、对象图、可执行比较、独立读回与推荐。先读[T12对象研究](t12-object-study.md)，细节在[组合研究](operation-composition-review.md)。阶段提交4901ed9固定路径与骨架，358d92a保存三布局与计划对照；收尾提交从当前HEAD核对。

推荐逻辑对象Goal/Plan/Attempt/Product/Evidence，Change记录转换；这是起点，不是对四个身份选择的最终裁定。单父范围先选parent责任权威；relation/child备选保持。Plan独立版与可寻址内嵌版均保留旧引用，不声称顶层Plan为唯一正确形式；旧引用保留不等同于“原Attempt采用新版”的路径已经成立。旧四入口不等本轮工作操作结论。新增实验在Agent任务状态管理/tools/work-operation-checks/t12_study.py和t12_responsibility.py，原checker/workbench和旧案例未修改。

已执行六事实与源补充重放、三布局同序列、两计划布局、合法/非法更新及整批失败回退。完整回归77项通过；该77项覆盖旧路径，不覆盖本轮列出的六组已测故障。输出当前交付目录从本批manifest确认，使用新目录复现，勿覆盖comparison-v1/delivery-v1。所有记录版不是上游版本；active只表示记录生命周期；六类初始范围到原PR逐hunk的精确分配仍为unknown，S029的item级状态和部分复用是已知事实，不能一并抹为unknown。报告与状态真实性另做来源审阅，不因basisID合法认定工程判断正确。

7个CodeBuddy任务已终止，6个有实质输出，HY第一次审查只有准备阅读一句，已用一个有界补充处理。DS在独立worker中只改两白名单文件，原稿已保留；Sol核对并集成。GLM仅凭冻结输入读回，不访问工具/底稿；旧版Q3计划引用遗漏和GUI措辞差异已裁定，索引修正仅本地验证。Kimi未调用。原始材料、任务ID、预期、读回与裁定均在本工作树artifacts/agent-task-state/maintenance/t12-object-study-2026-10-29/。

上一轮原定下一项工作：在本方案下登记新的真实小步变化，检验对象边界、剩余责任和计划关联的使用负担，再定向跨过程检查。该安排已由后续2a1/2a2切片接替，旧记录保留。没有授权新的模型批次、数据库迁移、DSH运行或付费效果实验。研究仍在codex/task-state-activity-research，worker工作树仅保留原始模型实现，不作接手入口。

## 2026-10-28 历史状态：对象与连续变化研究

用户要求四模型协助构思，本轮已完成。先读[综合裁定](operation-composition-review.md#2026-10-28对象与变化的四模型构思及裁定)，任务材料与产出约定见[统一交接](object-operation-handoff-2026-10-28.md)。DeepSeek V4.1 Flash、HY4 Preview、GLM5.3、Kimi K3.1 Pro均通过CodeBuddy独立读取固定e15f6f4提交、请求effort=max，四任务completed，无重试。原答及任务ID、来源核对和Sol判断保存在本地artifacts/agent-task-state/maintenance/object-review-2026-10-28/。

当前方向由用户明确：先确定开发对象，再由真实变化推导操作，保住整体意图、计划与小步实施的联系。四入口只作为现行记录器接口，不再宣称工作元操作已可靠筛选；v0.5是旧实现依据。parts保留与split连续一致性存在已复现缺口；revise可更新adoption本身只是别名问题，它仍执行scope和引用检查，不能称采用保护失效。

本轮获得三种责任权威布局（父表/独立关系/子项）及Plan、Change的实际分歧。下一项研究是用相同小步变化和保留条件比较布局，随后用T03阶段计划检查Plan身份；不立即扩大系统或另造操作清单。尚未执行三布局比较，尚未修改原型。T14.02不能补成#2217之后的后端升级，T02规则不能补成实际holder事件。用户未授权新的模型批次，后续按明确任务控制调用。

## 2026-10-27 历史交付记录

先读[人类主成果](dsh-work-history.md)、[现行候选v0.5](work-operation-candidates-v0.5.md)，运行方式见[工具说明](../../../tools/work-operation-checks/README.md)。本轮已完成。实现阶段提交05c1f84、a44a401；收尾修正以当前研究分支HEAD为准。

## 历史：截至2026-10-27的可用成果

四个基本入口create/revise/statement/select，八类执行组合partial_revert、replace_parts、split、rework、close、reuse、adopt、correct。已完整表达固定16段、83条来源事实与16条研究缺口；七条跨过程联系与两组内部分解保存为14条可查询关系。五个存储阶段和两个聊天承接范围有独立身份。固定truth v1未改。

工具位于Agent任务状态管理/tools/work-operation-checks/。build生成完整工作台，case支持--object/--revision/--scope/--step；输出目录必须新建。当前本机阅读器：本工作树 artifacts/agent-task-state/maintenance/dsh-workbench-2026-10-27/delivery-final/index.html；同目录有bundle.json与16段逐步Markdown。本地程序回归41项通过，最终页面核验16段切换、指定版本、父子结构、精确端点/事实导航、报告性质、合成采用冲突，以及桌面/窄屏。

## 历史：已经裁定的规则

记录修订、产品发布和运行修订分别保存。选择查询同时提供采用时快照和当前说明；视图取副本，不反写工作状态。未知不等于未完成，未分配不等于未完成，持续限制不自动生成待办。旧保证、旧问题与当前状态有范围；correct精确指向被修正命题，来源报告另存，不因推翻解释而否定报告曾发生。

32个候选编号和去向保留：4核心、14组合/便利、2合并、12待补证。本轮新增可执行实现和规则，核心候选新增0、移除0。v0.4归档，v0.5当时为唯一现行。下一轮按用户指令推进工作视图与上下文压缩后接续，不再默认重枚举名称。

## 历史：验证与来源边界

Sol负责实现、主来源走查和裁定；CodeBuddy起稿包1/2/4并审查Sol起稿包3。首次24条新上下文读回发现旧字段残留与unknown/residual误读；修正后只做四个问题的定向读回，关键区别恢复。定向任务bf697373 completed，JSON原文有孤立case-ID词元，另存仅格式规范化版本，答案文字未改；输入与原答卷保留。记录解释与阅读定义同时修改，不将结果单独归因于某接口。

CodeBuddy固定a44a401审查（c885e691，completed）提出六项实质问题；Sol逐项修复并完成本地回归，最后差异由Sol复查。模型没有运行测试，不把模型审查覆盖范围扩展到后来提交。源码语义判断与程序一致性、图和交互验证分别保存。

包1任务c0282143及初次读回e32075a6为needs_attention，原因是同Git根主Agent并行改文件；已核对路径/工具事件，读回允许输入哈希不变且仅观察到读取input。后续包2=829b5c5e、包4/包3审阅=94ccb24c以及定向/固定提交审查均completed。全部任务已终止，不重复派单。

## 历史：本地复现与接续

本批根目录为本工作树 artifacts/agent-task-state/maintenance/dsh-workbench-2026-10-27/。四包模型原稿、source-walkthrough-final.json、readback-adjudication.json、code-review-adjudication.json、错误探针、普通文档基线与生成输出均保留。readback-v1未派单，v2为首次实际24答；delivery-v1至v4为历史生成物，delivery-final为现行。历史encode-pack3-sol.py、run-probes.py只作原始执行依据，不直接重跑覆盖当前文件；复现使用已提交fixtures与工具README命令并新建输出目录。

CodeBuddy独立工作树artifacts/worktrees/task-state-codebuddy-round1保留冻结输入（HEAD2861b59），不是现行成果入口。正式成果在codex/task-state-activity-research，Git状态实时核对，保护其他项目内容。原始资料截止2026-10-15。本轮未运行DSH和任务效果实验；后续SWE-Milestone与付费实验需另行授权。

成本继续采用Sol加本地脚本、必要的有界CodeBuddy任务；不默认Codex三并发，不重连Qoder，不自动重试失败任务或切换服务。无token/费用回执时记未知。

</details>

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
