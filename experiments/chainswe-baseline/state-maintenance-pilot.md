# ChainSWE 状态维护校准

2026 年 11 月 23 日至 24 日的校准形成了三组实验入口，并确认了一个状态维护问题。作者版 StateHarness 会把任务焦点复制到简报，部分实际写入没有触发同步。StateSystem 首版改用链接，在真实 Pi 单题运行中读回了更新后的焦点。同线路下的两份单题补丁都通过评分，完整链的维护收益仍待比较。

## 实验设置

- [冻结样本](sample-v1.json)含 12 条主链和 12 条备用链。当前证据来自 Dulwich 和 mpmath 两条校准链及 mpmath 第一题的后续复跑。
- 逐题揭示，同一条链沿用各组自己的 Pi 会话、代码和状态。各组使用相同初始快照。独立评分器有参考材料，Agent 看不到评分反馈。
- 三组为纯 Pi 1.5.2、按作者原始 hook 移植的 StateHarness A4、StateSystem v0.1.0。StateSystem 首版保留提醒、校验和诊断。任务焦点、进展和警告各有来源，简报用链接指向原处。切题时归档上一题的任务记录。

## 首轮逐题校准

11 月 23 日，两组使用 DeepSeek 官方 `deepseek-flash`，每条链预算 30 分钟。

| 链 | 纯 Pi | StateHarness A4 |
| --- | --- | --- |
| Dulwich，3 题 | 完成 3 题。修复用例 2/25，原有行为 434/435。 | 完成 3 题。修复用例 2/25，原有行为 434/435。 |
| mpmath，4 题 | 到时保存第三题补丁，第四题未发。已见题的修复用例 3/4，原有行为 79/79。 | 到时保存第四题补丁。修复用例 3/5，原有行为 85/85。前三题的修复用例为 2/4。 |

Dulwich 切分支题中，纯 Pi 反复调试已有的 `checkout_branch`，A4 更快收敛到该入口的路径参数问题。许多评分用例调用 `porcelain.checkout`，两份补丁均为 0/22。两组也都漏掉了第一题评分要求的分叉合并。四份原始 Pi 会话里只记录到一次压缩，发生在纯 Pi 的 Dulwich 第三题开头。第二题的反复调试发生在压缩之前。Dulwich 的 A4 辅助诊断用量记录不全，整组用量无法直接比对。

mpmath 的 A4 在第一题改写了 `task_state.md`，简报仍显示初始焦点，后来做 Hankel 和 `repr` 时仍看到第一题的补零问题。作者的同步脚本从 Bash 命令文本匹配重定向目标。先 `cd` 到状态目录再用相对路径写入，或用 Python 写入，都可能漏识别。日志能确认状态滞后，无法据此判断它对得分的影响。两组都触及时间预算，截止时看到的题数不同。

## mpmath #922 同线路复跑

11 月 24 日，两组使用同一题面、镜像、评分器和 Magpie 免费线路 `opencode-zen/deepseek-v4.1-flash-free`。第一题修复的是数字格式化时补零与千位分隔符的顺序。

| 组别 | 修复用例 | 回归用例 | 会话结果 |
| --- | --- | --- | --- |
| StateSystem v0.1.0 | 1/1 | 11/11 | 399 秒，正常交卷 |
| StateHarness A4 | 1/1 | 11/11 | 413 秒，最终答复前收到免费额度限制 HTTP 429。评分使用已保存补丁。 |

两份补丁都对无穷大等特殊值保留了原格式化路径，避开首轮 A4 把 `0000inf` 错写为 `0,000inf` 的失败。修复评分中的一个用例涵盖许多格式组合，一个反例就会让整项失败。

- A4 第一次推送简报时焦点为空。Agent 随后用 Pi 的 `write` 写入焦点，作者脚本成功同步到简报，本次没有重现漏同步。
- StateSystem 发出的简报含源文件链接。Agent 通过 Python 改写焦点并读回最新内容。v0.1.0 的任务模板仍有一条描述旧同步机制的注释，待下版更正。

两组单题补丁得分相同，A4 的用时截至额度中断。下一轮应在同一线路下按原协议跑完四题，再观察跨题维护、历史复用和额外读取成本。Magpie 的额度中断应单独登记。

## 本地证据位置

原始记录保留在本地 `evidence/`。以下路径从仓库根目录起算。

| 内容 | 路径 |
| --- | --- |
| 首轮逐题评分与运行索引 | `evidence/pi-baseline/frozen-chainswe-v1/` 中 Dulwich、mpmath 各自的 `paired-result.json` |
| StateSystem 版本与单题复跑 | `evidence/pi-baseline/statesystem/versions/v0.1.0/` 和 `evidence/pi-baseline/statesystem/runs/pi-chainswe-magpie-sequential-locked-first-issue-statesystem-v0.1.0-20261124-144134/` |
| 作者版 A4 同线路单题复跑 | `evidence/pi-baseline/calibration/meltano-sdk/magpie-preliminary/pi-chainswe-magpie-sequential-locked-first-issue-a4-20261124-145144/` |

两份单题目录各有 `experiment.json`、`grader.log`、Pi 会话及第一题补丁。
