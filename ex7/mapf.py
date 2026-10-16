from __future__ import annotations

import argparse
import os
import random
import sys
import time
from collections import deque

from z3 import (And, AtMost, Bool, Implies, Int, Not, Or, Solver, is_true, sat, unsat)

MOVES = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]


class Instance:
    def __init__(self, name, W, H, obstacles, robots, horizon=None):
        self.name = name
        self.W, self.H = W, H
        self.obstacles = set(obstacles)
        self.robots = list(robots)
        self.horizon = horizon
        self.validate()

    def inside(self, c):
        return 0 <= c[0] < self.W and 0 <= c[1] < self.H

    def free(self, c):
        return self.inside(c) and c not in self.obstacles

    def free_cells(self):
        return [(x, y) for y in range(self.H) for x in range(self.W) if (x, y) not in self.obstacles]

    def adjacent(self, c):
        return [(c[0] + dx, c[1] + dy) for dx, dy in MOVES[1:] if self.free((c[0] + dx, c[1] + dy))]

    def edges(self):
        return [(u, v) for u in self.free_cells() for v in self.adjacent(u) if u < v]

    def bfs(self, src):
        dist = {src: 0}
        q = deque([src])
        while q:
            u = q.popleft()
            for v in self.adjacent(u):
                if v not in dist:
                    dist[v] = dist[u] + 1
                    q.append(v)
        return dist

    def lower_bound(self):
        lb = 0
        for _, s, g in self.robots:
            d = self.bfs(s)
            if g not in d:
                return None
            lb = max(lb, d[g])
        return lb

    def validate(self):
        if self.W <= 0 or self.H <= 0:
            raise ValueError("grid must be non-empty")
        for c in self.obstacles:
            if not self.inside(c):
                raise ValueError(f"obstacle {c} outside the grid")
        starts, goals = set(), set()
        for name, s, g in self.robots:
            for c in (s, g):
                if not self.free(c):
                    raise ValueError(f"robot {name}: cell {c} is not a free cell")
            if s in starts:
                raise ValueError(f"two robots start in {s}")
            if g in goals:
                raise ValueError(f"two robots have goal {g}")
            starts.add(s)
            goals.add(g)

    @staticmethod
    def parse(path):
        W = H = horizon = None
        obstacles, robots, rows = [], [], None
        with open(path, encoding="utf-8") as f:
            for raw in f:
                line = raw.split("#", 1)[0].strip() if rows is None else raw.rstrip("\n")
                if rows is not None:
                    if line.strip() == "end":
                        H = len(rows)
                        W = max(len(r) for r in rows)
                        obstacles += [(x, y) for y, r in enumerate(rows) for x, ch in enumerate(r) if ch != "."]
                        rows = None
                    elif line.strip():
                        rows.append(line.strip())
                    continue
                if not line:
                    continue
                key, *args = line.split()
                if key == "map":
                    rows = []
                elif key == "width":
                    W = int(args[0])
                elif key == "height":
                    H = int(args[0])
                elif key == "obstacle":
                    obstacles.append((int(args[0]), int(args[1])))
                elif key == "robot":
                    name, sx, sy, gx, gy = args
                    robots.append((name, (int(sx), int(sy)), (int(gx), int(gy))))
                elif key == "horizon":
                    horizon = int(args[0])
                else:
                    raise ValueError(f"unknown keyword {key!r} in {path}")
        if W is None or H is None:
            raise ValueError("grid size missing (use a map block or width/height)")
        name = os.path.splitext(os.path.basename(path))[0]
        return Instance(name, W, H, obstacles, robots, horizon)

    def to_text(self):
        lines = [f"# {self.name}: {self.W}x{self.H}, {len(self.robots)} robots, {len(self.obstacles)} obstacles", "map"]
        for y in range(self.H):
            lines.append("".join("#" if (x, y) in self.obstacles else "." for x in range(self.W)))
        lines.append("end")
        for name, s, g in self.robots:
            lines.append(f"robot {name} {s[0]} {s[1]} {g[0]} {g[1]}")
        if self.horizon is not None:
            lines.append(f"horizon {self.horizon}")
        return "\n".join(lines) + "\n"

    def ascii_map(self, plan=None, t=None):
        grid = [["#" if (x, y) in self.obstacles else "." for x in range(self.W)] for y in range(self.H)]
        for k, (name, s, g) in enumerate(self.robots):
            label = str(k + 1) if len(self.robots) < 10 else chr(ord("a") + k)
            if plan is None:
                grid[s[1]][s[0]] = label
                grid[g[1]][g[0]] = label.upper() if label.isalpha() else label
            else:
                x, y = plan[k][t]
                grid[y][x] = label
        return "\n".join("".join(r) for r in grid)


