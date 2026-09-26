"""
Exercise 5 -- Configurable Systems (BDD-based minimum valid configurations)

Requires: pip install oxidd
Tested against oxidd 0.12.0 (BDDManager / BDDFunction API).
"""

from __future__ import annotations
import re
import time
from pathlib import Path

from oxidd.bdd import BDDManager, BDDFunction


# ---------------------------------------------------------------------------
# 1. DIMACS parsing
# ---------------------------------------------------------------------------

def parse_dimacs(path: str):
    """Parse a DIMACS CNF file.

    Returns:
        n_vars:   number of features (1-indexed in the file)
        clauses:  list[list[int]] of clauses, each a list of signed literals
                  (positive i means feature i selected, negative means i not selected)
        var_order: list[int] | None -- the order given by a 'c vo ...' line,
                   as feature numbers (1-indexed), topmost first; None if absent
    """
    n_vars = None
    clauses: list[list[int]] = []
    var_order = None

    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith("c vo"):
                var_order = [int(t) for t in line.split()[2:]]
                continue
            if line.startswith("c"):
                continue
            if line.startswith("p"):
                # p cnf n_vars n_clauses
                parts = line.split()
                n_vars = int(parts[2])
                continue
            # a clause line: space separated ints ending in 0
            lits = [int(t) for t in line.split()]
            assert lits[-1] == 0
            clauses.append(lits[:-1])

    if n_vars is None:
        raise ValueError("No 'p cnf ...' header line found")
    return n_vars, clauses, var_order


# ---------------------------------------------------------------------------
# 2. Build the BDD for phi from the parsed CNF
# ---------------------------------------------------------------------------

def build_phi(manager: BDDManager, n_vars: int, clauses: list[list[int]],
              var_order: list[int] | None):
    """Create n_vars BDD variables (in var_order if given, else natural order)
    and conjoin the clause BDDs into a single BDD representing phi.

    Returns:
        phi:      BDDFunction for the CNF
        var_of:   dict feature_number (1-indexed, as in DIMACS) -> variable number (0-indexed, oxidd)
    """
    order = var_order if var_order is not None else list(range(1, n_vars + 1))
    assert sorted(order) == list(range(1, n_vars + 1)), "var order must be a permutation of 1..n"

    varnums = list(manager.add_vars(n_vars))
    # order[0] should end up as the top-most variable
    var_of = {feature: varnums[i] for i, feature in enumerate(order)}

    phi = manager.true()
    for clause in clauses:
        clause_bdd = manager.false()
        for lit in clause:
            feature = abs(lit)
            f = manager.var(var_of[feature])
            lit_bdd = f if lit > 0 else ~f
            clause_bdd = clause_bdd | lit_bdd
        phi = phi & clause_bdd

    return phi, var_of


# ---------------------------------------------------------------------------
# 3. Weighted DP over the (reduced, shared) BDD: minimum number of selected
#    features among all satisfying assignments.
# ---------------------------------------------------------------------------

INF = float("inf")


def min_weight(f: BDDFunction) -> tuple[float, dict]:
    """Returns (w*, memo) where w* = minimum Hamming weight (#selected features)
    among satisfying assignments of f, and memo is the weight memo table
    (reusable for reading off a witness).

    Implemented iteratively with an explicit stack (post-order DFS) rather
    than plain recursion: a BDD's longest root-to-terminal path can be as
    long as the number of variables, which for real instances (thousands of
    features) exceeds Python's default recursion limit and -- because each
    call also crosses into the Rust extension -- naively raising the
    recursion limit risks a hard crash instead of a clean error.
    """
    memo: dict[BDDFunction, float] = {}
    stack = [f]
    while stack:
        g = stack[-1]
        if g in memo:
            stack.pop()
            continue
        if not g.satisfiable():
            memo[g] = INF
            stack.pop()
            continue
        if g.valid():           # always true: 0 more features needed
            memo[g] = 0.0
            stack.pop()
            continue
        lo = g.cofactor_false()
        hi = g.cofactor_true()
        if lo not in memo:
            stack.append(lo)
            continue
        if hi not in memo:
            stack.append(hi)
            continue
        memo[g] = min(memo[lo], 1.0 + memo[hi])
        stack.pop()

    return memo[f], memo


