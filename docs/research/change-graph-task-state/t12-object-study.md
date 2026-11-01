---
title: T12 开发对象与连续变化
status: active
created: 2026-10-29
updated: 2026-11-01
---

# T12 开发对象与连续变化

**推荐五类逻辑对象：目标、计划、尝试、成果、依据；Change 保存每次变化的前后状态与出处，关系连接对象与范围。** 五类分别承担意图与验收、实施安排、一次有边界的推进、可继续更新的产出、带来源的判断。本轮保留这五类，对象新增 0、合并 0。它把容易压成一个状态的进展拆开：目标可以继续，尝试可以结束；计划可以改版，旧成果仍指旧版；成果可以只推进或撤回一部分；依据可以纠正一条命题而不删旧报告。这是当前实现选择，五类是否最小、顶层是否分成五张表仍开放。

| 对象 | 保存什么 | 独立变化的例子 |
|---|---|---|
| 目标 | 原始范围、验收口径、验收决定 | 整批尝试因性能回退结束，目标仍待验收 |
| 计划 | 实施前或实施中的安排、阶段、精确版本、归属 | 计划局部改版后，旧尝试与旧成果仍指旧版；新尝试显式采用新版 |
| 尝试 | 一次推进的边界、结局、未解决责任 | 同一目标下新尝试接续，旧尝试保持 ended |
| 成果 | 可继续更新的产出、part 定位与局部状态、四项维度、整体进展派生 | 已提交功能保留，草稿仍在 turnstep；撤回只影响列明 part，全部撤回时整体回 unknown |
| 依据 | 带来源的报告、判断、范围与纠正 | 两个假说可分别纠正，旧解释与范围外命题保留 |

五类是分析用的逻辑角色；底层记录仍由对象、版本、Change、关系与 item 组成，是否拆成五张顶层表属于存储选择。Change 记录任一对象一次登记变化的前后状态、依据、性质与实际改动位置；关系按对象与范围连接两端。

![T12 开发路径：目标继续、实施分路与继续验收](figures/t12-development-path.png)

图把目标与要求、整批尝试回退、调整后的三路状态和继续验收放在一条阅读路径上：目标继续，实施路线分开推进，三路并排表示同一目标下的不同成果与验收状态。箭头是叙事顺序，实际对象可以并行、局部撤回或转入新尝试。

![T12 对象主干：目标、计划、尝试、成果与依据](figures/t12-object-backbone.png)

图按目标 → 安排（计划）→ 尝试 → 成果 → 反馈（依据）画出一条引用主干，底部单独放 Change 记录；它表达的是对象之间怎样追踪，而不是唯一的线性流程。计划可属于目标或尝试，成果与依据可以被多个 Change 和关系引用。可编辑图源：[开发路径](figures/t12-development-path.svg)、[对象图](figures/t12-object-backbone.svg)。

## 对象边界

目标是意图与验收，尝试是一次推进；结束尝试不等于完成目标。计划可以属于 Goal 或 Attempt，阶段各有状态；尝试在开始时或之后显式采用某个计划版本，新成果记录实际使用的版本，旧成果仍指旧版。成果的 part 在首次细分时复制当时的共享维度，之后只更新列明 part；整体进展由 present parts 派生并与 part 状态分开，验收仍取成果级判断；全部 part 撤回时整体三项进展回到 unknown，空整组推进在写入前拒绝。依据是带来源的报告或判断；纠正只改具体命题与范围，两个假说可以分别纠正，旧报告和范围外内容继续有效。精确依赖固定对象、版本、范围与外部名称，端点移动后读为 `needs_recheck`。它们能分别变化，是因为各自保存的状态轴不同：目标的验收、计划的版本、尝试的结局、成果的 part 与依据的范围互不替代。

最近一轮补齐的是查询与空状态规则：不含 changes 的接手视图也能按当前或历史 revision 查询对象与内嵌计划；未细分成果在全部 part 撤回后不再复用旧的完成维度。这些和计划归属、局部状态、范围纠正、精确依赖一样，属于记录与查询规则，不构成第六类对象。

## 计划与成果的两种存放方式