def generate_random(W, H, n, density, seed, name=None):
    rng = random.Random(seed)
    for _attempt in range(1000):
        cells = [(x, y) for y in range(H) for x in range(W)]
        obstacles = set(rng.sample(cells, int(round(density * W * H))))
        free = [c for c in cells if c not in obstacles]
        if len(free) < 2 * n:
            continue
        picks = rng.sample(free, 2 * n)
        robots = [(f"r{i + 1}", picks[2 * i], picks[2 * i + 1]) for i in range(n)]
        inst = Instance(name or f"random_{W}x{H}_n{n}_d{int(density * 100)}_s{seed}", W, H, obstacles, robots)
        if inst.lower_bound() is not None:
            return inst
    raise RuntimeError("could not generate a solvable instance")


class IntEncoding:
    name = "int"

    def __init__(self, inst, edge_constraint=True):
        self.inst = inst
        self.edge_constraint = edge_constraint
        self.solver = Solver()
        self.x, self.y = [], []
        self.T = -1

    def extend_to(self, T):
        while self.T < T:
            self._add_layer(self.T + 1)

    def _add_layer(self, t):
        inst, s = self.inst, self.solver
        n = len(inst.robots)
        xs = [Int(f"x_{i}_{t}") for i in range(n)]
        ys = [Int(f"y_{i}_{t}") for i in range(n)]
        self.x.append(xs)
        self.y.append(ys)
        for i, (_, (sx, sy), _) in enumerate(inst.robots):
            if t == 0:
                s.add(xs[i] == sx, ys[i] == sy)
            s.add(xs[i] >= 0, xs[i] < inst.W, ys[i] >= 0, ys[i] < inst.H)
            for ox, oy in inst.obstacles:
                s.add(Not(And(xs[i] == ox, ys[i] == oy)))
            if t > 0:
                px, py = self.x[t - 1][i], self.y[t - 1][i]
                s.add(Or([And(xs[i] == px + dx, ys[i] == py + dy) for dx, dy in MOVES]))
        for i in range(n):
            for j in range(i + 1, n):
                s.add(Or(xs[i] != xs[j], ys[i] != ys[j]))
                if t > 0 and self.edge_constraint:
                    px, py = self.x[t - 1], self.y[t - 1]
                    s.add(Not(And(px[i] == xs[j], py[i] == ys[j],
                                  px[j] == xs[i], py[j] == ys[i])))
        self.T = t

    def goal(self, T):
        return And([And(self.x[T][i] == gx, self.y[T][i] == gy)
                    for i, (_, _, (gx, gy)) in enumerate(self.inst.robots)])

    def decode(self, model, T):
        return [[(model[self.x[t][i]].as_long(), model[self.y[t][i]].as_long())
                 for t in range(T + 1)] for i in range(len(self.inst.robots))]