def witness_min_config(f: BDDFunction, memo: dict) -> set:
    """Walk the BDD following the branch that achieves the minimum weight,
    returning the set of oxidd variable numbers set to 1 in some cmin."""
    selected = set()
    g = f
    while True:
        if g.valid() or not g.satisfiable():
            break
        var = g.node_var()
        hi, lo = g.cofactors()  # cofactors() returns (f_true, f_false)
        w_lo = memo[lo] if lo in memo else min_weight(lo)[0]
        w_hi = memo[hi] if hi in memo else min_weight(hi)[0]
        if w_lo <= 1 + w_hi:
            g = lo  # set var = 0
        else:
            g = hi  # set var = 1
            selected.add(var)
    return selected


# ---------------------------------------------------------------------------
# 4. Cardinality-constraint BDD: exactly k of the given variables are true
# ---------------------------------------------------------------------------

def cardinality_exactly_k(manager: BDDManager, varnums: list[int], k: int) -> BDDFunction:
    """Build the BDD for 'exactly k of varnums are true', bottom-up.

    Built iteratively (i from n down to 0) instead of via recursion on i,
    for the same recursion-depth reason as min_weight above: n can be in
    the thousands.
    """
    n = len(varnums)
    # table[remaining] = BDD for 'exactly `remaining` of varnums[i:] are true'
    table = {remaining: (manager.true() if remaining == 0 else manager.false())
             for remaining in range(0, k + 1)}

    for i in range(n - 1, -1, -1):
        v = manager.var(varnums[i])
        new_table = {}
        for remaining in range(0, k + 1):
            then_branch = table[remaining - 1] if remaining >= 1 else manager.false()
            else_branch = table[remaining]
            new_table[remaining] = v.ite(then_branch, else_branch)
        table = new_table

    return table[k]


# ---------------------------------------------------------------------------
# 5. Putting it together: analyse one DIMACS system
# ---------------------------------------------------------------------------

def analyse_system(path: str, essential_features: list[int] | None = None):
    t0 = time.time()
    n_vars, clauses, var_order = parse_dimacs(path)

    manager = BDDManager(1 << 22, 1 << 20, 1)
    phi, var_of = build_phi(manager, n_vars, clauses, var_order)

    results = {}
    results["n_vars"] = n_vars
    results["bdd_nodes_phi"] = phi.node_count()                 # (i)
    results["num_valid_configs"] = phi.sat_count(n_vars)          # (ii)

    w_star, memo = min_weight(phi)
    results["min_config_size"] = w_star                          # (iii)

    if essential_features:
        varnums_S = [var_of[feat] for feat in essential_features]
        sub = phi.make_substitution([(v, manager.true()) for v in varnums_S])
        phi_S = phi.substitute(sub)
        if not phi_S.satisfiable():
            results["min_config_size_S"] = None  # no valid config contains S
        else:
            w_S, _ = min_weight(phi_S)
            results["min_config_size_S"] = len(essential_features) + w_S   # (iv)

    all_varnums = list(var_of.values())
    card_bdd = cardinality_exactly_k(manager, all_varnums, int(w_star))
    min_configs_bdd = phi & card_bdd
    results["bdd_nodes_min_configs"] = min_configs_bdd.node_count()        # (v)
    results["num_min_configs"] = min_configs_bdd.sat_count(n_vars)         # (vi)

    results["runtime_sec"] = time.time() - t0
    return results


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("usage: python configurable_systems.py <dimacs_file> [feat1 feat2 ...]")
        sys.exit(1)
    essentials = [int(x) for x in sys.argv[2:]] or None
    r = analyse_system(sys.argv[1], essentials)
    for k, v in r.items():
        print(f"{k}: {v}")