from z3 import *
import time

S, A, B, C = 0, 1, 2, 3
NAMES = "SABC"
VILLAGES = (A, B, C)

EDGES = [
    (S, A, 15), (A, S, 15),
    (S, C, 15), (C, S, 15),
    (A, C, 12), (C, A, 12),
    (A, B, 17), (B, A, 17),
    (B, C, 13),
    (C, B, 9),
]
STORAGE = {A: 90, B: 120, C: 90}
INIT_STOCK = 60


def unfold(n, cap):
    loc  = [Int(f"loc_{i}")  for i in range(n + 1)]
    load = [Int(f"load_{i}") for i in range(n + 1)]
    t    = [Int(f"t_{i}")    for i in range(n + 1)]
    st   = {v: [Int(f"{NAMES[v]}_{i}") for i in range(n + 1)] for v in VILLAGES}
    d    = [Int(f"d_{i}") for i in range(n)]
    x    = [Int(f"x_{i}") for i in range(n)]

    cons = [loc[0] == S, load[0] == cap, t[0] == 0]
    cons += [st[v][0] == INIT_STOCK for v in VILLAGES]

    for i in range(n):
        cons.append(Or([And(loc[i] == u, loc[i + 1] == v, d[i] == w) for (u, v, w) in EDGES]))
        cons.append(t[i + 1] == t[i] + d[i])

        cons += [st[v][i] - d[i] >= 0 for v in VILLAGES]

        cons += [x[i] >= 0, x[i] <= load[i]]
        cons.append(Implies(loc[i + 1] == S, And(load[i + 1] == cap, x[i] == 0)))
        cons.append(Implies(loc[i + 1] != S, load[i + 1] == load[i] - x[i]))
        for v in VILLAGES:
            cons.append(Implies(loc[i + 1] == v,
                                And(st[v][i + 1] == st[v][i] - d[i] + x[i],
                                    st[v][i + 1] <= STORAGE[v])))
            cons.append(Implies(loc[i + 1] != v, st[v][i + 1] == st[v][i] - d[i]))

    return cons, dict(loc=loc, load=load, t=t, st=st, d=d, x=x)


def print_schedule(m, V, n, j=None):
    for i in range(n + 1):
        row = (f"  step {i:2d}: t={m[V['t'][i]].as_long():4d}  at {NAMES[m[V['loc'][i]].as_long()]}  "
               f"load={m[V['load'][i]].as_long():3d}  "
               f"A={m[V['st'][A][i]].as_long():3d} B={m[V['st'][B][i]].as_long():3d} C={m[V['st'][C][i]].as_long():3d}")
        if i > 0:
            row += f"   (moved {m[V['d'][i-1]].as_long():2d}, delivered {m[V['x'][i-1]].as_long():3d})"
        if j is not None and i == j:
            row += "   <-- loop starts here"
        print(row)


def part_a(cap=130, max_n=60):
    print(f"=== (a) capacity {cap}: how long can the villages survive? ===")
    surv = Int("surv")
    best = None
    for n in range(1, max_n + 1):
        cons, V = unfold(n, cap)
        o = Optimize()
        o.add(cons)
        o.add([surv <= V["t"][n] + V["st"][v][n] for v in VILLAGES])
        h = o.maximize(surv)
        t0 = time.time()
        r = o.check()
        if r != sat:
            print(f"  n = {n:2d} moves: UNSAT  ({time.time() - t0:.1f}s)  -> no schedule with {n} or more moves exists")
            break
        T = o.upper(h).as_long()
        print(f"  n = {n:2d} moves: max survival time = {T}  ({time.time() - t0:.1f}s)")
        if best is None or T > best[0]:
            best = (T, n, o.model(), V)
    T, n, m, V = best
    print(f"\n  RESULT (a): the villages can be kept alive for at most {T} time units "
          f"(schedule with {n} moves); no schedule survives longer.")
    print("  witness schedule:")
    print_schedule(m, V, n)
    return T


def same_state(V, j, n):
    return And(V["loc"][j] == V["loc"][n],
               V["load"][j] == V["load"][n],
               *[V["st"][v][j] == V["st"][v][n] for v in VILLAGES])


def part_b(cap=150, max_n=20):
    print(f"\n=== (b) capacity {cap}: sustain forever (find a repeated state) ===")

    for n in range(1, max_n + 1):
        cons, V = unfold(n, cap)
        s = Solver(); s.add(cons)
        s.add(Or([same_state(V, j, n) for j in range(n)]))
        if s.check() == sat:
            m = s.model()
            j = next(jj for jj in range(n) if is_true(m.eval(same_state(V, jj, n))))
            print(f"  fewest moves: n = {n} (loop from step {j} to {n}, "
                  f"period {m[V['t'][n]].as_long() - m[V['t'][j]].as_long()} time units)")
            print_schedule(m, V, n, j)
            break
    else:
        print("  no lasso found up to", max_n)
        return

    best = None
    for n in range(1, max_n + 1):
        cons, V = unfold(n, cap)
        o = Optimize(); o.add(cons)
        jj = Int("jj"); period = Int("period")
        o.add(Or([And(jj == j, same_state(V, j, n), period == V["t"][n] - V["t"][j]) for j in range(n)]))
        h = o.minimize(period)
        t0 = time.time()
        if o.check() != sat:
            print(f"  n = {n:2d}: no lasso  ({time.time() - t0:.1f}s)")
            continue
        m = o.model(); P = m[period].as_long(); j = m[jj].as_long()
        print(f"  n = {n:2d}: shortest period = {P} (loop {j}..{n}, {n - j} moves)  ({time.time() - t0:.1f}s)")
        if best is None or P < best[0] or (P == best[0] and n - j < best[1] - best[2]):
            best = (P, n, j, m, V)
    P, n, j, m, V = best
    print(f"\n  RESULT (b): shortest sustainable loop has period {P} time units "
          f"({n - j} moves, reached after a prefix of {j} moves)")
    print_schedule(m, V, n, j)


if __name__ == "__main__":
    t0 = time.time()
    part_a(130)
    print(f"\n  [(a) took {time.time() - t0:.1f}s]")
    t0 = time.time()
    part_b(150)
    print(f"\n  [(b) took {time.time() - t0:.1f}s]")
