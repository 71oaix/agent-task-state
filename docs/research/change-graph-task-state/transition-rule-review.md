---
title: 工作转换检验：对象、效果与拒绝条件
status: active
created: 2026-10-25
updated: 2026-10-25
tags: [research, transitions, work-operations]
---

# 工作转换检验：对象、效果与拒绝条件

本页保存[工程全景](dsh-work-history.md)中工作操作研究的本轮明细：固定来源、具体转换、两种表示、探针与取舍。当前为主 Agent 离线走查；Qoder 配置已过期，独立构造与读回包已准备，尚未派发。

## 怎么解释这里的版本与顺序

`U14@1 → U14@2` 表示本研究中的成果**描述记录**从未知/先前内容更新为来源报告的内容。源码版本只读独立 `code_revision` 字段，未知继续为 `null`。PR 名称、来源提交、研究工作身份和记录版本分别保存。

每份来源快照形成一个可见块；块内按“登记对象、保存依据、表达变化、记录结果”分解，序号用于检查，并不证明历史按这些 API 或时间顺序执行。T14 的主要信息来自同一份回顾笔记；T12 的分工、基础实现和草稿保留来源局部顺序。T02 按 S030、S005、S020 的可见版本区分。

初始对象也是成本：先把已有目标、契约和成果的已知描述登记为初版，并保留未知。七接口方案若只允许 open 新建工作，就仍需要这条一般对象初始登记规则；统一登记方案同样要定义类型和引用约束。原型规格把这条规则放进统一写入底座，避免隐藏初始化步骤。

## 共用规则

| 编号 | 要保住的含义 | 如何检查 |
|---|---|---|
| R01 身份和类型 | 引用已登记的对象/记录版本；类型与操作适用对象相符。已知 PR/issue 名称登记为来源标识，研究工作 ID 另分配。 | 结构检查 |
| R02 准确前态 | 更新写明 expected 记录版本及修改字段；前态不匹配拒绝。来源报告缺少源码基线时只登记报告。 | 结构检查 |
| R03 显式写集 | 只改变列明字段；未列字段逐项保留。修订不隐含关闭、采用或完成父目标。 | 结构检查 |
| R04 归属与时间 | 每步有 source/fact、报告者、记录性质；来源可见块与历史先后分别记录。 | 结构检查+来源核对 |
| R05 报告与已确认状态 | 报告、判断、实施、检查、验收采用独立字段；提升证据等级需要额外依据和主体。 | 结构检查+证据语义判断 |
| R06 有类型的联系 | 关系有 kind、精确端点及作用范围；修改关系建立后继版本，旧版继续可查。 | 结构检查 |
| R07 采用独立 | select 更新指定 scope 的旧采用/新采用；不同 scope 不互相覆盖，同一 expected 下冲突不静默合并。 | 结构检查 |
| R08 责任守恒 | 拆分保留父原责任及验收；列出子项分配、残余、重叠和未决。每个已知责任项有去向；内容分类由调用者核对。 | 结构检查+范围判断 |
| R09 设计与实例 | 产品运行规则保存为设计内容；实例事件必须有实例身份与事件依据。研究者合成的实例仅用于探针。 | 结构检查+来源核对 |
| R10 可见顺序 | 补录较早事件只增加历史报告；当前投影由明确采用及效力依据决定，不能按入库先后自动覆盖。 | 结构检查+效力判断 |
| R11 相关更新成组 | 责任拆分等共同变化有 group 和读写集；组内全部满足才能作为一致快照使用。保存未完成提案可另记 proposal。 | 结构检查 |
| R12 缺失的保留 | 不知道源码复用、历史创建/关闭时间或最终验收，保存 null；结构合法的虚假理由仍需核对来源。 | 来源核对 |

R01—R12 是规则族，不是十二个调用接口。身份判断、责任分类、相容性和证据适用性由调用者提供。程序可以检查声明完整、引用存在和更新一致；内容与来源是否相符仍需核对。

<a id="t14"></a>
## T14：旧尝试收束，沿已有后端重做 UI

这段转换要保住三条连续性：用户要的反馈入口继续存在；旧全栈尝试被关闭；新 UI 接着已落地后端实现。来源还确认用户可见入口后来存在，所以记录应同时保留“后端落地时未完成”和“后来入口已有实现报告”。

