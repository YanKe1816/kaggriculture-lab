# 实验日志

## E000：公开强基线快速筛选

- 日期：2026-09-08
- 对照版本：Public State Router（候选冠军）
- 唯一主要变量：被比较的公开策略实现；未修改任何候选内部逻辑。
- 配置：官方 `kaggle-environments==1.32.7`，720 回合，每组双方换边；Fast Routes 使用 seeds 0–2，另外两组使用 seed 0。
- 对局：Fast Routes 6 局，另外两组各 2 局，共 10 局。

| 候选 A | 对照 Router | A 胜-平-负 | A 平均金币差 | 保留判断 |
|---|---|---:|---:|---|
| v48 Fast Routes | Public State Router | 0-0-6 | -18,958.7 | 不作为首提 |
| V16 RC5 Premium Market Lead | Public State Router | 0-0-2 | -23,448.5 | 不作为首提 |
| Shape the Shop / Pasture Top-10 | Public State Router | 0-0-2 | -9,260 | 不作为首提 |

结论：Router 在快速闸门中双边击败另外三条公开强路线，且所有进程均正常结束，因此选为首次官方提交。可信度为**低到中**：换边消除了座位这一明显混杂，Fast Routes 也跨 3 个种子复现；另外两个对手仍只有一个种子。该结果只支持“值得首提”，不支持“稳定最强”。

反方检查：结果可能仅适配 seed 0 或这些 tape 家族，也可能被专门的 clone/tape 对策攻击。下一轮必须加入多种子、官方回放对手和运行时/资源统计。

原始结果：

- `results/fast-vs-router.json`
- `results/v16-vs-router-seed0.json`
- `results/pasture-vs-router-seed0.json`

## E001：20-seed 扩大基线赛

- 日期：2026-09-08
- 对照版本：Public State Router 不变。
- 唯一主要变量：对手基线。
- 配置：官方 `kaggle-environments==1.32.7`，seeds 0–19，每 seed 双方换边，全部 720 回合。
- 对局：每组 40 局，共 120 局、240 个 agent seat runs；全部状态 `DONE`，无异常退出。

| 对手 | Router 胜-平-负 | 胜率 | 平均金币差 | 中位金币差 | Router seat 0 / seat 1 |
|---|---:|---:|---:|---:|---:|
| Fast Routes | 34-0-6 | 85.0% | +14,988.5 | +18,328.5 | 17-0-3 / 17-0-3 |
| V16 RC5 | 40-0-0 | 100% | +19,397.4 | +17,741.5 | 20-0-0 / 20-0-0 |
| Pasture Top-10 | 40-0-0 | 100% | +8,663.9 | +8,544 | 20-0-0 / 20-0-0 |

Fast Routes 的 6 负集中在 seeds 10、15、18，三个种子换边均负；两个座位各 17-3，seat 平均差仅相差 396.45。失败随 seed 而非座位重复，排除了评测方向写反、明显位置偏差和对手异常退出。结果稳定，停止在 20 seeds，不机械扩到 50。

结论：Router 以总计 114-0-6（95.0%）守擂；但 Fast Routes 是唯一能稳定找到特定 seed 弱点的近邻，应保留为回归对手。

## E002：Farmers Market bridge（拒绝）

- 对照版本：原 Public State Router。
- 唯一主要改动：turn 226 的 bridge 由只计 `YARN_STORE` 改为计 `YARN_STORE + FARMERS_MARKET`；其他代码逐字不变。
- 证据场景：官方最大败局 `106755835` 在 turn 226 已有 Farmers Market，turn 360 有两个 Pet Cafe、carrot price 43；原 `MAIN` 因前缀保护不能进入 carrot tail。
- 配置：seeds 0–19，每 seed 换边，40 局完整 720 回合。
- 结果：候选 2-28-10，胜率 5.0%，平均金币差 -1,835.95，中位 0；seat 0 为 0-14-6，seat 1 为 2-14-4；80 个 seat runs 全部 `DONE`。
- 反方结论：扩桥确实改变目标场景，但把多个普通 Farmers Market 种子过早送入 wool-compatible tail；损害（10 负）远大于改善（2 胜），不是随机小波动。
- 决策：拒绝，不升级擂主，不作第二次官方提交。原 Router 保持可回退且继续作为 `main.py`。
