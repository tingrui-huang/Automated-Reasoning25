import time

from z3 import And, Optimize, sat

from food_supply import unfold, same_state, VILLAGES, STORAGE

CAP = 150
best = None
for n in range(1, 11):
    cons, V = unfold(n, CAP)
    cons = cons[6:]
    o = Optimize()
    o.add(cons)
    o.add(V["t"][0] == 0, V["loc"][0] >= 0, V["loc"][0] <= 3, V["load"][0] >= 0, V["load"][0] <= CAP)
    o.add([And(V["st"][v][0] >= 0, V["st"][v][0] <= STORAGE[v]) for v in VILLAGES])
    o.add(same_state(V, 0, n))
    o.minimize(V["t"][n])
    t0 = time.time()
    r = o.check()
    if r == sat:
        p = o.model()[V["t"][n]].as_long()
        print(f"n = {n:2d} moves: shortest cycle period = {p:3d}   ({time.time() - t0:.1f}s)")
        best = p if best is None else min(best, p)
    else:
        print(f"n = {n:2d} moves: no cycle                       ({time.time() - t0:.1f}s)")
print(f"\nshortest period of any cycle with <= 10 moves (hence of any cycle with period < 99): {best}")
