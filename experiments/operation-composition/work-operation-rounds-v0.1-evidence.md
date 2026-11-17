
# 工作操作分轮检验：输入、替代规则与裁定

状态：已归档

本页保存候选集合的变化依据；人类结论见[分轮收敛](work-operation-rounds-v0.1.md)。固定输入仍为[16 段底稿](../dsh-process/dsh-process-truth-v1.md)，截止 2026-10-15。本地批次：`artifacts/agent-task-state/maintenance/dsh-primitives-2026-10-23/`。操作序列是研究重构；未知工件基线的记录按来源陈述保存，不冒充实际 API 执行。

## 第一轮：尝试身份与生命周期

两种表达都允许精确子记录。A 使用同目标整体版本，B 使用开启、修订、收束等工作动作；普通文档拥有同样状态、引用和证据。三者共享规范化历史，控制信息差异。

首批 Qoder 分别编码 A、B、核对 S031/S025 全文；主 Agent 先存 `main-before.json`，核对后形成 `adjudication.json`。首批删减把去掉接口同时做成去掉事实，第二批明确允许类型化 revise 的强替代，分别接手读回、删减、跨案例核对。

| 检查 | 结果与取舍 |
|---|---|
| 尝试身份 | T14 旧分支关闭而用户目标继续，新 UI 使用既有后端；身份可以独立也可嵌套，须能精确引用 |
| 删除 open | 用类型化身份声明代替；仍需新身份唯一性、目标归属、原创建时间未知、研究声明归属 |
| 删除 close | 用类型化状态修订代替；仍需指定目标、原状态、处置理由、后继引用和不影响父目标的规则 |
| 删除 revise | T01 的选择性撤回仍需同成果前后状态、改变范围和保留映射；open/close 无法单独表达 |
| 使用 fork | 两案均缺确定共同起点与独立推进证据，保持待补证 |
| 普通文档 | 精确子项和状态足以表达本轮；维护耗时未测量，不据条数声称更省 |

第二批读者共回答 12 个语义问题，主 Agent 判 10 项主要含义准确、2 项部分：T01 工作目标未完全显式、读者把没有明确未完扩大为没有未完。三种包装共用历史，读者一次回答后对照包装，不计作 36 次独立读回。观察/实现报告、最终接受、常设契约和当前待办继续分开。

复核不采纳：强制把每个 #932 提交集升级为独立工作；因摘要没有同句出现而否认 S031 明确的后端契约关系；因没有独立运行而否认来源报告。S025 的具体修补名在首批全文可查，第二批仅有摘要的审查者需要额外查证，记为权限内信息差异。

首批 A 返回缺一个 JSON 右括号；删减路返回未闭合前段后重复完整对象。原输出保留，解析修复另存，未改变模型结论。首批父目录扫描有拒绝，但任务目录 input 已读取；后批增加本目录指引，只读本目录，不扩大权限。

### 候选起点：30 项完整保留

| 编号 | 候选 | 第一轮去向 |
|---|---|---|
| C01 | `open` | 明确工作接口边界，继续检验 |
| C02 | `propose` | 保留，按计划后续检验 |
| C03 | `revise` | 明确工作接口边界，继续检验 |
| C04 | `fork` | 待证共同起点与独立推进 |
| C05 | `split` | 保留，按计划后续检验 |
| C06 | `integrate` | 保留，按计划后续检验 |
| C07 | `close` | 明确工作接口边界，继续检验 |
| C08 | `observe` | 保留，按计划后续检验 |
| C09 | `review` | 保留，按计划后续检验 |
| C10 | `judge` | 保留，按计划后续检验 |
| C11 | `decide` | 保留，按计划后续检验 |
| C12 | `select` | 保留，按计划后续检验 |
| C13 | `implement` | 保留，按计划后续检验 |
| C14 | `land` | 保留，按计划后续检验 |
| C15 | `verify` | 保留，按计划后续检验 |
| C16 | `accept` | 保留，按计划后续检验 |
| C17 | `revert` | 保留，按计划后续检验 |
| C18 | `adapt` | 保留，按计划后续检验 |
| C19 | `repair` | 保留，按计划后续检验 |
| C20 | `migrate` | 保留，按计划后续检验 |
| C21 | `bind` | 保留，按计划后续检验 |
| C22 | `release` | 保留，按计划后续检验 |
| C23 | `replace` | 保留，按计划后续检验 |
| C24 | `retire` | 保留，按计划后续检验 |
| C25 | `constrain` | 保留，按计划后续检验 |
| C26 | `followup` | 保留，按计划后续检验 |
| C27 | `execute` | 保留，按计划后续检验 |
| C28 | `authorize` | 保留，按计划后续检验 |
| C29 | `suspend` | 保留，按计划后续检验 |
| C30 | `resume` | 保留，按计划后续检验 |