class BoolEncoding:
    name = "bool"

    def __init__(self, inst, edge_constraint=True):
        self.inst = inst
        self.edge_constraint = edge_constraint
        self.solver = Solver()
        self.cells = inst.free_cells()
        self.succ = {c: [c] + inst.adjacent(c) for c in self.cells}
        self.edge_list = inst.edges()
        self.at = []
        self.T = -1

    def extend_to(self, T):
        while self.T < T:
            self._add_layer(self.T + 1)

    def _add_layer(self, t):
        inst, s = self.inst, self.solver
        n = len(inst.robots)
        layer = [{c: Bool(f"at_{i}_{c[0]}_{c[1]}_{t}") for c in self.cells} for i in range(n)]
        self.at.append(layer)
        for i, (_, start, _) in enumerate(inst.robots):
            lits = list(layer[i].values())
            s.add(Or(lits))
            s.add(AtMost(*lits, 1))
            if t == 0:
                s.add(layer[i][start])
            else:
                prev = self.at[t - 1][i]
                for c in self.cells:
                    s.add(Implies(prev[c], Or([layer[i][d] for d in self.succ[c]])))
        if n > 1:
            for c in self.cells:
                s.add(AtMost(*[layer[i][c] for i in range(n)], 1))
            if t > 0 and self.edge_constraint:
                prev = self.at[t - 1]
                for u, v in self.edge_list:
                    u_to_v = Or([And(prev[i][u], layer[i][v]) for i in range(n)])
                    v_to_u = Or([And(prev[i][v], layer[i][u]) for i in range(n)])
                    s.add(Not(And(u_to_v, v_to_u)))
        self.T = t

    def goal(self, T):
        return And([self.at[T][i][g] for i, (_, _, g) in enumerate(self.inst.robots)])

    def decode(self, model, T):
        plan = []
        for i in range(len(self.inst.robots)):
            path = []
            for t in range(T + 1):
                here = [c for c in self.cells if is_true(model.eval(self.at[t][i][c], model_completion=True))]
                assert len(here) == 1, "exactly-one constraint violated in model"
                path.append(here[0])
            plan.append(path)
        return plan


ENCODINGS = {"int": IntEncoding, "bool": BoolEncoding}


def check_horizon(enc, T, timeout_ms=None, smt2_path=None):
    enc.extend_to(T)
    s = enc.solver
    if timeout_ms:
        s.set("timeout", timeout_ms)
    s.push()
    s.add(enc.goal(T))
    if smt2_path:
        with open(smt2_path, "w", encoding="utf-8") as f:
            f.write(f"; {enc.inst.name}: encoding {enc.name}, horizon T = {T}\n")
            f.write(s.to_smt2())
    t0 = time.time()
    res = s.check()
    elapsed = time.time() - t0
    plan = enc.decode(s.model(), T) if res == sat else None
    s.pop()
    return res, plan, elapsed


def solve_fixed(inst, T, encoding="int", edge_constraint=True, timeout_ms=None, smt2_path=None):
    enc = ENCODINGS[encoding](inst, edge_constraint)
    return check_horizon(enc, T, timeout_ms, smt2_path)


def min_makespan(inst, encoding="int", edge_constraint=True, max_T=60, incremental=True,
                 timeout_ms=None, log=print):
    lb = inst.lower_bound()
    history = []
    if lb is None:
        log("  some goal is unreachable: infeasible for every T")
        return None, None, history
    log(f"  lower bound from shortest paths: T >= {lb}")
    enc = ENCODINGS[encoding](inst, edge_constraint) if incremental else None
    for T in range(lb, max_T + 1):
        if not incremental:
            enc = ENCODINGS[encoding](inst, edge_constraint)
        res, plan, secs = check_horizon(enc, T, timeout_ms)
        history.append((T, res, secs))
        log(f"  T = {T:3d}: {str(res).upper():7s} ({secs:7.2f} s)")
        if res == sat:
            return T, plan, history
        if res != unsat:
            log("  solver gave up (timeout)")
            return None, None, history
    log(f"  no plan with T <= {max_T}")
    return None, None, history


