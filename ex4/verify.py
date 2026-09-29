from z3 import *
import time

def verify_program(k_value, max_iterations=36):
    
    solver = Solver()

    # Symbolic variables for each step: a_i, b_i, and the choice at step i
    a = [Int(f"a_{i}") for i in range(max_iterations + 1)]
    b = [Int(f"b_{i}") for i in range(max_iterations + 1)]
    choice = [Bool(f"c_{i}") for i in range(max_iterations)]
    # active[i] == True means the loop is still running at step i
    active = [Bool(f"act_{i}") for i in range(max_iterations + 1)]

    # Initial values
    solver.add(a[0] == 1)
    solver.add(b[0] == 1)
    solver.add(active[0] == True)

    for i in range(max_iterations):
        # If the loop is active (a[i] < 180), take a step
        solver.add(Implies(active[i], a[i] < 180))

        # Branch 1 (choice == True):  b' = b + 3,  a' = a + 2*(b+3)
        # Branch 2 (choice == False): b' = b + a,  a' = a + 5
        solver.add(Implies(active[i],
            If(choice[i],
               And(b[i+1] == b[i] + 3,
                   a[i+1] == a[i] + 2 * b[i+1]),
               And(b[i+1] == b[i] + a[i],
                   a[i+1] == a[i] + 5)
            )
        ))

        # When the loop is inactive, a and b stay the same
        solver.add(Implies(Not(active[i]),
            And(a[i+1] == a[i], b[i+1] == b[i])
        ))

        # The loop becomes inactive once a >= 180
        solver.add(active[i+1] == And(active[i], a[i+1] < 180))

    # The loop must have terminated at some point
    solver.add(Not(active[max_iterations]))

    # The crash condition
    target = 190 + k_value
    solver.add(b[max_iterations] == target)

    start_time = time.perf_counter()
    result = solver.check()
    elapsed = time.perf_counter() - start_time

    if result == sat:
        model = solver.model()

        # Reconstruct the trace
        trace = []
        for i in range(max_iterations):
            if is_true(model.evaluate(active[i])):
                c = is_true(model.evaluate(choice[i]))
                ai = model.evaluate(a[i]).as_long()
                bi = model.evaluate(b[i]).as_long()
                ai1 = model.evaluate(a[i+1]).as_long()
                bi1 = model.evaluate(b[i+1]).as_long()
                branch = "if-branch" if c else "else-branch"
                trace.append((i, branch, ai, bi, ai1, bi1))
            else:
                break

        return "UNSAFE", elapsed, trace
    elif result == unsat:
        return "SAFE", elapsed, None
    else:
        return "UNKNOWN", elapsed, None


if __name__ == "__main__":
    print("=" * 70)
    print("Exercise 4: Program Verification")
    print("=" * 70)

    for k in range(11):
        status, elapsed, trace = verify_program(k)
        target = 190 + k

        if status == "UNSAFE":
            print(f"\nk={k:2d} (b == {target}): UNSAFE (can crash) "
                  f"[{elapsed:.4f}s, {len(trace)} iterations]")
            print(f"  Trace (step, branch, a_before, b_before -> a_after, b_after):")
            for step, branch, ai, bi, ai1, bi1 in trace:
                print(f"    Step {step:2d}: {branch:12s}  "
                      f"a={ai:4d}, b={bi:4d}  ->  a={ai1:4d}, b={bi1:4d}")
        elif status == "SAFE":
            print(f"\nk={k:2d} (b == {target}): SAFE (cannot crash) "
                  f"[{elapsed:.4f}s]")
        else:
            print(f"\nk={k:2d} (b == {target}): UNKNOWN "
                  f"[{elapsed:.4f}s]")  

    print("\n" + "=" * 70)
