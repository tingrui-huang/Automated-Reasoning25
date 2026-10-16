"""
Exercise 7 -- runtime experiments for the multi-robot warehouse planner.

Table 1: random instances of growing size (grid, robots, obstacle density);
         minimum-makespan search with the integer encoding and with the
         propositional encoding.  The generated instances are stored in
         instances/random/ so that every number can be reproduced with
             python mapf.py instances/random/<name>.txt --min-makespan [--encoding bool]
Table 2: incremental solving (one solver, push/pop of the goal constraint)
         versus a fresh solver per horizon, on the hand-made instances.

Usage:  python experiments.py [--seeds 1 2 3] [--timeout 120] [--out experiments.md]
"""
import argparse
import functools
import os
import time

print = functools.partial(print, flush=True)      # show progress even when redirected to a file

from mapf import Instance, generate_random, min_makespan

HERE = os.path.dirname(os.path.abspath(__file__))

# (W, H, robots, obstacle density)
CONFIGS = [
    (8, 8, 2, 0.10),
    (8, 8, 4, 0.10),
    (12, 12, 6, 0.20),
    (16, 16, 10, 0.20),
    (16, 16, 14, 0.20),
    (20, 20, 12, 0.25),
]


def run(inst, encoding, timeout_ms, incremental=True):
    t0 = time.time()
    T, _plan, history = min_makespan(inst, encoding, True, max_T=200, incremental=incremental,
                                     timeout_ms=timeout_ms, log=lambda *_: None)
    total = time.time() - t0
    solver_time = sum(h[2] for h in history)
    return T, len(history), solver_time, total


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, nargs="+", default=[1])
    ap.add_argument("--timeout", type=float, default=120.0, help="per check, seconds")
    ap.add_argument("--out", default=os.path.join(HERE, "experiments.md"))
    ap.add_argument("--skip-table2", action="store_true")
    args = ap.parse_args()
    timeout_ms = int(args.timeout * 1000)
    os.makedirs(os.path.join(HERE, "instances", "random"), exist_ok=True)

    lines = ["# Runtime experiments (exercise 7)", "",
             f"Per-check timeout: {args.timeout:.0f} s.  Times are summed over all horizons of the "
             "minimum-makespan search (lower bound LB from BFS up to the first SAT horizon).",
             "", "## Table 1: random instances, integer vs. propositional encoding", "",
             "'solver' = z3 solver time (check() calls only); 'total' = wall-clock time of the whole search "
             "including the construction of the formula, so total - solver = encoding time.",
             "",
             "| instance | grid | robots | obstacles | LB | min T | #checks | int: solver / total | bool: solver / total |",
             "|---|---|---:|---:|---:|---:|---:|---:|---:|"]
    print("\n".join(lines[-2:]))
    for (W, H, n, dens) in CONFIGS:
        for seed in args.seeds:
            inst = generate_random(W, H, n, dens, seed)
            path = os.path.join(HERE, "instances", "random", inst.name + ".txt")
            with open(path, "w", encoding="utf-8") as f:
                f.write(inst.to_text())
            lb = inst.lower_bound()
            res = {}
            for enc in ("int", "bool"):
                res[enc] = run(inst, enc, timeout_ms)
            T_int, checks, t_int, w_int = res["int"]
            T_bool, _, t_bool, w_bool = res["bool"]
            fmt = lambda T, t, w: (f"{t:.2f} s / {w:.2f} s" if T is not None else f"timeout (> {t:.0f} s)")
            minT = T_int if T_int is not None else T_bool
            row = (f"| {inst.name} | {W}x{H} | {n} | {len(inst.obstacles)} ({int(dens * 100)}%) | {lb} | "
                   f"{minT if minT is not None else '?'} | {checks} | {fmt(T_int, t_int, w_int)} | "
                   f"{fmt(T_bool, t_bool, w_bool)} |")
            if T_int is not None and T_bool is not None and T_int != T_bool:
                row += "  **mismatch!**"
            print(row)
            lines.append(row)

    if not args.skip_table2:
        lines += ["", "## Table 2: incremental vs. fresh solver per horizon (integer encoding)", "",
                  "| instance | LB | min T | #checks | incremental: solver / total | fresh solver per T: solver / total |",
                  "|---|---:|---:|---:|---:|---:|"]
        print("\n".join(lines[-2:]))
        for name in ("example", "corridor", "warehouse"):
            inst = Instance.parse(os.path.join(HERE, "instances", name + ".txt"))
            T1, checks, t_inc, w_inc = run(inst, "int", timeout_ms, incremental=True)
            T2, _, t_fresh, w_fresh = run(inst, "int", timeout_ms, incremental=False)
            assert T1 == T2
            row = (f"| {name} | {inst.lower_bound()} | {T1} | {checks} | {t_inc:.2f} s / {w_inc:.2f} s | "
                   f"{t_fresh:.2f} s / {w_fresh:.2f} s |")
            print(row)
            lines.append(row)

    with open(args.out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"\nwritten to {args.out}")


if __name__ == "__main__":
    main()
