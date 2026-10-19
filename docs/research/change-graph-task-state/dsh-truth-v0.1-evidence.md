---
title: DSH truth v0.1 证据与边界
status: active
created: 2026-10-19
updated: 2026-10-19
tags: [research, dsh, evidence, truth]
---

# DSH truth v0.1 证据与边界

[阅读版](dsh-truth-v0.1.md)连续讲述十段过程。本页保存完整的54条事实、固定来源和待查项，是后续编码与重建评估的事实对照清单。阅读版与本页使用相同材料截止日：2026年10月15日。

## 证据归属与核验范围

- 提交记录提供Git事件、时间和署名；署名按author、committer原样登记。
- 版本化设计记录提供当时的方案、理由、结果和限制，回顾性描述保留作者归属。
- 本研究已核验来源Git对象、提交先后和本地引用。运行结果、性能和测试结论沿用作者报告，独立复验待做。
- 快照时间、笔记文件名日期和主线合入时间分别记录。各过程内部按证据明确的先后叙述，跨分支顺序保留待查项。

<a id="t01"></a>

## T01 · 插件加载：加入事务重载，后来选择性撤回

范围：事务式插件重载及撤回后的消费者调整。

<details><summary>完整事实与待查项</summary>

**T01.01**　8月2日有一个提交加入事务式配置重载。

**T01.02**　后来的决定要求撤回 #932 的五个提交；它记录的理由是候选导入、回滚和生命周期处理使 vendored 实现偏离上游过多。

**T01.03**　撤回保留了文件初始化、模块导出的两项修补，以及较大合并中的无关仓库插件能力。

**T01.04**　9月9日出现撤回提交及消费者适配提交，9月11日又有保持启动失败策略的修补。

**T01.05**　截止快照记录的结果是：插件失败可以留下部分应用的配置树，Loader 不自动恢复旧配置；需要可用插件的消费者自行审查实际激活结果。

待查：完整#932/#936审阅讨论和最终决策者待查。

</details>

