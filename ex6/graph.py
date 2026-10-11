import argparse
import csv
from pathlib import Path
from time import perf_counter

from oxidd.bdd import BDDFunction, BDDManager


DEFAULT_CAPACITIES = {
    "congress": 1_000_000,
    "pokec-small": 8_000_000,
    "pokec-medium": 32_000_000,
    "pokec": 64_000_000,
}


def iter_edges(edges_file, labels):
    with edges_file.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            source = int(row["source"])
            target = int(row["target"])
            if source not in labels or target not in labels:
                raise ValueError("An edge refers to a node missing from the nodes CSV")
            yield source, target


def load_graph(nodes_file, edges_file):
    labels = {}
    with nodes_file.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            node_id = int(row["id"])
            label = int(row["label"])
            if label not in (0, 1):
                raise ValueError("Node labels must be 0 or 1")
            labels[node_id] = label

    return labels, iter_edges(edges_file, labels)


def node_to_bdd(manager, node_id, variables):
    nbits = len(variables)
    if node_id < 0 or node_id >= 2 ** nbits:
        raise ValueError("Node ID does not fit in the supplied bits")

    bits = format(node_id, f"0{nbits}b")
    result = manager.true()
    for bit in range(nbits):
        digit = bits[nbits - 1 - bit]
        if digit == "1":
            result = result & variables[bit]
        else:
            result = result & ~variables[bit]
    return result


def image(states_bdd, transition_bdd, source_vars, target_to_source):
    outgoing_edges_bdd = states_bdd & transition_bdd
    targets_bdd = outgoing_edges_bdd.exists(source_vars)
    return targets_bdd.substitute(target_to_source)


def count_source_nodes(states_bdd, nbits):
    total_bits = states_bdd.manager.num_vars()
    return states_bdd.sat_count(total_bits) // (2 ** (total_bits - nbits))


def count_graph_bdd_nodes(T, L):
    if T == L:
        return T.node_count()

    manager = T.manager
    old_order = []
    for level in range(manager.num_vars()):
        old_order.append(manager.level_to_var(level))
    selector_id = manager.add_vars(1)[0]
    manager.set_var_order([selector_id] + old_order)

    selector = manager.var(selector_id)
    combined = selector.ite(T, L)
    return combined.node_count() - 1


def reachability(manager, start_bdd, T, source_vars, target_to_source, nbits):
    reached_bdd = start_bdd
    frontier_bdd = start_bdd
    step = 0

    while frontier_bdd != manager.false():
        successors_bdd = image(frontier_bdd, T, source_vars, target_to_source)
        new_nodes_bdd = successors_bdd & ~reached_bdd
        reached_bdd = reached_bdd | new_nodes_bdd
        frontier_bdd = new_nodes_bdd

        step += 1
        print("  Step", step, "- new nodes:", count_source_nodes(new_nodes_bdd, nbits))

    return reached_bdd


def alternating_reachability(
    manager, start_bdd, start_label, T, L, source_vars, target_to_source, nbits
):
    if start_label != 0:
        print("  Node 1 has label", start_label,
              "but the required path must start with label 0; no valid path.")
        return manager.false()

    reached_bdd = start_bdd
    frontier_bdd = start_bdd
    next_label = 1
    step = 0

    while frontier_bdd != manager.false():
        successors_bdd = image(frontier_bdd, T, source_vars, target_to_source)

        if next_label == 1:
            successors_bdd = successors_bdd & L
        else:
            successors_bdd = successors_bdd & ~L

        new_nodes_bdd = successors_bdd & ~reached_bdd
        reached_bdd = reached_bdd | new_nodes_bdd
        frontier_bdd = new_nodes_bdd

        step += 1
        print("  Step", step, "- required label:", next_label,
              "- new nodes:", count_source_nodes(new_nodes_bdd, nbits))
        next_label = 1 - next_label

    return reached_bdd


