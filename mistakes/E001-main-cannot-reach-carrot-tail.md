# E001：Main 路线无法到达 Carrot tail

- 局面：官方 episode `106755835`，我方 seat 0。turn 226 已公开 `FARMERS_MARKET`，但没有 `YARN_STORE`；turn 360 又出现两个 `PET_CAFE`。
- 对手：最终金币 107,593；我方 88,189，负 19,404。
- 原行为：turn 226 的第一跳只识别 `YARN_STORE`，因此保持 `MAIN`。turn 360 虽然 carrot price 已为 43（达到阈值 42），`YARN_CARROT` 与 `MAIN` 的前缀不相同，`_switch_ok` 禁止直接切换。
- 表面现象：季末 carrot price 升至 65，我方没有进入为 carrot 高需求准备的 tail。
- 根因证据：三个决策点的公开 observation 与 Router 的前缀保护逻辑共同证明，carrot tail 的唯一入口依赖 turn 226 先进入 `YARN`；该局公开 Farmers Market 信号未被用作入口。未来 Pet Cafe 在 turn 226 不可见，因此归因不是“没有预测随机商店”。
- 单变量候选：只把 turn 226 bridge 的公开 shop 计数从 `YARN_STORE` 扩为 `YARN_STORE + FARMERS_MARKET`；路线、阈值、决策时刻和修复层全部不变。
- 预期改善：Farmers Market 开局可保留 turn 360 进入 carrot tail 的路径。
- 可能副作用：只有 Farmers Market、后续 carrot 需求不足的种子会被错误送进 wool/carrot 兼容路线。
- 固定回归：episode seed `106755835` 对应场景，以及 seeds 0–19 的新旧 Router 换边直赛；候选不能只改善单局而牺牲常见无 Yarn 场景。
- 验证结果：候选对原版在 seeds 0–19 换边为 2-28-10，平均差 -1,835.95；目标信号过宽。
- 新副作用：普通 Farmers Market 不足以预测后续双 Pet Cafe，过早进入 wool-compatible tail 在 seeds 1、10、11、14 等产生可重复损失。
- 最终处理：撤销候选（根 `main.py` 从未替换），该场景继续保留为错题，但不能用宽 bridge 修复。
