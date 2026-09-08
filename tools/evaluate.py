#!/usr/bin/env python3
"""Run reproducible, seat-swapped Kaggriculture matchups and save summaries."""

from __future__ import annotations

import argparse
import json
import statistics
import subprocess
import sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path


def play_once(agent_a: str, agent_b: str, seed: int, replay: str | None) -> dict:
    command = [sys.executable, str(Path(__file__).resolve()), "--worker", agent_a, agent_b, str(seed)]
    if replay:
        command.append(replay)
    result = subprocess.run(command, check=True, capture_output=True, text=True)
    # kaggle-environments may print optional-environment import warnings on stdout.
    return json.loads(result.stdout.strip().splitlines()[-1])


def worker(agent_a: str, agent_b: str, seed: int, replay: str | None) -> None:
    from kaggle_environments import make

    env = make(
        "kaggriculture",
        configuration={"episodeSteps": 720, "seed": seed},
        debug=True,
    )
    env.run([agent_a, agent_b])
    final = env.steps[-1]
    row = {
        "seed": seed,
        "rewards": [final[0].reward, final[1].reward],
        "statuses": [final[0].status, final[1].status],
    }
    if replay:
        Path(replay).parent.mkdir(parents=True, exist_ok=True)
        Path(replay).write_text(json.dumps(env.toJSON()), encoding="utf-8")
    print(json.dumps(row))


def main() -> None:
    if len(sys.argv) >= 5 and sys.argv[1] == "--worker":
        worker(sys.argv[2], sys.argv[3], int(sys.argv[4]), sys.argv[5] if len(sys.argv) > 5 else None)
        return

    parser = argparse.ArgumentParser()
    parser.add_argument("agent_a")
    parser.add_argument("agent_b")
    parser.add_argument("--seeds", default="0,1,2")
    parser.add_argument("--no-swap", action="store_true")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--replay-dir", type=Path)
    parser.add_argument("--workers", type=int, default=1)
    args = parser.parse_args()

    seeds = [int(value) for value in args.seeds.split(",")]
    builtins = {"pass", "random", "starter"}
    agents = [value if value in builtins else str(Path(value).resolve()) for value in (args.agent_a, args.agent_b)]
    jobs = []
    for seed in seeds:
        seatings = [(0, agents)] if args.no_swap else [(0, agents), (1, agents[::-1])]
        for swap, seated in seatings:
            replay = None
            if args.replay_dir:
                replay = str(args.replay_dir / f"seed-{seed}-swap-{swap}.json")
            jobs.append((seed, swap, seated, replay))

    games = []
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {
            pool.submit(play_once, seated[0], seated[1], seed, replay): (seed, swap)
            for seed, swap, seated, replay in jobs
        }
        for future in as_completed(futures):
            seed, swap = futures[future]
            row = future.result()
            a_seat = swap
            a_reward, b_reward = row["rewards"][a_seat], row["rewards"][1 - a_seat]
            row.update(
                swap=bool(swap),
                a_reward=a_reward,
                b_reward=b_reward,
                margin=a_reward - b_reward,
                outcome="win" if a_reward > b_reward else "loss" if a_reward < b_reward else "tie",
            )
            games.append(row)
            print(f"seed={seed} swap={swap} {row['outcome']} margin={row['margin']:.0f}")

    games.sort(key=lambda game: (game["seed"], game["swap"]))

    outcomes = Counter(game["outcome"] for game in games)
    margins = [game["margin"] for game in games]
    by_seat = {}
    for seat in (0, 1):
        seated = [game for game in games if int(game["swap"]) == seat]
        if seated:
            seat_outcomes = Counter(game["outcome"] for game in seated)
            by_seat[str(seat)] = {
                "games": len(seated),
                "wins": seat_outcomes["win"],
                "ties": seat_outcomes["tie"],
                "losses": seat_outcomes["loss"],
                "mean_margin": statistics.fmean(game["margin"] for game in seated),
            }
    summary = {
        "schema_version": 1,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "agent_a": agents[0],
        "agent_b": agents[1],
        "seeds": seeds,
        "seat_swapped": not args.no_swap,
        "games": len(games),
        "wins": outcomes["win"],
        "ties": outcomes["tie"],
        "losses": outcomes["loss"],
        "win_rate": outcomes["win"] / len(games),
        "mean_margin": statistics.fmean(margins),
        "median_margin": statistics.median(margins),
        "status_counts": dict(Counter(status for game in games for status in game["statuses"])),
        "by_agent_a_seat": by_seat,
        "abnormal_games": [
            {"seed": game["seed"], "swap": game["swap"], "statuses": game["statuses"]}
            for game in games
            if game["statuses"] != ["DONE", "DONE"]
        ],
        "results": games,
    }
    rendered = json.dumps(summary, indent=2)
    print(rendered)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