def build_transition(manager, edges, source_bits, target_bits, capacity):
    T = manager.false()
    target_cache = {}
    current_source = None
    source_bdd = manager.false()
    targets_bdd = manager.false()
    processed_edges = 0
    start = perf_counter()

    for source, target in edges:
        if source != current_source:
            if current_source is not None:
                T = T | (source_bdd & targets_bdd)
            current_source = source
            source_bdd = node_to_bdd(manager, source, source_bits)
            targets_bdd = manager.false()

        target_bdd = target_cache.get(target)
        if target_bdd is None:
            target_bdd = node_to_bdd(manager, target, target_bits)
            target_cache[target] = target_bdd
        targets_bdd = targets_bdd | target_bdd

        processed_edges += 1
        if processed_edges % 10_000 == 0:
            if manager.approx_num_inner_nodes() > capacity * 0.7:
                manager.gc()
        if processed_edges % 1_000_000 == 0:
            print("  Processed", processed_edges, "edges - elapsed:",
                  f"{perf_counter() - start:.1f}s", flush=True)

    if current_source is not None:
        T = T | (source_bdd & targets_bdd)
    target_cache.clear()
    manager.gc()
    return T, processed_edges


def main(graph_name="congress"):
    base = Path(__file__).resolve().parent
    print("Loading node CSV for", graph_name, "...", flush=True)
    labels, edges = load_graph(
        base / f"{graph_name}_nodes.csv",
        base / f"{graph_name}_edges.csv",
    )
    if 1 not in labels:
        raise ValueError("The starting node with ID 1 is missing")

    nbits = max(1, max(labels).bit_length())
    print("Graph:", graph_name)
    print("Graph nodes:", len(labels))
    print("Bits per node ID:", nbits, "Start node: 1", "Start label:", labels[1])

    build_start = perf_counter()
    capacity = DEFAULT_CAPACITIES[graph_name]
    print("BDD inner-node capacity:", capacity)
    manager = BDDManager(capacity, 100_000, 1)
    manager.add_vars(2 * nbits)

    source_bits = []
    target_bits = []
    for bit in range(nbits):
        source_bits.append(manager.var(bit))
        target_bits.append(manager.var(nbits + bit))

    print("Building transition relation T ...", flush=True)
    T, processed_edges = build_transition(
        manager, edges, source_bits, target_bits, capacity
    )

    print("Directed edges:", processed_edges, flush=True)

    print("Building labelling BDD L ...", flush=True)
    L = manager.false()
    processed_nodes = 0
    for node_id, label in labels.items():
        if label == 1:
            node_bdd = node_to_bdd(manager, node_id, source_bits)
            L = L | node_bdd
        processed_nodes += 1
        if processed_nodes % 10_000 == 0:
            if manager.approx_num_inner_nodes() > capacity * 0.7:
                manager.gc()
    manager.gc()
    print("Graph construction time (including edge CSV reading):",
          f"{perf_counter() - build_start:.4f}s", flush=True)

    source_vars = manager.true()
    for variable in source_bits:
        source_vars = source_vars & variable

    rename_pairs = []
    for bit in range(nbits):
        rename_pairs.append((nbits + bit, source_bits[bit]))
    target_to_source = BDDFunction.make_substitution(rename_pairs)
    start_bdd = node_to_bdd(manager, 1, source_bits)

    print("Part (b): ordinary reachability")
    reach_start = perf_counter()
    reached_bdd = reachability(
        manager, start_bdd, T, source_vars, target_to_source, nbits
    )
    print("Reachable nodes:", count_source_nodes(reached_bdd, nbits))
    print("Reachability time:", f"{perf_counter() - reach_start:.4f}s")

    print("Part (c): alternating-label reachability (0 -> 1 -> 0 -> ...)")
    alternating_start = perf_counter()
    alt_reached_bdd = alternating_reachability(
        manager, start_bdd, labels[1], T, L,
        source_vars, target_to_source, nbits,
    )
    print("Alternating-reachable nodes:", count_source_nodes(alt_reached_bdd, nbits))
    print("Alternating reachability time:", f"{perf_counter() - alternating_start:.4f}s")

    print("BDD node counts (including terminal nodes):")
    print("  T - directed edges:", T.node_count())
    print("  L - label-1 nodes:", L.node_count())
    print("  R_b - ordinary reachable nodes:", reached_bdd.node_count())
    print("  R_c - alternating reachable nodes:", alt_reached_bdd.node_count())
    print("  Graph representation T and L, shared nodes counted once:",
          count_graph_bdd_nodes(T, L))

    return reached_bdd, alt_reached_bdd


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("graph", nargs="?", default="congress",
                        choices=tuple(DEFAULT_CAPACITIES),
                        help="CSV graph to process (default: congress)")
    args = parser.parse_args()
    main(args.graph)