## 第二轮 A：责任拆分

T12 比较独立 split 与 open 子工作、bind 分配责任、revise 父项残余；T03 五阶段作为接续检查。三种表示共享事实，读者六问主要范围准确。责任、状态、证据分别可引用；T03 首次拆分事件仍未知。

**split 转为组合动作候选。**替代必须保留分配前责任、子项范围、父项残余、父验收判据引用、未知分区和一致发布的逻辑组。未穷尽分配可显式保留，不能自动推断分配范围并集等于全部目标。

Qoder 指出 B 接口没重列判据是有效的调用约定缺口，规则补上；共同 history 已保存子状态，不能误判删除。专用 split 也没有天然的原子保证，本轮保留逻辑组一致性，不据此要求实现数据库回滚。来源补读提供性能对比与阶段依赖细节，按补充记录保存，不改冻结底稿。

候选变化：split 从核心竞争项转为组合动作候选；新增 0、删除 0。局部结论将回查全部 16 段。下一项检查采用范围。

## 第二轮 B：采用范围

T02/T08 对照独立 select 与有效决定日志重放。六问中五项主要范围准确，一项部分：读者把缺具体运行事件扩大成 T08 也没有报告的合入/采用。保留来源报告与运行实例的区别。

**select 继续保留为范围内采用接口候选。**替代日志须同时保留建议/采用状态、scope、prior/next、生效时间或未知、同范围冲突及跨范围约束。旧运行修订由持有者保留，新定义控制新绑定，重启另按身份解析；三个范围可以同时有效。

Qoder 删减路把 select 想成只读 what-if，从而添加并不存在的查询优势，此项不采纳。判据是采用效果能否保留；采用可以由有效决策日志实现。T08 的工作流、模型调用者与外部提供者分属不同维度，关系类型不能压成单一 scope 字符串。

两轮累计：split 转为组合动作；其余 29 项保留各自检验状态。主 Agent 为完整规则提出 7 个工作层核心候选 open/revise/close/observe/judge/select/bind，进入全部过程与强删减检查。它们的强替代规则全部计入，不按入口数量声称最小。

## 第三轮：全部过程与机械展开的纠正

首批三路分别审查成果变化、知识与采用、实施与交付。主 Agent 在读结果前保存候选组合和 16 段表示。模型发现，原 proposed_expansion 只有操作名，没有逐次目标、前后范围和参数绑定；land/implement 固定展开为 revise，decide 只展开为 judge，会掩盖外部动作、状态快照和决定效果。

主 Agent 采纳这些问题，保留原稿，产生 corrected-all16-v2：每条分开 source observation 与 semantic effects，T08 历史可读不再生成 select，T14 契约比较不再当 bind，T12 的责任和 T02 的作用范围分别声明。它仍是来源记录与语义分解，精确基线未知的步骤不作为可执行调用。

第二批全部 16 段向接手者读回；另一路拿全部来源及九条跨过程关系删减七核心，补齐首批分组输入的组外见证缺口。读回者只得表示与五问，答案依据另存，并在读取结果前固定 scoring-key-v2。主 Agent 逐条核对来源，结果如下。