| 标识 | 对象及来源身份 | 初始已知范围 |
|---|---|---|
| G14 | 用户目标；issue #1326 | 后端落地时尚无 Web 入口，最终验收未知 |
| B14 | 已落地后端契约；PR #2217 | 逐项 ifVersion；messageFeedback API；准确源码前版未知 |
| W14old / W14new | 旧 #1010 尝试 / 新 UI 尝试 | 两个研究工作 ID；新尝试原始创建事件未知 |
| U14 | 重做 UI 的成果描述 | 初版内容未掌握，后续补入实现报告 |
| A14 | 新 UI 后端契约采用记录 | 只针对新 UI 的契约范围 |

### 初始对象

<details><summary>展开初始描述及未知项</summary>

```json
{
  "G14": {
    "revision": 1,
    "kind": "goal",
    "fields": {
      "label": "Web 逐消息反馈",
      "user_request": "#1326",
      "ui_status": "absent_at_backend_landing",
      "final_acceptance": null
    }
  },
  "B14": {
    "revision": 1,
    "kind": "contract",
    "fields": {
      "source_identity": "#2217",
      "api": [
        "messageFeedback.list",
        "messageFeedback.put",
        "messageFeedback.delete"
      ],
      "version_rule": "per-item ifVersion",
      "state": "backend landed as reported",
      "code_revision": null
    }
  },
  "U14": {
    "revision": 1,
    "kind": "artifact",
    "fields": {
      "label": "重做的 Web UI",
      "implementation": null,
      "verification": null,
      "code_revision": null
    }
  },
  "A14": {
    "revision": 1,
    "kind": "adoption",
    "fields": {
      "scope": "new Web UI backend contract",
      "selected": null,
      "effect": "unknown"
    }
  }
}
```

</details>

### 转换总览

| 步骤 | 操作与对象 | 具体变化 |
|---|---|---|
| T14.01 | `open(W14old)` | 登记旧尝试的已知范围；实际开启时间未知 |
| T14.02 | `observe(O14inspection)` | 保存检查报告及三个不兼容点 |
| T14.03 | `judge(J14route)` | 保存路线取舍及依据 |
| T14.04 | `close(W14old)` | 旧尝试停止；父目标不随之完成 |
| T14.05 | `open(W14new)` | 登记同一用户目标下的新尝试 |
| T14.06 | `bind(L14contract)` | 把新 UI 的契约依赖与旧代码取用分开 |
| T14.07 | `select(A14)` | 记录重做 UI 的实际契约选择范围 |
| T14.08 | `revise(U14)` | 保存新实现的报告内容；源码基线仍未知 |
| T14.09 | `observe(O14e2e)` | 保存作者报告的检查及覆盖范围 |
| T14.10 | `revise(G14)` | 更新用户功能已存在的报告；最终验收保留未知 |

<details><summary>展开逐步调用：前态、效果、保留、来源与拒绝规则</summary>

#### T14.01 · open(W14old)

登记旧尝试的已知范围；实际开启时间未知。

