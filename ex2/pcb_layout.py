import matplotlib.pyplot as plt
import matplotlib.patches as patches
from z3 import *

def solve_pcb(added_cameras=0, draw=False):
    N = 14
    
    # Chip dimensions from Figure 1
    W = [5, 5, 4, 4, 5, 3, 7, 6, 6, 4, 6, 5, 6, 5]
    H = [6, 6, 6, 10, 7, 7, 7, 10, 12, 10, 9, 11, 10, 10]
    HOT = [True, True, False, False, True, False, False, False, False, False, False, False, False, False]
    
    solver = Solver()
    
    x = [Int(f"x_{i}") for i in range(N)]
    y = [Int(f"y_{i}") for i in range(N)]
    w = [Int(f"w_{i}") for i in range(N)]
    h = [Int(f"h_{i}") for i in range(N)]
    pcb = [Int(f"pcb_{i}") for i in range(N)] # 1 for PCB1, 2 for PCB2
    
    for i in range(N):
        # 1. chip dimensions / rotation
        solver.add(Or(
            And(w[i] == W[i], h[i] == H[i]),
            And(w[i] == H[i], h[i] == W[i])
        ))
        
        # 2 & 5. chip inside PCB / battery / camera geometry
        solver.add(Or(pcb[i] == 1, pcb[i] == 2))
        
        # PCB 1 Constraints
        solver.add(Implies(pcb[i] == 1, And(
            x[i] >= 0, y[i] >= 0,
            x[i] + w[i] <= 20,
            y[i] + h[i] <= 20,
            # Battery cutout: [0, 12] x [0, 8]
            Or(x[i] >= 12, y[i] >= 8)
        )))
        
        # PCB 2 Constraints
        c = added_cameras
        solver.add(Implies(pcb[i] == 2, And(
            x[i] >= 0, y[i] >= 0,
            x[i] + w[i] <= 22,
            y[i] + h[i] <= 27,
            Or(x[i] + w[i] <= 14, y[i] >= 12),
            Or(x[i] + w[i] <= (15 - 4 * c), y[i] + h[i] <= 22)
        )))
        
    # 3. no overlap
    for i in range(N):
        for j in range(i + 1, N):
            solver.add(Or(
                pcb[i] != pcb[j], # If on different PCBs, they don't overlap
                x[i] + w[i] <= x[j],
                x[j] + w[j] <= x[i],
                y[i] + h[i] <= y[j],
                y[j] + h[j] <= y[i]
            ))
            
    # 4. hot-chip distance
    for i in range(N):
        for j in range(i + 1, N):
            if HOT[i] and HOT[j]:
                solver.add(Or(
                    pcb[i] != pcb[j],
                    (2 * x[i] + w[i]) - (2 * x[j] + w[j]) >= 40,
                    (2 * x[j] + w[j]) - (2 * x[i] + w[i]) >= 40,
                    (2 * y[i] + h[i]) - (2 * y[j] + h[j]) >= 40,
                    (2 * y[j] + h[j]) - (2 * y[i] + h[i]) >= 40
                ))
                
    result = solver.check()
    if result == sat:
        m = solver.model()
        layout_str = "SAT (found a valid layout):\n"
        for i in range(N):
            layout_str += f"  Chip {i+1:2}: PCB={m.evaluate(pcb[i]).as_long()}, X={m.evaluate(x[i]).as_long():2}, Y={m.evaluate(y[i]).as_long():2}, W={m.evaluate(w[i]).as_long()}, H={m.evaluate(h[i]).as_long()}\n"
        
        if draw:
            draw_solution(m, pcb, x, y, w, h, HOT, added_cameras, N)
            
        return layout_str
    else:
        return "UNSAT (impossible to fit)"

def draw_solution(m, pcb, x, y, w, h, HOT, added_cameras, N):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

    # PCB 1
    ax1.set_title("PCB 1")
    ax1.set_xlim(0, 20)
    ax1.set_ylim(0, 20)
    ax1.set_xticks(range(0, 21, 2))
    ax1.set_yticks(range(0, 21, 2))
    ax1.grid(True, linestyle='--', alpha=0.5)
    ax1.add_patch(patches.Rectangle((0, 0), 12, 8, facecolor='gray', alpha=0.5, hatch='//', label='Battery Cutout'))
    ax1.legend(loc="upper right")

    # PCB 2
    ax2.set_title(f"PCB 2 ({added_cameras} Cameras)")
    ax2.set_xlim(0, 22)
    ax2.set_ylim(0, 27)
    ax2.set_xticks(range(0, 23, 2))
    ax2.set_yticks(range(0, 28, 2))
    ax2.grid(True, linestyle='--', alpha=0.5)
    ax2.add_patch(patches.Rectangle((14, 0), 8, 12, facecolor='gray', alpha=0.5, hatch='//', label='Battery Cutout'))
    
    c = added_cameras
    cam_w = 7 + 4 * c
    cam_x_start = 22 - cam_w
    ax2.add_patch(patches.Rectangle((cam_x_start, 22), cam_w, 5, facecolor='black', alpha=0.5, hatch='\\\\', label='Camera Cutout'))
    ax2.legend(loc="upper right")

    for i in range(N):
        chip_pcb = m.evaluate(pcb[i]).as_long()
        chip_x = m.evaluate(x[i]).as_long()
        chip_y = m.evaluate(y[i]).as_long()
        chip_w = m.evaluate(w[i]).as_long()
        chip_h = m.evaluate(h[i]).as_long()
        chip_hot = HOT[i]
        
        ax = ax1 if chip_pcb == 1 else ax2
        color = 'salmon' if chip_hot else 'lightblue'
        rect = patches.Rectangle((chip_x, chip_y), chip_w, chip_h, linewidth=1, edgecolor='black', facecolor=color)
        ax.add_patch(rect)
        ax.text(chip_x + chip_w/2, chip_y + chip_h/2, str(i+1),
                horizontalalignment='center', verticalalignment='center', fontweight='bold')

    plt.tight_layout()
    filename = f'layout_{added_cameras}_cameras.png'
    plt.savefig(filename, dpi=150)
    print(f"Saved layout drawing to {filename}")
    plt.close()

if __name__ == "__main__":
    print("(a) 0 added cameras:\n", solve_pcb(0, draw=True))
    print("(b) 1 added camera: \n", solve_pcb(1, draw=True))
    print("(c) 3 added cameras:\n", solve_pcb(3, draw=True))