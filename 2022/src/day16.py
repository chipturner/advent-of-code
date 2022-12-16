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
    print(dfs(simplified_valve_graph, valve_rates, visit_times, "AA"))


def score_visits(valve_rates, visit_times):
    score = 0
    for valve, time in visit_times.items():
        if time < 30:
            rate = valve_rates[valve]
            score += (30 - time) * rate
    return score


def dfs(graph, valve_rates, visit_times, cur_node):
    cur_time = visit_times[cur_node]
    sub_scores = [score_visits(valve_rates, visit_times)]
    for nxt, nxt_time in graph[cur_node]:
        if nxt not in visit_times and nxt_time + cur_time < 30:
            visit_times[nxt] = nxt_time + cur_time + 1
            sub_scores.append(dfs(graph, valve_rates, visit_times, nxt))
            del visit_times[nxt]
    return max(sub_scores)


main()