- 前态：该研究对象尚未登记，要求身份不存在；后态：`W14old@1`。
- 新增/改写：`{"code_reuse": null, "contract": "session revision / feedback.upsert", "goal": "G14", "source_identity": "#1010", "status": "historical_attempt"}`。
- 保留：初次登记，无旧字段；其他对象均不改变。
- 引用：`G14@1`；范围：`T14`。
- 调用者判断：把 #1010 作为独立尝试的研究身份；不推导代码血缘。
- 依据：[T14.02](dsh-process-truth-v1.md#t14)；报告归属：来源作者，确切个人未知；历史事件时间未知；可见块：`S031`。
- 检查/拒绝：R01, R02, R03, R04, R05, R12。来源报告投影不声称执行过历史 API。

#### T14.02 · observe(O14inspection)

保存检查报告及三个不兼容点。

- 前态：该研究对象尚未登记，要求身份不存在；后态：`O14inspection@1`。
- 新增/改写：`{"reported_method": "old branch inspection", "result": ["API incompatible with landed backend", "duplicate backend", "directory drift"], "subject": "W14old", "verification_level": "author_report"}`。
- 保留：初次登记，无旧字段；其他对象均不改变。
- 引用：`W14old@1`；`B14@1`；范围：`T14`。
- 调用者判断：核对原文确实给出这些区别。
- 依据：[T14.02](dsh-process-truth-v1.md#t14)；[T14.03](dsh-process-truth-v1.md#t14)；报告归属：来源作者，确切个人未知；历史事件时间未知；可见块：`S031`。
- 检查/拒绝：R01, R02, R03, R04, R05, R12。来源报告投影不声称执行过历史 API。

#### T14.03 · judge(J14route)

保存路线取舍及依据。

- 前态：该研究对象尚未登记，要求身份不存在；后态：`J14route@1`。
- 新增/改写：`{"applicability": "feedback Web surface", "conclusion": "close old attempt as superseded and rewrite UI", "evidence": "O14inspection", "supersedes": null}`。
- 保留：初次登记，无旧字段；其他对象均不改变。
- 引用：`O14inspection@1`；范围：`T14`。
- 调用者判断：来源作者的工程判断；程序只校验引用。
- 依据：[T14.03](dsh-process-truth-v1.md#t14)；报告归属：来源作者，确切个人未知；历史事件时间未知；可见块：`S031`。
- 检查/拒绝：R01, R02, R03, R04, R05, R12。来源报告投影不声称执行过历史 API。

#### T14.04 · close(W14old)

旧尝试停止；父目标不随之完成。

- 前态：`W14old@1`；后态：`W14old@2`。
- 新增/改写：`{"disposition": "historical reference; exact code reuse unknown", "status": "closed_superseded", "successor": "W14new"}`。
- 保留：`code_reuse`、`contract`、`goal`、`source_identity`。
- 引用：`J14route@1`；`G14@1`；范围：`T14`。
- 调用者判断：关闭范围限定为旧尝试。
- 依据：[T14.03](dsh-process-truth-v1.md#t14)；报告归属：来源作者，确切个人未知；历史事件时间未知；可见块：`S031`。
- 检查/拒绝：R01, R02, R03, R04, R05, R12；逻辑组 `T14.route` 整体检查。来源报告投影不声称执行过历史 API。

#### T14.05 · open(W14new)

登记同一用户目标下的新尝试。

- 前态：该研究对象尚未登记，要求身份不存在；后态：`W14new@1`。
- 新增/改写：`{"goal": "G14", "predecessor": "W14old", "responsibility": "UI against landed backend", "source_identity": null, "status": "rewrite_as_reported"}`。
- 保留：初次登记，无旧字段；其他对象均不改变。
- 引用：`G14@1`；`W14old@2`；范围：`T14`。
- 调用者判断：新尝试 ID 为研究分配，原文没有提供其创建事件。
- 依据：[T14.03](dsh-process-truth-v1.md#t14)；报告归属：来源作者，确切个人未知；历史事件时间未知；可见块：`S031`。
- 检查/拒绝：R01, R02, R03, R04, R05, R12；逻辑组 `T14.route` 整体检查。来源报告投影不声称执行过历史 API。

#### T14.06 · bind(L14contract)

把新 UI 的契约依赖与旧代码取用分开。

- 前态：该研究对象尚未登记，要求身份不存在；后态：`L14contract@1`。
- 新增/改写：`{"code_ancestry": null, "from": "W14new", "range": "per-message feedback Web UI", "relation": "uses_contract", "to": "B14"}`。
- 保留：初次登记，无旧字段；其他对象均不改变。
- 引用：`W14new@1`；`B14@1`；范围：`T14`。
- 调用者判断：依赖契约不等于取用旧代码。
- 依据：[T14.02](dsh-process-truth-v1.md#t14)；[T14.04](dsh-process-truth-v1.md#t14)；报告归属：来源作者，确切个人未知；历史事件时间未知；可见块：`S031`。
- 检查/拒绝：R01, R02, R04, R06, R12。来源报告投影不声称执行过历史 API。

#### T14.07 · select(A14)

记录重做 UI 的实际契约选择范围。

- 前态：`A14@1`；后态：`A14@2`。
- 新增/改写：`{"effect": "source reports UI implemented against this contract", "selected": "B14@1"}`。
- 保留：`scope`。
- 引用：`B14@1`；`W14new@1`；范围：`new Web UI backend contract`。
- 调用者判断：这是作者报告的选择；不是本次执行安装。
- 依据：[T14.04](dsh-process-truth-v1.md#t14)；报告归属：来源作者，确切个人未知；历史事件时间未知；可见块：`S031`。
- 检查/拒绝：R01, R02, R03, R04, R07, R12。来源报告投影不声称执行过历史 API。

#### T14.08 · revise(U14)

保存新实现的报告内容；源码基线仍未知。

- 前态：`U14@1`；后态：`U14@2`。
- 新增/改写：`{"implementation": ["finalized assistant MessageId", "per-session serialized per-item mutations", "conflict response reconciliation"], "reported_user_surface": "ratings and notes exist", "source_identity": null}`。
- 保留：`code_revision`、`label`、`verification`。
- 引用：`W14new@1`；`B14@1`；范围：`T14`。
- 调用者判断：从文档提取实现范围，不把本地描述版当作源码版。
- 依据：[T14.04](dsh-process-truth-v1.md#t14)；报告归属：来源作者，确切个人未知；历史事件时间未知；可见块：`S031`。
- 检查/拒绝：R01, R02, R03, R04, R05, R12。来源报告投影不声称执行过历史 API。

#### T14.09 · observe(O14e2e)

保存作者报告的检查及覆盖范围。

- 前态：该研究对象尚未登记，要求身份不存在；后态：`O14e2e@1`。
- 新增/改写：`{"accepting_actor": null, "method": "shipped bundle Web E2E", "result": ["rate", "note", "reload restore", "retract"], "subject": "U14", "verification_level": "author_report"}`。
- 保留：初次登记，无旧字段；其他对象均不改变。
- 引用：`U14@2`；范围：`T14`。
- 调用者判断：E2E 报告不能替代有权主体的最终验收。
- 依据：[T14.04](dsh-process-truth-v1.md#t14)；报告归属：来源作者，确切个人未知；历史事件时间未知；可见块：`S031`。
- 检查/拒绝：R01, R02, R03, R04, R05, R12。来源报告投影不声称执行过历史 API。

#### T14.10 · revise(G14)

更新用户功能已存在的报告；最终验收保留未知。

- 前态：`G14@1`；后态：`G14@2`。
- 新增/改写：`{"check_evidence": "O14e2e", "implementation_evidence": "U14", "ui_status": "user-visible half exists as reported"}`。
- 保留：`final_acceptance`、`label`、`user_request`。
- 引用：`U14@2`；`O14e2e@1`；范围：`T14`。
- 调用者判断：来源 Consequences 明说入口存在；不擅自判为仍无入口或已最终验收。
- 依据：[T14.04](dsh-process-truth-v1.md#t14)；报告归属：来源作者，确切个人未知；历史事件时间未知；可见块：`S031`。
- 检查/拒绝：R01, R02, R03, R04, R05, R12。来源报告投影不声称执行过历史 API。

</details>

### 读回

| 问题 | 仅据表示可恢复的回答 | 记录入口 |
|---|---|---|
| 什么结束、什么继续？ | W14old@2 已报告 superseded；G14@2 的入口已报告存在；W14new 承接同一目标。 | T14.04/05/10 |
| 新工作依赖什么？ | L14contract@1 指向 B14@1；A14@2 选用逐项 ifVersion/messageFeedback.put 契约。 | T14.06/07 |
| 哪些旧成果仍使用？ | 已落地后端契约继续使用；旧分支为历史参考，代码取用范围未知。 | T14.04/06/07 |
| 新旧代码来源已知吗？ | 未知；W14old.code_reuse 和 L14contract.code_ancestry 均为 null。 | T14.01/06 |
| 实施与检查结果？ | U14@2 保存 MessageId、串行变更、冲突响应；O14e2e@1 保存作者报告的 E2E 四项范围。 | T14.08/09 |
| 剩余责任或验收？ | 来源确认用户可见入口存在；最终有权验收主体及完整验收状态未知，不能补写已通过或仍无入口。 | T14.09/10 |

以上为主作者离线读回，独立读回尚待执行。

## 两种机制的实际差别

每个专用调用都展开为相同的 target、expected、delta、refs、scope、group、guard_rules。统一方案将调用名替换为 record，并由 record_type 分派检查。两者保留同一份明确效果；这使我们能检查规则被放到了哪里。

例如 T14.04 的 close(W14old) 展开为：expected=1，写入 status=closed_superseded、disposition、successor，其余字段和 G14 全部保留；统一方案的 record(work, W14old, expected=1, delta=...) 必须保留同样的关闭约束。T14.05 与它成组，允许组内引用尚未提交的后继；对外只发布完整组，不能把中间孤立后继当成有效配置。

普通文档也保存相同事实：目标和尝试分别列状态，说明旧分支仅供参考、新后端契约继续使用、UI 已有实现报告，最后列出检查与验收状态。文档作者需要主动维护范围和前后关系；两种结构化方案把这些责任变成可检查的声明。维护时间、错误率和使用体验需独立任务检验，本轮不按接口数推导优胜。

| 移除接口 | 具体替代表达 | 仍需承担的规则 | 本轮判断 |
|---|---|---|---|
| open | 统一 record 创建 work 的初版 | 需要身份唯一、kind=work、初始责任、来源归属；创建时 expected=absent | 登记规则可替代；独立接口可把初始化责任集中起来 |
| close | record 修订 work 的 status/disposition/successor | 限制对象为 work；保留父目标、历史、处置与后继；关闭与创建后继同逻辑组 | 可作为受约束的工作修订接口 |
| revise | record 的 expected + delta + successor | 准确前态、显式写集、后继版本及保留字段；已知对象的修订与历史报告导入分别处理 | 版本更新规则是共用底座；接口名可换，规则需保留 |
| observe | record 创建 observation 记录 | 对象、方法、结果、报告主体、来源版本与时间；报告和确认独立 | 适合类型化追加记录，不能压成无归属备注 |
| judge | record 创建 judgment 并引用观察 | 结论、证据、适用范围、被替代判断；证据引用有效不等于结论正确 | 语义判断由调用者给出，接口负责保存与约束引用 |
| select | record 修订 adoption；或有效决定日志恢复 | scope、old/new、expected、效力与冲突；持有者状态独立 | 显式采用关系不可省；独立函数可由带规则的登记替代 |
| bind | record 创建/修订有类型的关系，或对象内嵌准确引用 | kind、端点版本、范围、修订与旧关系；责任分配还需覆盖检查 | T02 持有规则适合留在设计内容；没有实例时不强造关系事件 |

因此七项继续作为语义接口候选；统一登记成为底层实现候选。是否把某个接口归为便利封装，由后续独立使用结果裁定，当前不凭可改写性删除其语义责任。

## 错误更新与正常输入探针

期待结果在检查前固定。下表为按规则逐项推演的判定；本轮没有实现状态引擎。结构类探针说明未来检查器应拒绝什么，语义类探针说明即使形状合法也仍需来源核对。

| 编号 | 输入变化 | 期待结果及理由 | 检查性质 |
|---|---|---|---|
| P01 T14 | close(G14) 后把父目标置完成 | **拒绝**：close 只作用 work；G14 为 goal。 | 结构可查；R01/R03 |
| P02 T14 | 用合法 revise(G14) 声称后端落地时 UI 已完成 | **保存报告，阻止无依据确认**：修订形状可合法；来源 T14.01 反向说明无入口，需核对含义。 | 语义需核对；R05/R12 |
| P03 T14 | 以旧分支被参考为由声明 UI 代码已复用 | **保存报告，复用关系保持未确认**：reference 与 derived_from 的证据要求不同；源码取用范围未给出。 | 语义需核对；R06/R12 |
| P04 T14 | U14 当前描述版为 2，更新仍给 expected=1 | **拒绝**：本地记录前版不匹配。 | 结构可查；R02 |
| P05 T14 | bind 引用未登记的 backend-X@7 | **拒绝**：准确引用无法解析。 | 结构可查；R01/R06 |
| P06 T14 | revise(U14) 的声明写集顺带包含 A14 | **拒绝**：单对象修订的声明效果越界；采用须有独立显式效果。 | 结构可查；R03/R07 |
| P07 T14 | 补录旧后台报告后，以入库顺序重置 G14.ui_status=absent | **只入历史报告**：早期事件不自动取代后续结果；缺乏当前生效依据。 | 混合；R10 |
| P08 T14 | 未知源码前版，却声明执行了对准确源码版的补丁 | **拒绝该执行断言；可保存报告**：描述记录 expected 与工件 code_revision 属于不同空间。 | 结构可查；R02/R05 |
| P19 T14 | 合法补录缺源码版本的作者实现报告 | **接受报告**：足以登记来源报告；source code_revision=null 保留。 | 结构可查；R02/R05/R12 |

## 检查记录与待执行工作

本地静态核对覆盖声明的前态、expected、引用、后态、保留字段及两种表示的同效果，共 148 项，通过 148 项。它检查转换材料的内部一致性，来源含义另按本页逐项走查。

原始输入、两套结构化表示、主作者答案、探针期待结果、删减依据、十三段影响表及 Qoder 待发包保存在仓库根目录 `artifacts/agent-task-state/maintenance/dsh-transitions-2026-10-25/`。本批次另建，前轮原始输出与固定底稿保持不变。

Qoder 健康检查返回 expired=true，截止 2026-10-25 00:00（Asia/Shanghai）。三案例各准备构造/检验两批三并发输入，共十八包；读回包无评分答案，来源核对包才带原文。配置恢复后按构造→主裁定→检验顺序执行。当前模型调用为零，独立读回与易用性比较均待执行。
