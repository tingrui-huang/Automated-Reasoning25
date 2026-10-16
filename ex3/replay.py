import re
import sys

from food_supply import EDGES, STORAGE, INIT_STOCK, NAMES, VILLAGES, S

ROAD = {(u, v): w for (u, v, w) in EDGES}
STEP = re.compile(r"step\s+(\d+): t=\s*(\d+)\s+at ([SABC])\s+load=\s*(\d+)\s+A=\s*(\d+) B=\s*(\d+) C=\s*(\d+)"
                  r"(?:\s+\(moved\s+(\d+), delivered\s+(\d+)\))?(.*)")


def check_schedule(rows, cap, name):
    errors = []
    loop_start = None
    prev = None
    for (i, t, loc, load, stocks, moved, delivered, mark) in rows:
        if i == 0:
            if not (loc == S and load == cap and t == 0 and all(s == INIT_STOCK for s in stocks)):
                errors.append("wrong initial state")
        else:
            pi, pt, ploc, pload, pstocks = prev
            if ROAD.get((ploc, loc)) != moved:
                errors.append(f"step {i}: no road {NAMES[ploc]}->{NAMES[loc]} of duration {moved}")
            if t != pt + moved:
                errors.append(f"step {i}: time {t} != {pt} + {moved}")
            for v, ps in zip(VILLAGES, pstocks):
                if ps - moved < 0:
                    errors.append(f"step {i}: village {NAMES[v]} runs dry on the road")
            if loc == S:
                if delivered != 0 or load != cap:
                    errors.append(f"step {i}: at S the truck must deliver 0 and reload to {cap}")
                expect = [ps - moved for ps in pstocks]
            else:
                if delivered > pload or load != pload - delivered:
                    errors.append(f"step {i}: delivered {delivered} with load {pload} -> {load}")
                expect = [ps - moved + (delivered if v == loc else 0) for v, ps in zip(VILLAGES, pstocks)]
            if list(stocks) != expect:
                errors.append(f"step {i}: stocks {stocks} != expected {expect}")
            for v, s in zip(VILLAGES, stocks):
                if s > STORAGE[v]:
                    errors.append(f"step {i}: stock of {NAMES[v]} = {s} exceeds capacity {STORAGE[v]}")
        if "loop starts here" in mark:
            loop_start = (loc, load, tuple(stocks), t)
        prev = (i, t, loc, load, stocks)
    i, t, loc, load, stocks = prev
    survival = t + min(stocks)
    msg = f"{name}: {i} moves, last arrival t={t}, first village runs dry at t={survival}"
    if loop_start is not None:
        lloc, lload, lstocks, lt = loop_start
        if (lloc, lload, lstocks) == (loc, load, tuple(stocks)):
            msg += f"; loop state repeats, period {t - lt}"
        else:
            errors.append("state at loop start differs from final state")
    return msg, errors


def main(path="output.txt"):
    blocks, current, title, cap = [], [], None, None
    for line in open(path, encoding="utf-8"):
        if line.startswith("==="):
            cap = int(re.search(r"capacity (\d+)", line).group(1))
        m = STEP.search(line)
        if m:
            g = m.groups()
            row = (int(g[0]), int(g[1]), NAMES.index(g[2]), int(g[3]), (int(g[4]), int(g[5]), int(g[6])),
                   int(g[7]) if g[7] else None, int(g[8]) if g[8] else None, g[9])
            if row[0] == 0 and current:
                blocks.append((title, cur_cap, current))
                current = []
            if row[0] == 0:
                cur_cap = cap
                title = f"schedule #{len(blocks) + 1} (capacity {cap})"
            current.append(row)
    if current:
        blocks.append((title, cur_cap, current))
    ok = True
    for title, cap, rows in blocks:
        msg, errors = check_schedule(rows, cap, title)
        print(msg, "-> OK" if not errors else "-> ERRORS")
        for e in errors:
            print("   ", e)
        ok &= not errors
    return ok


if __name__ == "__main__":
    sys.exit(0 if main(*sys.argv[1:]) else 1)
