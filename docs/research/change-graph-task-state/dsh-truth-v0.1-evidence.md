---
title: DSH truth v0.1 证据与边界
status: active
created: 2026-10-19
updated: 2026-10-19
tags: [research, dsh, evidence, truth]
---

# DSH truth v0.1 证据与边界

[真实过程正文](dsh-truth-v0.1.md)是事实对照入口。本文供查证和执行，登记各条来源的固定版本，不提出记录机制。版本目录来自此前已校验的全量采集批次，本轮再次校验选定文件的Git对象哈希与提交元数据。没有重新获取完整PR审阅或运行upstream。

## 证据如何理解

- `commit_record`仅证明Git提交元数据和主线事件；提交标题本身不证明全部预期行为运行正确。
- `documented_state/result/limit/status/transition`表示固定版本记录中的状态、结果、限制或变化；不是独立运行验收。
- `recorded_decision/rationale/transition`保存作者记录的决定和理由，不替其证明理由客观成立。
- `author_reported_*`和`retrospective_report`保留作者归属及回顾性质，不能据此捏造现场时间。
- 编号顺序仅在证据明确叙述前后变化时表达先后；同版本并存不证明两项工作严格串行。Git author/committer只证明记录中的署名，不等于决策发出者、需求提出者或唯一实施者。

<a id="t01"></a>

## T01 · 插件加载：加入事务重载，后来选择性撤回

范围：事务式插件重载及撤回后的消费者调整，不覆盖所有插件管理功能。

