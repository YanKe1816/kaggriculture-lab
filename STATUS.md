# Kaggriculture 状态

更新：2026-09-08 11:25 UTC

## 当前阶段

- Kaggle 认证成功，账号已加入 `kaggriculture`。
- 官方 Starter 已下载；`kaggle-environments==1.32.7` 已安装并完成 720 回合比赛。
- 已筛选 4 条公开强路线，当前基线为 `main.py`（Public State Router）。
- 首次官方提交 `56093103` 已完成 76 场正式天梯对局；当前 public rating 为 1987.9。

## 已核实规则

- 截止：2026-09-30 23:59 UTC；截止后约继续匹配至 2026-10-15。
- 每日最多 5 次提交；只有最新 2 个提交持续跟踪并用于最终评估，榜单展示两者中较高分。
- 每局 720 回合，只按胜/负/平影响 rating，金币差不直接影响 rating；最终使用 Bradley–Terry tournament。
- 提交必须包含根目录 `main.py` 和 `agent`；比赛运行期间禁止网络 ingress/egress。
- 总奖金 $50,000，前 10 名各 $5,000；获奖方案采用 CC-BY 4.0，并须提供完整可复现说明。
- 最多 5 人团队；地域、制裁、年龄及身份资格适用官方规则。

## 当前最好版本

`main.py` 是 Thomas Tschinkel 公开 Notebook “Kaggriculture: Public State Router (74.5% Win Rate)” 的忠实基线副本。它以公开状态选择预录路线，并包含薄的运行时路由层。

### 第二轮本地结果

官方 1.32.7 引擎、seeds 0–19、完整 720 回合、每 seed 双方换边：

| 对手 | Router 胜-平-负 | 胜率 | 平均 / 中位金币差 |
|---|---:|---:|---:|
| v48 Fast Routes | 34-0-6 | 85.0% | +14,988.5 / +18,328.5 |
| V16 RC5 | 40-0-0 | 100% | +19,397.4 / +17,741.5 |
| Shape the Shop / Pasture Top-10 | 40-0-0 | 100% | +8,663.9 / +8,544 |

共 120 局、240 个 agent seat runs，全部 `DONE`。两个座位结果近似；Fast Routes 的失败固定集中 seeds 10、15、18 且换边仍失败，排除方向写反和主要座位偏差。Router 以总计 114-0-6（95.0%）继续守擂。

单变量 Farmers Market bridge 对原 Router 为 2-28-10，平均差 -1,835.95，已拒绝。

## 官方成绩

- Submission ID: `56093103`
- 描述：`Public-state router faithful baseline v1`
- 当前状态：`COMPLETE`
- Public score：1987.9（76 场正式天梯对局后的实时 rating，仍会变化）
- Episodes：77（1 validation + 76 public）
- 最近下载的 10 场正式回放：5 胜 2 平 3 负

## 与公开强方案差距

当前 Router rating 1987.9，仍明显低于本轮开始时约 2900 的榜首区间。内部对三条公开路线很强，但真实天梯最近样本仅 5-2-3，说明公开基线面板不能替代官方分布。

## 当前阻塞

无比赛实验阻塞。GitHub HTTPS push 因本环境尚未授权 GitHub 而失败；不影响本地实验和 Kaggle。

## 下一项单变量实验

不要继续扩大 Farmers Market bridge。下一项最值得验证的是 Fast Routes seeds 10/15/18 与官方三场败局的共同公开状态，寻找比“所有 Farmers Market”更窄、在 turn 226 已可见的路由条件。
