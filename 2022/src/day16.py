from __future__ import annotations

import re
import helpers
import collections

valve_re = re.compile(
    r"Valve (..) has flow rate=(\d+); tunnels? leads? to valves? (.*)$"
)


def main() -> None:
    lines = helpers.read_input()
    print(lines)

    valve_graph = {}
    valve_rates = {}
    for line in lines:
        m = valve_re.match(line)
        valve, rate, dst_valves = m.groups()
        rate = int(rate)
        dst_valves = dst_valves.split(", ")
        print(valve, rate, dst_valves)
        valve_graph[valve] = dst_valves
        valve_rates[valve] = rate

    valve_distances = {}
    simplified_valve_graph = collections.defaultdict(list)
    for initial_valve in valve_graph:
        distances = {}
        queue = [(initial_valve, 0)]
        while len(queue):
            n, d = queue.pop(0)
            if n in distances:
                continue
            distances[n] = d
            for nxt in valve_graph[n]:
                queue.append((nxt, d + 1))
        for nxt, distance in distances.items():
            if (
                distance > 0
                and valve_rates[nxt] > 0
                and (initial_valve == "AA" or valve_rates[initial_valve] > 0)
            ):
                valve_distances[initial_valve, nxt] = distance
                simplified_valve_graph[initial_valve].append((nxt, distance))
    simplified_valve_graph = dict(simplified_valve_graph.items())
    print(valve_distances)
    print(simplified_valve_graph)

    visit_times = {"AA": 0}
    all_paths = dfs(simplified_valve_graph, valve_rates, visit_times, "AA")
    scored_paths = sorted(
        [
            (
                score_visits(valve_rates, path),
                set(p for p in path.keys() if p != "AA"),
                list(path.keys()),
            )
            for path in all_paths
        ],
        key=lambda p: p[0],
        reverse=True,
    )
    for (score, path_set, path) in scored_paths:
        print(f"{score} {path_set} {path}")

    sorted_path_pairs = []
    max_score = 0
    for idx, (s1, p1s, p1) in enumerate(scored_paths):
        print(idx, len(scored_paths))
        for s2, p2s, p2 in scored_paths[idx:]:
            if s1 + s2 > max_score and p1s.isdisjoint(p2s):
                max_score = s1 + s2
                sorted_path_pairs.append([s1 + s2, p1, p2])
    sorted_path_pairs.sort(key=lambda p: p[0])
    print(sorted_path_pairs[-1])
    for p in sorted_path_pairs:
        print(p[0], sorted(p[1]), sorted(p[2]))


MINUTES_AVAILABLE = 26


def score_visits(valve_rates, visit_times):
    score = 0
    for valve, time in visit_times.items():
        if time < MINUTES_AVAILABLE:
            rate = valve_rates[valve]
            score += (MINUTES_AVAILABLE - time) * rate
    return score


def dfs(graph, valve_rates, visit_times, cur_node):
    cur_time = visit_times[cur_node]
    ret = [visit_times.copy()]
    for nxt, nxt_time in graph[cur_node]:
        if nxt not in visit_times and nxt_time + cur_time <= MINUTES_AVAILABLE:
            visit_times[nxt] = nxt_time + cur_time + 1
            ret.extend(dfs(graph, valve_rates, visit_times, nxt))
            del visit_times[nxt]
    return ret


main()
