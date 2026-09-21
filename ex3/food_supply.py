"""
Exercise 3 -- Food Supply (bounded model checking with z3).

Model
-----
A schedule is a sequence of moves of the truck along the edges of the graph.
Step i (i = 0..n-1) moves the truck from loc_i to loc_{i+1}; this takes d_i time
units, during which every village consumes d_i packages.  On arrival the truck
delivers x_i packages (only at a village; at S it is refilled to `cap`).

State after step i:  loc_i, load_i, t_i (time), A_i, B_i, C_i (stocks after delivery).

Constraints per step:
  * (loc_i, loc_{i+1}, d_i) is an edge of the graph
  * t_{i+1} = t_i + d_i
  * A_i - d_i >= 0  (and B, C): nobody runs dry while the truck is on the road
    (stocks only decrease between two arrivals, so checking at arrivals suffices)
  * 0 <= x_i <= load_i, delivered village stays <= its storage capacity
  * load_{i+1} = cap if loc_{i+1} = S, else load_i - x_i

(a) maximise  surv = t_n + min(A_n, B_n, C_n)  (the moment the first village runs
    dry if the truck stops after n moves) for n = 1, 2, ...  As soon as the
    n-step unfolding is UNSAT, no schedule with >= n moves exists, so the maximum
    over smaller n is the true optimum -- and "forever" is impossible.

(b) sustain forever  <=>  some state repeats:  exists j < n with state_j = state_n
    (hint of the exercise: path v -> w plus a non-empty path w -> w).
    The loop j..n can then be repeated indefinitely.  We minimise its period.
"""
from z3 import *
import time

# ---------------------------------------------------------------------------
# Problem data
# ---------------------------------------------------------------------------
S, A, B, C = 0, 1, 2, 3
NAMES = "SABC"
VILLAGES = (A, B, C)

# (from, to, travel time incl. loading/delivering)
EDGES = [
    (S, A, 15), (A, S, 15),
    (S, C, 15), (C, S, 15),
    (A, C, 12), (C, A, 12),
    (A, B, 17), (B, A, 17),
    (B, C, 13),            # B -> C is slower (traffic)
    (C, B, 9),
]
STORAGE = {A: 90, B: 120, C: 90}
INIT_STOCK = 60


# ---------------------------------------------------------------------------
# Bounded unfolding: n steps, truck capacity cap
# ---------------------------------------------------------------------------
def unfold(n, cap):
    loc  = [Int(f"loc_{i}")  for i in range(n + 1)]   # 0..3
    load = [Int(f"load_{i}") for i in range(n + 1)]   # food on the truck
    t    = [Int(f"t_{i}")    for i in range(n + 1)]   # time of arrival at loc_i
    st   = {v: [Int(f"{NAMES[v]}_{i}") for i in range(n + 1)] for v in VILLAGES}
    d    = [Int(f"d_{i}") for i in range(n)]          # duration of step i
    x    = [Int(f"x_{i}") for i in range(n)]          # amount delivered at end of step i

    cons = [loc[0] == S, load[0] == cap, t[0] == 0]
    cons += [st[v][0] == INIT_STOCK for v in VILLAGES]

    for i in range(n):
        # choose an edge
        cons.append(Or([And(loc[i] == u, loc[i + 1] == v, d[i] == w) for (u, v, w) in EDGES]))
        cons.append(t[i + 1] == t[i] + d[i])

        # nobody starves while the truck is on the road
        cons += [st[v][i] - d[i] >= 0 for v in VILLAGES]

        # delivery / reload
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


# ---------------------------------------------------------------------------
# (a) capacity 130: maximal survival time
# ---------------------------------------------------------------------------
def part_a(cap=130, max_n=60):
    print(f"=== (a) capacity {cap}: how long can the villages survive? ===")
    surv = Int("surv")          # moment at which the first village runs dry
    best = None                 # (T, n, model, V)
    for n in range(1, max_n + 1):
        cons, V = unfold(n, cap)
        o = Optimize()
        o.add(cons)
        o.add([surv <= V["t"][n] + V["st"][v][n] for v in VILLAGES])
        h = o.maximize(surv)
        t0 = time.time()
        r = o.check()
        if r != sat:
            # no schedule of n moves keeps everybody alive  =>  no schedule has >= n moves
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


# ---------------------------------------------------------------------------
# (b) capacity 150: find a lasso  (prefix 0..j, loop j..n with state_j == state_n)
# ---------------------------------------------------------------------------
def same_state(V, j, n):
    return And(V["loc"][j] == V["loc"][n],
               V["load"][j] == V["load"][n],
               *[V["st"][v][j] == V["st"][v][n] for v in VILLAGES])


def part_b(cap=150, max_n=20):
    print(f"\n=== (b) capacity {cap}: sustain forever (find a repeated state) ===")

    # 1. fewest moves in total (prefix + loop)
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

    # 2. shortest loop period (time units), over all lassos with at most max_n moves
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