计划与成果各做了一次单变量存放对照。强内嵌计划放在宿主 Attempt 的完整 revision 历史里，第二个尝试可以直接引用 `(宿主, revision, section)` 而不复制；强内嵌成果保留 `(attempt, slot)` 的逻辑定位，另一个尝试推进原 slot 时宿主仍可保持 ended，slot 的每个 revision 记录推进者。两组都保留旧文本、旧 revision 与旧报告，内嵌也能保留身份和历史。

推荐独立存放，理由落在引用和生命周期：计划与成果的引用不需要宿主存在；改计划只推进 Plan revision，不推进尝试版本；结束尝试也不产生新的计划版本；删除或归档宿主不带走成果历史。内嵌省掉顶层 ID，代价是逐版保留宿主 revision、逐 slot 保留 revision 与推进者，并把定位绑在宿主上。整份删除宿主只是存放依赖的边界探针，正常工作不会这样删除历史，不能单独证明独立对象必需。C2 的 `(attempt, slot)` 仍是逻辑身份；技术详情里的 0 指没有独立顶层记录，不是没有身份。依据并入 Change、目标与尝试合并的对照未发现行为差异。

## T12 六条事实与合成接续

T12.01—06 六条固定事实都在历史锚点内：原始范围、整批回退、分开推进、提交与草稿并存、分组基础、检查与待验收。其后的接续是合成的：身份比较的两组走完计划局部改版 → 原尝试显式采用 → 新成果按采用版本登记 → 旧报告仍指旧成果 → 结束并交代剩余责任，并继续到结束后的第二次尝试；`handoff-v1` 从历史锚点续接计划改版、显式采用、新成果与报告，并把快照整理成单一分支。两者都标 `SYN:`、nature 为 synthetic，不是 DSH 事件。其中第二个尝试（A2）推进同一成果并记录推进者属于 C2 比较外壳；核心的成果推进入口只更新维度，推进者由比较记录保存。

## 其余十五段

其余十五段（T01—T11、T13—T16）做了静态语义回查：这些事实都能放进五类加 Change 的图式，没有段落要求新增第六个顶层类型；当前实现的缺口在关系词汇与个别更新规则。T03 的计划阶段、T13 的判断纠正、T15 的精确依赖另有可执行检查，分别固定了计划可先于尝试、纠正限定范围、依赖固定对象/版本/范围三条规则。产品运行规则作为成果内容记录，不实现 job、queue 或 Goal 授权。

## 操作怎样组合

当前核心支持三类组合。计划改版后，原尝试显式采用新版，新成果按采用版本登记：`migration-plan` 从 rev1 改到 rev2，`draft-continuation-v2` 的 turnstep section 记录 rev2，旧成果 `draft-code` 仍指 rev1，报告 `channel-checks` 继续指向 `independent` rev1。局部撤回只撤回列明 part，其他 part、其他成果、旧 revision 与旧报告保留；全部撤回时整体进展回 unknown，空的整组更新被拒绝。依据先保存带范围的旧解释，再按范围纠正一条命题；另一个假说仍可单独纠正，旧报告保留。跨尝试推进同一成果属于 C2 比较，核心入口只改维度，不记录 producer。

本轮改动集中在计划归属、成果局部状态、依据纠正与精确依赖，以及上述查询和空状态规则。接手者能恢复当前工作，新增变化的依据仍需要审查；这是当前可用的实验性记录机制。T12 研究到此完成，成果保存到 `853d073`；下一轮用一个真实 Agent 小任务实际接续，观察这些规则在连续小步里是否仍然直接，而不是继续完善固定 T12 材料。全部材料本地存档入口为 [t12-object-stage-2026-11-01](../../../../artifacts/agent-task-state/archives/t12-object-stage-2026-11-01/)，归档由主调度审核脚本后执行，打包范围、逐文件哈希与链接核对以该目录 `manifest.json`、`verification.json` 为准。