| 过程 | 准确/部分/需查证/不支持 | 对机制的影响 |
|---|---|---|
| [T01](../dsh-process/dsh-process-truth-v1.md#t01) | 5/0/0/0 | 主要范围恢复准确，来源缺口按未知保存 |
| [T02](../dsh-process/dsh-process-truth-v1.md#t02) | 3/2/0/0 | Q3：撤回目录式默认定义的措辞扩大到退出动作；新声明式定义不自动表明兼容入口全撤；Q5：以没有释放/恢复事件代替最终接受状态，混淆运行实例与验收 |
| [T03](../dsh-process/dsh-process-truth-v1.md#t03) | 4/1/0/0 | Q4：关系含义基本正确，事实定位用了内存故障与阶段记录，迁移关系应指 T03.05/T16.02 |
| [T04](../dsh-process/dsh-process-truth-v1.md#t04) | 5/0/0/0 | 主要范围恢复准确，来源缺口按未知保存 |
| [T05](../dsh-process/dsh-process-truth-v1.md#t05) | 4/0/1/0 | Q2：同对话安装使用理由来自 S036 补读，表示无直接来源定位 |
| [T06](../dsh-process/dsh-process-truth-v1.md#t06) | 4/0/1/0 | Q2：Host 理由来源 S004 补读未纳入事实 ID，须补可查入口 |
| [T07](../dsh-process/dsh-process-truth-v1.md#t07) | 4/1/0/0 | Q4：把没有 links 数组记录表述为无跨工作链接，随后又列公共接口和 SSH，需按关系含义读回 |
| [T08](../dsh-process/dsh-process-truth-v1.md#t08) | 3/1/1/0 | Q2：多套生命周期重复的更细理由来自 S034 原文，83 事实只有早期 Task 耦合与后次合入；Q4：未恢复 workflow 无额外父通知与 model 可能重复的适用区分；本轮压缩表示省略此处 |
| [T09](../dsh-process/dsh-process-truth-v1.md#t09) | 4/1/0/0 | Q3：禁止移动保留页面祖先是当前策略，不能直接叙成撤回一个已记录的移动实现 |
| [T10](../dsh-process/dsh-process-truth-v1.md#t10) | 4/1/0/0 | Q5：原表示未明确保存来源已报告的 UI 授权分示结果，读回省略 |
| [T11](../dsh-process/dsh-process-truth-v1.md#t11) | 5/0/0/0 | 主要范围恢复准确，来源缺口按未知保存 |
| [T12](../dsh-process/dsh-process-truth-v1.md#t12) | 3/2/0/0 | Q1：真实模型 GUI 被改写为真机 GUI，改变验收条件；Q3：未区分撤回时保留与后来分组基础成果，其他答案虽提实现但此问未恢复完整保留范围 |
| [T13](../dsh-process/dsh-process-truth-v1.md#t13) | 4/1/0/0 | Q5：作者观察成功的范围不能代替最终接受状态；需保持最终接受未知 |
| [T14](../dsh-process/dsh-process-truth-v1.md#t14) | 5/0/0/0 | 主要范围恢复准确，来源缺口按未知保存 |
| [T15](../dsh-process/dsh-process-truth-v1.md#t15) | 3/2/0/0 | Q1：kit 独立维护并锁 npm 的概括易将锁版本职责归 kit；实际 Harness 锁版本；Q5：作者运行报告不能作为最终接受状态；签名与运行结果仍各有范围 |
| [T16](../dsh-process/dsh-process-truth-v1.md#t16) | 4/0/0/1 | Q3：撤回 V4 直接读旧包装虚构旧 V4 曾支持；来源只规定 V4 原生读取与 V3 迁移 |

合计 64 准确、12 部分、3 需额外查证、1 不支持。不是接口必要性的得分。唯一不支持为把“V4 只读原生表示”写成“撤回 V4 读旧包装”，补造了旧 V4 能力。workflow 与 model 的通知差异、已报告 UI 授权分示在压缩表示中仍缺，后续表示修订须保留；本轮答卷及得分不重跑覆盖。

### 七核心逐项删减

| 去掉的接口 | 强替代 | 仍必须承担的规则 | 具体见证 |
|---|---|---|---|
| `open` | revise nested identity declaration | identity allocation/uniqueness, goal ownership, origin and creation-time unknown | T14.03 |
| `revise` | open independent artifact versions + links | same identity successor, exact baseline/change/preserve mapping and history | T01.02-05 |
| `close` | revise typed work state | allowed terminal state, disposition, successor, parent non-propagation | T14.03 |
| `observe` | revise typed source-report object | subject/method/result/version/time attribution; keep observation separate from interpretation | T13.02-04 |
| `judge` | revise typed conclusion object | evidence, assumptions, scope, superseded judgment; old observations immutable | T13.01-03 |
| `select` | replay adopted-decision log | effective vs recommended, scope, prior/next, conflicts and holder policies | T09.02;T02.04 |
| `bind` | embed typed relations in source/target record | relation identity/endpoints, version/scope, predicate-specific rules and supersession | T13.05;T12.03 |

这些检查支持当前职责划分；强替代可保存事实，同时把规则移到类型化版本、日志或内嵌关系中。没有依据判定七入口是数学最小值。普通文档基线允许相同精确状态、清单和证据；未测人工维护时间，操作条数不作为成本优劣。

组合变化：split/review/decide/verify/repair/replace/retire 保留组合方向；revert/adapt 采用有条件步骤，原因或检查未知时不补造；implement/land/propose/migrate/constrain/followup 撤下机械归约，转待补证。逐项理由统一见[候选 v0.2](../../history/primitives-and-operations/work-operation-candidates-v0.2.md)，实际原始模型裁定在批次 r3/ 下。

## 第四轮：缺见证项的定向补查

查前问题是：哪里有真实的开发分叉、暂停恢复、取用旧成果和发布结果，答案是否改变候选去向。固定提交的英文笔记做一次关键词定位，选三份原文核对；不建立命中项逐条清理队列。

### 补查来源

| 来源 | 发现及候选影响 |
|---|---|
| [X1 原文](https://github.com/deepseek-ai/deepseek-harness/blob/86a402200d95fecef4529d969836f1fe13c6cb0d/.agents/notes/archived/feature/2026-07-23-session-telemetry-otel-revival.md) | 遥测捕获侧设计被重新取用，外发策略改变；integrate 进入组合设计；同工作恢复与共同分叉基线仍未知。此文截止已 archived。|
| [X2 原文](https://github.com/deepseek-ai/deepseek-harness/blob/86a402200d95fecef4529d969836f1fe13c6cb0d/.agents/notes/implemented/process/2026-08-10-npm-release-sequences.md) | 九 vendor 包首发版本为作者报告；release 进入记录发布结果的组合设计。标签不代表成功；旧私有政策与后续公开修订分开，不推断当前 registry。|
| [X3 原文](https://github.com/deepseek-ai/deepseek-harness/blob/86a402200d95fecef4529d969836f1fe13c6cb0d/.agents/notes/implemented/feature/2026-09-16-sidebar-browser.md) | Electron 载体曾延后；不足以构造正式开发暂停和恢复事件。|

本地 Git 对象已核对存在，链接指向固定版本；未进行在线访问。来源身份为项目作者笔记，非论文，发表 venue 不适用；核对日期 2026-10-23。

不采纳 Qoder 的两项推断：分支存在就算 fork；无 merge 就否认 integrate。前者仍需共同起点与两条路线的证据，后者可以是部分成果吸收而无整支合并。复活设计不自动说明同一工作 resume；推迟功能不自动说明正式 suspend。

最终完整去向为七核心候选、十一组合动作、十二待补证，新增/删除名称均零。集成与发布各自限制到取用和来源报告范围。下一阶段先完成 T14 的完整转换规约，再用 T12/T02 检查复用，当前不足以直接实施一套通用 API。

## 执行记录与验证范围

本轮共 18 项 Qoder 任务，分六批：身份比较与验证各三项，责任/采用各三项，全量分组审查三项，全量接手/删减/补查三项。提示、完整输出、输入哈希、格式修复、主 Agent 先行分析和裁定保存在本地批次；原输出不上传。任务编号、真实模型、时间、工具报告费用与拒绝项以批次 task-summary.json 为准。

本轮离线研究。保留来源与语义规则的区别、同作者裁定、输入分离而非严格安全隔离。候选是职责与组合建议，未计算长期收益或跨项目推广性；SWE-Milestone 仍用于后续任务效果验证。
