# DSH 工作表达输入契约

本文件规定本轮案例和组合动作的可执行输入。`checker.py` 保持原有四个入口与版本规则；`workbench.py` 将组合展开为这些入口，并保存展开过程。

## 案例包

JSON 顶层为 `{"schema":1,"cases":[...]}`。每个案例有 `id`（T01 等）、`title`、`objects`、`steps`。研究者建立的对象身份不是上游原有身份。

`objects` 是身份骨架列表，每项 `{id,kind,fields}`；字段可有 title、status、responsibilities、parts、domain。骨架只放标题、研究范围和明确未知的初态，不提前写入后续事实。ID 一律用 `T01/goal`、`T01/work`、`T01/loader` 等形式；kind 使用 checker 已支持的 goal/work/artifact/contract/statement 等。

`steps` 每项 `{id,facts,actions}`；id 如 T01.S01，facts 是底稿编号列表（如 T01.01）。每条事实恰好在一个步骤出现；Txx.GAP 自动最后登记。顺序表示资料给定的局部可见次序，同源回顾保持回顾归属，不能冒充事件发生顺序。

## 动作

一条 step 可顺序包含多个动作。每个动作单独是原子事务；整个步骤失败时工作台返回步骤前状态。系统保存完整展开，使用者也可先 prepare 后 apply；过期前态仍会拒绝。

| action | 参数与效果 |
|---|---|
| create | id, kind, fields；登记对象首版 |
| revise | id, delta；产生同一对象的新版本，旧版可查 |
| partial_revert | id, withdraw:[part_key], retain:[part_key], reason；对象须已具有 parts 字典。仅把 withdraw 部分改为 withdrawn；retain 部分内容不变；保留其他字段 |
| replace_parts | id, remove:[part_key], retain:[part_key], add:{key:value}, reason；指定旧部分退出、新部分进入，旧版和保留部分继续可查 |
| split | id, children:[{id,title,responsibilities:[token],status}], residual:[token], overlaps:[token]；父 work 须已有完整 responsibilities。原子建立子工作并修订父分配；父状态不自动完成 |
| rework | old, new, goal, reason, reference_scope, new_fields；关闭旧尝试、建立同目标新尝试、建立 historical_reference 关系。reference_scope 只说明历史参考，不承诺代码复用；new_fields 显式提供新尝试的已知状态 |
| close | id, disposition；只改工作关闭状态和处置，不改变父目标 |
| reuse | owner, provider, range, relation；provider 为精确 `{id,revision}` 或当前对象 ID 字符串，由 prepare 固定为精确版本。relation 仅限 implements/uses_contract/reuses_result/historical_reference/depends_on/shared_mechanism/contains。range 明确取用范围；owner.links 追加类型化版本引用 |
| adopt | id, scope, selected:[对象ID或精确版本], reason；创建或修订 adoption。scope 不变；每次明确采用版本，不影响其他 scope |
| correct | id, prior, conclusion, scope, evidence:[事实编号]；prior 是先前 statement；新建 judgment，保留旧陈述，并记录 supersedes 类型关系及具体适用范围 |

四入口可直接使用；组合按已观察到的变化选择。事实只是报告或设计规则时，actions 可为空；此时必须把类型、结果和限制写入相应对象，或由事实陈述保留，不能虚构已经运行的事件。

`parts` 的值使用对象，如 `{"status":"reported_implemented","description":"..."}`。withdrawn 说明退出该记录中的组成范围，不自动断言运行现场已完成清理。status、implementation、verification、acceptance、adoption 分字段保存；未知用 unknown，作者报告带 reported 前缀或归属说明。产品规则对象使用 `domain:"product_design"`；开发工作使用 `domain:"development"`。职责 tokens 由研究者标识，不能扩充来源承诺。

所有动作由 facts 绑定原始来源与报告归属。程序不能从自然语言判断“来源是否支持这次更新”；这由来源核对与隔离读回检验。

## 编码交付要求

逐条事实进入有来源的 statement，并非仅靠复制全文代替语义表达。可执行对象应体现变化的目标、采用、保留、失败和剩余责任。复杂事实可多个动作，同一对象可多次修订。不要为凑动作把产品运行规则变成实际开发授权、暂停、恢复事件。

每包同时给出 `difficulties` 列表：`{case,facts,problem,handling}`。来源未知与表达失败分开。Sol 对原始来源裁定后再运行与修订，编码者自检不算独立读回。

校准规则：决定与落地分别记录；reported_scope 不能提前写成 merged；未知验收不写成尚未开始。资料没有给出细分责任归属时，split 可建立已知承接范围，children.responsibilities 留空、父 residual 保留全部未明确分配项；后续有依据才修订分配。原文明确采用一种设计时，可 adopt 到 documented_design 范围，不需要虚构实际运行实例；产品行为用 contract/artifact 保存。
