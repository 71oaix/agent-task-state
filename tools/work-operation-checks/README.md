# 离线记录更新检查器

Python 标准库实现的小型确定性检查器，比较语义操作与通用类型更新的显式记录效果。只检查结构约束，不推断文字是否真实、证据是否支持结论，也不评判实验答案。

```powershell
python checker.py apply input.json
python checker.py replay replay.json
python checker.py export state.json
python -m unittest -v
```

API 为 `apply_transaction(state, transaction, expected=None)`、`replay(initial_state, transactions)`、`export_projection(state)`。

`apply` 输入为 `{state, transaction, expected}`。状态包含 `objects: {id: {kind, revision, fields}}` 与 `history: []`；本地 revision 从 1 开始。事务包含 `commands`、`provenance: {source, actor, nature}`，可选 `group` 标识和 `required_targets` 精确目标列表。每条命令仅允许 `op,target,kind,fields,delta,refs`。创建用完整 `fields`，更新用浅层命名字段 `delta`，未指明字段保留；同一事务每个目标仅一条命令。`expected` 必须恰好覆盖所有命令目标，值为现有整数版本或新对象的 `"absent"`。来源版本在 fields 中独立保存，不与本地 revision 换算。

支持 kind 为 work、goal、contract、report、artifact、evidence、statement、observation、judgment、relation、adoption、decision。observation/judgment 也可作为 statement type 的独立 kind 表达。支持 open/close/revise/observe/judge/bind/select 和 create/amend/statement/inline_link/decision。close 仅修改 status/disposition/successor 且要求 status=closed；通用 amend 也不能利用关闭状态修改其他字段。父对象不会自动更新。观察 statement 要有 type=observation、subject、result；判断要有 type=judgment、conclusion、evidence。两者均需事务来源，nature 原样保存。report 普通内容字段开放。

relation 要有 relation/from/to/scope；adoption 与 decision 要有 scope/selected。已有 scope 不可修改。decision 可更新已有 adoption 目标并保留其 kind。所有 from/to、selected、successor 及显式 refs 都使用 `{id,revision}`；selected 也可为端点列表。inline_link 仅更新 owner 的 links，列表项使用 relation/from/to/scope。版本必须存在于当前对象、保留历史或同组创建结果中。自由文本中的名称、subject、evidence 和来源标识不会自动成为正式引用；需要额外精确依赖时显式列入 refs。

当对象 fields 声明 allocations 时，responsibilities 为唯一字符串 token 列表，allocations 为 `{childID:[token]}` 映射或 `{target, responsibilities:[token]}` 列表，residual 为剩余 token 列表，overlaps 精确列出重复分配 token。检查目标存在、无未知 token、全部原责任有去处、重叠已声明。不声明 allocations 时不启用此约束，不解析自然语言责任。required_targets 由调用方显式提供，用于发现缺少整个目标的组合；检查器不能凭意图自动发现漏发命令。

成功返回 applied、新状态、changes；历史追加被替换的完整对象快照。失败原子返回 rejected、原状态副本、错误码和空 changes。输入对象不被修改。replay 输入 `{initial_state, transactions:[{transaction,expected}]}`，顺序处理，拒绝的事务不改变后续状态。export 输出 objects/relations/adoptions 公共投影，把 inline links 与 relation、decision 与 adoption 对齐；投影省去本地 revision、来源和历史，原状态仍完整保留。CLI JSON 键排序固定。

这是受限离线原型：不含持久数据库、并发服务、自动真实性/语义支持判断、自由文本责任分析或完整领域模式；结果相等只说明该显式编码下的记录效果相等。

