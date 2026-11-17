
# DSH 连续开发过程底稿 v1

状态：已归档

本版固定 16 段有连接的工程过程，用于三种记录方式的同输入比较。来源截止为 2026-10-15 的固定提交。T01—T10 沿用前版完整 54 条事实及来源，T11—T16 增补执行、工作台、诊断、接口漂移、交付与消息协议。

这是公开记录的研究整理版。提交署名、笔记中的决策者、研究整理者分别标注；未具名的决策主体保留未知。作者报告的测试与测量保持该归属。每个事实的原始来源及版本可查。

## 本版覆盖与顺序

八条工作线分别由以下过程覆盖：插件 T01/T02/T05；会话 T03；协作 T04/T08；执行 T07/T11/T13；工作台 T09/T12/T14/T15；模型消息 T16；自动化 T06/T10；交付 T13/T15。Creator、Schedule、侧栏、Goal、Office 和消息协议补入了持久化入口替换、跨存储边界、内容保活、权限主体、共享成果寿命与格式兼容等区别。

过程内的事实编号是研究整理顺序。发生先后遵循提交或来源明确叙述；同一快照中的回顾性事实在该源版本可见时一起取得。跨分支事件保留局部顺序，没有构造全项目唯一时间线。后来的测量、验收状态和解释仅在对应来源版本出现后可读。

## 连续过程与查证


<a id="t01"></a>
### T01 · 插件加载：加入事务重载，后来选择性撤回

这段工作涉及Loader 回滚保证与独立修补。记录的演化到达“撤回事务式重载，保留独立修补”；促成变化的依据是维护上游偏离成本；完整决策者未知。过程中，文件初始化、模块导出及无关能力保留。继续接手时还需知道：消费者审查实际激活；启动失败策略继续修补。

