from z3 import *
import time

TRUCKS = range(1,7)

n = {t: Int(f"n_{t}") for t in TRUCKS}
p = {t: Int(f"p_{t}") for t in TRUCKS}
s = {t: Int(f"s_{t}") for t in TRUCKS}
c = {t: Int(f"c_{t}") for t in TRUCKS}
u = {t: Int(f"u_{t}") for t in TRUCKS}
z = {t: Bool(f"z_{t}") for t in TRUCKS}
D = Int("D")

W_n, W_p, W_s, W_c, W_u = 800, 405, 500, 2500, 600
MAX_WEIGHT = 8000

SKIPPLES = {1, 2}

optimizer = Optimize()


def main():
    # non-negative
    for t in TRUCKS:
        optimizer.add(n[t] >= 0)
        optimizer.add(p[t] >= 0)
        optimizer.add(s[t] >= 0)
        optimizer.add(c[t] >= 0)
        optimizer.add(u[t] >= 0)

    # sum constraints
    optimizer.add(D >= 0)
    optimizer.add(Sum(n[t] for t in TRUCKS) == 6)
    optimizer.add(Sum(p[t] for t in TRUCKS) == 12)
    optimizer.add(Sum(s[t] for t in TRUCKS) == 15)
    optimizer.add(Sum(c[t] for t in TRUCKS) == 8)
    optimizer.add(Sum(u[t] for t in TRUCKS) == D)

    #weight and block constraints
    for t in TRUCKS:
        weight_t = n[t] * W_n + p[t] * W_p + s[t] * W_s + c[t] * W_c + u[t] * W_u
        optimizer.add(weight_t <= MAX_WEIGHT)
        optimizer.add(n[t] + p[t] + s[t] + c[t] + u[t] <= 10)

    for t in TRUCKS:
        if t not in SKIPPLES:
            optimizer.add(s[t] == 0)

    for t in TRUCKS:
        optimizer.add(z[t] == (p[t] >= 1))

    optimizer.add(Sum([If(z[t], 1, 0) for t in TRUCKS]) >= 5)

    #objective
    optimizer.maximize(D)

    start_time = time.time()
    result = optimizer.check()
    elapsed_time = time.time() - start_time
    print(result)
    print(f"Time taken: {elapsed_time} seconds")

    if result == sat:
        model = optimizer.model()
        for t in TRUCKS:
            print(f"Truck {t}: n={model[n[t]]}, p={model[p[t]]}, s={model[s[t]]}, c={model[c[t]]}, u={model[u[t]]}, z={model[z[t]]}")
        print(f"D = {model[D]}")

    with open("output.txt", "w") as f:
        f.write(f"{result}\n")
        f.write(f"Time taken: {elapsed_time} seconds\n")

        if result == sat:
            model = optimizer.model()
            for t in TRUCKS:
                f.write(f"Truck {t}: n={model[n[t]]}, p={model[p[t]]}, s={model[s[t]]}, "f"c={model[c[t]]}, u={model[u[t]]}, z={model[z[t]]}\n")
            f.write(f"D = {model[D]}\n")

    print("Results written to output.txt")

    #prove that 14 is really the max
    optimizer.add(D >= 15)
    start_time = time.time()
    result_15 = optimizer.check()
    elapsed_time = time.time() - start_time
    print(f"Result for D >= 15: {result_15}")
    print(f"Time taken: {elapsed_time} seconds")
    with open("output.txt", "a") as f:
        f.write(f"Result for D >= 15: {result_15}\n")
        f.write(f"Time taken: {elapsed_time} seconds\n")


if __name__ == "__main__":
    main()
