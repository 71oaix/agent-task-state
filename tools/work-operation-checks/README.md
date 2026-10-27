# 工作操作与 DSH 演化工作台

在原有版本检查器上，新增可执行组合、指定版本查询和 DSH 过程阅读器。选择一段过程，可以看见来源事实、展开的基本操作、前后版本及未完成责任。

在仓库根目录运行（输出目录必须是新目录，以保留旧结果）：

```powershell
python Agent任务状态管理/tools/work-operation-checks/workbench.py build --out artifacts/agent-task-state/maintenance/dsh-workbench-new
python Agent任务状态管理/tools/work-operation-checks/workbench.py case T01
python Agent任务状态管理/tools/work-operation-checks/workbench.py case T01 --object T01/loader --revision 2
python -m unittest discover -s Agent任务状态管理/tools/work-operation-checks -v
```

打开输出目录中的 `index.html` 可浏览全部过程、组合展开、证据入口、跨工作联系和历史版本；`bundle.json` 保存实际记录与展开，T01.md 等是逐步明细。四个案例包和 [表达契约](EXPRESSION.md) 是可维护输入；固定来源继续从研究底稿读取。来源更新须另存底稿版本。

`expand(state, action, provenance)` 只生成准备包，固定读写前版与精确引用；`apply_prepared` 检查前态并应用；`execute_step` 依序登记来源与展开动作，任一动作失败则整步回退到调用前状态；`run_case` 重放整段。`query` 查询当前或指定版本；按scope查询同时返回采用时快照和该对象的当前说明，后续说明不自动改写采用，`readback_view` 导出隔离读回所用的对象、历史和效果，来源全文可另按权限查证。

组合包括部分撤回、组成替换、责任拆分、接续重做、尝试收束、范围引用/复用、版本采用、判断修正。它们展开为 create/revise/statement/select；每次展开和原子回执都保留。字段中的精确引用表示可追溯关系，来源是否支持工程判断由语义核对承担。

研究者建立的身份是索引；产品设计规则、开发事件、作者报告和实际验收按来源分别保存。status 仍允许各案例的领域描述；本轮优先保住含义，后续根据真实使用再统一领域状态。

<details><summary>原记录检查器接口与兼容规则</summary>


Python 标准库实现的小型确定性检查器，比较语义操作与通用类型更新的显式记录效果。只检查结构约束，不推断文字是否真实、证据是否支持结论，也不评判实验答案。

```powershell
python checker.py apply input.json
python checker.py replay replay.json
python checker.py export state.json
python -m unittest -v
```

API 为 `apply_transaction(state, transaction, expected=None)`、`replay(initial_state, transactions)`、`export_projection(state)`。

`resolve_adoptions(state)` 另行解析实际生效采用状态：adoption 的所有已知版本与 `effective=true` 的 decision 构成节点；同 ID 后续版本替代前版，显式 `supersedes:{id,revision}` 替代同 scope 的指定有效节点。每个 scope 唯一未被替代节点为 resolved；多个独立末端为 conflict，即使 selected 相同也不按插入顺序选胜者。返回 `{scopes:{scope:{status,heads:[{record,selected}]}},errors:[]}`，heads 按 ID/版本确定排序。append-log 应新建 decision 并指明 supersedes；既有 decision 更新 adoption 别名仍保留，供旧夹具兼容。

前驱必须是确切存在的 adoption 或 effective decision，且 scope 相同；自环与包含隐式同 ID 版本边的循环均为非法。解析结构错误时返回空 scopes 和 errors，`apply_transaction` 会据此原子拒绝整个事务；合法分叉本身可写入，由 resolver 显式呈现冲突。该机制只认显式替代关系，历史采用更新与引用其旧版本的新日志会成为两个末端。

`apply` 输入为 `{state, transaction, expected}`。状态包含 `objects: {id: {kind, revision, fields}}` 与 `history: []`；本地 revision 从 1 开始。事务包含 `commands`、`provenance: {source, actor, nature}`，可选 `group` 标识和 `required_targets` 精确目标列表。每条命令仅允许 `op,target,kind,fields,delta,refs`。创建用完整 `fields`，更新用浅层命名字段 `delta`，未指明字段保留；同一事务每个目标仅一条命令。`expected` 必须恰好覆盖所有命令目标，值为现有整数版本或新对象的 `"absent"`。来源版本在 fields 中独立保存，不与本地 revision 换算。

支持 kind 为 work、goal、contract、report、artifact、evidence、statement、observation、judgment、relation、adoption、decision。observation/judgment 也可作为 statement type 的独立 kind 表达。支持 open/close/revise/observe/judge/bind/select 和 create/amend/statement/inline_link/decision。close 仅修改 status/disposition/successor 且要求 status=closed；通用 amend 也不能利用关闭状态修改其他字段。父对象不会自动更新。观察 statement 要有 type=observation、subject、result；判断要有 type=judgment、conclusion、evidence。两者均需事务来源，nature 原样保存。report 普通内容字段开放。

relation 要有 relation/from/to/scope；adoption 与 decision 要有 scope/selected。relation/adoption/decision 的既有 scope 不可修改；普通陈述可修订解释范围，旧记录版保留。decision 可更新已有 adoption 目标并保留其 kind。所有 from/to、selected、successor 及显式 refs 都使用 `{id,revision}`；selected 也可为端点列表。inline_link 仅更新 owner 的 links，列表项使用 relation/from/to/scope。版本必须存在于当前对象、保留历史或同组创建结果中。自由文本中的名称、subject、evidence 和来源标识不会自动成为正式引用；需要额外精确依赖时显式列入 refs。

当对象 fields 声明 allocations 时，responsibilities 为唯一字符串 token 列表，allocations 为 `{childID:[token]}` 映射或 `{target, responsibilities:[token]}` 列表，residual 为剩余 token 列表，overlaps 精确列出重复分配 token。检查目标存在、无未知 token、全部原责任有去处、重叠已声明。不声明 allocations 时不启用此约束，不解析自然语言责任。required_targets 由调用方显式提供，用于发现缺少整个目标的组合；检查器不能凭意图自动发现漏发命令。

成功返回 applied、新状态、changes；历史追加被替换的完整对象快照。失败原子返回 rejected、原状态副本、错误码和空 changes。输入对象不被修改。replay 输入 `{initial_state, transactions:[{transaction,expected}]}`，顺序处理，拒绝的事务不改变后续状态。export 输出 objects/relations/adoptions 公共投影，把 inline links 与 relation、decision 与 adoption 对齐；投影省去本地 revision、来源和历史，原状态仍完整保留。CLI JSON 键排序固定。

这是受限离线原型：不含持久数据库、并发服务、自动真实性/语义支持判断、自由文本责任分析或完整领域模式；结果相等只说明该显式编码下的记录效果相等。

显式 refs 随对象版本保存。修订时省略 refs 继承前版，显式列表替换；旧版保留旧 refs。交付审查补上了这一存留保证，旧实验输出未覆盖，原始提案已用交付版本地重放。

</details>
