# DSH 全历史轨迹：探测结论与构建方案

最后更新：2026-11-10

已在 2026-11-10 运行 CodeBuddy 构建器生成全量轨迹。全部 22346 个节点与 2172 个主线节点已纳入，路径提取无未知项。Codex 独立核对了节点集合、父边、原始标题和拓扑顺序，页面 JavaScript 语法检查通过；浏览器交互尚未验收。

本地入口为 [全量轨迹](../../../evidence/trajectory-builders/a/runs/full-path-v1/trajectory.html)，[覆盖报告](../../../evidence/trajectory-builders/a/runs/full-path-v1/coverage.json)保存结构、路径和 83/49/98 来源映射核对。生成物在私有 evidence 中，不提交。Grok 4.7 的独立版本仍在构建，首轮完成声明未通过文件存在性核验。

## 探测结论

- **仓库基线。** DSH 固定 HEAD 为 `86a402200d95fecef4529d969836f1fe13c6cb0d`。离线 `rev-list` 加元数据父向遍历得到 22346 个提交；first-parent 2172 与既有 txt 逐项一致，首次主线 integration 独立重算 22346 项全部一致。仓库为 partial clone（promisor=true、blob:none），过滤配置允许缺失 blob；固定截止的提交与父边已核对齐全。
- **事实与来源。** 83 条唯一事实、49 个来源（36 条正文 + 13 个 commit）、98 条事实—来源引用；49 个 Git 对象本地均存在，其中 36 个 blob 内容匹配。
- **路径索引不均。** 主线 2172 个提交有全路径索引，共 148869 行；全部可达历史中仅 11753 个提交有英文笔记路径索引，20174 个非主线提交尚无全路径索引。故分支目前是结构覆盖，不冒充语义覆盖。
- **时间排序已纠正。** 早先 303 条“时间倒序”源于混合时区字符串比较，属误计；改用 datetime aware 重算后，仅有 5 条 committer 倒序的父子边，这 5 条仍需在轨迹中明确标注。
- **过程段是 overlay。** 16 段主题过程可重叠，不是时间分区；正文中的 commit+path+blob 只证明“观测到”，不等于“该提交发生了该实现”，触碰路径不证明实现成立。
- **方向取舍。** 两轮 Grok 已完成；Codex 否定“按 16 段铺满主线、以标题唯一性判定事实发生”的建议。采用主线时间骨架加侧枝展开：主线承担连续时间轴，侧枝承载分叉与回溯。

## 执行方案

下一阶段由 CodeBuddy 构建离线工具，Codex 作出实现取舍并独立验收。

产物写入新输出目录，原始快照不改：

1. 离线可搜索分页 HTML：主线视图、侧枝视图，支持 SHA、主题、事实三类筛选。
2. 全 22346 节点 JSONL：原始 subject、父边、拓扑序、作者时间、提交者时间、首次主线合入点、变更路径及逐项提取状态。
3. coverage JSON：83/49/98 的双向映射与输入哈希。

提取规则：

- 每个父边用 tree-only `diff-tree --no-renames` 提取 path，并显式记录 `comparison_parent`。
- 禁止懒下载与网络访问；失败逐项保留为未知，不以空值顶替。
- 当前只有样本成功，不据此报告全量路径通过。

时间与语义：

- 拓扑序保证父先子后；日期仅用于展示，不改变序号。
- 区分来源快照时间、正文主张的发生时间、主线合入时间；不强造唯一“发生 SHA”。

验收：全 SHA 集合、父边、主线顺序与 integration 重算一致；83/49/98 守恒；输入哈希可复现；页面每个节点可检索并定位到 JSONL 记录。

## 来源

- `Agent任务状态管理/evidence/agent-task-state/repository-snapshots/dsh-full-history-2026-10-16/commits-metadata.json`
- `Agent任务状态管理/evidence/agent-task-state/repository-snapshots/dsh-full-history-2026-10-16/first-parent-metadata.txt`
- `Agent任务状态管理/evidence/agent-task-state/repository-snapshots/dsh-exhaustive-2026-10-19/commit-first-mainline-integration.json`
- `Agent任务状态管理/evidence/agent-task-state/repository-snapshots/dsh-exhaustive-2026-10-19/first-parent-path-events.json`
- `Agent任务状态管理/evidence/agent-task-state/maintenance/dsh-composition-2026-10-20/v2/sources.json`
- `Agent任务状态管理/evidence/agent-task-state/maintenance/dsh-composition-2026-10-20/v2/input-facts.json`
- `Agent任务状态管理/experiments/dsh-process/dsh-process-truth-v1.md`

责任与下一步：本轮探测由 CodeBuddy 记录，已由 Codex 复核并修正；下一验收为浏览器交互与 Grok 独立结果核查。`artifacts/` 为本地忽略目录，路径按仓库根相对书写，不代表已提交。
