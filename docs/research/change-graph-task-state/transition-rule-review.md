---
title: 工作转换检验：对象、效果与拒绝条件
status: active
created: 2026-10-25
updated: 2026-10-25
tags: [research, transitions, work-operations]
---

# 工作转换检验：对象、效果与拒绝条件

本页保存[工程全景](dsh-work-history.md)中工作操作研究的本轮明细：固定来源、具体转换、两种表示、探针与取舍。当前为主 Agent 离线走查；Qoder MCP 已移除，原独立构造与读回包保留为停用材料，尚未派发。

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

初始记录的来源也逐项登记：；`G14@1` → T14.01；`B14@1` → T14.01、T14.02；`U14@1` → 研究占位，内容未知，不声称历史创建；`A14@1` → 研究占位，内容未知，不声称历史创建。

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

- 前态：该研究对象尚未登记，要求 expected=absent；后态：`W14old@1`。
- 新增/改写：`{"code_reuse": null, "contract": "session revision / feedback.upsert", "goal": "G14", "source_identity": "#1010", "status": "historical_attempt"}`。
- 保留：初次登记，无旧字段；其他对象均不改变。
- 引用：`G14@1`；范围：`T14`。
- 调用者判断：把 #1010 作为独立尝试的研究身份；不推导代码血缘。
- 依据：[T14.02](dsh-process-truth-v1.md#t14)；报告归属：来源作者，确切个人未知；历史事件时间未知；可见块：`S031`。
- 检查/拒绝：R01, R02, R03, R04, R05, R12。来源报告投影不声称执行过历史 API。

#### T14.02 · observe(O14inspection)

保存检查报告及三个不兼容点。

- 前态：该研究对象尚未登记，要求 expected=absent；后态：`O14inspection@1`。
- 新增/改写：`{"reported_method": "old branch inspection", "result": ["API incompatible with landed backend", "duplicate backend", "directory drift"], "subject": "W14old", "verification_level": "author_report"}`。
- 保留：初次登记，无旧字段；其他对象均不改变。
- 引用：`W14old@1`；`B14@1`；范围：`T14`。
- 调用者判断：核对原文确实给出这些区别。
- 依据：[T14.02](dsh-process-truth-v1.md#t14)；[T14.03](dsh-process-truth-v1.md#t14)；报告归属：来源作者，确切个人未知；历史事件时间未知；可见块：`S031`。
- 检查/拒绝：R01, R02, R03, R04, R05, R12。来源报告投影不声称执行过历史 API。

#### T14.03 · judge(J14route)

保存路线取舍及依据。

- 前态：该研究对象尚未登记，要求 expected=absent；后态：`J14route@1`。
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

- 前态：该研究对象尚未登记，要求 expected=absent；后态：`W14new@1`。
- 新增/改写：`{"goal": "G14", "predecessor": "W14old", "responsibility": "UI against landed backend", "source_identity": null, "status": "rewrite_as_reported"}`。
- 保留：初次登记，无旧字段；其他对象均不改变。
- 引用：`G14@1`；`W14old@2`；范围：`T14`。
- 调用者判断：新尝试 ID 为研究分配，原文没有提供其创建事件。
- 依据：[T14.03](dsh-process-truth-v1.md#t14)；报告归属：来源作者，确切个人未知；历史事件时间未知；可见块：`S031`。
- 检查/拒绝：R01, R02, R03, R04, R05, R12；逻辑组 `T14.route` 整体检查。来源报告投影不声称执行过历史 API。

#### T14.06 · bind(L14contract)

把新 UI 的契约依赖与旧代码取用分开。

- 前态：该研究对象尚未登记，要求 expected=absent；后态：`L14contract@1`。
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

- 前态：该研究对象尚未登记，要求 expected=absent；后态：`O14e2e@1`。
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

<a id="t12"></a>
## T12：整批撤回后分别推进，父责任保留

拆分保留的是责任，而非把父项状态复制给子项。我们将 S029 的清单概括为独立功能、Turn 行为、通知与 Context、产品分组、功能验收、性能验收六类：独立功能包含来源已列明的设置/摘要/视觉/过滤范围；Turn 对应 6/7/10/11，通知与 Context 对应 8/9-context，产品分组对应完整 grouping 要求。原始逐功能要求继续由 S029 负责；六类是本研究的责任索引。

本轮修订：拆分前保存六类完整责任；三子项承接前四类，父项保留两类验收。共同更新作为 T12.split 组检查。若责任分类遗漏原要求，集合检查本身无法发现，必须由来源核对补正。

### 初始对象

初始记录的来源也逐项登记：；`G12@1` → T12.01；`W12parent@1` → T12.01、T12.02；`F12@1` → T12.05。

<details><summary>展开初始描述及未知项</summary>

```json
{
  "G12": {
    "revision": 1,
    "kind": "goal",
    "fields": {
      "label": "三档聊天显示与分组",
      "requirements": [
        "independent_visuals",
        "turn_behavior",
        "trigger_and_context",
        "product_groups",
        "functional_acceptance",
        "performance_acceptance"
      ],
      "acceptance": "pending"
    }
  },
  "W12parent": {
    "revision": 1,
    "kind": "work",
    "fields": {
      "goal": "G12",
      "source_identity": "#4565",
      "adoption": "merged_then_reverted_as_reported",
      "retained_reference": "original PR",
      "allocation": null,
      "residual": [
        "independent_visuals",
        "turn_behavior",
        "trigger_and_context",
        "product_groups",
        "functional_acceptance",
        "performance_acceptance"
      ],
      "acceptance": "pending"
    }
  },
  "F12": {
    "revision": 1,
    "kind": "artifact",
    "fields": {
      "label": "Definition-owned Build Group foundation",
      "implementation": null,
      "product_integration": "incomplete",
      "performance_acceptance": "pending"
    }
  }
}
```

</details>

### 转换总览

| 步骤 | 操作与对象 | 具体变化 |
|---|---|---|
| T12.01 | `observe(O12revert)` | 保存整体撤回和检查盲区；需求继续保留 |
| T12.02 | `open(W12visual)` | 登记独立视觉工作及其状态维度 |
| T12.03 | `open(W12turn)` | 登记草稿所在工作及剩余责任 |
| T12.04 | `open(W12groups)` | 产品分组工作与已完成基础分开 |
| T12.05 | `bind(L12allocation)` | 显式列明分配；保留父层验收责任 |
| T12.06 | `revise(W12parent)` | 父项记录分配和剩余验收；原范围完整保留 |
| T12.07 | `revise(F12)` | 分组基础有实现报告，产品接入仍未完成 |
| T12.08 | `observe(O12checks)` | 检查结果限定到实际 channel |

<details><summary>展开逐步调用：前态、效果、保留、来源与拒绝规则</summary>

#### T12.01 · observe(O12revert)

保存整体撤回和检查盲区；需求继续保留。

- 前态：该研究对象尚未登记，要求 expected=absent；后态：`O12revert@1`。
- 新增/改写：`{"method": "author history and benchmark coverage review", "result": "batch reverted eight minutes after merge due performance", "subject": "W12parent", "uncovered": "streaming grouping and seat re-render hot paths"}`。
- 保留：初次登记，无旧字段；其他对象均不改变。
- 引用：`W12parent@1`；范围：`T12`。
- 调用者判断：撤回的是实现组合，不是产品要求。
- 依据：[T12.01](dsh-process-truth-v1.md#t12)；[T12.02](dsh-process-truth-v1.md#t12)；报告归属：来源作者，确切个人未知；历史事件时间未知；可见块：`S028/S029/S022 partial order`。
- 检查/拒绝：R01, R02, R03, R04, R05, R12。来源报告投影不声称执行过历史 API。

#### T12.02 · open(W12visual)

登记独立视觉工作及其状态维度。

- 前态：该研究对象尚未登记，要求 expected=absent；后态：`W12visual@1`。
- 新增/改写：`{"acceptance": "pending", "commit": "reported committed", "completion": "reported complete scope", "destination": "presentation channel", "goal": "G12", "responsibility": ["independent_visuals"]}`。
- 保留：初次登记，无旧字段；其他对象均不改变。
- 引用：`G12@1`；范围：`T12`。
- 调用者判断：分支承接工作为研究身份；完成的仅为来源列出的独立范围。
- 依据：[T12.03](dsh-process-truth-v1.md#t12)；[T12.04](dsh-process-truth-v1.md#t12)；报告归属：来源作者，确切个人未知；历史事件时间未知；可见块：`S028/S029/S022 partial order`。
- 检查/拒绝：R01, R02, R03, R04, R05, R12；逻辑组 `T12.split` 整体检查。来源报告投影不声称执行过历史 API。

#### T12.03 · open(W12turn)

登记草稿所在工作及剩余责任。

- 前态：该研究对象尚未登记，要求 expected=absent；后态：`W12turn@1`。
- 新增/改写：`{"acceptance": "pending", "commit": "unstaged", "completion": "incomplete", "destination": "turnstep worktree", "goal": "G12", "implementation": "drafts written", "responsibility": ["turn_behavior", "trigger_and_context"]}`。
- 保留：初次登记，无旧字段；其他对象均不改变。
- 引用：`G12@1`；范围：`T12`。
- 调用者判断：有草稿和已提交分别记录。
- 依据：[T12.03](dsh-process-truth-v1.md#t12)；[T12.04](dsh-process-truth-v1.md#t12)；报告归属：来源作者，确切个人未知；历史事件时间未知；可见块：`S028/S029/S022 partial order`。
- 检查/拒绝：R01, R02, R03, R04, R05, R12；逻辑组 `T12.split` 整体检查。来源报告投影不声称执行过历史 API。

#### T12.04 · open(W12groups)

产品分组工作与已完成基础分开。

- 前态：该研究对象尚未登记，要求 expected=absent；后态：`W12groups@1`。
- 新增/改写：`{"acceptance": "pending", "completion": "incomplete", "foundation": "F12", "goal": "G12", "responsibility": ["product_groups"]}`。
- 保留：初次登记，无旧字段；其他对象均不改变。
- 引用：`G12@1`；`F12@1`；范围：`T12`。
- 调用者判断：工作边界是研究索引，不虚构源码新建事件。
- 依据：[T12.05](dsh-process-truth-v1.md#t12)；报告归属：来源作者，确切个人未知；历史事件时间未知；可见块：`S028/S029/S022 partial order`。
- 检查/拒绝：R01, R02, R03, R04, R05, R12；逻辑组 `T12.split` 整体检查。来源报告投影不声称执行过历史 API。

#### T12.05 · bind(L12allocation)

显式列明分配；保留父层验收责任。

- 前态：该研究对象尚未登记，要求 expected=absent；后态：`L12allocation@1`。
- 新增/改写：`{"allocation": {"W12groups": ["product_groups"], "W12turn": ["turn_behavior", "trigger_and_context"], "W12visual": ["independent_visuals"]}, "from": "W12parent", "overlap": [], "relation": "responsibility_allocation", "to": ["W12visual", "W12turn", "W12groups"], "unresolved_partition": []}`。
- 保留：初次登记，无旧字段；其他对象均不改变。
- 引用：`W12parent@1`；`W12visual@1`；`W12turn@1`；`W12groups@1`；范围：`T12`。
- 调用者判断：六项是本次概括的责任单元；逐项原始功能清单仍由 S029 负责。
- 依据：[T12.03](dsh-process-truth-v1.md#t12)；[T12.04](dsh-process-truth-v1.md#t12)；[T12.05](dsh-process-truth-v1.md#t12)；报告归属：来源作者，确切个人未知；历史事件时间未知；可见块：`S028/S029/S022 partial order`。
- 检查/拒绝：R01, R02, R04, R06, R08, R11, R12；逻辑组 `T12.split` 整体检查。来源报告投影不声称执行过历史 API。

#### T12.06 · revise(W12parent)

父项记录分配和剩余验收；原范围完整保留。

- 前态：`W12parent@1`；后态：`W12parent@2`。
- 新增/改写：`{"allocation": "L12allocation", "residual": ["functional_acceptance", "performance_acceptance"]}`。
- 保留：`acceptance`、`adoption`、`goal`、`retained_reference`、`source_identity`。
- 引用：`L12allocation@1`；范围：`T12`。
- 调用者判断：责任分类为调用者判断；不能把子项完成当作整体验收。
- 依据：[T12.03](dsh-process-truth-v1.md#t12)；[T12.06](dsh-process-truth-v1.md#t12)；报告归属：来源作者，确切个人未知；历史事件时间未知；可见块：`S028/S029/S022 partial order`。
- 检查/拒绝：R01, R02, R03, R04, R08, R11, R12；逻辑组 `T12.split` 整体检查。来源报告投影不声称执行过历史 API。

#### T12.07 · revise(F12)

分组基础有实现报告，产品接入仍未完成。

- 前态：`F12@1`；后态：`F12@2`。
- 新增/改写：`{"implementation": "implemented as source reports"}`。
- 保留：`label`、`performance_acceptance`、`product_integration`。
- 引用：`W12groups@1`；范围：`T12`。
- 调用者判断：foundation 与 product_groups 的范围不同。
- 依据：[T12.05](dsh-process-truth-v1.md#t12)；报告归属：来源作者，确切个人未知；历史事件时间未知；可见块：`S028/S029/S022 partial order`。
- 检查/拒绝：R01, R02, R03, R04, R05, R12。来源报告投影不声称执行过历史 API。

#### T12.08 · observe(O12checks)

检查结果限定到实际 channel。

- 前态：该研究对象尚未登记，要求 expected=absent；后态：`O12checks@1`。
- 新增/改写：`{"excluded": ["turnstep drafts", "real-model GUI demo", "performance acceptance"], "result": "build/lint/coverage checks pass as reported", "subject": "W12visual", "verification_level": "author_report"}`。
- 保留：初次登记，无旧字段；其他对象均不改变。
- 引用：`W12visual@1`；范围：`T12`。
- 调用者判断：核对测试范围；不传播到另一个 worktree。
- 依据：[T12.06](dsh-process-truth-v1.md#t12)；报告归属：来源作者，确切个人未知；历史事件时间未知；可见块：`S028/S029/S022 partial order`。
- 检查/拒绝：R01, R02, R03, R04, R05, R12。来源报告投影不声称执行过历史 API。

</details>

### 读回

| 问题 | 仅据表示可恢复的回答 | 记录入口 |
|---|---|---|
| 整批撤回了什么？ | 撤回整批实现组合，保留原产品需求和 PR 参考；没有据此结束父目标。 | T12.01 |
| 责任去了哪里？ | visual、turn、groups 三项分工；功能和性能整体验收留在父项。 | T12.02-06 |
| 已完成与草稿？ | 来源列明的独立范围已提交，turnstep 部分草稿未暂存；两种状态单独保存。 | T12.02/03 |
| 基础完成意味着什么？ | F12@2 仅有基础实现报告，产品分组及性能接入仍未完成。 | T12.04/07 |
| 验证覆盖哪里？ | O12checks@1 仅覆盖 presentation channel，排除 turnstep、真实模型 GUI 和性能验收。 | T12.08 |
| 父项为何仍未验收？ | G12/W12parent 的验收仍 pending，原需求保留；子项 completion 不写父验收。 | T12.06/08 |

以上为主作者离线读回，独立读回尚待执行。

<a id="t02"></a>
## T02：开发演化记录与产品运行规则分层

本例记录的是一次开发设计与实现演化。旧运行版被保留、最后释放才清理，是来源提供的量化规则；来源没有给出具体 Agent、runtime 版本或释放事件。规则保存在 C02 内容中即可。为让 bind 出场而添加一个自指联系不会增加信息，因此本例没有额外的持有关系事件。

### 初始对象

初始记录的来源也逐项登记：；`W02@1` → T02.01；`C02@1` → T02.01；`A02@1` → 研究占位，内容未知，不声称历史创建。

<details><summary>展开初始描述及未知项</summary>

```json
{
  "W02": {
    "revision": 1,
    "kind": "work",
    "fields": {
      "label": "预设配置演化",
      "implementation": "per-Agent directory presets as reported",
      "commit": null
    }
  },
  "C02": {
    "revision": 1,
    "kind": "artifact",
    "fields": {
      "layer": "product_design",
      "definition": "per-Agent preset directories; Host shared",
      "update_rule": null,
      "holder_rule": null,
      "cleanup_rule": null,
      "restart_rule": null,
      "activation_rule": null
    }
  },
  "A02": {
    "revision": 1,
    "kind": "adoption",
    "fields": {
      "scope": "documented preset implementation design",
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
| T02.01 | `observe(O02issues)` | 记录先前实现遇到的问题 |
| T02.02 | `revise(C02)` | 修订产品设计；规则描述多版本共存条件 |
| T02.03 | `revise(W02)` | 记录已报告的开发实现变化 |
| T02.04 | `select(A02)` | 在开发设计层记录采用 |

<details><summary>展开逐步调用：前态、效果、保留、来源与拒绝规则</summary>

#### T02.01 · observe(O02issues)

记录先前实现遇到的问题。

- 前态：该研究对象尚未登记，要求 expected=absent；后态：`O02issues@1`。
- 新增/改写：`{"result": ["Host consumers missing moved services", "unload may write back input", "preset identity not all persisted", "missing idle release"], "subject": "W02", "verification_level": "author_report"}`。
- 保留：初次登记，无旧字段；其他对象均不改变。
- 引用：`W02@1`；`C02@1`；范围：`T02`。
- 调用者判断：按来源可见顺序登记，不补出精确故障发生时间。
- 依据：[T02.01](dsh-process-truth-v1.md#t02)；[T02.02](dsh-process-truth-v1.md#t02)；报告归属：来源作者，确切个人未知；历史事件时间未知；可见块：`S030`。
- 检查/拒绝：R01, R02, R03, R04, R05, R12。来源报告投影不声称执行过历史 API。

#### T02.02 · revise(C02)

修订产品设计；规则描述多版本共存条件。

- 前态：`C02@1`；后态：`C02@2`。
- 新增/改写：`{"activation_rule": "persistence and activation outcomes separate; failed activation rejects new bindings", "cleanup_rule": "dispose retired tree only on final release", "definition": "ordinary Cordis declarations; registry owns runtime revisions", "holder_rule": "Agents/children/cold readers retain exact revision", "restart_rule": "resolve saved identity against current configuration; missing definition fails; executable old revisions process-local", "update_rule": "update retires former runtime revision"}`。
- 保留：`layer`。
- 引用：`O02issues@1`；范围：`T02`。
- 调用者判断：保存量化规则，不虚构 runtime-r1、runtime-r2 或实际 Agent。
- 依据：[T02.03](dsh-process-truth-v1.md#t02)；[T02.04](dsh-process-truth-v1.md#t02)；[T02.05](dsh-process-truth-v1.md#t02)；报告归属：来源作者，确切个人未知；历史事件时间未知；可见块：`S005`。
- 检查/拒绝：R01, R02, R03, R04, R05, R12。来源报告投影不声称执行过历史 API。

#### T02.03 · revise(W02)

记录已报告的开发实现变化。

- 前态：`W02@1`；后态：`W02@2`。
- 新增/改写：`{"commit": "d1e22a7e247060496e1acdba9ef3be1700e23ec7", "implementation": "declarative presets as reported"}`。
- 保留：`label`。
- 引用：`C02@2`；范围：`T02`。
- 调用者判断：该 commit 说明开发提交；不是某个运行实例的版本。
- 依据：[T02.03](dsh-process-truth-v1.md#t02)；报告归属：来源作者，确切个人未知；历史事件时间未知；可见块：`S005`。
- 检查/拒绝：R01, R02, R03, R04, R05, R12。来源报告投影不声称执行过历史 API。

#### T02.04 · select(A02)

在开发设计层记录采用。

- 前态：`A02@1`；后态：`A02@2`。
- 新增/改写：`{"effect": "documented implementation adopts this design", "selected": "C02@2"}`。
- 保留：`scope`。
- 引用：`C02@2`；`W02@2`；范围：`documented preset implementation design`。
- 调用者判断：作用范围是已报告实现设计，不是所有在跑会话。
- 依据：[T02.03](dsh-process-truth-v1.md#t02)；报告归属：来源作者，确切个人未知；历史事件时间未知；可见块：`S005`。
- 检查/拒绝：R01, R02, R03, R04, R07, R09, R12。来源报告投影不声称执行过历史 API。

</details>

### 读回

| 问题 | 仅据表示可恢复的回答 | 记录入口 |
|---|---|---|
| 开发变化？ | W02@2 报告声明式实现提交；C02@2 保存替代后的设计。 | T02.02/03 |
| 谁采用什么？ | A02@2 的范围是文档报告的实现设计，选中 C02@2；没有所有运行会话的采用记录。 | T02.04 |
| 旧版为何还能存在？ | C02@2 的量化规则：旧 runtime 修订退役后，现有持有者保留，最后释放才清理。 | T02.02 |
| 重启如何处理？ | 按保存身份解析当前配置；缺定义失败；旧可执行修订仅进程内存活。 | T02.02 |
| 有真实运行实例吗？ | 本表示没有：来源没有提供具体持有/释放实例。本轮 runtime 探针另标 synthetic。 | T02.02/04 |
| 保存与激活关系？ | 两种结果分别报告；激活失败拒绝新绑定，不能由保存成功推出激活成功。 | T02.02 |

以上为主作者离线读回，独立读回尚待执行。

## 两种机制的实际差别

<details><summary>展开普通工作文档对照：与结构化表示使用相同事实</summary>

### T14 普通文档


用户目标是给 Web 提供逐消息评分和备注。#2217 已落地持久 sidecar 和 Host 的 list/put/delete，当时没有客户端入口，#1326 所需的用户可见部分尚未完成。

旧 #1010 是另一项全栈尝试，使用 session revision 和 feedback.upsert。后来后端采用逐项 ifVersion/messageFeedback.put，目录也发生更名。作者检查后认为旧分支含重复后端、接口不兼容及目录漂移，记录将 #1010 按 superseded 关闭，UI 改为围绕已落地后端重写。关闭的是这次旧尝试；用户目标继续，已有后端继续使用。旧分支留下参考价值，新 UI 取用了哪些旧代码没有证据。

新 UI 的已报告实现包括：给完成消息补入 MessageId、在 Session 内串行提交逐项变更、按冲突响应修正本地项。作者报告 Web 已可录入评分和备注，持久恢复 E2E 覆盖评分、备注、reload restore、撤回。它们说明用户可见入口已有实现报告。最终由谁验收及完整验收结论没有记录。

清单：旧尝试已报告关闭；新 UI 已报告实现；契约采用逐项后端；E2E 为作者报告；代码来源范围和最终有权验收待查。

依据：T14.01—04，S031@b1daf0eeaf596e91eab70603fea12f45105999dd。以上为同一笔记可见块，历史关闭/开启时间未知，记录保存时间不充当事件时间。

### T12 普通文档


原 #4565 混合三档显示、分组、Turn 状态、触发通知、工具视觉和隐藏行。作者记录整批合并八分钟后因性能撤回，原六项基准漏掉流式分组和 seat 重渲染热路径。产品要求继续保留，原 PR 供行为和实现参考。

分工清单：独立功能留 presentation channel，包含已列出的设置、摘要、视觉和过滤等完成范围；未完 Turn 行为（6/7/10/11）以及通知和 Context（8/9-context）留 turnstep 草稿；产品 grouping 的行为、summary、身份与性能要求单列继续。原 PR 的其他实验不自动并入。三类子工作不替代父层功能和性能验收。

状态分开维护：来源列明的独立范围已提交；turnstep 有草稿但未暂存，迁移尚未完成。Definition-owned grouping foundation 已有 implemented 记录，产品分组接入和性能要求仍未完成。channel 的构建、lint、覆盖检查通过是作者报告，范围不延伸到 turnstep。真实模型 GUI 演示和性能测量待做。

责任表：独立范围→presentation；Turn 与通知/Context→turnstep；产品分组→grouping 工作；功能验收和性能验收→父任务。全部原要求保留，子项完成不自动变成父项验收。

依据：T12.01—06，S028/S029@8b43d44cc6b12a9f494693f6e089ebae193b8487，S022@86a402200d95fecef4529d969836f1fe13c6cb0d；来源间只保留可证局部顺序，研究者归纳的责任分类不是上游新建事件。

### T02 普通文档


先前按 Agent 装载预设目录，Host 注册设施共享。作者记录实施中出现 Host 读者缺服务、卸载改写输入、存储缺预设身份和闲置释放问题。之后声明式预设在 9 月 21 日提交 d1e22a7e247060496e1acdba9ef3be1700e23ec7，0.1.7-rc.2 记录 registry 拥有运行修订和插件树。

设计规则：修改定义使旧运行修订退役；已有 Agent、子代理和临时读者持有准确旧修订，最后释放才清理。新定义与旧持有范围可同时有效。保存结果与激活结果分别报告，激活失败拒绝新绑定。

恢复规则：旧可执行修订只在进程内，重启按保存身份解析当前配置，缺少定义时恢复失败。Host 注册与 Agent loop 继续共享。

采用范围是文档已报告的实现设计。这里没有给出具体 Agent/r-old/r-new 运行实例，也没有某个持有或释放事件。不能由“实现采用新设计”改写成“全部现存会话已经切到新运行版本”。

依据：T02.01—05，S030@99f6f02fecdb7dff40c3fbc9470f5907c29f74ca，S005@477b4f420553e8a52c2fbccc464d7561b239c443，S020@86a402200d95fecef4529d969836f1fe13c6cb0d。后者对复用空会话的补充规则不在本次转换范围。

</details>

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
| P09 T12 | 子项 complete 触发父项 acceptance=accepted | **拒绝自动传播**：子项写集不含父验收；有权验收依据未给出。 | 混合；R03/R05 |
| P10 T12 | 分配后遗漏 trigger_and_context 且 residual 不含它 | **拒绝完整拆分确认**：固定责任集合出现无人承接项。 | 结构可查；R08 |
| P11 T12 | 同一责任给两个子项，未声明重叠 | **拒绝完整拆分确认**：结构发现重叠；调用者需声明允许共享或重新划分。 | 结构可查；R08 |
| P12 T12 | 只完成 split 组的 open，直接展示为责任已全部转移 | **保存未完成提案**：组尚未完成分配/父残余更新。 | 结构可查；R11 |
| P13 T12 | 分组基础 implemented 推导产品分组 complete | **保存报告，阻止无依据确认**：基础和产品范围不同；需核对 T12.05。 | 语义需核对；R05/R12 |
| P14 T12 | presentation channel 检查通过扩展到 turnstep 草稿 | **保存原范围报告**：来源明确排除另 worktree；越界确认无依据。 | 语义需核对；R05/R12 |
| P15 T02 | 根据设计文字创建已发生的 Agent-a 持有 r-old 事件 | **拒绝作为真实实例事件**：没有实例身份及实例事件依据。 | 混合；R09 |
| P16 T02 | 合成：新定义采用 r-new 后自动删除 holder-a -> r-old | **拒绝隐式删边**：不同 scope；采用新版本不包含持有者释放事件。 | 结构可查；R03/R07/R09 |
| P17 T02 | 合成：没有 final-release 依据，清理仍被持有的 r-old | **拒绝规则内清理**：违反已声明的量化持有/清理条件。 | 结构可查；R09 |
| P18 T02 | 合成：两个采用更新都基于 scope-X@1，顺序覆盖 | **第二项拒绝当前应用，保留候选**：第二项 expected 已过期；不替调用者决定路线。 | 结构可查；R02/R07 |
| P19 T14 | 合法补录缺源码版本的作者实现报告 | **接受报告**：足以登记来源报告；source code_revision=null 保留。 | 结构可查；R02/R05/R12 |
| P20 T02 | 合成：scope-X 与 scope-Y 各自采用不同版本 | **接受，分别保留**：两者未写同一采用对象；共同依赖仍需检查。 | 结构可查；R07 |

## 规则回查其余十三段

本表核对本轮规则对固定底稿事实的影响；不把它算作十三次完整编码或独立读回。所有事实保持原文，原来未知的原因、代码复用和运行实例继续未知。

| 过程 | 应用规则与事实 | 恢复出的关键区别 | 判断及剩余事项 |
|---|---|---|---|
| [T01](dsh-process-truth-v1.md#t01) | R02/R03/R05；T01.02-05 | 局部撤回保持独立修补；撤回决定、执行中间态、消费者适配分开 | 适用；无额外规则；未取得准确源码基线时保留提交报告，不构造可执行补丁 |
| [T03](dsh-process-truth-v1.md#t03) | R04/R05/R08/R10；T03.01-06 | 首次迁移合入与撤回、后续流式迁移、LogicalSession 阶段分别记录 | 适用；阶段父责任按 R08；首次撤回原因和两个实现代码复用仍未知 |
| [T04](dsh-process-truth-v1.md#t04) | R03/R06/R07；T04.01-06 | 机制替换、独立名单任务与当前投递方式按对象/范围保存 | 适用；无额外规则；不能由成员机制统一推导所有能力已完成 |
| [T05](dsh-process-truth-v1.md#t05) | R03/R05/R06；T05.01-05 | Creator 入口与存储边界分别保存，替代范围显式化 | 适用；无额外规则；文档中的实现状态按实际覆盖范围保留 |
| [T06](dsh-process-truth-v1.md#t06) | R05/R06/R09；T06.01-06 | Schedule 状态和投递规则存为契约；与 Team 共享入口不合并两份持久状态 | 适用；无额外规则；运行投递事件需另有实例证据 |
| [T07](dsh-process-truth-v1.md#t07) | R03/R06/R07；T07.01-05 | E2B 退出与 SSH 接续；共享接口保留，具体提供者退出范围单列 | 适用；无额外规则；接口连续不构成旧实现源码继承 |
| [T08](dsh-process-truth-v1.md#t08) | R05/R06/R07/R09；T08.01-06 | 不同消费者规则分别保存；已报告采用不因缺运行事件被抹掉 | 适用；无额外规则；workflow/model 的投递效果限定各自消费者 |
| [T09](dsh-process-truth-v1.md#t09) | R03/R05/R09；T09.01-05 | 旧解释、评审、DOM 保活方案分开；保留规则不伪写为撤回历史 | 适用；无额外规则；产品保活规则与真实实例寿命不同 |
| [T10](dsh-process-truth-v1.md#t10) | R05/R06/R09；T10.01-05 | Goal 持久化、Host/UI 权限主体和后续修补分开 | 适用；无额外规则；产品权限规则不能充当开发工作的授权事件 |
| [T11](dsh-process-truth-v1.md#t11) | R03/R05/R06；T11.01-05 | 评审否定交接协议，开始即登记方案及限制分别保存 | 适用；无额外规则；新方案设计不自动变成每次任务的运行事件 |
| [T13](dsh-process-truth-v1.md#t13) | R04/R05/R10/R12；T13.01-05 | 旧延迟解释、失败修补、测量、新判断与随包依赖各自留存 | 适用；judge 修正需旧判断引用；本轮未对这五步另做完整状态转换；旧推演继续查前轮 |
| [T15](dsh-process-truth-v1.md#t15) | R03/R05/R06/R09；T15.01-05 | 共享转换/独立引擎/交付 payload 分对象；应用运行、签名和发布分维度 | 适用；无额外规则；作者运行成功不等同完整交付验收 |
| [T16](dsh-process-truth-v1.md#t16) | R02/R03/R05/R12；T16.01-04 | V3→V4 规则存为迁移契约；保留源代际；不虚构 V4 曾支持旧包装 | 适用；无额外规则；契约不能替代某次真实迁移输入输出 |

## 检查记录与待执行工作

本地静态核对覆盖声明的前态、expected、引用、后态、保留字段及两种表示的同效果，共 148 项，通过 148 项。它检查转换材料的内部一致性，来源含义另按本页逐项走查。

原始输入、两套结构化表示、主作者答案、探针期待结果、删减依据、十三段影响表及 Qoder 待发包保存在仓库根目录 `artifacts/agent-task-state/maintenance/dsh-transitions-2026-10-25/`。本批次另建，前轮原始输出与固定底稿保持不变。

Qoder 健康检查返回 expired=true，截止 2026-10-25 00:00（Asia/Shanghai）。三案例各准备构造/检验两批三并发输入，共十八包；读回包无评分答案，来源核对包才带原文。用户随后要求移除 Qoder MCP，原派单安排停用；材料继续保留。当前模型调用为零，独立读回与易用性比较均待执行。

## 离线原型规格与启动条件

建议先实现一个只读入固定夹具的内存检查器。它接收描述记录变更，输出本地记录状态、拒绝原因和证据追踪；专用入口与统一登记共用检查器。实现范围由本轮三案例决定。

### 输入与共同写入接口

`record(expected, changes, basis, provenance, group)`：

- expected 是对象 ID 到准确记录版的映射；新建使用 `absent`，表示已知不存在。`null` 留给内容字段中的未知，不作新建前提。依赖某个可变对象仍为当前版时，也将它列入 expected；只引用旧历史版本则写进 basis。
- changes 是显式对象变化列表，每项包含 target、kind、delta。新建给全量已知描述，修订只给改变字段，其他字段保留。当前夹具采用 work、goal、contract、artifact、observation、judgment、relation、adoption 八个类型标签；这是检查范围，不预设八种数据库表。
- basis 保存精确对象/记录版引用和证据入口。relation 的端点语义由 relation kind 决定；字段中的方便名称必须能解析到这些准确引用。
- provenance 保存来源/事实、报告者、报告或判断性质、历史事件时间和可见块；缺失时间/主体保存 unknown。来源报告与研究者建立的身份分别归属。
- group 声明同一逻辑变化。先检查组的完整读写集，再统一应用；组内新对象可互相引用。失败保留候选与原因，不发布部分已采用快照。

初始描述也用 record(expected=absent) 登记；这与后续新建共用规则。记录版与源码版分字段，未知源码版不能满足源代码执行的准确基线条件。本检查器的写入只作用记录。

七入口映射：open 创建 work 初版；close 修订 work 的处置/后继；revise 修改已知描述；observe 创建带归属的 observation；judge 创建/修订有证据的 judgment；select 修订指定 adoption；bind 创建/修订有类型 relation。每个入口声明允许类型与写集，并编译成相同 record 变化。源码实施、审批和发布事件在本原型中作为报告内容导入。

### 输出与拒绝结果

每个输入组输出：applied 或 rejected、变化前后记录版、实际写集、保持字段、准确引用、来源入口。拒绝原因固定为类型不符、身份冲突、准确前态不符、引用缺失、写集越界、范围冲突、责任缺口/未声明重叠、逻辑组不完整、把设计伪作实例、缺少必要效力依据。原始候选保留，当前状态不改变。

语义不充分的报告可以保留为 attributed claim；把它提升为已确认结论需要单独依据。检查器只验证依据的形状与引用，人工核对负责“依据是否支持结论”。例如 P02/P03 的合法字符串和有效链接不足以机械辨别内容为真；输出应显示待核对，而非伪造一次自动证伪。

### 固定验收输入

真实材料夹具为 T14 十步、T12 八步、T02 四步，另有初始描述。两套入口必须产生同样的规范化状态及证据追踪；这项等价检验只检查实现保持了相同效果。

二十项探针固定包括合法补录、过期前版、缺失引用、暗改采用、旧报告覆盖新结果、责任遗漏/重叠、不完整拆分、跨 worktree 扩大检查结论、设计与实例混淆，以及合成的不同 scope、旧版持有与并发采用。结构类按期待拒绝或接受；语义类必须把需要核对的地方暴露出来。P16—18/P20 为合成运行探针，不能计作 DSH 真实运行事件。

原型阶段才运行这些状态转换。当前批次的 static-inspection.json 检查的是转换表的声明一致性；probe-inputs.json 保存具体输入，probe-verdicts.json 保存本轮主作者的期待判定，二者没有被冒充为运行结果。

### 独立比较与启动 gate

原 Qoder 三并发安排现已停用。后续独立检验沿用逐案例构造→主 Agent 逐项裁定→检验的协议，执行方式另行安排。构造任务只接收固定事实、来源和规则；读回任务接收三种表示与问题，不接收评分答案。先记录原答，再评分，修订另存。

独立结果须逐项回答：是否恢复正确、是否漏失或扩大范围、是否需要额外规则或查证。遇到失败先归因为来源缺失、表示缺失、规则歧义、编码错误或读回错误；修正表示后回查所有受影响步骤。独立读回无未归因差异、类型规则完整、全部探针期待结果明确、十三段影响检查无新增冲突后，再提出实现该检查器的批准请求。

本轮规格和本地走查已交付；Qoder MCP 已移除，独立构造与读回方式待重新安排。维护时间、模型费用和长程效果由后续实验另测，SWE-Milestone 保持后续效果验证入口。