| 事实编号 | 证据归属 | 来源 |
|---|---|---|
| T01.01 | commit_record | [L1](https://github.com/deepseek-ai/deepseek-harness/commit/195f7fa9af0ff33e75f44e767a23b8e1e8aaa200) |
| T01.02 | recorded_decision | [L2](https://github.com/deepseek-ai/deepseek-harness/blob/86a402200d95fecef4529d969836f1fe13c6cb0d/.agents/notes/implemented/simplification/2026-09-09-nontransactional-loader.md) |
| T01.03 | recorded_decision | [L2](https://github.com/deepseek-ai/deepseek-harness/blob/86a402200d95fecef4529d969836f1fe13c6cb0d/.agents/notes/implemented/simplification/2026-09-09-nontransactional-loader.md) |
| T01.04 | commit_record | [L3](https://github.com/deepseek-ai/deepseek-harness/commit/e07f41d5fd8ca172287fda0f923b4d1f69c592f3)、[L4](https://github.com/deepseek-ai/deepseek-harness/commit/2abb542a222032b1ad3c5abd7bb65ffffe15b8de)、[L5](https://github.com/deepseek-ai/deepseek-harness/commit/f4a7dd607709025bc3ad19dab8ffbb038cd13962) |
| T01.05 | documented_result | [L2](https://github.com/deepseek-ai/deepseek-harness/blob/86a402200d95fecef4529d969836f1fe13c6cb0d/.agents/notes/implemented/simplification/2026-09-09-nontransactional-loader.md) |

<details><summary>固定来源、版本和本地校验依据</summary>

- **L1**：fix(cordis): make config reload transactional；提交 `195f7fa9af0ff33e75f44e767a23b8e1e8aaa200`；committer时间 `2026-08-02T01:25:01+08:00`；记录署名 author=Tianyi Cui，committer=Tianyi Cui。不是决策主体证明。
- **L2**：Agent Note: Keep Loader mutations non-transactional；dsh-v0.2.1-alpha.4；提交 `86a402200d95fecef4529d969836f1fe13c6cb0d`；内容 `d37539cb3e34c32cd026f330ce92a48baf4bcd0c`。提交时间 `2026-10-15T20:22:44+08:00` 只是该快照的时间，不是主题发生时间。
- **L3**：Revert #932 transactional Cordis reload changes；提交 `e07f41d5fd8ca172287fda0f923b4d1f69c592f3`；committer时间 `2026-09-09T17:32:09+08:00`；记录署名 author=turtle1999，committer=turtle1999。不是决策主体证明。
- **L4**：Adapt current consumers to nontransactional Cordis Loader；提交 `2abb542a222032b1ad3c5abd7bb65ffffe15b8de`；committer时间 `2026-09-09T17:33:32+08:00`；记录署名 author=turtle1999，committer=turtle1999。不是决策主体证明。
- **L5**：fix(boot): preserve failure policy on nontransactional Loader；提交 `f4a7dd607709025bc3ad19dab8ffbb038cd13962`；committer时间 `2026-09-11T12:47:46+08:00`；记录署名 author=turtle1999，committer=turtle1999。不是决策主体证明。

</details>

<a id="t02"></a>

## T02 · Agent 预设：按会话装载，改为声明式配置并保留旧修订

范围：预设配置、运行修订和重启恢复的边界。

| 事实编号 | 证据归属 | 来源 |
|---|---|---|
| T02.01 | documented_state | [P1](https://github.com/deepseek-ai/deepseek-harness/blob/99f6f02fecdb7dff40c3fbc9470f5907c29f74ca/.agents/notes/implemented/architecture/2026-08-03-per-session-agent-presets.md) |
| T02.02 | author_reported_findings | [P1](https://github.com/deepseek-ai/deepseek-harness/blob/99f6f02fecdb7dff40c3fbc9470f5907c29f74ca/.agents/notes/implemented/architecture/2026-08-03-per-session-agent-presets.md) |
| T02.03 | documented_transition | [P4](https://github.com/deepseek-ai/deepseek-harness/commit/d1e22a7e247060496e1acdba9ef3be1700e23ec7)、[P2](https://github.com/deepseek-ai/deepseek-harness/blob/477b4f420553e8a52c2fbccc464d7561b239c443/.agents/notes/implemented/architecture/2026-09-18-declarative-agent-presets.md) |
| T02.04 | documented_result | [P2](https://github.com/deepseek-ai/deepseek-harness/blob/477b4f420553e8a52c2fbccc464d7561b239c443/.agents/notes/implemented/architecture/2026-09-18-declarative-agent-presets.md) |
| T02.05 | documented_limit | [P2](https://github.com/deepseek-ai/deepseek-harness/blob/477b4f420553e8a52c2fbccc464d7561b239c443/.agents/notes/implemented/architecture/2026-09-18-declarative-agent-presets.md)、[P3](https://github.com/deepseek-ai/deepseek-harness/blob/86a402200d95fecef4529d969836f1fe13c6cb0d/.agents/notes/implemented/architecture/2026-09-18-declarative-agent-presets.md) |

<details><summary>固定来源、版本和本地校验依据</summary>

- **P1**：Agent Note: A session's agent is composed from a preset cordis.yml；dsh-v0.1.0-rc.7；提交 `99f6f02fecdb7dff40c3fbc9470f5907c29f74ca`；内容 `5a82f0220058c10892b819a83499c817aa9be6ad`。提交时间 `2026-08-17T19:03:17+08:00` 只是该快照的时间，不是主题发生时间。
- **P4**：feat(preset): declare Agent compositions in profile YAML (#4569)；提交 `d1e22a7e247060496e1acdba9ef3be1700e23ec7`；committer时间 `2026-09-21T08:24:18Z`；记录署名 author=Turtle，committer=GitHub。不是决策主体证明。
- **P2**：Agent Note: Declarative Agent presets and retained revisions；dsh-v0.1.7-rc.2；提交 `477b4f420553e8a52c2fbccc464d7561b239c443`；内容 `bf900bc4dc99f12af4624d14a6ec5497adaa1993`。提交时间 `2026-09-24T21:39:59+08:00` 只是该快照的时间，不是主题发生时间。
- **P3**：Agent Note: Declarative Agent presets and retained revisions；dsh-v0.2.1-alpha.4；提交 `86a402200d95fecef4529d969836f1fe13c6cb0d`；内容 `38fa045ef149ab9fb607641d4a37465847ae77b0`。提交时间 `2026-10-15T20:22:44+08:00` 只是该快照的时间，不是主题发生时间。

</details>

<a id="t03"></a>

## T03 · 会话迁移：一次合入与撤回，之后再引入流式实现

范围：迁移实现的反复、当前迁移协议和未完成提案；不声称恢复所有格式改动。

| 事实编号 | 证据归属 | 来源 |
|---|---|---|
| T03.01 | commit_record | [M1](https://github.com/deepseek-ai/deepseek-harness/commit/3fefcdbe3f83a309f05075b9e9f05450509318ed) |
| T03.02 | commit_record | [M2](https://github.com/deepseek-ai/deepseek-harness/commit/a1781cc4a81bf14551ed0d6e0ee618d14fd9b823) |
| T03.03 | commit_record | [M3](https://github.com/deepseek-ai/deepseek-harness/commit/80306f51a6f36e26c71bcf0be5621af6b8ad8e65) |
| T03.04 | author_reported_failure | [M4](https://github.com/deepseek-ai/deepseek-harness/blob/86a402200d95fecef4529d969836f1fe13c6cb0d/.agents/notes/implemented/architecture/2026-08-31-released-session-format-migrations.md) |
| T03.05 | documented_result | [M4](https://github.com/deepseek-ai/deepseek-harness/blob/86a402200d95fecef4529d969836f1fe13c6cb0d/.agents/notes/implemented/architecture/2026-08-31-released-session-format-migrations.md) |
| T03.06 | documented_status | [M5](https://github.com/deepseek-ai/deepseek-harness/blob/86a402200d95fecef4529d969836f1fe13c6cb0d/.agents/notes/proposed/architecture/2026-09-06-logical-session-storage-rebuild.md) |

<details><summary>固定来源、版本和本地校验依据</summary>

- **M1**：Merge pull request #2698 from deepseek-harness/xtr/session-format-migration；提交 `3fefcdbe3f83a309f05075b9e9f05450509318ed`；committer时间 `2026-08-25T13:47:43+08:00`；记录署名 author=_Kerman，committer=GitHub。不是决策主体证明。
- **M2**：Merge pull request #3054 from deepseek-harness/worktree-revert2698；提交 `a1781cc4a81bf14551ed0d6e0ee618d14fd9b823`；committer时间 `2026-08-25T15:47:19+08:00`；记录署名 author=imccyu，committer=GitHub。不是决策主体证明。
- **M3**：Merge pull request #3585 from deepseek-harness/session-migration-streaming；提交 `80306f51a6f36e26c71bcf0be5621af6b8ad8e65`；committer时间 `2026-09-06T02:34:12+08:00`；记录署名 author=imccyu，committer=GitHub。不是决策主体证明。
- **M4**：Agent Note: Released Session formats migrate through stateful streaming stages；dsh-v0.2.1-alpha.4；提交 `86a402200d95fecef4529d969836f1fe13c6cb0d`；内容 `007620d641c65955409bebb98c4cbd5c5e449a18`。提交时间 `2026-10-15T20:22:44+08:00` 只是该快照的时间，不是主题发生时间。
- **M5**：Agent Note: Logical session and storage rebuild；dsh-v0.2.1-alpha.4；提交 `86a402200d95fecef4529d969836f1fe13c6cb0d`；内容 `cb639c0052417eb5a621925bc02dccae7f8f1c6c`。提交时间 `2026-10-15T20:22:44+08:00` 只是该快照的时间，不是主题发生时间。

</details>

<a id="t04"></a>

## T04 · Team 消息：从独立 outbox 改为目标 inbox，保留名单与任务

范围：消息交付承诺的部分替代及历史记录处理。

| 事实编号 | 证据归属 | 来源 |
|---|---|---|
| T04.01 | documented_state | [T1](https://github.com/deepseek-ai/deepseek-harness/blob/477b4f420553e8a52c2fbccc464d7561b239c443/.agents/notes/implemented/feature/2026-08-05-agent-teams.md) |
| T04.02 | recorded_decision | [T2](https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/.agents/notes/implemented/simplification/2026-09-26-team-direct-inbox.md) |
| T04.03 | commit_record | [T3](https://github.com/deepseek-ai/deepseek-harness/commit/ea0980dab432263a9d1cd2b8e4998a1d6e6e6ae7)、[T2](https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/.agents/notes/implemented/simplification/2026-09-26-team-direct-inbox.md) |
| T04.04 | documented_result | [T2](https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/.agents/notes/implemented/simplification/2026-09-26-team-direct-inbox.md) |
| T04.05 | documented_result | [T2](https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/.agents/notes/implemented/simplification/2026-09-26-team-direct-inbox.md) |
| T04.06 | recorded_rationale | [T2](https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/.agents/notes/implemented/simplification/2026-09-26-team-direct-inbox.md) |

<details><summary>固定来源、版本和本地校验依据</summary>

- **T1**：Agent Note: Durable Agent Teams over continuable children；dsh-v0.1.7-rc.2；提交 `477b4f420553e8a52c2fbccc464d7561b239c443`；内容 `6333e511ba1e71823cfa55c27ba46b2665d1ef15`。提交时间 `2026-09-24T21:39:59+08:00` 只是该快照的时间，不是主题发生时间。
- **T2**：Agent Note: Team messages use the target inbox；dsh-v0.2.1-alpha.2；提交 `d743267388641bc76f17c45ce8b4c231aed1d32c`；内容 `58d18d0ecfef4d292cfbb8cbf3e4c449b1fa1d6d`。提交时间 `2026-10-09T17:31:32+08:00` 只是该快照的时间，不是主题发生时间。
- **T3**：Merge pull request #5247 from deepseek-harness/refactor/agent-team-direct-steer；提交 `ea0980dab432263a9d1cd2b8e4998a1d6e6e6ae7`；committer时间 `2026-10-08T16:42:56+08:00`；记录署名 author=Dudu-0223，committer=GitHub。不是决策主体证明。

</details>

<a id="t05"></a>

## T05 · Creator：临时修改运行时，转为安装持久插件

范围：模型修改能力的工作流替换，不把所有运行时写API一并删除。

| 事实编号 | 证据归属 | 来源 |
|---|---|---|
| T05.01 | documented_state | [C1](https://github.com/deepseek-ai/deepseek-harness/blob/141eb6fef83422698aef7a981029e843e8161534/.agents/notes/implemented/feature/2026-07-08-self-referential-cordis-toolset.md) |
| T05.02 | documented_limit | [C1](https://github.com/deepseek-ai/deepseek-harness/blob/141eb6fef83422698aef7a981029e843e8161534/.agents/notes/implemented/feature/2026-07-08-self-referential-cordis-toolset.md) |
| T05.03 | documented_transition | [C3](https://github.com/deepseek-ai/deepseek-harness/commit/f756097108d1fc69f71bae1ee3c6114e5ae40b12)、[C2](https://github.com/deepseek-ai/deepseek-harness/blob/ddefc45fbc7f8e46dd73185e68295696d1297887/.agents/notes/implemented/architecture/2026-09-16-creator-persistent-plugin-management.md) |
| T05.04 | documented_result | [C2](https://github.com/deepseek-ai/deepseek-harness/blob/ddefc45fbc7f8e46dd73185e68295696d1297887/.agents/notes/implemented/architecture/2026-09-16-creator-persistent-plugin-management.md) |
| T05.05 | documented_result | [C2](https://github.com/deepseek-ai/deepseek-harness/blob/ddefc45fbc7f8e46dd73185e68295696d1297887/.agents/notes/implemented/architecture/2026-09-16-creator-persistent-plugin-management.md) |

<details><summary>固定来源、版本和本地校验依据</summary>

- **C1**：Agent Note: The self-referential cordis toolset；dsh-v0.1.0-rc.8；提交 `141eb6fef83422698aef7a981029e843e8161534`；内容 `d408bb774fa62dd6ff0deef7003f5b0851b80e82`。提交时间 `2026-08-19T23:11:50+08:00` 只是该快照的时间，不是主题发生时间。
- **C3**：Merge pull request #4324 from deepseek-harness/turtle/creator-plugin-manager；提交 `f756097108d1fc69f71bae1ee3c6114e5ae40b12`；committer时间 `2026-09-16T17:58:53+08:00`；记录署名 author=Turtle，committer=GitHub。不是决策主体证明。
- **C2**：Agent Note: Creator mode installs persistent plugin bundles；dsh-v0.1.6-alpha.2；提交 `ddefc45fbc7f8e46dd73185e68295696d1297887`；内容 `04ccbb83fe6d2f5c460f53100a9087cce119ea4d`。提交时间 `2026-09-17T21:19:19+08:00` 只是该快照的时间，不是主题发生时间。

</details>

<a id="t06"></a>

## T06 · 定时任务：从会话日志转为Host存储，再限制历史保留

范围：权威存储、冷会话投递、删除和回执保留；不覆盖后续所有入口默认值变化。

| 事实编号 | 证据归属 | 来源 |
|---|---|---|
| T06.01 | documented_state | [S1](https://github.com/deepseek-ai/deepseek-harness/blob/46a7f68b0922371ce7144b668b90e377d8e799f4/.agents/notes/implemented/feature/2026-08-05-durable-web-schedule.md) |
| T06.02 | documented_transition | [S2](https://github.com/deepseek-ai/deepseek-harness/blob/477b4f420553e8a52c2fbccc464d7561b239c443/.agents/notes/implemented/architecture/2026-09-16-host-schedule-storage.md) |
| T06.03 | documented_result | [S2](https://github.com/deepseek-ai/deepseek-harness/blob/477b4f420553e8a52c2fbccc464d7561b239c443/.agents/notes/implemented/architecture/2026-09-16-host-schedule-storage.md) |
| T06.04 | recorded_transition | [S2](https://github.com/deepseek-ai/deepseek-harness/blob/477b4f420553e8a52c2fbccc464d7561b239c443/.agents/notes/implemented/architecture/2026-09-16-host-schedule-storage.md)、[S3](https://github.com/deepseek-ai/deepseek-harness/blob/86a402200d95fecef4529d969836f1fe13c6cb0d/.agents/notes/implemented/architecture/2026-09-22-schedule-hard-delete-and-bounded-history.md) |
| T06.05 | documented_result | [S3](https://github.com/deepseek-ai/deepseek-harness/blob/86a402200d95fecef4529d969836f1fe13c6cb0d/.agents/notes/implemented/architecture/2026-09-22-schedule-hard-delete-and-bounded-history.md)、[S2](https://github.com/deepseek-ai/deepseek-harness/blob/477b4f420553e8a52c2fbccc464d7561b239c443/.agents/notes/implemented/architecture/2026-09-16-host-schedule-storage.md) |
| T06.06 | documented_limit | [S2](https://github.com/deepseek-ai/deepseek-harness/blob/477b4f420553e8a52c2fbccc464d7561b239c443/.agents/notes/implemented/architecture/2026-09-16-host-schedule-storage.md) |

<details><summary>固定来源、版本和本地校验依据</summary>

- **S1**：Agent Note: Durable Session-local reminders；dsh-v0.1.7-rc.1；提交 `46a7f68b0922371ce7144b668b90e377d8e799f4`；内容 `b09ab752c9db0587b49dbe50a152144b9ff19515`。提交时间 `2026-09-23T21:03:33+08:00` 只是该快照的时间，不是主题发生时间。
- **S2**：Agent Note: Host-owned scheduled messages；dsh-v0.1.7-rc.2；提交 `477b4f420553e8a52c2fbccc464d7561b239c443`；内容 `79a4f7207184e592f00a4d9946c2ca2e9345032d`。提交时间 `2026-09-24T21:39:59+08:00` 只是该快照的时间，不是主题发生时间。
- **S3**：Agent Note: Schedule deletes task rows and bounds delivery history；dsh-v0.2.1-alpha.4；提交 `86a402200d95fecef4529d969836f1fe13c6cb0d`；内容 `90127d688777a7c0c63d6d817e6df35a9f5b77b5`。提交时间 `2026-10-15T20:22:44+08:00` 只是该快照的时间，不是主题发生时间。

</details>

<a id="t07"></a>

## T07 · 远程执行：移除E2B实现，保留接口并继续SSH路线

范围：一个供应实现的引入、退出、保留成果和另一供应实现。

| 事实编号 | 证据归属 | 来源 |
|---|---|---|
| T07.01 | documented_transition | [R3](https://github.com/deepseek-ai/deepseek-harness/commit/33312c6a89e2c4c7efd7b067d88506df2a9d982f)、[R1](https://github.com/deepseek-ai/deepseek-harness/blob/86a402200d95fecef4529d969836f1fe13c6cb0d/.agents/notes/implemented/simplification/2026-09-11-remove-e2b-providers.md) |
| T07.02 | recorded_rationale | [R1](https://github.com/deepseek-ai/deepseek-harness/blob/86a402200d95fecef4529d969836f1fe13c6cb0d/.agents/notes/implemented/simplification/2026-09-11-remove-e2b-providers.md) |
| T07.03 | documented_transition | [R4](https://github.com/deepseek-ai/deepseek-harness/commit/09a6fbc388bc6de135dea7d86b85f6e96b3bf32a)、[R1](https://github.com/deepseek-ai/deepseek-harness/blob/86a402200d95fecef4529d969836f1fe13c6cb0d/.agents/notes/implemented/simplification/2026-09-11-remove-e2b-providers.md) |
| T07.04 | documented_result | [R1](https://github.com/deepseek-ai/deepseek-harness/blob/86a402200d95fecef4529d969836f1fe13c6cb0d/.agents/notes/implemented/simplification/2026-09-11-remove-e2b-providers.md) |
| T07.05 | documented_state | [R2](https://github.com/deepseek-ai/deepseek-harness/blob/86a402200d95fecef4529d969836f1fe13c6cb0d/.agents/notes/implemented/architecture/2026-09-11-posix-ssh-runtime.md) |

<details><summary>固定来源、版本和本地校验依据</summary>

- **R3**：Merge pull request #796 from deepseek-harness/worktree/e2b-poc-20260727；提交 `33312c6a89e2c4c7efd7b067d88506df2a9d982f`；committer时间 `2026-08-08T23:15:49+08:00`；记录署名 author=Tianyi Cui，committer=GitHub。不是决策主体证明。
- **R1**：Agent Note: Remove the E2B execution providers；dsh-v0.2.1-alpha.4；提交 `86a402200d95fecef4529d969836f1fe13c6cb0d`；内容 `a73c5849ff98751b76903b1ef0c284112efba073`。提交时间 `2026-10-15T20:22:44+08:00` 只是该快照的时间，不是主题发生时间。
- **R4**：Merge pull request #4036 from deepseek-harness/worktree/ptc-sandbox/remove-e2b；提交 `09a6fbc388bc6de135dea7d86b85f6e96b3bf32a`；committer时间 `2026-09-11T23:30:29+08:00`；记录署名 author=Tianyi Cui，committer=GitHub。不是决策主体证明。
- **R2**：Agent Note: POSIX SSH execution providers；dsh-v0.2.1-alpha.4；提交 `86a402200d95fecef4529d969836f1fe13c6cb0d`；内容 `3bd1c340d158709826ab7cbd5d724cb151a23ec1`。提交时间 `2026-10-15T20:22:44+08:00` 只是该快照的时间，不是主题发生时间。

</details>

<a id="t08"></a>

## T08 · 子代理：先分开持续会话与一次执行，再统一activation入口

范围：持续会话与一次执行的管理路径变化及仍保留的后端差异。

| 事实编号 | 证据归属 | 来源 |
|---|---|---|
| T08.01 | retrospective_report | [A1](https://github.com/deepseek-ai/deepseek-harness/blob/5badb15009ae1756c3afe0ae0cef1faafc290ccc/.agents/notes/implemented/feature/2026-07-28-continuable-subagent-conversations.md) |
| T08.02 | documented_state | [A1](https://github.com/deepseek-ai/deepseek-harness/blob/5badb15009ae1756c3afe0ae0cef1faafc290ccc/.agents/notes/implemented/feature/2026-07-28-continuable-subagent-conversations.md) |
| T08.03 | documented_transition | [A3](https://github.com/deepseek-ai/deepseek-harness/commit/bf1c4e01ba7088b3cb0aeb36caa702965eb5f6ec)、[A2](https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/.agents/notes/implemented/simplification/2026-09-17-unified-subagent-activations.md) |
| T08.04 | documented_result | [A2](https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/.agents/notes/implemented/simplification/2026-09-17-unified-subagent-activations.md) |
| T08.05 | documented_result | [A2](https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/.agents/notes/implemented/simplification/2026-09-17-unified-subagent-activations.md) |
| T08.06 | documented_limit | [A2](https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/.agents/notes/implemented/simplification/2026-09-17-unified-subagent-activations.md) |

<details><summary>固定来源、版本和本地校验依据</summary>

- **A1**：Agent Note: Continuable subagents；dsh-v0.2.1-alpha.1；提交 `5badb15009ae1756c3afe0ae0cef1faafc290ccc`；内容 `142119cd0ade998332fadf73b6b41441d2ab59a2`。提交时间 `2026-10-03T11:48:13+08:00` 只是该快照的时间，不是主题发生时间。
- **A3**：Merge pull request #4394 from deepseek-harness/refactor/subagent；提交 `bf1c4e01ba7088b3cb0aeb36caa702965eb5f6ec`；committer时间 `2026-10-06T15:08:30+08:00`；记录署名 author=Dudu-0223，committer=GitHub。不是决策主体证明。
- **A2**：Agent Note: Unified subagent activations；dsh-v0.2.1-alpha.2；提交 `d743267388641bc76f17c45ce8b4c231aed1d32c`；内容 `07268e40160f7a8a84f564c95440849b8c28c7a8`。提交时间 `2026-10-09T17:31:32+08:00` 只是该快照的时间，不是主题发生时间。

</details>

<a id="t09"></a>

## T09 · 侧栏：从工具详情到通用工作区，调整布局和内容的寿命

范围：侧栏基础设施与内容树保留，不覆盖所有后续文档插件。

| 事实编号 | 证据归属 | 来源 |
|---|---|---|
| T09.01 | retrospective_report | [U1](https://github.com/deepseek-ai/deepseek-harness/blob/5dda764ed3aa172535a7967b06ff95d9cbfe536a/.agents/notes/implemented/feature/2026-09-04-right-sidebar-docking-infrastructure.md) |
| T09.02 | author_reported_trial | [U1](https://github.com/deepseek-ai/deepseek-harness/blob/5dda764ed3aa172535a7967b06ff95d9cbfe536a/.agents/notes/implemented/feature/2026-09-04-right-sidebar-docking-infrastructure.md) |
| T09.03 | recorded_transition | [U1](https://github.com/deepseek-ai/deepseek-harness/blob/5dda764ed3aa172535a7967b06ff95d9cbfe536a/.agents/notes/implemented/feature/2026-09-04-right-sidebar-docking-infrastructure.md) |
| T09.04 | recorded_transition | [U2](https://github.com/deepseek-ai/deepseek-harness/blob/86a402200d95fecef4529d969836f1fe13c6cb0d/.agents/notes/implemented/architecture/2026-09-20-sidebar-retained-tab-layout.md) |
| T09.05 | documented_result | [U1](https://github.com/deepseek-ai/deepseek-harness/blob/5dda764ed3aa172535a7967b06ff95d9cbfe536a/.agents/notes/implemented/feature/2026-09-04-right-sidebar-docking-infrastructure.md)、[U2](https://github.com/deepseek-ai/deepseek-harness/blob/86a402200d95fecef4529d969836f1fe13c6cb0d/.agents/notes/implemented/architecture/2026-09-20-sidebar-retained-tab-layout.md) |

<details><summary>固定来源、版本和本地校验依据</summary>

- **U1**：Agent Note: Right Sidebar docking infrastructure；dsh-v0.1.5-alpha.1；提交 `5dda764ed3aa172535a7967b06ff95d9cbfe536a`；内容 `8e1d1b5518c3b80a05be877ee9796883b6eb9a60`。提交时间 `2026-09-08T23:25:45+08:00` 只是该快照的时间，不是主题发生时间。
- **U2**：Agent Note: Stable Sidebar tab mounting and Session retention；dsh-v0.2.1-alpha.4；提交 `86a402200d95fecef4529d969836f1fe13c6cb0d`；内容 `574667c79f15643f0b2f58b2e8c54d793a7df869`。提交时间 `2026-10-15T20:22:44+08:00` 只是该快照的时间，不是主题发生时间。

</details>

<a id="t10"></a>

## T10 · 目标控制：保存目标，再修复人工暂停被执行绕过的问题

范围：目标持久状态、运行授权及两轮暂停修正。

| 事实编号 | 证据归属 | 来源 |
|---|---|---|
| T10.01 | documented_state | [G1](https://github.com/deepseek-ai/deepseek-harness/blob/b64c3ac1ba37a8afe20de534ab666e85ae69377b/.agents/notes/implemented/architecture/2026-07-31-goal-owned-durable-events.md) |
| T10.02 | documented_state | [G4](https://github.com/deepseek-ai/deepseek-harness/blob/86a402200d95fecef4529d969836f1fe13c6cb0d/.agents/notes/archived/feature/2026-07-19-persisted-same-session-goal-domain.md) |
| T10.03 | author_reported_fix | [G2](https://github.com/deepseek-ai/deepseek-harness/blob/86a402200d95fecef4529d969836f1fe13c6cb0d/.agents/notes/archived/bug-fix/2026-09-01-host-goal-pause-aborts-turn.md) |
| T10.04 | author_reported_remaining_issue | [G3](https://github.com/deepseek-ai/deepseek-harness/blob/86a402200d95fecef4529d969836f1fe13c6cb0d/.agents/notes/archived/bug-fix/2026-09-03-user-owned-goal-pause-activation.md) |
| T10.05 | documented_result | [G3](https://github.com/deepseek-ai/deepseek-harness/blob/86a402200d95fecef4529d969836f1fe13c6cb0d/.agents/notes/archived/bug-fix/2026-09-03-user-owned-goal-pause-activation.md) |

<details><summary>固定来源、版本和本地校验依据</summary>

- **G1**：Agent Note: Goal-owned durable events；dsh-v0.0.1-rc.1；提交 `b64c3ac1ba37a8afe20de534ab666e85ae69377b`；内容 `ac0358469958319f7629adb5e96845b7e0013297`。提交时间 `2026-08-11T03:20:36+08:00` 只是该快照的时间，不是主题发生时间。
- **G4**：Agent Note: Persisted same-session goal domain；dsh-v0.2.1-alpha.4；提交 `86a402200d95fecef4529d969836f1fe13c6cb0d`；内容 `5304af8375b5367c3d75e4ba4a7c5ac0034d696d`。提交时间 `2026-10-15T20:22:44+08:00` 只是该快照的时间，不是主题发生时间。
- **G2**：Agent Note: Host-initiated goal pause aborts the live turn；dsh-v0.2.1-alpha.4；提交 `86a402200d95fecef4529d969836f1fe13c6cb0d`；内容 `3a0246f4cc119097498d840682b29c1c5eb3bb56`。提交时间 `2026-10-15T20:22:44+08:00` 只是该快照的时间，不是主题发生时间。
- **G3**：Agent Note: User-owned goal pause exposes live activation；dsh-v0.2.1-alpha.4；提交 `86a402200d95fecef4529d969836f1fe13c6cb0d`；内容 `a38011025b0c18a55e5ca2358c409331eb892136`。提交时间 `2026-10-15T20:22:44+08:00` 只是该快照的时间，不是主题发生时间。

</details>

## 本地原始材料及本轮核验

所有路径从主仓库根目录起算：

- 原始Git历史：`artifacts/agent-task-state/third-party/dsh-history-2026-10-16/`。
- 40版目录和正文：`artifacts/agent-task-state/repository-snapshots/dsh-full-history-2026-10-16/all-version-note-catalog.json`及`historical-note-objects/`。
- 本轮固定源索引、事实清单、全部所选主题版本映射与核验：`artifacts/agent-task-state/repository-snapshots/dsh-truth-2026-10-19/`。其中`truth-facts.json`为本页事实编号的派生执行清单，正文修订后须同步，不作为绕过正文的第二套权威。
- 本轮自有提取辅助脚本和运行记录：`artifacts/agent-task-state/maintenance/dsh-truth-2026-10-19/`。第三方正文不复制进项目文档或提交。

对所有所选主题保留40版目录中出现的每个映射，不通过文件名或时间替它们推导语义关系。哈希不同只证明字节变化，不能直接统计成一次工程决定。相同正文可在多个版本中存在；它们不应重复算成发生多次。

## 未覆盖和防止错误还原

并发分支间精确决策顺序、完整PR讨论、私下决定、运行中的用户反馈均未完整恢复。十条过程是有证据边界的首批底稿，不是随机样本，不证明开发活动分布或机制优越性。不能据此编造“领导要求切换”等不存在的主体动作。

后续重建时，未知项应继续未知；提案不能变成实现，作者测量不能变成独立验证，部分替代不能变成全盘推翻，读取旧历史不能变成承诺继续旧执行。冻结输入时同时固定本文、过程正文和来源哈希，编码方案不得反向更改truth。原始材料和本地事实清单只能由编码/评估侧查证，不能与编码结果一并提供给盲重建者。
