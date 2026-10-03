import time
import sys

from oxidd.bdd import BDDManager, BDDFunction

INF = float("inf")

def parse_dimacs(path: str):
    n = 0
    clauses = []
    order = None

    for line in open(path, "r"):
        line = line.strip()
        if line.startswith("c vo"):
            order = [int(t) for t in line.split()[2:]]
        elif line.startswith("p"):
            n = int(line.split()[2])
        elif line and not line.startswith("c"):
            lits = [int(t) for t in line.split()]
            clauses.append(lits[:-1]) #drop trailing 0
    return n, clauses, order

def build_phi(m, n, clauses, order):
    if order is None:
        order = list(range(1, n + 1))
    vs = list(m.add_vars(n))
    var_of = {feature: vs[i] for i, feature in enumerate(order)}

    phi = m.true()
    for clause in clauses:
        c = m.false()
        for lit in clause:
            v = m.var(var_of[abs(lit)])
            c = c | (v if lit > 0 else ~v)
        phi = phi & c
    return phi, var_of


def min_weight(m, f, memo):
    # min num of true variables over satisfying assignments of f
    # iterative because the BDD can be thousands of levels deep and recursive failed for the big dimacs input
    # memo can be shared between calls
    memo.setdefault(m.true(), 0)
    memo.setdefault(m.false(), INF)
    stack = [f]
    while stack:
        g = stack[-1]
        if g in memo:
            stack.pop()
            continue
        lo = g.cofactor_false()
        hi = g.cofactor_true()
        if lo not in memo:
            stack.append(lo)
        elif hi not in memo:
            stack.append(hi)
        else:
            memo[g] = min(memo[lo], 1.0 + memo[hi])
            stack.pop()
    return memo[f]


def exactly_k(m, vs, k):
    # table[r] = BDD for "exactly r of the remaining vars are true"
    table = [m.true() if r == 0 else m.false() for r in range(k + 1)]
    for v in reversed(vs):
        x = m.var(v)
        new = []
        for r in range(k + 1):
            yes = table[r - 1] if r > 0 else m.false()
            new.append(x.ite(yes, table[r]))
        table = new
    return table[k]

def analyse(path, essential=None):
    start = time.time()
    n, clauses, order = parse_dimacs(path)
    m = BDDManager(1 << 22, 1 << 20, 1)
    phi, var_of = build_phi(m, n, clauses, order)
 
    res = {"features": n}
    res["nodes_phi"] = phi.node_count()
    res["num_configs"] = phi.sat_count(n)
 
    memo = {}
    w = min_weight(m, phi, memo)
    res["min_size"] = w
 
    if essential:
        cube = m.true()
        for feat in essential:
            cube = cube & m.var(var_of[feat])
        phi_s = phi & cube
        # essential vars are still in phi_s, so they are already counted
        res["min_size_S"] = None if phi_s == m.false() else min_weight(m, phi_s, memo)
 
    card = exactly_k(m, list(var_of.values()), int(w))
    mins = phi & card
    res["nodes_min_configs"] = mins.node_count()
    res["num_min_configs"] = mins.sat_count(n)
 
    res["seconds"] = round(time.time() - start, 2)
    return res

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python conf_systems.py file.dimacs [essential features...]")
        sys.exit(1)

    ess = [int(x) for x in sys.argv[2:]] or None
    for key, val in analyse(sys.argv[1], ess).items():
        print(key, val)