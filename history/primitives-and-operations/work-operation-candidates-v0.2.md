
# 工作操作候选 v0.2：七个接口、组合动作与待证项目

状态：已归档

**当前选择七个工作接口作为骨架，十一项优先采用组合表达，十二项继续补证。**本页为历史版本，现行清单见[工作操作 v0.3](work-operation-candidates-v0.3.md)；[人类结论](../experiments/operation-composition/work-operation-rounds-v0.1.md)解释取舍，[分轮证据](../experiments/operation-composition/work-operation-rounds-v0.1-evidence.md)保存删减、失败与读回。

## 七个工作接口分别改变什么

| 接口 | 作用 | 需要保留的规则 | 来源见证 |
|---|---|---|---|
| `open` | 开启一次可独立跟踪的工作 | 工作身份、目标归属与初始责任；历史创建时间可未知 | [T14.03](../experiments/dsh-process/dsh-process-truth-v1.md#t14) |
| `revise` | 修订同一对象的成果 | 前版、改变与保留范围；产生后继，采用另记 | [T01.02](../experiments/dsh-process/dsh-process-truth-v1.md#t01)、[T01.03](../experiments/dsh-process/dsh-process-truth-v1.md#t01)、[T01.04](../experiments/dsh-process/dsh-process-truth-v1.md#t01) |
| `close` | 收束指定工作尝试 | 停止推进、处置与后继；父目标状态独立 | [T14.03](../experiments/dsh-process/dsh-process-truth-v1.md#t14) |
| `observe` | 留下可查的观察 | 对象、方法、结果、时间与报告归属；观察与解释分别保存 | [T13.02](../experiments/dsh-process/dsh-process-truth-v1.md#t13)、[T13.03](../experiments/dsh-process/dsh-process-truth-v1.md#t13)、[T13.04](../experiments/dsh-process/dsh-process-truth-v1.md#t13) |
| `judge` | 形成或修正判断 | 证据、前提、适用范围与取代的旧判断 | [T13.01](../experiments/dsh-process/dsh-process-truth-v1.md#t13)、[T13.02](../experiments/dsh-process/dsh-process-truth-v1.md#t13)、[T13.03](../experiments/dsh-process/dsh-process-truth-v1.md#t13) |
| `select` | 改变一个范围内的采用 | 原采用、新采用、决定及冲突；持有旧版的范围另存 | [T09.02](../experiments/dsh-process/dsh-process-truth-v1.md#t09)、[T13.04](../experiments/dsh-process/dsh-process-truth-v1.md#t13) |
| `bind` | 绑定有明确含义的联系 | 如使用契约、分配责任、证据支持；端点、版本与范围固定 | [T13.05](../experiments/dsh-process/dsh-process-truth-v1.md#t13)、[T12.03](../experiments/dsh-process/dsh-process-truth-v1.md#t12) |

身份分配与继续同一工作的判断由调用者声明并留依据。接口处理记录及其一致性；来源报告、研究归纳、实际执行分别归属。已有观察与工件版本继续可查，当前采用按具体范围解释。

## 十一项组合设计

下表记录工作含义的展开。步骤由证据决定：原因未知可没有 judge，未报告采用可没有 select，检查未进行可保留待检查。原始来源缺少的动作不自动补齐。

| 动作 | 操作组合 | 必须保留的含义 | 依据 |
|---|---|---|---|
| `split` | 开启子工作 → 绑定分配责任 → 修订父项残余 | 分配前责任、子范围、重叠/未决、父判据与一致逻辑组 | [T12.03](../experiments/dsh-process/dsh-process-truth-v1.md#t12)、[T12.05](../experiments/dsh-process/dsh-process-truth-v1.md#t12)、[T03.06](../experiments/dsh-process/dsh-process-truth-v1.md#t03) |
| `review` | 观察被评审对象 → 形成评审判断 | 评审对象、评审角色、依据、适用范围；不改变采用 | [T11.03](../experiments/dsh-process/dsh-process-truth-v1.md#t11)、[T09.02](../experiments/dsh-process/dsh-process-truth-v1.md#t09) |
| `decide` | 记录理由和意图 → 按实际效果组合采用、收束、开启或修订 | 意图与已报告效果分开；按来源决定可选步骤 | [T14.03](../experiments/dsh-process/dsh-process-truth-v1.md#t14)、[T04.02](../experiments/dsh-process/dsh-process-truth-v1.md#t04) |
| `verify` | 观察检查方法与结果 → 按明确判据给结论 | 对象版本、方法、判据、未覆盖范围和报告者；接受另记 | [T12.06](../experiments/dsh-process/dsh-process-truth-v1.md#t12)、[T13.04](../experiments/dsh-process/dsh-process-truth-v1.md#t13)、[T14.04](../experiments/dsh-process/dsh-process-truth-v1.md#t14)、[T15.05](../experiments/dsh-process/dsh-process-truth-v1.md#t15) |
| `revert` | 有理由时保存判断 → 修订撤回/保留范围 → 有采用依据时更新采用 | 局部撤回、后续独立修补、未知原因均保留 | [T01.02](../experiments/dsh-process/dsh-process-truth-v1.md#t01)、[T01.03](../experiments/dsh-process/dsh-process-truth-v1.md#t01)、[T03.02](../experiments/dsh-process/dsh-process-truth-v1.md#t03)、[T12.02](../experiments/dsh-process/dsh-process-truth-v1.md#t12) |
| `adapt` | 绑定变化后的契约 → 修订消费者 → 有检查结果时留观察 | 兼容判断及取用范围由调用者提供；未见证步骤留缺口 | [T01.04](../experiments/dsh-process/dsh-process-truth-v1.md#t01)、[T01.05](../experiments/dsh-process/dsh-process-truth-v1.md#t01)、[T14.02](../experiments/dsh-process/dsh-process-truth-v1.md#t14)、[T14.04](../experiments/dsh-process/dsh-process-truth-v1.md#t14) |
| `repair` | 观察故障 → 有依据时修正判断 → 修订成果 → 记录检查或再失败 | 保留旧解释、失败修补及新证据；不补造每一步 | [T10.03](../experiments/dsh-process/dsh-process-truth-v1.md#t10)、[T10.04](../experiments/dsh-process/dsh-process-truth-v1.md#t10)、[T10.05](../experiments/dsh-process/dsh-process-truth-v1.md#t10)、[T13.01](../experiments/dsh-process/dsh-process-truth-v1.md#t13)、[T13.04](../experiments/dsh-process/dsh-process-truth-v1.md#t13) |
| `replace` | 修订组成 → 绑定新使用关系 → 有采用依据时更新采用 | 旧新范围与兼容/历史去向；名单任务等独立部分保留 | [T04.02](../experiments/dsh-process/dsh-process-truth-v1.md#t04)、[T04.04](../experiments/dsh-process/dsh-process-truth-v1.md#t04)、[T04.05](../experiments/dsh-process/dsh-process-truth-v1.md#t04)、[T05.04](../experiments/dsh-process/dsh-process-truth-v1.md#t05) |
| `retire` | 修订可用范围 → 调整新选择 → 保留仍有效的持有或接口联系 | 提供者退出、旧运行修订退役和工作收束分别限定对象 | [T07.03](../experiments/dsh-process/dsh-process-truth-v1.md#t07)、[T07.04](../experiments/dsh-process/dsh-process-truth-v1.md#t07)、[T02.04](../experiments/dsh-process/dsh-process-truth-v1.md#t02) |
| `integrate` | 绑定来源及取用范围 → 修订目标 → 记录变化后的前提与检查 | 捕获侧可复用，旧外发承诺不自动继承；代码取用范围未知另记 | [X1](../experiments/operation-composition/work-operation-rounds-v0.1-evidence.md#补查来源) |
| `release` | 观察发布报告或实际结果 → 绑定包、版本及渠道依据 → 有渠道变化时更新采用 | tag、发布成功、渠道采用分开；未知回执不得补造 | [X2](../experiments/operation-composition/work-operation-rounds-v0.1-evidence.md#补查来源) |

## 三十项完整去向

名称全部保留，未作同义词合并。十一项移出优先核心竞争，作为组合设计继续检验；来源与调用参数缺口列在依据中。

| 编号 | 候选 | 当前状态 | 原因及检验方向 |
|---|---|---|---|
| C01 | `open` | 保留为核心候选 | 工作身份、目标归属与初始责任；历史创建时间可未知 |
| C02 | `propose` | 待补证 | 当前主要是 proposed 状态与 PR 范围；首次提议事件、后续处置尚未展开。|
| C03 | `revise` | 保留为核心候选 | 前版、改变与保留范围；产生后继，采用另记 |
| C04 | `fork` | 待补证 | 分支存在不足以说明两条独立工作路线的共同起点；需适当见证。|
| C05 | `split` | 作为组合动作 | 开启子工作 → 绑定分配责任 → 修订父项残余；分配前责任、子范围、重叠/未决、父判据与一致逻辑组 |
| C06 | `integrate` | 作为组合动作 | 绑定来源及取用范围 → 修订目标 → 记录变化后的前提与检查；捕获侧可复用，旧外发承诺不自动继承；代码取用范围未知另记 |
| C07 | `close` | 保留为核心候选 | 停止推进、处置与后继；父目标状态独立 |
| C08 | `observe` | 保留为核心候选 | 对象、方法、结果、时间与报告归属；观察与解释分别保存 |
| C09 | `review` | 作为组合动作 | 观察被评审对象 → 形成评审判断；评审对象、评审角色、依据、适用范围；不改变采用 |
| C10 | `judge` | 保留为核心候选 | 证据、前提、适用范围与取代的旧判断 |
| C11 | `decide` | 作为组合动作 | 记录理由和意图 → 按实际效果组合采用、收束、开启或修订；意图与已报告效果分开；按来源决定可选步骤 |
| C12 | `select` | 保留为核心候选 | 原采用、新采用、决定及冲突；持有旧版的范围另存 |
| C13 | `implement` | 待补证 | 实施尝试、实际产出与失败之间的映射不完整，撤销机械 observe+revise 展开。|
| C14 | `land` | 待补证 | 需指定集成目标与合入效果；合入、采用、验收分别记录，撤销固定三步展开。|
| C15 | `verify` | 作为组合动作 | 观察检查方法与结果 → 按明确判据给结论；对象版本、方法、判据、未覆盖范围和报告者；接受另记 |
| C16 | `accept` | 待补证 | 缺有权主体依据判据接受结果的事件。|
| C17 | `revert` | 作为组合动作 | 有理由时保存判断 → 修订撤回/保留范围 → 有采用依据时更新采用；局部撤回、后续独立修补、未知原因均保留 |
| C18 | `adapt` | 作为组合动作 | 绑定变化后的契约 → 修订消费者 → 有检查结果时留观察；兼容判断及取用范围由调用者提供；未见证步骤留缺口 |
| C19 | `repair` | 作为组合动作 | 观察故障 → 有依据时修正判断 → 修订成果 → 记录检查或再失败；保留旧解释、失败修补及新证据；不补造每一步 |
| C20 | `migrate` | 待补证 | 主要见证迁移契约；实际实例、拒绝结果与产出映射尚缺。|
| C21 | `bind` | 保留为核心候选 | 如使用契约、分配责任、证据支持；端点、版本与范围固定 |
| C22 | `release` | 作为组合动作 | 观察发布报告或实际结果 → 绑定包、版本及渠道依据 → 有渠道变化时更新采用；tag、发布成功、渠道采用分开；未知回执不得补造 |
| C23 | `replace` | 作为组合动作 | 修订组成 → 绑定新使用关系 → 有采用依据时更新采用；旧新范围与兼容/历史去向；名单任务等独立部分保留 |
| C24 | `retire` | 作为组合动作 | 修订可用范围 → 调整新选择 → 保留仍有效的持有或接口联系；提供者退出、旧运行修订退役和工作收束分别限定对象 |
| C25 | `constrain` | 待补证 | 多为常设规则；规则的制定、修订和生效事件尚未厘清。|
| C26 | `followup` | 待补证 | 待办状态不直接说明已创建承接工作，需独立身份与责任依据。|
| C27 | `execute` | 待补证 | 上位外部行动概念，需明确它与实施、合入、检查的共同输入输出。|
| C28 | `authorize` | 待补证 | 产品权限与审批环境不等于一项开发执行许可；当前缺正向见证。|
| C29 | `suspend` | 待补证 | 延后某功能的决定尚未说明同一工作的暂停处置与恢复条件。|
| C30 | `resume` | 待补证 | 重新取用旧设计可另开工作，尚缺同一工作身份恢复推进的见证。|

## 替代规则与下一步

七个接口都有强替代：用类型化版本记录保存身份、终止和判断，用有效决策日志恢复采用，用内嵌关系保存依赖。对应规则仍要实现。比较范围因此是“接口 + 对象 + 规则 + 调用者判断”，不只比较函数数量。

下一阶段先完成 T14 的一张完整转换表：对象身份、前版、改变、保留、后继、来源归属、未知和拒绝条件都落到具体值。通过后，将相同规则用于 T12 责任拆分和 T02 采用范围，再确定离线检查原型。当前阻止直接实施的缺口是：部分步骤仍只有操作注释，尚未形成完整调用映射。

本版依据 16 段来源整理及三份定向补查；组合为有条件的设计建议。具体程序拒绝规则、维护时间和长程任务收益留待原型与后续效果实验检验。