完整事实与原始署名见[前版证据 T01](dsh-truth-v0.1-evidence.md#t01)，本版保留其全部事实，不补造未知项。

**T01.01**　8月2日有一个提交加入事务式配置重载。截止版本设计记录回顾，该方案在配置修改失败后保留旧插件代际。（commit_record + retrospective_report；[S025](https://github.com/deepseek-ai/deepseek-harness/blob/86a402200d95fecef4529d969836f1fe13c6cb0d/.agents/notes/implemented/simplification/2026-09-09-nontransactional-loader.md)、[S038](https://github.com/deepseek-ai/deepseek-harness/commit/195f7fa9af0ff33e75f44e767a23b8e1e8aaa200)）

**T01.02**　后来的决定要求撤回 #932 的五个提交；它记录的理由是候选导入、回滚和生命周期处理使 vendored 实现偏离上游过多。（recorded_decision；[S025](https://github.com/deepseek-ai/deepseek-harness/blob/86a402200d95fecef4529d969836f1fe13c6cb0d/.agents/notes/implemented/simplification/2026-09-09-nontransactional-loader.md)）

**T01.03**　撤回保留了文件初始化、模块导出的两项修补，以及较大合并中的无关仓库插件能力。（recorded_decision；[S025](https://github.com/deepseek-ai/deepseek-harness/blob/86a402200d95fecef4529d969836f1fe13c6cb0d/.agents/notes/implemented/simplification/2026-09-09-nontransactional-loader.md)）

**T01.04**　9月9日出现撤回提交及消费者适配提交，9月11日又有保持启动失败策略的修补。（commit_record；[S046](https://github.com/deepseek-ai/deepseek-harness/commit/e07f41d5fd8ca172287fda0f923b4d1f69c592f3)、[S039](https://github.com/deepseek-ai/deepseek-harness/commit/2abb542a222032b1ad3c5abd7bb65ffffe15b8de)、[S048](https://github.com/deepseek-ai/deepseek-harness/commit/f4a7dd607709025bc3ad19dab8ffbb038cd13962)）

**T01.05**　截止快照记录的结果是：插件失败可以留下部分应用的配置树，Loader 不自动恢复旧配置；需要可用插件的消费者自行审查实际激活结果。（documented_result；[S025](https://github.com/deepseek-ai/deepseek-harness/blob/86a402200d95fecef4529d969836f1fe13c6cb0d/.agents/notes/implemented/simplification/2026-09-09-nontransactional-loader.md)）

**未决与使用边界：**消费者审查实际激活；启动失败策略继续修补。

<a id="t02"></a>
### T02 · Agent 预设：按会话装载，改为声明式配置并保留旧修订

这段工作涉及预设定义、运行修订与恢复。记录的演化到达“声明式配置，活跃使用者保留旧修订”；促成变化的依据是跨会话读者、配置写回与资源寿命问题。过程中，旧修订在进程内存活，重启解析当前定义。继续接手时还需知道：缺失定义会恢复失败；局部修补主线日期未知。

完整事实与原始署名见[前版证据 T02](dsh-truth-v0.1-evidence.md#t02)，本版保留其全部事实，不补造未知项。

**T02.01**　rc.7 的记录说明，先前进程级配置决定全部会话能力；当时已改为每个 Agent 装载自己的预设目录，Host 的注册服务和跨会话设施仍共享。（documented_state；[S030](https://github.com/deepseek-ai/deepseek-harness/blob/99f6f02fecdb7dff40c3fbc9470f5907c29f74ca/.agents/notes/implemented/architecture/2026-08-03-per-session-agent-presets.md)）

**T02.02**　同一份历史记录记下了实施中的问题：Host 读者曾找不到移入会话的服务，卸载可能改写预设输入，存储后端没有全部保存新增预设身份，Host 缺少闲置 Agent 的释放时机。（author_reported_findings；[S030](https://github.com/deepseek-ai/deepseek-harness/blob/99f6f02fecdb7dff40c3fbc9470f5907c29f74ca/.agents/notes/implemented/architecture/2026-08-03-per-session-agent-presets.md)）

**T02.03**　9月21日主线有声明式预设提交；在 0.1.7-rc.2 中，预设已由普通配置声明，注册器拥有运行修订及其插件树。（documented_transition；[S045](https://github.com/deepseek-ai/deepseek-harness/commit/d1e22a7e247060496e1acdba9ef3be1700e23ec7)、[S005](https://github.com/deepseek-ai/deepseek-harness/blob/477b4f420553e8a52c2fbccc464d7561b239c443/.agents/notes/implemented/architecture/2026-09-18-declarative-agent-presets.md)）

**T02.04**　修改定义会使旧修订退役；正在使用它的 Agent、子代理和临时读取者继续持有引用，最后释放时才清理。配置持久化与实际激活结果分别报告。（documented_result；[S005](https://github.com/deepseek-ai/deepseek-harness/blob/477b4f420553e8a52c2fbccc464d7561b239c443/.agents/notes/implemented/architecture/2026-09-18-declarative-agent-presets.md)）

**T02.05**　旧可执行修订保存在进程内；重启按保存的预设身份解析当前配置，缺少定义时恢复失败。（documented_limit；[S005](https://github.com/deepseek-ai/deepseek-harness/blob/477b4f420553e8a52c2fbccc464d7561b239c443/.agents/notes/implemented/architecture/2026-09-18-declarative-agent-presets.md)、[S020](https://github.com/deepseek-ai/deepseek-harness/blob/86a402200d95fecef4529d969836f1fe13c6cb0d/.agents/notes/implemented/architecture/2026-09-18-declarative-agent-presets.md)）

**未决与使用边界：**缺失定义会恢复失败；局部修补主线日期未知。

<a id="t03"></a>
### T03 · 会话迁移：一次合入与撤回，之后再引入流式实现

这段工作涉及迁移实现与 LogicalSession 分阶段计划。记录的演化到达“后续流式迁移已记录；重建仍有草稿和未完阶段”；促成变化的依据是首次撤回原因未知；大文件性能为作者报告。过程中，源代际保留；两次实现的复用范围未知。继续接手时还需知道：阶段1/2草稿完成、3有实现与CI但仍草稿、4/5未完。

完整事实与原始署名见[前版证据 T03](dsh-truth-v0.1-evidence.md#t03)，本版保留其全部事实，不补造未知项。

**T03.01**　8月25日主线合入 #2698，提交正文将其称为流式格式迁移管线。（commit_record；[S041](https://github.com/deepseek-ai/deepseek-harness/commit/3fefcdbe3f83a309f05075b9e9f05450509318ed)）

**T03.02**　同日主线合入 #3054，正文为撤回该迁移管线；撤回理由待查。（commit_record；[S043](https://github.com/deepseek-ai/deepseek-harness/commit/a1781cc4a81bf14551ed0d6e0ee618d14fd9b823)）

**T03.03**　9月6日主线合入 #3585，属于后来的流式迁移实现；两次实现的对应关系和复用范围待查。（commit_record；[S042](https://github.com/deepseek-ai/deepseek-harness/commit/80306f51a6f36e26c71bcf0be5621af6b8ad8e65)）

**T03.04**　截止快照的设计记录报告，一份116 MB会话在整份转换实现中耗尽16 GB Node进程。测量归属为作者报告。（author_reported_failure；[S015](https://github.com/deepseek-ai/deepseek-harness/blob/86a402200d95fecef4529d969836f1fe13c6cb0d/.agents/notes/implemented/architecture/2026-08-31-released-session-format-migrations.md)）

**T03.05**　截止记录采用每份会话独立的有状态转换阶段；原已提交格式文件保留，仅发布最终当前代际，中间格式不逐份落盘。不同历史代际的解释和拒绝规则分别保留。（documented_result；[S015](https://github.com/deepseek-ai/deepseek-harness/blob/86a402200d95fecef4529d969836f1fe13c6cb0d/.agents/notes/implemented/architecture/2026-08-31-released-session-format-migrations.md)）

**T03.06**　LogicalSession存储重建仍是proposed：阶段1、2为draft work complete，阶段3记录实现与远程CI完成但仍为draft，阶段4、5未完成。（documented_status；[S027](https://github.com/deepseek-ai/deepseek-harness/blob/86a402200d95fecef4529d969836f1fe13c6cb0d/.agents/notes/proposed/architecture/2026-09-06-logical-session-storage-rebuild.md)）

**未决与使用边界：**阶段1/2草稿完成、3有实现与CI但仍草稿、4/5未完。

<a id="t04"></a>
### T04 · Team 消息：从独立 outbox 改为目标 inbox，保留名单与任务

这段工作涉及Team 消息交付，名单与任务另存。记录的演化到达“直接向目标 inbox 投递”；促成变化的依据是减少独立 outbox 身份、确认与重试管理。过程中，名单、任务和旧消息展示保留；旧待发不再投递。继续接手时还需知道：成功仅为接纳；实际用户待发损失未知。

完整事实与原始署名见[前版证据 T04](dsh-truth-v0.1-evidence.md#t04)，本版保留其全部事实，不补造未知项。

**T04.01**　0.1.7-rc.2 的 Team 记录将发送意图先写入并刷盘到 Lead 日志，再向目标投递并确认；恢复时重试未确认项，并提供目标侧去重。名单和共享任务也有各自的持久状态。（documented_state；[S006](https://github.com/deepseek-ai/deepseek-harness/blob/477b4f420553e8a52c2fbccc464d7561b239c443/.agents/notes/implemented/feature/2026-08-05-agent-teams.md)）

**T04.02**　新记录把独立 outbox 的身份、确认、重试和清理视为重复管理，选择直接通过目标 Agent inbox 接纳消息。（recorded_decision；[S035](https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/.agents/notes/implemented/simplification/2026-09-26-team-direct-inbox.md)）

**T04.03**　该变更10月8日合入主线，0.2.1-alpha.2中已有对应记录；主题笔记文件名日期为9月26日。（commit_record；[S047](https://github.com/deepseek-ai/deepseek-harness/commit/ea0980dab432263a9d1cd2b8e4998a1d6e6e6ae7)、[S035](https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/.agents/notes/implemented/simplification/2026-09-26-team-direct-inbox.md)）

**T04.04**　新发送返回目标inbox接纳的消息身份或失败。Team的未接纳意图保存、重启重试和显式重发去重机制退出；成功结果表示队列接纳，模型处理状态待确认。（documented_result；[S035](https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/.agents/notes/implemented/simplification/2026-09-26-team-direct-inbox.md)）

**T04.05**　旧 mailbox 记录仍可解码和展示，但旧待发项不再投递；替代范围仅为消息机制，成员名单和任务决定继续保留。（documented_result；[S035](https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/.agents/notes/implemented/simplification/2026-09-26-team-direct-inbox.md)）

**T04.06**　记录以实验功能的稳定性约定为取舍条件，接受了旧待发消息失去恢复投递能力的后果。（recorded_rationale；[S035](https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/.agents/notes/implemented/simplification/2026-09-26-team-direct-inbox.md)）

**未决与使用边界：**成功仅为接纳；实际用户待发损失未知。

<a id="t05"></a>
### T05 · Creator：临时修改运行时，转为安装持久插件

这段工作涉及Creator 模型修改入口与安装配置。记录的演化到达“改为写文件并使用普通插件管理器安装”；促成变化的依据是临时运行时代码重启不恢复，持久成果需普通插件。过程中，原运行时消费者与历史卡片保留。继续接手时还需知道：配置保存与激活分开；当时包替换仍需重启。

完整事实与原始署名见[前版证据 T05](dsh-truth-v0.1-evidence.md#t05)，本版保留其全部事实，不补造未知项。

**T05.01**　rc.8 的旧工具允许模型检查、临时装载和卸载进程内插件；临时插件不写文件，不修改配置，重启后不恢复。（documented_state；[S001](https://github.com/deepseek-ai/deepseek-harness/blob/141eb6fef83422698aef7a981029e843e8161534/.agents/notes/implemented/feature/2026-07-08-self-referential-cordis-toolset.md)）

**T05.02**　旧记录要求保留实验成果时另行实现普通项目插件或可安装 bundle，没有自动转正路径。（documented_limit；[S001](https://github.com/deepseek-ai/deepseek-harness/blob/141eb6fef83422698aef7a981029e843e8161534/.agents/notes/implemented/feature/2026-07-08-self-referential-cordis-toolset.md)）

**T05.03**　9月16日 #4324 合入主线；0.1.6-alpha.2记录Creator改走已有插件管理器：先写包和配置文件，再安装bundle。（documented_transition；[S049](https://github.com/deepseek-ai/deepseek-harness/commit/f756097108d1fc69f71bae1ee3c6114e5ae40b12)、[S036](https://github.com/deepseek-ai/deepseek-harness/blob/ddefc45fbc7f8e46dd73185e68295696d1297887/.agents/notes/implemented/architecture/2026-09-16-creator-persistent-plugin-management.md)）

**T05.04**　模型侧旧的生成代码修改入口退出，但已有运行时和Client消费者继续保留所用服务；历史工具卡片仍可读取。（documented_result；[S036](https://github.com/deepseek-ai/deepseek-harness/blob/ddefc45fbc7f8e46dd73185e68295696d1297887/.agents/notes/implemented/architecture/2026-09-16-creator-persistent-plugin-management.md)）

**T05.05**　新安装的配置跨重启保留并影响同一profile中的会话；工具操作要求完整访问或单次批准，配置保存与能力实际生效分别报告，已安装包替换当时需要重启。（documented_result；[S036](https://github.com/deepseek-ai/deepseek-harness/blob/ddefc45fbc7f8e46dd73185e68295696d1297887/.agents/notes/implemented/architecture/2026-09-16-creator-persistent-plugin-management.md)）

**未决与使用边界：**配置保存与激活分开；当时包替换仍需重启。

<a id="t06"></a>
### T06 · 定时任务：从会话日志转为Host存储，再限制历史保留

这段工作涉及Schedule 权威存储与历史。记录的演化到达“Host 任务存储、冷会话到期恢复，历史有限保留”；促成变化的依据是会话未加载时旧提醒不触发；全量JSON增长。过程中，旧事件可读但不自动导入；已入会话消息保留。继续接手时还需知道：跨存储崩溃可重复投递；接纳不等于模型完成。

完整事实与原始署名见[前版证据 T06](dsh-truth-v0.1-evidence.md#t06)，本版保留其全部事实，不补造未知项。

**T06.01**　0.1.7-rc.1 的提醒以原会话日志为唯一持久依据，只在会话活跃时运行；冷会话不触发，重新加载后再处理过期提醒，分叉不继承父任务的活跃执行。（documented_state；[S003](https://github.com/deepseek-ai/deepseek-harness/blob/46a7f68b0922371ce7144b668b90e377d8e799f4/.agents/notes/implemented/feature/2026-08-05-durable-web-schedule.md)）

**T06.02**　0.1.7-rc.2 已记录改用独立Host任务存储，恢复计时器不必先加载全部会话；到期时再恢复原会话并投递。作者记录的目标包含独立查看待处理和已投递任务。（documented_transition；[S004](https://github.com/deepseek-ai/deepseek-harness/blob/477b4f420553e8a52c2fbccc464d7561b239c443/.agents/notes/implemented/architecture/2026-09-16-host-schedule-storage.md)）

**T06.03**　历史schedule事件仍可读，但不自动导入新任务存储；加载有旧活跃提醒的会话会提示重建。规则中部分旧时间计算和接纳语义继续适用。（documented_result；[S004](https://github.com/deepseek-ai/deepseek-harness/blob/477b4f420553e8a52c2fbccc464d7561b239c443/.agents/notes/implemented/architecture/2026-09-16-host-schedule-storage.md)）

**T06.04**　同一Host存储记录后来保留任务和回执；专门的后续决定记下了全量JSON重写下的增长问题，改为删除任务时删除其行与回执，并按时间和数量限制交付历史。（recorded_transition；[S004](https://github.com/deepseek-ai/deepseek-harness/blob/477b4f420553e8a52c2fbccc464d7561b239c443/.agents/notes/implemented/architecture/2026-09-16-host-schedule-storage.md)、[S023](https://github.com/deepseek-ai/deepseek-harness/blob/86a402200d95fecef4529d969836f1fe13c6cb0d/.agents/notes/implemented/architecture/2026-09-22-schedule-hard-delete-and-bounded-history.md)）

**T06.05**　交付历史分别标记实际裁剪与旧历史不可用；删除任务后，已经进入会话的消息保留。（documented_result；[S023](https://github.com/deepseek-ai/deepseek-harness/blob/86a402200d95fecef4529d969836f1fe13c6cb0d/.agents/notes/implemented/architecture/2026-09-22-schedule-hard-delete-and-bounded-history.md)、[S004](https://github.com/deepseek-ai/deepseek-harness/blob/477b4f420553e8a52c2fbccc464d7561b239c443/.agents/notes/implemented/architecture/2026-09-16-host-schedule-storage.md)）

**T06.06**　回执记录消息已持久进入inbox，模型完成状态待确认。任务存储与消息存储分开提交，崩溃存在重复投递风险。（documented_limit；[S004](https://github.com/deepseek-ai/deepseek-harness/blob/477b4f420553e8a52c2fbccc464d7561b239c443/.agents/notes/implemented/architecture/2026-09-16-host-schedule-storage.md)）

**未决与使用边界：**跨存储崩溃可重复投递；接纳不等于模型完成。

<a id="t07"></a>
### T07 · 远程执行：移除E2B实现，保留接口并继续SSH路线

这段工作涉及执行接口、E2B 与 SSH 后端。记录的演化到达“退出 E2B 供应实现，远程接口继续供 SSH 等使用”；促成变化的依据是固定 E2B SDK 的控制通道与输出保留成本。过程中，文件、进程、终端接口及异步操作约定保留。继续接手时还需知道：SSH 与删除的准确先后未知；不推导整个路线证伪。

完整事实与原始署名见[前版证据 T07](dsh-truth-v0.1-evidence.md#t07)，本版保留其全部事实，不补造未知项。

**T07.01**　8月8日主线合入E2B概念验证相关分支；后来的退出记录说明，它曾为文件、进程、终端等提供同一个远程执行世界。（documented_transition；[S040](https://github.com/deepseek-ai/deepseek-harness/commit/33312c6a89e2c4c7efd7b067d88506df2a9d982f)、[S026](https://github.com/deepseek-ai/deepseek-harness/blob/86a402200d95fecef4529d969836f1fe13c6cb0d/.agents/notes/implemented/simplification/2026-09-11-remove-e2b-providers.md)）

**T07.02**　退出记录说明，新PTC需要与程序标准流独立的双向控制流；当时固定E2B SDK的通道能力及输出保留使继续适配需要额外传输工程。（recorded_rationale；[S026](https://github.com/deepseek-ai/deepseek-harness/blob/86a402200d95fecef4529d969836f1fe13c6cb0d/.agents/notes/implemented/simplification/2026-09-11-remove-e2b-providers.md)）

**T07.03**　9月11日主线合入移除E2B提供者的变更；截止记录列出实现、SDK依赖、集成夹具及可选工作流等移除范围。（documented_transition；[S037](https://github.com/deepseek-ai/deepseek-harness/commit/09a6fbc388bc6de135dea7d86b85f6e96b3bf32a)、[S026](https://github.com/deepseek-ai/deepseek-harness/blob/86a402200d95fecef4529d969836f1fe13c6cb0d/.agents/notes/implemented/simplification/2026-09-11-remove-e2b-providers.md)）

**T07.04**　通用文件系统、进程和终端接口及其异步语义继续保留；远程执行需求继续存在。退出理由针对当时固定SDK的集成成本。（documented_result；[S026](https://github.com/deepseek-ai/deepseek-harness/blob/86a402200d95fecef4529d969836f1fe13c6cb0d/.agents/notes/implemented/simplification/2026-09-11-remove-e2b-providers.md)）

**T07.05**　截止SSH记录由远端helper提供执行能力，Harness、凭据、模型传输与会话持久化仍在本地；断连后的修改性操作不自动重放。（documented_state；[S016](https://github.com/deepseek-ai/deepseek-harness/blob/86a402200d95fecef4529d969836f1fe13c6cb0d/.agents/notes/implemented/architecture/2026-09-11-posix-ssh-runtime.md)）

**未决与使用边界：**SSH 与删除的准确先后未知；不推导整个路线证伪。

<a id="t08"></a>
### T08 · 子代理：先分开持续会话与一次执行，再统一activation入口

这段工作涉及持续 Session 与一次 Activation。记录的演化到达“统一 activation 入口，本地与外部后端保留差异”；促成变化的依据是Task 不宜代表持续 Agent；避免多套执行生命周期。过程中，历史单次描述与外部单次执行适配保留。继续接手时还需知道：通知允许重复；清理失败不抹去执行结果。

完整事实与原始署名见[前版证据 T08](dsh-truth-v0.1-evidence.md#t08)，本版保留其全部事实，不补造未知项。

**T08.01**　0.2.1-alpha.1 的持续子代理记录回顾了先前Task结束就销毁Agent的办法，并指出它把会话生命周期与一次结果绑定在一起。（retrospective_report；[S007](https://github.com/deepseek-ai/deepseek-harness/blob/5badb15009ae1756c3afe0ae0cef1faafc290ccc/.agents/notes/implemented/feature/2026-07-28-continuable-subagent-conversations.md)）

**T08.02**　该版已将持久Session与进程内Activation分开：同一会话可多轮续接、冷恢复，Agent inbox负责消息顺序；一次性提供者执行路径仍独立存在。（documented_state；[S007](https://github.com/deepseek-ai/deepseek-harness/blob/5badb15009ae1756c3afe0ae0cef1faafc290ccc/.agents/notes/implemented/feature/2026-07-28-continuable-subagent-conversations.md)）

**T08.03**　10月6日统一子代理重构合入主线；alpha.2记录将所有提供者接入统一activation入口，本地spawn/fork只提供创建数据。（documented_transition；[S044](https://github.com/deepseek-ai/deepseek-harness/commit/bf1c4e01ba7088b3cb0aeb36caa702965eb5f6ec)、[S034](https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/.agents/notes/implemented/simplification/2026-09-17-unified-subagent-activations.md)）

**T08.04**　模型委派返回后台子任务身份；工作流通过同一activation等待结果并清理，不额外给父Agent发送完成通知。（documented_result；[S034](https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/.agents/notes/implemented/simplification/2026-09-17-unified-subagent-activations.md)）

**T08.05**　外部后端保留一次执行适配器，通过同一入口管理容量和生命周期；外部执行保持无本地Session、无多轮续接的能力范围。执行结果在清理失败时保留，清理错误另报。（documented_result；[S034](https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/.agents/notes/implemented/simplification/2026-09-17-unified-subagent-activations.md)）

**T08.06**　历史一次执行描述仍可读取。完成通知可能与子代理主动汇报重复，记录接受了这项代价。（documented_limit；[S034](https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/.agents/notes/implemented/simplification/2026-09-17-unified-subagent-activations.md)）

**未决与使用边界：**通知允许重复；清理失败不抹去执行结果。

<a id="t09"></a>
### T09 · 侧栏：从工具详情到通用工作区，调整布局和内容的寿命

这段工作涉及侧栏布局、内容实例与数据读取。记录的演化到达“通用侧栏加按类型内容保留”；促成变化的依据是旧详情栏限制；卸载或DOM祖先改变会断开浏览器。过程中，布局引擎继续使用，其他类型按可见性挂载。继续接手时还需知道：原型和评审完整记录未知；保活不等于所有页常驻。

完整事实与原始署名见[前版证据 T09](dsh-truth-v0.1-evidence.md#t09)，本版保留其全部事实，不补造未知项。

**T09.01**　0.1.5-alpha.1 记录旧右栏只能显示工具详情；文件链接交给Host操作系统，远程浏览器无法直接查看文件。（retrospective_report；[S008](https://github.com/deepseek-ai/deepseek-harness/blob/5dda764ed3aa172535a7967b06ff95d9cbfe536a/.agents/notes/implemented/feature/2026-09-04-right-sidebar-docking-infrastructure.md)）

**T09.02**　团队评估第三方布局库，保留FlexLayout作备选；设计记录称自建原型通过相关浏览器检查后继续自建。（author_reported_trial；[S008](https://github.com/deepseek-ai/deepseek-harness/blob/5dda764ed3aa172535a7967b06ff95d9cbfe536a/.agents/notes/implemented/feature/2026-09-04-right-sidebar-docking-infrastructure.md)）

**T09.03**　记录中的首个原型采用drawer；产品形态改为实际挤占聊天宽度的右侧栏，布局支持分栏、标签、浮窗及撤销，内容类型由另外的插件接口提供。（recorded_transition；[S008](https://github.com/deepseek-ai/deepseek-harness/blob/5dda764ed3aa172535a7967b06ff95d9cbfe536a/.agents/notes/implemented/feature/2026-09-04-right-sidebar-docking-infrastructure.md)）

**T09.04**　后续记录指出，卸载内容或改变其DOM祖先会断开浏览器页面；侧栏为声明keepMounted的类型提供内容保留，Desktop Browser启用它，其他类型仍按可见性挂载。停靠、浮动和会话切换不移动已保留页面的DOM祖先。（recorded_transition；[S021](https://github.com/deepseek-ai/deepseek-harness/blob/86a402200d95fecef4529d969836f1fe13c6cb0d/.agents/notes/implemented/architecture/2026-09-20-sidebar-retained-tab-layout.md)）

**T09.05**　布局状态、内容实例寿命和数据读取分别承担责任；后续保留内容树的决定没有整体废弃侧栏布局引擎。（documented_result；[S008](https://github.com/deepseek-ai/deepseek-harness/blob/5dda764ed3aa172535a7967b06ff95d9cbfe536a/.agents/notes/implemented/feature/2026-09-04-right-sidebar-docking-infrastructure.md)、[S021](https://github.com/deepseek-ai/deepseek-harness/blob/86a402200d95fecef4529d969836f1fe13c6cb0d/.agents/notes/implemented/architecture/2026-09-20-sidebar-retained-tab-layout.md)）

**未决与使用边界：**原型和评审完整记录未知；保活不等于所有页常驻。

<a id="t10"></a>
### T10 · 目标控制：保存目标，再修复人工暂停被执行绕过的问题

这段工作涉及Goal 持久状态与运行授权。记录的演化到达“人工持久暂停由用户恢复”；促成变化的依据是第一次取消当前轮后，后续人类轮仍可被模型绕过。过程中，目标事件、输入队列、active-but-disarmed 的条件式恢复保留。继续接手时还需知道：运行故障原始日志与精确合入时间未知。

完整事实与原始署名见[前版证据 T10](dsh-truth-v0.1-evidence.md#t10)，本版保留其全部事实，不补造未知项。

**T10.01**　早期goal记录将目标修改写成独立goal/change事件，下一轮提示另由驱动组件入队；目标存在不以消息是否被模型接纳为条件。（documented_state；[S033](https://github.com/deepseek-ai/deepseek-harness/blob/b64c3ac1ba37a8afe20de534ab666e85ae69377b/.agents/notes/implemented/architecture/2026-07-31-goal-owned-durable-events.md)）

**T10.02**　持久目标与进程内运行授权分开；恢复或分叉可保留active目标，但默认disarmed，不会因打开会话就自动继续。（documented_state；[S013](https://github.com/deepseek-ai/deepseek-harness/blob/86a402200d95fecef4529d969836f1fe13c6cb0d/.agents/notes/archived/feature/2026-07-19-persisted-same-session-goal-domain.md)）

**T10.03**　第一次暂停修复记录的问题是：Web已标记paused并禁止后续自动轮次，但当前模型轮仍在执行，还可能自行调用resume。修复增加人工暂停时取消当前轮，并保留输入队列。（author_reported_fix；[S011](https://github.com/deepseek-ai/deepseek-harness/blob/86a402200d95fecef4529d969836f1fe13c6cb0d/.agents/notes/archived/bug-fix/2026-09-01-host-goal-pause-aborts-turn.md)）

**T10.04**　后续记录指出，前一个修复后，稍后的人类轮次仍可能被模型用来恢复持久paused目标；UI也混淆了active-but-disarmed与armed。（author_reported_remaining_issue；[S012](https://github.com/deepseek-ai/deepseek-harness/blob/86a402200d95fecef4529d969836f1fe13c6cb0d/.agents/notes/archived/bug-fix/2026-09-03-user-owned-goal-pause-activation.md)）

**T10.05**　后续改动禁止模型工具恢复持久paused目标，仍允许它在合适人类输入下恢复active-but-disarmed或blocked目标；界面分别显示运行授权，人类显式恢复入口继续保留。（documented_result；[S012](https://github.com/deepseek-ai/deepseek-harness/blob/86a402200d95fecef4529d969836f1fe13c6cb0d/.agents/notes/archived/bug-fix/2026-09-03-user-owned-goal-pause-activation.md)）

**未决与使用边界：**运行故障原始日志与精确合入时间未知。

<a id="t11"></a>
### T11 · Shell：从超时交接改为从启动就登记任务

这段工作涉及Shell 执行期限、job 与前台等待。记录的演化到达“开始即登记 job；前台只是限时等待”；促成变化的依据是评审发现超时才登记造成额外交接协议。过程中，同一进程、输出游标与取消路径；jobs 可选。继续接手时还需知道：无 registry 等情况仍期限终止；前台分组后续。

**T11.01**　旧 run 将期限与执行捆绑，start 返回句柄但没有同样的期限行为；长构建超时会被杀掉。（retrospective_report；[S014](https://github.com/deepseek-ai/deepseek-harness/blob/86a402200d95fecef4529d969836f1fe13c6cb0d/.agents/notes/archived/feature/2026-08-26-shell-execute-projection-and-jobs-at-start.md)）

**T11.02**　早先已交付的 execute 版本在超时时提供 promotion offer，由工具同步接纳并登记后台任务。（documented_state；[S032](https://github.com/deepseek-ai/deepseek-harness/blob/b42a93d62f713b0c84f501ab682dbf57eca2a410/.agents/notes/implemented/feature/2026-08-26-shell-execute-timeout-promotion.md)）

**T11.03**　后续记录称评审否定该交接协议：延迟到超时才登记，造成执行器和消费者都承担额外时序责任。（recorded_review；[S014](https://github.com/deepseek-ai/deepseek-harness/blob/86a402200d95fecef4529d969836f1fe13c6cb0d/.agents/notes/archived/feature/2026-08-26-shell-execute-projection-and-jobs-at-start.md)）

**T11.04**　采用开始即登记同一个 job，再限时等待结果；前台等待结束后进程仍可运行，用户从开始就能查看和停止。（recorded_decision；[S014](https://github.com/deepseek-ai/deepseek-harness/blob/86a402200d95fecef4529d969836f1fe13c6cb0d/.agents/notes/archived/feature/2026-08-26-shell-execute-projection-and-jobs-at-start.md)）

**T11.05**　jobs 仍为可选组成；没有 registry、禁止转后台或登记被拒时保留期限终止；前台任务分组是后续工作。（documented_limit；[S014](https://github.com/deepseek-ai/deepseek-harness/blob/86a402200d95fecef4529d969836f1fe13c6cb0d/.agents/notes/archived/feature/2026-08-26-shell-execute-projection-and-jobs-at-start.md)）

**未决与使用边界：**无 registry 等情况仍期限终止；前台分组后续。

<a id="t12"></a>
### T12 · 聊天折叠：从整批迁移拆为独立功能与分组基础

这段工作涉及聊天迁移各功能、实现与验收。记录的演化到达“已完成独立功能留 channel，其余分阶段推进”；促成变化的依据是整批迁移混合独立视觉和结构，难分辨性能。过程中，原 PR 留作参考；独立功能和分组基础分别保留。继续接手时还需知道：未暂存草稿、产品接入、GUI演示与性能待验收。

**T12.01**　PR #4565 同时包含三种详略模式、过程分组、整轮状态、触发通知、工具视觉和行隐藏。（documented_scope；[S029](https://github.com/deepseek-ai/deepseek-harness/blob/8b43d44cc6b12a9f494693f6e089ebae193b8487/.agents/notes/proposed/feature/2026-09-20-chat-work-details-migration.md)）

**T12.02**　架构记录称整批功能合并八分钟后因性能回退；原有六项基准没有覆盖流式分组和节点重渲染的新热路径。（author_reported_history；[S028](https://github.com/deepseek-ai/deepseek-harness/blob/8b43d44cc6b12a9f494693f6e089ebae193b8487/.agents/notes/proposed/architecture/2026-09-20-chat-presentation-policy-and-step-groups.md)）

**T12.03**　迁移记录将已完成独立功能留在 presentation channel，未完成部分留在 turnstep worktree，原 PR 作为参考。（recorded_plan；[S029](https://github.com/deepseek-ai/deepseek-harness/blob/8b43d44cc6b12a9f494693f6e089ebae193b8487/.agents/notes/proposed/feature/2026-09-20-chat-work-details-migration.md)）

**T12.04**　部分独立视觉、摘要和过滤功能已提交；整轮状态、通知和若干行为仍有未暂存草稿，验收待做。（documented_partial_result；[S029](https://github.com/deepseek-ai/deepseek-harness/blob/8b43d44cc6b12a9f494693f6e089ebae193b8487/.agents/notes/proposed/feature/2026-09-20-chat-work-details-migration.md)）

**T12.05**　Definition-owned 分组基础已有 implemented 记录；迁移清单明确产品分组行为和性能要求仍未完成。（documented_result；[S029](https://github.com/deepseek-ai/deepseek-harness/blob/8b43d44cc6b12a9f494693f6e089ebae193b8487/.agents/notes/proposed/feature/2026-09-20-chat-work-details-migration.md)、[S022](https://github.com/deepseek-ai/deepseek-harness/blob/86a402200d95fecef4529d969836f1fe13c6cb0d/.agents/notes/implemented/architecture/2026-09-21-conversation-build-groups.md)）

**T12.06**　该 channel 的构建、lint、覆盖检查通过是作者报告；真实模型 GUI 演示和性能测量仍待完成。（documented_limit；[S029](https://github.com/deepseek-ai/deepseek-harness/blob/8b43d44cc6b12a9f494693f6e089ebae193b8487/.agents/notes/proposed/feature/2026-09-20-chat-work-details-migration.md)）

**未决与使用边界：**未暂存草稿、产品接入、GUI演示与性能待验收。

<a id="t13"></a>
### T13 · Windows 终端：等待假设被测量修正

这段工作涉及Windows 特定故障解释与修补。记录的演化到达“该宿主改用随包控制台”；促成变化的依据是20.8秒对照及畸变尾部推翻该故障的延迟解释。过程中，宽限历史保留；未由本次证据否定所有延迟场景。继续接手时还需知道：桌面需保留随包二进制；七次成功为作者报告。

**T13.01**　早期解释认为自托管 Windows 的就绪故障属于提示符尾部延迟，并引用已交付的等待宽限修补。（author_reported_diagnosis；[S002](https://github.com/deepseek-ai/deepseek-harness/blob/21507982e62aee5c86e13d9ffcd95ac6e817f747/.agents/notes/implemented/testing/2026-09-27-observation-waits-on-observed-state.md)）

**T13.02**　后续对照记录称修补前后该用例都耗时 20.8 秒，等待宽限没有解决这次故障。（author_reported_measurement；[S010](https://github.com/deepseek-ai/deepseek-harness/blob/6514255930926026af9bf87fedc9a23e743d93ac/.agents/notes/implemented/testing/2026-09-27-observation-waits-on-observed-state.md)）

**T13.03**　直接探查发现宿主控制台在滚屏后改写尾部格式；已经到达的非前缀字符串无法满足等待条件。（author_reported_measurement；[S009](https://github.com/deepseek-ai/deepseek-harness/blob/6514255930926026af9bf87fedc9a23e743d93ac/.agents/notes/implemented/bug-fix/2026-09-28-pty-bundled-console-host.md)）

**T13.04**　Windows PTY 改用 node-pty 随包 OpenConsole；同一序列的七个提示符均正常是作者报告。（recorded_decision；[S009](https://github.com/deepseek-ai/deepseek-harness/blob/6514255930926026af9bf87fedc9a23e743d93ac/.agents/notes/implemented/bug-fix/2026-09-28-pty-bundled-console-host.md)）

**T13.05**　桌面包原有的 OpenConsole 与 conpty.dll 保留策略成为终端分配的必要条件；其他 Windows 宿主与 POSIX 的范围分别说明。（documented_dependency；[S009](https://github.com/deepseek-ai/deepseek-harness/blob/6514255930926026af9bf87fedc9a23e743d93ac/.agents/notes/implemented/bug-fix/2026-09-28-pty-bundled-console-host.md)）

**未决与使用边界：**桌面需保留随包二进制；七次成功为作者报告。

<a id="t14"></a>
### T14 · 消息反馈：旧全栈方案因接口演化转为重做 UI

这段工作涉及反馈后端契约与 Web 入口。记录的演化到达“按已落地的逐项版本后端重写 UI”；促成变化的依据是旧接口与目录漂移，另有重复后端。过程中，新后端继续用，旧分支作为历史来源；无代码复用范围证据。继续接手时还需知道：后端合入时用户功能未完；之后 E2E 为作者报告。

**T14.01**　记录称 #2217 先落地持久反馈 sidecar 与 Host 方法，未提供 Web 入口；对应用户需求当时仍未完成。（author_reported_history；[S031](https://github.com/deepseek-ai/deepseek-harness/blob/b1daf0eeaf596e91eab70603fea12f45105999dd/.agents/notes/implemented/feature/2026-08-11-message-feedback-web-surface.md)）

**T14.02**　早期 #1010 使用会话级 revision 与 feedback.upsert；已落地后端改为逐项 ifVersion 与 messageFeedback.put，目录也已更名。（author_reported_history；[S031](https://github.com/deepseek-ai/deepseek-harness/blob/b1daf0eeaf596e91eab70603fea12f45105999dd/.agents/notes/implemented/feature/2026-08-11-message-feedback-web-surface.md)）

**T14.03**　作者记录检查旧分支后选择以 superseded 关闭并重写 UI，理由包含接口不兼容、重复后端与目录漂移。（recorded_decision；[S031](https://github.com/deepseek-ai/deepseek-harness/blob/b1daf0eeaf596e91eab70603fea12f45105999dd/.agents/notes/implemented/feature/2026-08-11-message-feedback-web-surface.md)）

**T14.04**　新 UI 为已完成消息补入 MessageId，按逐项版本串行变更并用冲突响应更新本地项；持久恢复 E2E 为作者报告。（documented_result；[S031](https://github.com/deepseek-ai/deepseek-harness/blob/b1daf0eeaf596e91eab70603fea12f45105999dd/.agents/notes/implemented/feature/2026-08-11-message-feedback-web-surface.md)）

**未决与使用边界：**后端合入时用户功能未完；之后 E2E 为作者报告。

<a id="t15"></a>
### T15 · Office 与交付：共享转换、引擎独立发布、桌面绑定运行时

这段工作涉及共享转换服务、独立引擎与桌面运行时。记录的演化到达“共享转换、锁定外部引擎、交付绑定版本运行时”；促成变化的依据是并发资源与独立引擎维护周期、用户环境需求。过程中，多个读者共享结果，单个取消不取消他人任务。继续接手时还需知道：内存限制有范围；应用运行、签名和引擎发布分别验收。

**T15.01**　预览和显式文档检查会请求同一次转换；只缓存完成结果仍不能限制源读取、排队数据和并发读者。（documented_problem；[S018](https://github.com/deepseek-ai/deepseek-harness/blob/86a402200d95fecef4529d969836f1fe13c6cb0d/.agents/notes/implemented/architecture/2026-09-15-bounded-office-conversion.md)）

**T15.02**　Host 共享转换队列先授权与接纳后读文件，前台优先；读者独立取消，最后读者离开后才取消共享工作。（recorded_decision；[S018](https://github.com/deepseek-ai/deepseek-harness/blob/86a402200d95fecef4529d969836f1fe13c6cb0d/.agents/notes/implemented/architecture/2026-09-15-bounded-office-conversion.md)）

**T15.03**　LibreOffice kit 独立拥有 API、引擎、测试和发布；Harness 拥有适配、授权、转换生命周期与 UI，并锁定准确 npm 版本。（documented_dependency；[S017](https://github.com/deepseek-ai/deepseek-harness/blob/86a402200d95fecef4529d969836f1fe13c6cb0d/.agents/notes/implemented/architecture/2026-09-14-independent-libreoffice-kit.md)）

**T15.04**　Desktop 将解释器与库作为 release-bound payload，记录版本和锁定输入摘要，先暂存完成再替换安装；系统解释器选择仍由用户控制。（documented_state；[S024](https://github.com/deepseek-ai/deepseek-harness/blob/86a402200d95fecef4529d969836f1fe13c6cb0d/.agents/notes/implemented/feature/2026-09-14-desktop-primary-runtime.md)）

**T15.05**　转换限制不覆盖引擎 RSS、调用者保留输出等全部内存；桌面签名检查和最终运行检查分别进行，运行成功沿用作者测试记录。（documented_limit；[S018](https://github.com/deepseek-ai/deepseek-harness/blob/86a402200d95fecef4529d969836f1fe13c6cb0d/.agents/notes/implemented/architecture/2026-09-15-bounded-office-conversion.md)、[S024](https://github.com/deepseek-ai/deepseek-harness/blob/86a402200d95fecef4529d969836f1fe13c6cb0d/.agents/notes/implemented/feature/2026-09-14-desktop-primary-runtime.md)）

**未决与使用边界：**内存限制有范围；应用运行、签名和引擎发布分别验收。

<a id="t16"></a>
### T16 · 模型协议与会话：工具角色变化要求迁移历史表示

这段工作涉及工具角色、持久格式与适配器。记录的演化到达“采用原生 tool 消息和相邻迁移”；促成变化的依据是会话包装与模型角色不一致。过程中，消息、调用和内容身份保留，原扩展归属保留。继续接手时还需知道：嵌套包装拒绝并留源；新角色需日志与适配投影。

**T16.01**　旧会话把工具结果放入 user-role 包装，模型对话和 provider 协议却将其视为独立角色，验证和回放因此不一致。（documented_problem；[S019](https://github.com/deepseek-ai/deepseek-harness/blob/86a402200d95fecef4529d969836f1fe13c6cb0d/.agents/notes/implemented/architecture/2026-09-15-first-class-tool-role-messages.md)）

**T16.02**　V4 使用独立 tool 消息；V3→V4 相邻迁移提升一层包装，拒绝嵌套包装并保留源代际。（recorded_decision；[S019](https://github.com/deepseek-ai/deepseek-harness/blob/86a402200d95fecef4529d969836f1fe13c6cb0d/.agents/notes/implemented/architecture/2026-09-15-first-class-tool-role-messages.md)）

**T16.03**　迁移保留消息身份、工具调用身份和结果内容；扩展字段按原归属加前缀保存，旧外层同名字段保持不透明。（documented_preservation；[S019](https://github.com/deepseek-ai/deepseek-harness/blob/86a402200d95fecef4529d969836f1fe13c6cb0d/.agents/notes/implemented/architecture/2026-09-15-first-class-tool-role-messages.md)）

**T16.04**　当前 V4 只读原生表示，适配器负责 provider 投影；新模型可见角色必须同时有持久事件与适配投影。（documented_constraint；[S019](https://github.com/deepseek-ai/deepseek-harness/blob/86a402200d95fecef4529d969836f1fe13c6cb0d/.agents/notes/implemented/architecture/2026-09-15-first-class-tool-role-messages.md)）

**未决与使用边界：**嵌套包装拒绝并留源；新角色需日志与适配投影。

## 跨过程联系

| 起点与终点 | 连接含义 | 来源定位 |
|---|---|---|
| T05 Creator → T01 插件管理环境 | 安装复用既有管理器，保存配置与激活分别报告 | T05.03—05；不推导 Loader 撤回导致 Creator 改造 |
| T02 预设 → T08 子代理 | 子代理属于旧运行修订的引用持有者之一 | T02.04 |
| T08 持续子代理 → T04 Team | Team 基于可接续成员；消息改用其 inbox | T04.01—05 与旧 Team 来源 |
| T04 Team ↔ T06 Schedule | 共用 inbox 接纳语义，各自持久状态和投递保证不同 | T04.04、T06.06；共享机制，非发生因果 |
| T16 消息角色 → T03 会话格式 | V3→V4 必须转换 tool 包装并保留源代际 | T16.01—04；T03.05 |
| T09 侧栏 ↔ T15 Office | 预览是共享转换的消费者；内容实例与转换队列各有寿命 | T09.04—05、T15.01—03 |
| T13 终端 → T15 交付 | 随包控制台的保留成为终端分配依赖 | T13.05；T15 的桌面来源 |
| T03 LogicalSession → 子阶段 | 阶段1—5，前三有草稿进展，后两未完；阶段1另有子任务 | T03.06 及 M5 原始计划 |
| T12 聊天迁移 → 子功能 | 独立视觉、Turn、分组和验收拆开跟踪 | T12.02—06 |

## 固定、修订与证据边界

本版包含83条来源事实。各过程的“未决与使用边界”另形成16条research_gap记录，属于研究者在2026-10-20登记的接手范围，不冒充上游事实。三份表示同时接收这99条记录，编号如T01.GAP；原始资料版本时间与研究缺口记录日期分别保留。

v1 的文件哈希、原 54 条事实输入哈希、全部来源对象与三种表示哈希保存在主工作区 `artifacts/agent-task-state/maintenance/dsh-composition-2026-10-20/v2/manifest.json`。该目录是本地分析产物，不提交原始第三方正文。后续修改本页须形成新的输入版本与批次，不能覆盖本轮已比较的输入。

原始 PR 审阅和运行现场并未全部取得；缺失项已随过程保留。此处完整指本版列出的事实完整进入比较；全项目还有可扩展过程，跨项目适用性未验证。