def verify_plan(inst, plan, T, edge_constraint=True):
    errors = []
    n = len(inst.robots)
    for i, (name, s, g) in enumerate(inst.robots):
        path = plan[i]
        if len(path) != T + 1:
            errors.append(f"{name}: path has {len(path)} positions, expected {T + 1}")
            continue
        if path[0] != s:
            errors.append(f"(1) {name} starts in {path[0]} instead of {s}")
        if path[T] != g:
            errors.append(f"(2) {name} ends in {path[T]} instead of {g}")
        for t, c in enumerate(path):
            if not inst.inside(c):
                errors.append(f"(4) {name} leaves the grid at t={t}: {c}")
            elif c in inst.obstacles:
                errors.append(f"(5) {name} is in obstacle {c} at t={t}")
            if t > 0 and abs(c[0] - path[t - 1][0]) + abs(c[1] - path[t - 1][1]) > 1:
                errors.append(f"(3) {name} jumps {path[t - 1]} -> {c} at step {t}")
    for t in range(T + 1):
        for i in range(n):
            for j in range(i + 1, n):
                if plan[i][t] == plan[j][t]:
                    errors.append(f"(6) {inst.robots[i][0]} and {inst.robots[j][0]} both in {plan[i][t]} at t={t}")
                if (edge_constraint and t > 0 and plan[i][t - 1] != plan[j][t - 1]
                        and plan[i][t] == plan[j][t - 1] and plan[j][t] == plan[i][t - 1]):
                    errors.append(f"(7) {inst.robots[i][0]} and {inst.robots[j][0]} swap "
                                  f"{plan[i][t - 1]} <-> {plan[j][t - 1]} at step {t}")
    return errors


def format_plan(inst, plan, T):
    names = [r[0] for r in inst.robots]
    width = max(9, max(len(nm) for nm in names) + 2)
    out = ["t    " + "".join(f"{nm:<{width}}" for nm in names)]
    for t in range(T + 1):
        row = f"{t:<5d}"
        for i in range(len(names)):
            x, y = plan[i][t]
            cell = f"({x},{y})"
            if t > 0 and plan[i][t] == plan[i][t - 1]:
                cell += "*"
            row += f"{cell:<{width}}"
        out.append(row)
    out.append("(* = robot stayed in place during this step)")
    return "\n".join(out)