复现、逐组结果、最终审查回执与读回差异见[本轮组合记录](operation-composition-review.md#2026-10-30五类对象推荐与操作组合)，实现入口见[离线检验说明](../../../tools/work-operation-checks/README.md)。

<details><summary>技术详情：四组存放对照、成本、逐段回查、固定事实、最终审查与操作入口</summary>

### 四组存放方式对照

| 组 | 只改的存放 | 可执行观察 | 对推荐的作用 |
|---|---|---|---|
| C1 计划 | 独立 Plan 记录 vs 宿主 Attempt 完整 revision 历史内嵌 | A2 直接引用 A 的精确旧版 section，不复制；计划修改与无关生命周期都推进宿主 revision | 内嵌可复用；独立存放让计划引用更窄、计划版本不与宿主版本绑定 |
| C2 成果 | 独立 Product 记录 vs 宿主 Attempt 内的结果 slot | A2 推进 A 的原 slot，A 保持 ended；逻辑定位 `(attempt, slot)` 不变，slot revision 记录 producer | 内嵌可续写且保留历史；独立存放让引用不依赖宿主、生命周期分开 |
| C3 依据 | 独立 Evidence 对象 vs Change 内稳定 statement locator | 共同链、合法/非法探针与删除探针未发现行为差异 | 可保留在 Change 内；独立身份条件性 |
| C4 目标/尝试 | 分开 vs 合并为一个 Work 记录 | 未发现行为差异；合并记录仍需 attempt key/status | 不据此证明必须分开 |

成本只计数可执行结构：C1 B 保留 6 个宿主 revision、0 个独立顶层 plan 记录，逻辑定位仍是 `(attempt, revision, section)`；C2 B 保留 2 个 slot、6 个 slot revision、0 个独立顶层 product 记录，逻辑身份仍是 `(attempt, slot)`；单次变化最多触及 5 个记录。内嵌需要逐版保留宿主 revision、逐 slot 保留 revision 与 producer，独立对象需要 ID、版本与第二条更新路径；两者都不是免费。

### 十五段静态回查

| 范围 | 结果 |
|---|---|
| T01—T11、T13—T16，77 条事实 | 静态语义回查；五类加 Change 均可放置，没有段落证明必须新增第六个顶层类型；T03/T13/T15 有可执行边界 |
| T03 计划阶段 | phase 1—5 可无 Attempt；Plan 可关联 Goal 或 Attempt |
| T13 判断修正 | 旧解释与纠正证据均可引用；纠正限定 scope，旧报告保留；多个假说可按范围分别纠正 |
| T15 精确依赖 | 固定 object、revision、scope 与 external name；version/digest 记为值或 unknown；端点移动读为 `needs_recheck` |
| T12 六条事实 | 不进入本轮十五段逐条回查；对象比较与合成链见 `identity-v2`、`handoff-v1` |
| 旧 16 段工作台 | 历史记录器执行结果；不能冒充本轮新链 |

### T12 固定事实

| 可见材料 | 变化 | 必须继续保留 |
|---|---|---|
| T12.01：原PR六类范围 | 登记迁移工作范围 | 精确目标/验收未完整披露，不由研究者补全 |
| T12.02：作者报告性能回退 | 整批合入被回退，旧基准未覆盖新热路径 | 需求范围、原PR参考、报告归属 |
| T12.03：分开推进 | 独立功能留channel，其余草稿在turnstep | 架构提案与实施结果各自存在 |
| T12.04：提交与草稿并存 | 记录独立成果、草稿与所在工作范围 | 每项进度与验收分别判断 |
| T12.05：分组基础 | 基础已有实现，产品分组仍未完成 | 基础成果不自动完成产品分组行为与性能要求 |
| T12.06：检查与验收 | 保存作者报告的 build/lint/coverage 检查结果 | 真实模型 GUI 演示与性能测量仍待完成 |

固定来源补充取自同一 S029 版本：完成、实施、暂存/提交、验收分别记录；迁移进度笔记不替代架构提案；ordinary Context hiding 与 trigger notifications 的产品依赖已登记为 `product_requirement` 关系（`S029.dep.9context-on-8`、`S029.dep.8-on-turn-inputs`），可按 item/scope 查询，关系不表示完成或验收。来源原文和批次元数据在 `artifacts/agent-task-state/maintenance/t12-object-study-2026-10-29/`；本轮存放对照见 [`identity-v2/review.md`](../../../../artifacts/agent-task-state/maintenance/t12-continuous-validation-2026-10-29/identity-v2/review.md)，十五段回查见 [`coverage-v2/adjudication.md`](../../../../artifacts/agent-task-state/maintenance/t12-continuous-validation-2026-10-29/coverage-v2/adjudication.md)，边界执行见 [`boundary-v2/adjudication.md`](../../../../artifacts/agent-task-state/maintenance/t12-continuous-validation-2026-10-29/boundary-v2/adjudication.md)，接续包见 [`handoff-v1/adjudication.md`](../../../../artifacts/agent-task-state/maintenance/t12-continuous-validation-2026-10-29/handoff-v1/adjudication.md)。

### 最终审查与失败记录

Kimi 在冻结提交 3369 上的静态审查（任务 `9d11c98e`）指出两项缺陷：不含 changes 的视图无法用 `version` 查询，以及全部 part 撤回后未细分成果仍报告完成并允许空整组推进。主调度核对源码后修正；上一任务在修正前先复现了 2 项断言失败与 3 项视图 `KeyError`，修正后本次独立上下文 180 项全部通过。上一任务保存的原始失败回执与语义裁定见 [`results.json`](../../../../artifacts/agent-task-state/maintenance/t12-continuous-validation-2026-10-29/final-review-v1/results.json) 和 [`adjudication.md`](../../../../artifacts/agent-task-state/maintenance/t12-continuous-validation-2026-10-29/final-review-v1/adjudication.md)；本次新上下文运行结果见 [`verification.md`](../../../../artifacts/agent-task-state/maintenance/t12-continuous-validation-2026-10-29/final-review-v1/verification.md)。GLM 第二次读回、依据纠正与工具 HEAD 偏差见 [`handoff-v2/adjudication.md`](../../../../artifacts/agent-task-state/maintenance/t12-continuous-validation-2026-10-29/handoff-v2/adjudication.md) 和组合记录。

### 当前操作入口

| 用途 | 当前入口 | 作用与限制 |
|---|---|---|
| 目标 | `goal` / `accept_goal` | 建立范围与验收；验收需显式角色、标准与同一目标的依据 |
| 计划 | `plan` / `change_plan` / `adopt_plan` | 计划可属 Goal 或 Attempt；改版生成新 revision；显式采用写在尝试上，指向精确版本与 section |
| 尝试 | `begin` / `end` / `reopen` | `begin` 可带初始计划；`end` 在仍有未交代责任时要求披露；`reopen` 保留前次结局 |
| 成果 | `produce` / `advance_parts` / `advance_product` / `withdraw_parts` | `produce` 记录 `plan_usage`；`advance_parts` 可只列部分，细分后 `advance_product` 要求整组；两者只改维度，不记录 producer；`withdraw_parts` 只改列明 part |
| 依据 | `report` / `correct_interpretation` | `report` 可带 content_kind/scope_ids；纠正只接受 interpretation，scope 必须在旧命题内，旧报告不改 |
| 责任 | `assign` / `transfer` / `share` / `unassign` / `unknown` | 责任 token 与 holder；转交、共享与未知分开 |
| 关系 | `relate` / `relate_exact` / `relations_for` / `relations_for_item` | `relate` 只支持 product_requirement；`relate_exact` 只支持 delivery_dependency，固定对象/revision/scope 与外部版本；端点移动读 `needs_recheck` |
| 查询 | `version` / `at` / `part_progress` / `interpretations` / `relation_status` / `s029_items` | 精确版本、历史位置、part 派生、解释历史、关系状态与 S029 投影；`version` 可直接用于不含 changes 的视图 |
| 事务 | `apply` | 检查 expected head，整批执行或回退；语义判断在对象入口 |

代码位置：`Agent任务状态管理/tools/work-operation-checks/t12_study.py`；跨尝试身份比较在 `t12_identity_trials_v2.py`，接续包在 `t12_handoff.py`，边界检查在 `t12_boundary_checks.py`，最终审查在 `test_t12_final_review.py`。

上一轮三责任布局与两计划存放方式的执行依据，保留在[组合研究的历史节](operation-composition-review.md#2026-10-29t12对象方案与可执行比较)。

</details>