| 事实编号 | 证据归属 | 来源 |
|---|---|---|
| T01.01 | commit_record | [L1](https://github.com/deepseek-ai/deepseek-harness/commit/195f7fa9af0ff33e75f44e767a23b8e1e8aaa200) |
| T01.02 | recorded_decision | [L2](https://github.com/deepseek-ai/deepseek-harness/blob/86a402200d95fecef4529d969836f1fe13c6cb0d/.agents/notes/implemented/simplification/2026-09-09-nontransactional-loader.md) |
| T01.03 | recorded_decision | [L2](https://github.com/deepseek-ai/deepseek-harness/blob/86a402200d95fecef4529d969836f1fe13c6cb0d/.agents/notes/implemented/simplification/2026-09-09-nontransactional-loader.md) |
| T01.04 | commit_record | [L3](https://github.com/deepseek-ai/deepseek-harness/commit/e07f41d5fd8ca172287fda0f923b4d1f69c592f3)、[L4](https://github.com/deepseek-ai/deepseek-harness/commit/2abb542a222032b1ad3c5abd7bb65ffffe15b8de)、[L5](https://github.com/deepseek-ai/deepseek-harness/commit/f4a7dd607709025bc3ad19dab8ffbb038cd13962) |
| T01.05 | documented_result | [L2](https://github.com/deepseek-ai/deepseek-harness/blob/86a402200d95fecef4529d969836f1fe13c6cb0d/.agents/notes/implemented/simplification/2026-09-09-nontransactional-loader.md) |

<details><summary>固定来源、版本和本地校验依据</summary>

- **L1**：fix(cordis): make config reload transactional；提交 `195f7fa9af0ff33e75f44e767a23b8e1e8aaa200`；committer时间 `2026-08-02T01:25:01+08:00`；记录署名 author=Tianyi Cui，committer=Tianyi Cui。
- **L2**：Agent Note: Keep Loader mutations non-transactional；dsh-v0.2.1-alpha.4；提交 `86a402200d95fecef4529d969836f1fe13c6cb0d`；内容 `d37539cb3e34c32cd026f330ce92a48baf4bcd0c`。提交时间 `2026-10-15T20:22:44+08:00`（快照时间）。
- **L3**：Revert #932 transactional Cordis reload changes；提交 `e07f41d5fd8ca172287fda0f923b4d1f69c592f3`；committer时间 `2026-09-09T17:32:09+08:00`；记录署名 author=turtle1999，committer=turtle1999。
- **L4**：Adapt current consumers to nontransactional Cordis Loader；提交 `2abb542a222032b1ad3c5abd7bb65ffffe15b8de`；committer时间 `2026-09-09T17:33:32+08:00`；记录署名 author=turtle1999，committer=turtle1999。
- **L5**：fix(boot): preserve failure policy on nontransactional Loader；提交 `f4a7dd607709025bc3ad19dab8ffbb038cd13962`；committer时间 `2026-09-11T12:47:46+08:00`；记录署名 author=turtle1999，committer=turtle1999。

</details>

<a id="t02"></a>

## T02 · Agent 预设：按会话装载，改为声明式配置并保留旧修订

范围：预设配置、运行修订和重启恢复的边界。

<details><summary>完整事实与待查项</summary>

**T02.01**　rc.7 的记录说明，先前进程级配置决定全部会话能力；当时已改为每个 Agent 装载自己的预设目录，Host 的注册服务和跨会话设施仍共享。

**T02.02**　同一份历史记录记下了实施中的问题：Host 读者曾找不到移入会话的服务，卸载可能改写预设输入，存储后端没有全部保存新增预设身份，Host 缺少闲置 Agent 的释放时机。

**T02.03**　9月21日主线有声明式预设提交；在 0.1.7-rc.2 中，预设已由普通配置声明，注册器拥有运行修订及其插件树。

**T02.04**　修改定义会使旧修订退役；正在使用它的 Agent、子代理和临时读取者继续持有引用，最后释放时才清理。配置持久化与实际激活结果分别报告。

**T02.05**　旧可执行修订保存在进程内；重启按保存的预设身份解析当前配置，缺少定义时恢复失败。

待查：局部修补各自进入主线的日期待补。

</details>

| 事实编号 | 证据归属 | 来源 |
|---|---|---|
| T02.01 | documented_state | [P1](https://github.com/deepseek-ai/deepseek-harness/blob/99f6f02fecdb7dff40c3fbc9470f5907c29f74ca/.agents/notes/implemented/architecture/2026-08-03-per-session-agent-presets.md) |
| T02.02 | author_reported_findings | [P1](https://github.com/deepseek-ai/deepseek-harness/blob/99f6f02fecdb7dff40c3fbc9470f5907c29f74ca/.agents/notes/implemented/architecture/2026-08-03-per-session-agent-presets.md) |
| T02.03 | documented_transition | [P4](https://github.com/deepseek-ai/deepseek-harness/commit/d1e22a7e247060496e1acdba9ef3be1700e23ec7)、[P2](https://github.com/deepseek-ai/deepseek-harness/blob/477b4f420553e8a52c2fbccc464d7561b239c443/.agents/notes/implemented/architecture/2026-09-18-declarative-agent-presets.md) |
| T02.04 | documented_result | [P2](https://github.com/deepseek-ai/deepseek-harness/blob/477b4f420553e8a52c2fbccc464d7561b239c443/.agents/notes/implemented/architecture/2026-09-18-declarative-agent-presets.md) |
| T02.05 | documented_limit | [P2](https://github.com/deepseek-ai/deepseek-harness/blob/477b4f420553e8a52c2fbccc464d7561b239c443/.agents/notes/implemented/architecture/2026-09-18-declarative-agent-presets.md)、[P3](https://github.com/deepseek-ai/deepseek-harness/blob/86a402200d95fecef4529d969836f1fe13c6cb0d/.agents/notes/implemented/architecture/2026-09-18-declarative-agent-presets.md) |

<details><summary>固定来源、版本和本地校验依据</summary>

- **P1**：Agent Note: A session's agent is composed from a preset cordis.yml；dsh-v0.1.0-rc.7；提交 `99f6f02fecdb7dff40c3fbc9470f5907c29f74ca`；内容 `5a82f0220058c10892b819a83499c817aa9be6ad`。提交时间 `2026-08-17T19:03:17+08:00`（快照时间）。
- **P4**：feat(preset): declare Agent compositions in profile YAML (#4569)；提交 `d1e22a7e247060496e1acdba9ef3be1700e23ec7`；committer时间 `2026-09-21T08:24:18Z`；记录署名 author=Turtle，committer=GitHub。
- **P2**：Agent Note: Declarative Agent presets and retained revisions；dsh-v0.1.7-rc.2；提交 `477b4f420553e8a52c2fbccc464d7561b239c443`；内容 `bf900bc4dc99f12af4624d14a6ec5497adaa1993`。提交时间 `2026-09-24T21:39:59+08:00`（快照时间）。
- **P3**：Agent Note: Declarative Agent presets and retained revisions；dsh-v0.2.1-alpha.4；提交 `86a402200d95fecef4529d969836f1fe13c6cb0d`；内容 `38fa045ef149ab9fb607641d4a37465847ae77b0`。提交时间 `2026-10-15T20:22:44+08:00`（快照时间）。

</details>

<a id="t03"></a>

## T03 · 会话迁移：一次合入与撤回，之后再引入流式实现

范围：迁移实现的反复、当前迁移协议和未完成提案。

<details><summary>完整事实与待查项</summary>

**T03.01**　8月25日主线合入 #2698，提交正文将其称为流式格式迁移管线。

**T03.02**　同日主线合入 #3054，正文为撤回该迁移管线；撤回理由待查。

**T03.03**　9月6日主线合入 #3585，属于后来的流式迁移实现；两次实现的对应关系和复用范围待查。

**T03.04**　截止快照的设计记录报告，一份116 MB会话在整份转换实现中耗尽16 GB Node进程。测量归属为作者报告。

**T03.05**　截止记录采用每份会话独立的有状态转换阶段；原已提交格式文件保留，仅发布最终当前代际，中间格式不逐份落盘。不同历史代际的解释和拒绝规则分别保留。

**T03.06**　LogicalSession存储重建仍是proposed：阶段1、2为draft work complete，阶段3记录实现与远程CI完成但仍为draft，阶段4、5未完成。

待查：第一次撤回原因、两个实现的完整diff及代码复用范围待查。 性能数字为作者记录，独立复测待做。

</details>

| 事实编号 | 证据归属 | 来源 |
|---|---|---|
| T03.01 | commit_record | [M1](https://github.com/deepseek-ai/deepseek-harness/commit/3fefcdbe3f83a309f05075b9e9f05450509318ed) |
| T03.02 | commit_record | [M2](https://github.com/deepseek-ai/deepseek-harness/commit/a1781cc4a81bf14551ed0d6e0ee618d14fd9b823) |
| T03.03 | commit_record | [M3](https://github.com/deepseek-ai/deepseek-harness/commit/80306f51a6f36e26c71bcf0be5621af6b8ad8e65) |
| T03.04 | author_reported_failure | [M4](https://github.com/deepseek-ai/deepseek-harness/blob/86a402200d95fecef4529d969836f1fe13c6cb0d/.agents/notes/implemented/architecture/2026-08-31-released-session-format-migrations.md) |
| T03.05 | documented_result | [M4](https://github.com/deepseek-ai/deepseek-harness/blob/86a402200d95fecef4529d969836f1fe13c6cb0d/.agents/notes/implemented/architecture/2026-08-31-released-session-format-migrations.md) |
| T03.06 | documented_status | [M5](https://github.com/deepseek-ai/deepseek-harness/blob/86a402200d95fecef4529d969836f1fe13c6cb0d/.agents/notes/proposed/architecture/2026-09-06-logical-session-storage-rebuild.md) |

<details><summary>固定来源、版本和本地校验依据</summary>

- **M1**：Merge pull request #2698 from deepseek-harness/xtr/session-format-migration；提交 `3fefcdbe3f83a309f05075b9e9f05450509318ed`；committer时间 `2026-08-25T13:47:43+08:00`；记录署名 author=_Kerman，committer=GitHub。
- **M2**：Merge pull request #3054 from deepseek-harness/worktree-revert2698；提交 `a1781cc4a81bf14551ed0d6e0ee618d14fd9b823`；committer时间 `2026-08-25T15:47:19+08:00`；记录署名 author=imccyu，committer=GitHub。
- **M3**：Merge pull request #3585 from deepseek-harness/session-migration-streaming；提交 `80306f51a6f36e26c71bcf0be5621af6b8ad8e65`；committer时间 `2026-09-06T02:34:12+08:00`；记录署名 author=imccyu，committer=GitHub。
- **M4**：Agent Note: Released Session formats migrate through stateful streaming stages；dsh-v0.2.1-alpha.4；提交 `86a402200d95fecef4529d969836f1fe13c6cb0d`；内容 `007620d641c65955409bebb98c4cbd5c5e449a18`。提交时间 `2026-10-15T20:22:44+08:00`（快照时间）。
- **M5**：Agent Note: Logical session and storage rebuild；dsh-v0.2.1-alpha.4；提交 `86a402200d95fecef4529d969836f1fe13c6cb0d`；内容 `cb639c0052417eb5a621925bc02dccae7f8f1c6c`。提交时间 `2026-10-15T20:22:44+08:00`（快照时间）。

</details>

<a id="t04"></a>

## T04 · Team 消息：从独立 outbox 改为目标 inbox，保留名单与任务

范围：消息交付承诺的部分替代及历史记录处理。

<details><summary>完整事实与待查项</summary>

**T04.01**　0.1.7-rc.2 的 Team 记录将发送意图先写入并刷盘到 Lead 日志，再向目标投递并确认；恢复时重试未确认项，并提供目标侧去重。名单和共享任务也有各自的持久状态。

**T04.02**　新记录把独立 outbox 的身份、确认、重试和清理视为重复管理，选择直接通过目标 Agent inbox 接纳消息。

**T04.03**　该变更10月8日合入主线，0.2.1-alpha.2中已有对应记录；主题笔记文件名日期为9月26日。

**T04.04**　新发送返回目标inbox接纳的消息身份或失败。Team的未接纳意图保存、重启重试和显式重发去重机制退出；成功结果表示队列接纳。

**T04.05**　旧 mailbox 记录仍可解码和展示，但旧待发项不再投递；替代范围仅为消息机制，成员名单和任务决定继续保留。

**T04.06**　记录以实验功能的稳定性约定为取舍条件，接受了旧待发消息失去恢复投递能力的后果。

待查：用户待发消息实际损失数量待查。

</details>

| 事实编号 | 证据归属 | 来源 |
|---|---|---|
| T04.01 | documented_state | [T1](https://github.com/deepseek-ai/deepseek-harness/blob/477b4f420553e8a52c2fbccc464d7561b239c443/.agents/notes/implemented/feature/2026-08-05-agent-teams.md) |
| T04.02 | recorded_decision | [T2](https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/.agents/notes/implemented/simplification/2026-09-26-team-direct-inbox.md) |
| T04.03 | commit_record | [T3](https://github.com/deepseek-ai/deepseek-harness/commit/ea0980dab432263a9d1cd2b8e4998a1d6e6e6ae7)、[T2](https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/.agents/notes/implemented/simplification/2026-09-26-team-direct-inbox.md) |
| T04.04 | documented_result | [T2](https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/.agents/notes/implemented/simplification/2026-09-26-team-direct-inbox.md) |
| T04.05 | documented_result | [T2](https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/.agents/notes/implemented/simplification/2026-09-26-team-direct-inbox.md) |
| T04.06 | recorded_rationale | [T2](https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/.agents/notes/implemented/simplification/2026-09-26-team-direct-inbox.md) |

<details><summary>固定来源、版本和本地校验依据</summary>

- **T1**：Agent Note: Durable Agent Teams over continuable children；dsh-v0.1.7-rc.2；提交 `477b4f420553e8a52c2fbccc464d7561b239c443`；内容 `6333e511ba1e71823cfa55c27ba46b2665d1ef15`。提交时间 `2026-09-24T21:39:59+08:00`（快照时间）。
- **T2**：Agent Note: Team messages use the target inbox；dsh-v0.2.1-alpha.2；提交 `d743267388641bc76f17c45ce8b4c231aed1d32c`；内容 `58d18d0ecfef4d292cfbb8cbf3e4c449b1fa1d6d`。提交时间 `2026-10-09T17:31:32+08:00`（快照时间）。
- **T3**：Merge pull request #5247 from deepseek-harness/refactor/agent-team-direct-steer；提交 `ea0980dab432263a9d1cd2b8e4998a1d6e6e6ae7`；committer时间 `2026-10-08T16:42:56+08:00`；记录署名 author=Dudu-0223，committer=GitHub。

</details>

<a id="t05"></a>

## T05 · Creator：临时修改运行时，转为安装持久插件

范围：模型修改能力的工作流替换。

<details><summary>完整事实与待查项</summary>

**T05.01**　rc.8 的旧工具允许模型检查、临时装载和卸载进程内插件；临时插件不写文件，不修改配置，重启后不恢复。

**T05.02**　旧记录要求保留实验成果时另行实现普通项目插件或可安装 bundle，没有自动转正路径。

**T05.03**　9月16日 #4324 合入主线；0.1.6-alpha.2记录Creator改走已有插件管理器：先写包和配置文件，再安装bundle。

**T05.04**　模型侧旧的生成代码修改入口退出，但已有运行时和Client消费者继续保留所用服务；历史工具卡片仍可读取。

**T05.05**　新安装的配置跨重启保留并影响同一profile中的会话；工具操作要求完整访问或单次批准，配置保存与能力实际生效分别报告，已安装包替换当时需要重启。

待查：中间工具命名和生成代码工作流的逐版修订待补。

</details>

| 事实编号 | 证据归属 | 来源 |
|---|---|---|
| T05.01 | documented_state | [C1](https://github.com/deepseek-ai/deepseek-harness/blob/141eb6fef83422698aef7a981029e843e8161534/.agents/notes/implemented/feature/2026-07-08-self-referential-cordis-toolset.md) |
| T05.02 | documented_limit | [C1](https://github.com/deepseek-ai/deepseek-harness/blob/141eb6fef83422698aef7a981029e843e8161534/.agents/notes/implemented/feature/2026-07-08-self-referential-cordis-toolset.md) |
| T05.03 | documented_transition | [C3](https://github.com/deepseek-ai/deepseek-harness/commit/f756097108d1fc69f71bae1ee3c6114e5ae40b12)、[C2](https://github.com/deepseek-ai/deepseek-harness/blob/ddefc45fbc7f8e46dd73185e68295696d1297887/.agents/notes/implemented/architecture/2026-09-16-creator-persistent-plugin-management.md) |
| T05.04 | documented_result | [C2](https://github.com/deepseek-ai/deepseek-harness/blob/ddefc45fbc7f8e46dd73185e68295696d1297887/.agents/notes/implemented/architecture/2026-09-16-creator-persistent-plugin-management.md) |
| T05.05 | documented_result | [C2](https://github.com/deepseek-ai/deepseek-harness/blob/ddefc45fbc7f8e46dd73185e68295696d1297887/.agents/notes/implemented/architecture/2026-09-16-creator-persistent-plugin-management.md) |

<details><summary>固定来源、版本和本地校验依据</summary>

- **C1**：Agent Note: The self-referential cordis toolset；dsh-v0.1.0-rc.8；提交 `141eb6fef83422698aef7a981029e843e8161534`；内容 `d408bb774fa62dd6ff0deef7003f5b0851b80e82`。提交时间 `2026-08-19T23:11:50+08:00`（快照时间）。
- **C3**：Merge pull request #4324 from deepseek-harness/turtle/creator-plugin-manager；提交 `f756097108d1fc69f71bae1ee3c6114e5ae40b12`；committer时间 `2026-09-16T17:58:53+08:00`；记录署名 author=Turtle，committer=GitHub。
- **C2**：Agent Note: Creator mode installs persistent plugin bundles；dsh-v0.1.6-alpha.2；提交 `ddefc45fbc7f8e46dd73185e68295696d1297887`；内容 `04ccbb83fe6d2f5c460f53100a9087cce119ea4d`。提交时间 `2026-09-17T21:19:19+08:00`（快照时间）。

</details>

<a id="t06"></a>

## T06 · 定时任务：从会话日志转为Host存储，再限制历史保留

范围：权威存储、冷会话投递、删除和回执保留。

<details><summary>完整事实与待查项</summary>

**T06.01**　0.1.7-rc.1 的提醒以原会话日志为唯一持久依据，只在会话活跃时运行；冷会话不触发，重新加载后再处理过期提醒，分叉不继承父任务的活跃执行。

**T06.02**　0.1.7-rc.2 已记录改用独立Host任务存储，恢复计时器不必先加载全部会话；到期时再恢复原会话并投递。作者记录的目标包含独立查看待处理和已投递任务。

**T06.03**　历史schedule事件仍可读，但不自动导入新任务存储；加载有旧活跃提醒的会话会提示重建。规则中部分旧时间计算和接纳语义继续适用。

**T06.04**　同一Host存储记录后来保留任务和回执；专门的后续决定记下了全量JSON重写下的增长问题，改为删除任务时删除其行与回执，并按时间和数量限制交付历史。

**T06.05**　交付历史分别标记实际裁剪与旧历史不可用；删除任务后，已经进入会话的消息保留。

**T06.06**　回执记录消息已持久进入inbox。任务存储与消息存储分开提交，崩溃存在重复投递风险。

待查：Host存储和裁剪决定均见于rc.2，两项改动间的实际部署间隔待查。

</details>

| 事实编号 | 证据归属 | 来源 |
|---|---|---|
| T06.01 | documented_state | [S1](https://github.com/deepseek-ai/deepseek-harness/blob/46a7f68b0922371ce7144b668b90e377d8e799f4/.agents/notes/implemented/feature/2026-08-05-durable-web-schedule.md) |
| T06.02 | documented_transition | [S2](https://github.com/deepseek-ai/deepseek-harness/blob/477b4f420553e8a52c2fbccc464d7561b239c443/.agents/notes/implemented/architecture/2026-09-16-host-schedule-storage.md) |
| T06.03 | documented_result | [S2](https://github.com/deepseek-ai/deepseek-harness/blob/477b4f420553e8a52c2fbccc464d7561b239c443/.agents/notes/implemented/architecture/2026-09-16-host-schedule-storage.md) |
| T06.04 | recorded_transition | [S2](https://github.com/deepseek-ai/deepseek-harness/blob/477b4f420553e8a52c2fbccc464d7561b239c443/.agents/notes/implemented/architecture/2026-09-16-host-schedule-storage.md)、[S3](https://github.com/deepseek-ai/deepseek-harness/blob/86a402200d95fecef4529d969836f1fe13c6cb0d/.agents/notes/implemented/architecture/2026-09-22-schedule-hard-delete-and-bounded-history.md) |
| T06.05 | documented_result | [S3](https://github.com/deepseek-ai/deepseek-harness/blob/86a402200d95fecef4529d969836f1fe13c6cb0d/.agents/notes/implemented/architecture/2026-09-22-schedule-hard-delete-and-bounded-history.md)、[S2](https://github.com/deepseek-ai/deepseek-harness/blob/477b4f420553e8a52c2fbccc464d7561b239c443/.agents/notes/implemented/architecture/2026-09-16-host-schedule-storage.md) |
| T06.06 | documented_limit | [S2](https://github.com/deepseek-ai/deepseek-harness/blob/477b4f420553e8a52c2fbccc464d7561b239c443/.agents/notes/implemented/architecture/2026-09-16-host-schedule-storage.md) |

<details><summary>固定来源、版本和本地校验依据</summary>

- **S1**：Agent Note: Durable Session-local reminders；dsh-v0.1.7-rc.1；提交 `46a7f68b0922371ce7144b668b90e377d8e799f4`；内容 `b09ab752c9db0587b49dbe50a152144b9ff19515`。提交时间 `2026-09-23T21:03:33+08:00`（快照时间）。
- **S2**：Agent Note: Host-owned scheduled messages；dsh-v0.1.7-rc.2；提交 `477b4f420553e8a52c2fbccc464d7561b239c443`；内容 `79a4f7207184e592f00a4d9946c2ca2e9345032d`。提交时间 `2026-09-24T21:39:59+08:00`（快照时间）。
- **S3**：Agent Note: Schedule deletes task rows and bounds delivery history；dsh-v0.2.1-alpha.4；提交 `86a402200d95fecef4529d969836f1fe13c6cb0d`；内容 `90127d688777a7c0c63d6d817e6df35a9f5b77b5`。提交时间 `2026-10-15T20:22:44+08:00`（快照时间）。

</details>

<a id="t07"></a>

## T07 · 远程执行：移除E2B实现，保留接口并继续SSH路线

范围：一个供应实现的引入、退出、保留成果和另一供应实现。

<details><summary>完整事实与待查项</summary>

**T07.01**　8月8日主线合入E2B概念验证相关分支；后来的退出记录说明，它曾为文件、进程、终端等提供同一个远程执行世界。

**T07.02**　退出记录说明，新PTC需要与程序标准流独立的双向控制流；当时固定E2B SDK的通道能力及输出保留使继续适配需要额外传输工程。

**T07.03**　9月11日主线合入移除E2B提供者的变更；截止记录列出实现、SDK依赖、集成夹具及可选工作流等移除范围。

**T07.04**　通用文件系统、进程和终端接口及其异步语义继续保留；远程执行需求继续存在。退出理由针对当时固定SDK的集成成本。

**T07.05**　截止SSH记录由远端helper提供执行能力，Harness、凭据、模型传输与会话持久化仍在本地；断连后的修改性操作不自动重放。

待查：SSH引入与E2B删除的逐提交依赖和精确先后待查。

</details>

| 事实编号 | 证据归属 | 来源 |
|---|---|---|
| T07.01 | documented_transition | [R3](https://github.com/deepseek-ai/deepseek-harness/commit/33312c6a89e2c4c7efd7b067d88506df2a9d982f)、[R1](https://github.com/deepseek-ai/deepseek-harness/blob/86a402200d95fecef4529d969836f1fe13c6cb0d/.agents/notes/implemented/simplification/2026-09-11-remove-e2b-providers.md) |
| T07.02 | recorded_rationale | [R1](https://github.com/deepseek-ai/deepseek-harness/blob/86a402200d95fecef4529d969836f1fe13c6cb0d/.agents/notes/implemented/simplification/2026-09-11-remove-e2b-providers.md) |
| T07.03 | documented_transition | [R4](https://github.com/deepseek-ai/deepseek-harness/commit/09a6fbc388bc6de135dea7d86b85f6e96b3bf32a)、[R1](https://github.com/deepseek-ai/deepseek-harness/blob/86a402200d95fecef4529d969836f1fe13c6cb0d/.agents/notes/implemented/simplification/2026-09-11-remove-e2b-providers.md) |
| T07.04 | documented_result | [R1](https://github.com/deepseek-ai/deepseek-harness/blob/86a402200d95fecef4529d969836f1fe13c6cb0d/.agents/notes/implemented/simplification/2026-09-11-remove-e2b-providers.md) |
| T07.05 | documented_state | [R2](https://github.com/deepseek-ai/deepseek-harness/blob/86a402200d95fecef4529d969836f1fe13c6cb0d/.agents/notes/implemented/architecture/2026-09-11-posix-ssh-runtime.md) |

<details><summary>固定来源、版本和本地校验依据</summary>

- **R3**：Merge pull request #796 from deepseek-harness/worktree/e2b-poc-20260727；提交 `33312c6a89e2c4c7efd7b067d88506df2a9d982f`；committer时间 `2026-08-08T23:15:49+08:00`；记录署名 author=Tianyi Cui，committer=GitHub。
- **R1**：Agent Note: Remove the E2B execution providers；dsh-v0.2.1-alpha.4；提交 `86a402200d95fecef4529d969836f1fe13c6cb0d`；内容 `a73c5849ff98751b76903b1ef0c284112efba073`。提交时间 `2026-10-15T20:22:44+08:00`（快照时间）。
- **R4**：Merge pull request #4036 from deepseek-harness/worktree/ptc-sandbox/remove-e2b；提交 `09a6fbc388bc6de135dea7d86b85f6e96b3bf32a`；committer时间 `2026-09-11T23:30:29+08:00`；记录署名 author=Tianyi Cui，committer=GitHub。
- **R2**：Agent Note: POSIX SSH execution providers；dsh-v0.2.1-alpha.4；提交 `86a402200d95fecef4529d969836f1fe13c6cb0d`；内容 `3bd1c340d158709826ab7cbd5d724cb151a23ec1`。提交时间 `2026-10-15T20:22:44+08:00`（快照时间）。

</details>

<a id="t08"></a>

## T08 · 子代理：先分开持续会话与一次执行，再统一activation入口

范围：持续会话与一次执行的管理路径变化及仍保留的后端差异。

<details><summary>完整事实与待查项</summary>

**T08.01**　0.2.1-alpha.1 的持续子代理记录回顾了先前Task结束就销毁Agent的办法，并指出它把会话生命周期与一次结果绑定在一起。

**T08.02**　该版已将持久Session与进程内Activation分开：同一会话可多轮续接、冷恢复，Agent inbox负责消息顺序；一次性提供者执行路径仍独立存在。

**T08.03**　10月6日统一子代理重构合入主线；alpha.2记录将所有提供者接入统一activation入口，本地spawn/fork只提供创建数据。

**T08.04**　模型委派返回后台子任务身份；工作流通过同一activation等待结果并清理，不额外给父Agent发送完成通知。

**T08.05**　外部后端保留一次执行适配器，通过同一入口管理容量和生命周期；外部执行保持无本地Session、无多轮续接的能力范围。执行结果在清理失败时保留，清理错误另报。

**T08.06**　历史一次执行描述仍可读取。完成通知可能与子代理主动汇报重复，记录接受了这项代价。

待查：早期Task方案的逐步现场记录待补。

</details>

| 事实编号 | 证据归属 | 来源 |
|---|---|---|
| T08.01 | retrospective_report | [A1](https://github.com/deepseek-ai/deepseek-harness/blob/5badb15009ae1756c3afe0ae0cef1faafc290ccc/.agents/notes/implemented/feature/2026-07-28-continuable-subagent-conversations.md) |
| T08.02 | documented_state | [A1](https://github.com/deepseek-ai/deepseek-harness/blob/5badb15009ae1756c3afe0ae0cef1faafc290ccc/.agents/notes/implemented/feature/2026-07-28-continuable-subagent-conversations.md) |
| T08.03 | documented_transition | [A3](https://github.com/deepseek-ai/deepseek-harness/commit/bf1c4e01ba7088b3cb0aeb36caa702965eb5f6ec)、[A2](https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/.agents/notes/implemented/simplification/2026-09-17-unified-subagent-activations.md) |
| T08.04 | documented_result | [A2](https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/.agents/notes/implemented/simplification/2026-09-17-unified-subagent-activations.md) |
| T08.05 | documented_result | [A2](https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/.agents/notes/implemented/simplification/2026-09-17-unified-subagent-activations.md) |
| T08.06 | documented_limit | [A2](https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/.agents/notes/implemented/simplification/2026-09-17-unified-subagent-activations.md) |

<details><summary>固定来源、版本和本地校验依据</summary>

- **A1**：Agent Note: Continuable subagents；dsh-v0.2.1-alpha.1；提交 `5badb15009ae1756c3afe0ae0cef1faafc290ccc`；内容 `142119cd0ade998332fadf73b6b41441d2ab59a2`。提交时间 `2026-10-03T11:48:13+08:00`（快照时间）。
- **A3**：Merge pull request #4394 from deepseek-harness/refactor/subagent；提交 `bf1c4e01ba7088b3cb0aeb36caa702965eb5f6ec`；committer时间 `2026-10-06T15:08:30+08:00`；记录署名 author=Dudu-0223，committer=GitHub。
- **A2**：Agent Note: Unified subagent activations；dsh-v0.2.1-alpha.2；提交 `d743267388641bc76f17c45ce8b4c231aed1d32c`；内容 `07268e40160f7a8a84f564c95440849b8c28c7a8`。提交时间 `2026-10-09T17:31:32+08:00`（快照时间）。

</details>

<a id="t09"></a>

## T09 · 侧栏：从工具详情到通用工作区，调整布局和内容的寿命

范围：侧栏基础设施与内容树保留。

<details><summary>完整事实与待查项</summary>

**T09.01**　0.1.5-alpha.1 记录旧右栏只能显示工具详情；文件链接交给Host操作系统，远程浏览器无法直接查看文件。

**T09.02**　团队评估第三方布局库，保留FlexLayout作备选；设计记录称自建原型通过相关浏览器检查后继续自建。

**T09.03**　记录中的首个原型采用drawer；产品形态改为实际挤占聊天宽度的右侧栏，布局支持分栏、标签、浮窗及撤销，内容类型由另外的插件接口提供。

**T09.04**　后续记录指出，卸载内容或改变其DOM祖先会断开浏览器页面；侧栏为声明keepMounted的类型提供内容保留，Desktop Browser启用它，其他类型仍按可见性挂载。停靠、浮动和会话切换不移动已保留页面的DOM祖先。

**T09.05**　布局状态、内容实例寿命和数据读取分别承担责任；后续保留内容树的决定没有整体废弃侧栏布局引擎。

待查：完整原型、用户评审和失败录像待取回；布局库评估结果归属为作者报告。

</details>

| 事实编号 | 证据归属 | 来源 |
|---|---|---|
| T09.01 | retrospective_report | [U1](https://github.com/deepseek-ai/deepseek-harness/blob/5dda764ed3aa172535a7967b06ff95d9cbfe536a/.agents/notes/implemented/feature/2026-09-04-right-sidebar-docking-infrastructure.md) |
| T09.02 | author_reported_trial | [U1](https://github.com/deepseek-ai/deepseek-harness/blob/5dda764ed3aa172535a7967b06ff95d9cbfe536a/.agents/notes/implemented/feature/2026-09-04-right-sidebar-docking-infrastructure.md) |
| T09.03 | recorded_transition | [U1](https://github.com/deepseek-ai/deepseek-harness/blob/5dda764ed3aa172535a7967b06ff95d9cbfe536a/.agents/notes/implemented/feature/2026-09-04-right-sidebar-docking-infrastructure.md) |
| T09.04 | recorded_transition | [U2](https://github.com/deepseek-ai/deepseek-harness/blob/86a402200d95fecef4529d969836f1fe13c6cb0d/.agents/notes/implemented/architecture/2026-09-20-sidebar-retained-tab-layout.md) |
| T09.05 | documented_result | [U1](https://github.com/deepseek-ai/deepseek-harness/blob/5dda764ed3aa172535a7967b06ff95d9cbfe536a/.agents/notes/implemented/feature/2026-09-04-right-sidebar-docking-infrastructure.md)、[U2](https://github.com/deepseek-ai/deepseek-harness/blob/86a402200d95fecef4529d969836f1fe13c6cb0d/.agents/notes/implemented/architecture/2026-09-20-sidebar-retained-tab-layout.md) |

<details><summary>固定来源、版本和本地校验依据</summary>

- **U1**：Agent Note: Right Sidebar docking infrastructure；dsh-v0.1.5-alpha.1；提交 `5dda764ed3aa172535a7967b06ff95d9cbfe536a`；内容 `8e1d1b5518c3b80a05be877ee9796883b6eb9a60`。提交时间 `2026-09-08T23:25:45+08:00`（快照时间）。
- **U2**：Agent Note: Stable Sidebar tab mounting and Session retention；dsh-v0.2.1-alpha.4；提交 `86a402200d95fecef4529d969836f1fe13c6cb0d`；内容 `574667c79f15643f0b2f58b2e8c54d793a7df869`。提交时间 `2026-10-15T20:22:44+08:00`（快照时间）。

</details>

<a id="t10"></a>

## T10 · 目标控制：保存目标，再修复人工暂停被执行绕过的问题

范围：目标持久状态、运行授权及两轮暂停修正。

<details><summary>完整事实与待查项</summary>

**T10.01**　早期goal记录将目标修改写成独立goal/change事件，下一轮提示另由驱动组件入队；目标存在不以消息是否被模型接纳为条件。

**T10.02**　持久目标与进程内运行授权分开；恢复或分叉可保留active目标，但默认disarmed，不会因打开会话就自动继续。

**T10.03**　第一次暂停修复记录的问题是：Web已标记paused并禁止后续自动轮次，但当前模型轮仍在执行，还可能自行调用resume。修复增加人工暂停时取消当前轮，并保留输入队列。

**T10.04**　后续记录指出，前一个修复后，稍后的人类轮次仍可能被模型用来恢复持久paused目标；UI也混淆了active-but-disarmed与armed。

**T10.05**　后续改动禁止模型工具恢复持久paused目标，仍允许它在合适人类输入下恢复active-but-disarmed或blocked目标；界面分别显示运行授权，人类显式恢复入口继续保留。

待查：前后暂停修复的运行故障日志及精确合入时间待补。

</details>

| 事实编号 | 证据归属 | 来源 |
|---|---|---|
| T10.01 | documented_state | [G1](https://github.com/deepseek-ai/deepseek-harness/blob/b64c3ac1ba37a8afe20de534ab666e85ae69377b/.agents/notes/implemented/architecture/2026-07-31-goal-owned-durable-events.md) |
| T10.02 | documented_state | [G4](https://github.com/deepseek-ai/deepseek-harness/blob/86a402200d95fecef4529d969836f1fe13c6cb0d/.agents/notes/archived/feature/2026-07-19-persisted-same-session-goal-domain.md) |
| T10.03 | author_reported_fix | [G2](https://github.com/deepseek-ai/deepseek-harness/blob/86a402200d95fecef4529d969836f1fe13c6cb0d/.agents/notes/archived/bug-fix/2026-09-01-host-goal-pause-aborts-turn.md) |
| T10.04 | author_reported_remaining_issue | [G3](https://github.com/deepseek-ai/deepseek-harness/blob/86a402200d95fecef4529d969836f1fe13c6cb0d/.agents/notes/archived/bug-fix/2026-09-03-user-owned-goal-pause-activation.md) |
| T10.05 | documented_result | [G3](https://github.com/deepseek-ai/deepseek-harness/blob/86a402200d95fecef4529d969836f1fe13c6cb0d/.agents/notes/archived/bug-fix/2026-09-03-user-owned-goal-pause-activation.md) |

<details><summary>固定来源、版本和本地校验依据</summary>

- **G1**：Agent Note: Goal-owned durable events；dsh-v0.0.1-rc.1；提交 `b64c3ac1ba37a8afe20de534ab666e85ae69377b`；内容 `ac0358469958319f7629adb5e96845b7e0013297`。提交时间 `2026-08-11T03:20:36+08:00`（快照时间）。
- **G4**：Agent Note: Persisted same-session goal domain；dsh-v0.2.1-alpha.4；提交 `86a402200d95fecef4529d969836f1fe13c6cb0d`；内容 `5304af8375b5367c3d75e4ba4a7c5ac0034d696d`。提交时间 `2026-10-15T20:22:44+08:00`（快照时间）。
- **G2**：Agent Note: Host-initiated goal pause aborts the live turn；dsh-v0.2.1-alpha.4；提交 `86a402200d95fecef4529d969836f1fe13c6cb0d`；内容 `3a0246f4cc119097498d840682b29c1c5eb3bb56`。提交时间 `2026-10-15T20:22:44+08:00`（快照时间）。
- **G3**：Agent Note: User-owned goal pause exposes live activation；dsh-v0.2.1-alpha.4；提交 `86a402200d95fecef4529d969836f1fe13c6cb0d`；内容 `a38011025b0c18a55e5ca2358c409331eb892136`。提交时间 `2026-10-15T20:22:44+08:00`（快照时间）。

</details>

## 本地原始材料及本轮核验

所有路径从主仓库根目录起算：

- 原始Git历史：`artifacts/agent-task-state/third-party/dsh-history-2026-10-16/`。
- 40版目录和正文：`artifacts/agent-task-state/repository-snapshots/dsh-full-history-2026-10-16/all-version-note-catalog.json`及`historical-note-objects/`。
- 本轮固定源索引、事实清单、全部所选主题版本映射与核验：`artifacts/agent-task-state/repository-snapshots/dsh-truth-2026-10-19/`。其中`truth-facts.json`保存修订前的事实清单；当前派生清单位置见文末。
- 本轮自有提取辅助脚本和运行记录：`artifacts/agent-task-state/maintenance/dsh-truth-2026-10-19/`。第三方正文不复制进项目文档或提交。

所选主题保留40版目录中的每个路径与内容哈希映射。内容版本按哈希区分，工程事件按逐事实证据登记。

## 资料覆盖与后续执行

本页固定十条过程，覆盖所选主题的54条事实。所选主题在40版目录中共有447个文件路径映射、91份不同正文，正文仍保存在原始采集批次。完整PR讨论、并发分支的决定顺序和私下反馈继续列为待补资料。

原始事实版保存在Git提交`7fbdda6`，本次阅读修订保留全部54个事实编号及36个直接来源。新清单位于主工作区`artifacts/agent-task-state/maintenance/dsh-truth-readable-2026-10-19/truth-facts-readable.json`，旧批次保留为修订前证据。本页完整事实为当前对照依据，阅读版负责连续叙述。

后续比较先固定本页及来源哈希，再让各套编码使用同一输入。编码侧与评估侧持有原始事实；重建侧只接收待检验的编码结果。重建结果逐项核对事件、状态、保留范围和待查项。本轮进度为事实整理与阅读修订。
