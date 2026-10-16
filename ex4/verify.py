import time

from z3 import And, Bool, If, Int, Solver, is_true, sat, unsat


def verify_program(k_value, max_iterations=36):
    # a grows by at least 5 each iteration, so 36 iterations cover every run.
    if max_iterations < 36:
        raise ValueError("Use at least 36 iterations to cover every run.")

    solver = Solver()
    a = [Int(f"a_{i}") for i in range(max_iterations + 1)]
    b = [Int(f"b_{i}") for i in range(max_iterations + 1)]
    choice = [Bool(f"c_{i}") for i in range(max_iterations)]

    solver.add(a[0] == 1, b[0] == 1)

    for i in range(max_iterations):
        # b is updated before a.
        if_step = And(b[i+1] == b[i] + 3,
                      a[i+1] == a[i] + 2 * b[i+1])
        else_step = And(b[i+1] == b[i] + a[i],
                        a[i+1] == a[i] + 5)

        stopped = And(a[i+1] == a[i], b[i+1] == b[i])
        solver.add(If(a[i] < 180, If(choice[i], if_step, else_step), stopped))

    solver.add(a[-1] >= 180, b[-1] == 190 + k_value)

    start_time = time.perf_counter()
    result = solver.check()
    elapsed = time.perf_counter() - start_time

    if result == unsat:
        return "SAFE", elapsed, None
    if result != sat:
        return "UNKNOWN", elapsed, None

    model = solver.model()
    trace = []
    for i in range(max_iterations):
        ai = model.evaluate(a[i]).as_long()
        if ai >= 180:
            break

        bi = model.evaluate(b[i]).as_long()
        ai1 = model.evaluate(a[i+1]).as_long()
        bi1 = model.evaluate(b[i+1]).as_long()
        branch = "if-branch" if is_true(model.evaluate(choice[i])) else "else-branch"
        trace.append((i, branch, ai, bi, ai1, bi1))

    return "UNSAFE", elapsed, trace


if __name__ == "__main__":
    for k in range(11):
        status, elapsed, trace = verify_program(k)
        print(f"\nFor k = {k}, the result is {status}. "
              f"The crash condition is b = {190 + k}. Z3 took {elapsed:.4f} seconds.")
        if trace:
            for step, branch, ai, bi, ai1, bi1 in trace:
                print(f"  Step {step + 1}: {branch}, ({ai}, {bi}) -> ({ai1}, {bi1})")
