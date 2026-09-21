import matplotlib.pyplot as plt
import matplotlib.patches as patches
from z3 import *


def z3_to_float(v):
    v = simplify(v)
    if is_int_value(v):
        return float(v.as_long())
    if is_rational_value(v):
        return v.numerator_as_long() / v.denominator_as_long()
    value = v.as_decimal(20)
    if value.endswith("?"):
        value = value[:-1]
    return float(value)


def solve_pcb(added_cameras=0, draw=False):
    N = 14
    W = [5, 5, 4, 4, 5, 3, 7, 6, 6, 4, 6, 5, 6, 5]
    H = [6, 6, 6, 10, 7, 7, 7, 10, 12, 10, 9, 11, 10, 10]
    HOT = [True, True, False, False, False, True, False, False, False, False, False, False, False, False]

    solver = Solver()

    x = [Real(f"x_{i}") for i in range(N)]
    y = [Real(f"y_{i}") for i in range(N)]
    w = [Int(f"w_{i}") for i in range(N)]
    h = [Int(f"h_{i}") for i in range(N)]
    board = [Int(f"board_{i}") for i in range(N)]

    cam_x_start = 22 - (7 + 4 * added_cameras)

    for i in range(N):
        solver.add(Or(
            And(w[i] == W[i], h[i] == H[i]),
            And(w[i] == H[i], h[i] == W[i])
        ))

        solver.add(Or(board[i] == 1, board[i] == 2))

        solver.add(Implies(board[i] == 1, And(
            x[i] >= 0, y[i] >= 0,
            x[i] + w[i] <= 20, y[i] + h[i] <= 20,
            Or(x[i] >= 12, y[i] >= 8)
        )))

        solver.add(Implies(board[i] == 2, And(
            x[i] >= 0, y[i] >= 0,
            x[i] + w[i] <= 22, y[i] + h[i] <= 27,
            Or(x[i] >= 14, y[i] >= 12),
            Or(x[i] + w[i] <= cam_x_start, y[i] + h[i] <= 22)
        )))

    for i in range(N):
        for j in range(i + 1, N):
            solver.add(Or(
                board[i] != board[j],
                x[i] + w[i] <= x[j], x[j] + w[j] <= x[i],
                y[i] + h[i] <= y[j], y[j] + h[j] <= y[i]
            ))

    for i in range(N):
        for j in range(i + 1, N):
            if HOT[i] and HOT[j]:
                solver.add(Or(
                    board[i] != board[j],
                    (2 * x[i] + w[i]) - (2 * x[j] + w[j]) >= 40,
                    (2 * x[j] + w[j]) - (2 * x[i] + w[i]) >= 40,
                    (2 * y[i] + h[i]) - (2 * y[j] + h[j]) >= 40,
                    (2 * y[j] + h[j]) - (2 * y[i] + h[i]) >= 40
                ))

    result = solver.check()

    if result == sat:
        model = solver.model()
        layout_str = "SAT (found a valid layout):\n"
        for i in range(N):
            brd = model.evaluate(board[i]).as_long()
            cx = z3_to_float(model.evaluate(x[i]))
            cy = z3_to_float(model.evaluate(y[i]))
            cw = model.evaluate(w[i]).as_long()
            ch = model.evaluate(h[i]).as_long()
            layout_str += f"  Chip {i+1:2}: PCB={brd}, X={cx:g}, Y={cy:g}, W={cw}, H={ch}\n"
        if draw:
            draw_solution(model, board, x, y, w, h, HOT, added_cameras, N)
        return layout_str
    elif result == unsat:
        return "UNSAT (impossible to fit)"
    else:
        return "UNKNOWN"


def draw_solution(model, board, x, y, w, h, HOT, added_cameras, N):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

    ax1.set_title("PCB 1")
    ax1.set_xlim(0, 20); ax1.set_ylim(0, 20)
    ax1.set_xticks(range(0, 21, 2)); ax1.set_yticks(range(0, 21, 2))
    ax1.grid(True, linestyle="--", alpha=0.5)
    ax1.add_patch(patches.Rectangle((0, 0), 12, 8, facecolor="gray", alpha=0.5, hatch="//", label="Battery"))
    ax1.legend(loc="upper right")

    ax2.set_title(f"PCB 2 ({added_cameras} Added Cameras)")
    ax2.set_xlim(0, 22); ax2.set_ylim(0, 27)
    ax2.set_xticks(range(0, 23, 2)); ax2.set_yticks(range(0, 28, 2))
    ax2.grid(True, linestyle="--", alpha=0.5)
    ax2.add_patch(patches.Rectangle((0, 0), 14, 12, facecolor="gray", alpha=0.5, hatch="//", label="Battery"))
    cam_width = 7 + 4 * added_cameras
    ax2.add_patch(patches.Rectangle((22 - cam_width, 22), cam_width, 5, facecolor="black", alpha=0.5, hatch="\\\\", label="Camera"))
    ax2.legend(loc="upper right")

    for i in range(N):
        brd = model.evaluate(board[i]).as_long()
        cx = z3_to_float(model.evaluate(x[i]))
        cy = z3_to_float(model.evaluate(y[i]))
        cw = model.evaluate(w[i]).as_long()
        ch = model.evaluate(h[i]).as_long()

        ax = ax1 if brd == 1 else ax2
        color = "salmon" if HOT[i] else "lightblue"
        ax.add_patch(patches.Rectangle((cx, cy), cw, ch, linewidth=1, edgecolor="black", facecolor=color))
        ax.text(cx + cw / 2, cy + ch / 2, str(i + 1), ha="center", va="center", fontweight="bold")

    plt.tight_layout()
    filename = f"layout_{added_cameras}_added_cameras.png"
    plt.savefig(filename, dpi=150)
    print(f"Saved layout drawing to {filename}")
    plt.close()


if __name__ == "__main__":
    print("(a) 0 added cameras:\n", solve_pcb(0, draw=True))
    print("(b) 1 added camera:\n", solve_pcb(1, draw=True))
    print("(c) 3 added cameras:\n", solve_pcb(3, draw=True))