def draw_plan(inst, plan, T, path, title=None):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib import colormaps

    n = len(inst.robots)
    fig, ax = plt.subplots(figsize=(max(4, inst.W * 0.55), max(4, inst.H * 0.55)))
    for x, y in inst.obstacles:
        ax.add_patch(plt.Rectangle((x - 0.5, y - 0.5), 1, 1, color="black"))
    colors = colormaps["tab10"] if n <= 10 else colormaps["tab20"]
    for i, (name, s, g) in enumerate(inst.robots):
        col = colors(i % colors.N)
        off = (i - (n - 1) / 2) * min(0.08, 0.5 / max(n, 1))
        xs = [c[0] + off for c in plan[i]]
        ys = [c[1] + off for c in plan[i]]
        ax.plot(xs, ys, "-", color=col, linewidth=2, alpha=0.85)
        ax.plot(xs[0], ys[0], "o", color=col, markersize=11, markeredgecolor="black")
        ax.plot(xs[-1], ys[-1], "*", color=col, markersize=16, markeredgecolor="black")
        ax.annotate(name, (xs[0], ys[0]), textcoords="offset points", xytext=(5, 5), fontsize=8, color=col)
        for t in range(1, T + 1):
            if plan[i][t] != plan[i][t - 1]:
                ax.annotate(str(t), (xs[t], ys[t]), fontsize=6, color=col,
                            textcoords="offset points", xytext=(2, -8))
    ax.set_xlim(-0.5, inst.W - 0.5)
    ax.set_ylim(inst.H - 0.5, -0.5)
    ax.set_xticks(range(inst.W))
    ax.set_yticks(range(inst.H))
    ax.set_aspect("equal")
    ax.grid(True, color="lightgray", linewidth=0.5)
    ax.set_title(title or f"{inst.name}: T = {T}\n(o = start, * = goal, small numbers = time step of a move)",
                 fontsize=9)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Multi-robot warehouse planning (bounded MAPF) with z3.")
    ap.add_argument("instance", nargs="?", help="instance file")
    ap.add_argument("--T", type=int, help="planning horizon (default: the one in the file)")
    ap.add_argument("--min-makespan", action="store_true", help="search the smallest feasible horizon")
    ap.add_argument("--max-T", type=int, default=60, help="give up above this horizon (default 60)")
    ap.add_argument("--encoding", choices=ENCODINGS, default="int")
    ap.add_argument("--no-edge-constraint", action="store_true", help="drop constraint (7) (demonstration)")
    ap.add_argument("--no-incremental", action="store_true", help="fresh solver for every horizon")
    ap.add_argument("--timeout", type=float, default=None, help="per-check timeout in seconds")
    ap.add_argument("--smt2", help="write the SMT-LIB 2 formula of the (first) checked horizon to this file")
    ap.add_argument("--plot", help="save a drawing of the plan (PNG)")
    ap.add_argument("--plan-out", help="write the plan table to this file")
    ap.add_argument("--generate", nargs=5, metavar=("W", "H", "N", "DENSITY", "SEED"),
                    help="generate a random instance instead of reading one")
    ap.add_argument("--save", help="with --generate: write the instance to this file")
    args = ap.parse_args(argv)

    if args.generate:
        W, H, n, dens, seed = int(args.generate[0]), int(args.generate[1]), int(args.generate[2]), \
            float(args.generate[3]), int(args.generate[4])
        inst = generate_random(W, H, n, dens, seed)
        if args.save:
            with open(args.save, "w", encoding="utf-8") as f:
                f.write(inst.to_text())
            inst.name = os.path.splitext(os.path.basename(args.save))[0]
            print(f"instance written to {args.save}")
        if not (args.min_makespan or args.T):
            print(inst.to_text())
            return
    elif args.instance:
        inst = Instance.parse(args.instance)
    else:
        ap.error("an instance file or --generate is required")

    edge = not args.no_edge_constraint
    timeout_ms = int(args.timeout * 1000) if args.timeout else None
    print(f"instance {inst.name}: {inst.W}x{inst.H} grid, {len(inst.obstacles)} obstacles, "
          f"{len(inst.robots)} robots, encoding = {args.encoding}"
          + ("" if edge else ", WITHOUT edge-collision constraint (7)"))
    print(inst.ascii_map())
    print()

    if args.min_makespan:
        print("minimum makespan search:")
        T, plan, _ = min_makespan(inst, args.encoding, edge, args.max_T, not args.no_incremental, timeout_ms)
        if T is None:
            return
        print(f"minimum makespan: T = {T}")
    else:
        T = args.T if args.T is not None else inst.horizon
        if T is None:
            ap.error("no horizon given (use --T or a 'horizon' line in the instance)")
        res, plan, secs = solve_fixed(inst, T, args.encoding, edge, timeout_ms, args.smt2)
        print(f"T = {T}: {str(res).upper()}  ({secs:.2f} s)")
        if args.smt2:
            print(f"SMT-LIB formula written to {args.smt2}")
        if res != sat:
            if res == unsat:
                print(f"UNSAT for T = {T}: no collision-free plan within {T} steps")
            return

    print()
    table = format_plan(inst, plan, T)
    print(table)
    errors = verify_plan(inst, plan, T, edge_constraint=True)
    print("independent check of constraints (1)-(7): " + ("OK, plan is valid" if not errors else "VIOLATIONS"))
    for e in errors:
        print("   " + e)
    if args.plan_out:
        with open(args.plan_out, "w", encoding="utf-8") as f:
            f.write(f"{inst.name}: T = {T}\n{table}\n")
    if args.plot:
        draw_plan(inst, plan, T, args.plot)
        print(f"drawing saved to {args.plot}")


if __name__ == "__main__":
    main()
