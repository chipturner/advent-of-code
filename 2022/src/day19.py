from __future__ import annotations

import helpers

import itertools
import collections
import sys

from dataclasses import dataclass, field, replace
import re

bp_re = re.compile(r'Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.')

ASSETS = [ 'geodes', 'ore', 'clay', 'obsidian' ]

def empty_asset_dict():
    return { asset: 0 for asset in ASSETS }    

@dataclass
class State:
    assets: dict = field(default_factory=empty_asset_dict)
    robots: dict = field(default_factory=empty_asset_dict)
    exclusions: set = field(default_factory=set)
    cracked_geodes: int = 0
    current_tick: int = 1

    def __post_init__(self):
        self.robots['ore'] = 1

    def copy(self):
        ret = State()
        ret.assets = self.assets.copy()
        ret.robots = self.robots.copy()
        ret.current_tick = self.current_tick
        ret.cracked_geodes = self.cracked_geodes
        ret.exclusions = self.exclusions.copy()
        return ret

    def tick(self):
        for ingredient in ASSETS:
            self.assets[ingredient] += self.robots[ingredient]
        self.current_tick += 1

    def calc_build_time(self, costs, robot_type):
        ret = 0
        for ingredient, cost in costs.items():
            if cost == 0:
                continue
            assert self.robots[ingredient] > 0, f'{ingredient} {self.robots[ingredient]}'
            needed = cost - self.assets[ingredient]
            if needed > 0:
                ret = max(ret, needed // self.robots[ingredient] + (needed % self.robots[ingredient] > 0))
        return ret

    def build(self, costs, robot_type):
        for ingredient, cost in costs.items():
            assert self.assets[ingredient] >= cost, f'{self.assets[ingredient]} {cost}'
            self.assets[ingredient] -= cost

        self.robots[robot_type] += 1

        return True

best_so_far = 0
@dataclass
class Blueprint:
    num: int
    robot_costs: dict = field(default_factory=empty_asset_dict)
    max_asset_use_per_turn: dict = field(default_factory=empty_asset_dict)

    def useless_to_consider(self, state, candidate):
        for ingredient, cost in self.robot_costs[candidate].items():
            if cost > 0 and state.robots[ingredient] == 0:
                return True

        if candidate == 'geodes':
            return False

        remaining = 24 - state.current_tick
        if state.robots[candidate] * remaining + state.assets[candidate] >= remaining * self.max_asset_use_per_turn[candidate]:
            return True

        return False

    
    def go(self, current_state, path):
        if current_state.current_tick >= 24:
            print('bp', self.num, 'tick', current_state.current_tick, 'path:', path, current_state.assets, current_state.assets['geodes'])

        ret = [ ]
        for next_build in ASSETS:
            state = current_state.copy()

            if self.useless_to_consider(state, next_build):
                continue

            ticks_to_build = state.calc_build_time(self.robot_costs[next_build], next_build);
            for _ in range(ticks_to_build):
                state.tick()
            state.build(self.robot_costs[next_build], next_build)

            if state.current_tick <= 24:
                ret.extend(self.go(state, path + [ (next_build, state.current_tick) ]))
        return ret

def main() -> None:
    lines = helpers.read_input()

    blueprints = []
    for line in lines:
        assert (m := bp_re.match(line)) != None
        num, ore_robot_cost_ore, clay_robot_cost_ore, obsidian_cost_ore, obsidian_cost_clay, geode_cost_ore, geode_cost_obsidian = [ int(v) for v in m.groups()]
        bp = Blueprint(num)
        bp.robot_costs['ore'] = empty_asset_dict() | { 'ore': ore_robot_cost_ore }
        bp.robot_costs['clay'] = empty_asset_dict() | { 'ore': clay_robot_cost_ore }
        bp.robot_costs['obsidian'] = empty_asset_dict() | { 'ore': obsidian_cost_ore, 'clay': obsidian_cost_clay }
        bp.robot_costs['geodes'] = empty_asset_dict() | { 'ore': geode_cost_ore, 'obsidian': geode_cost_obsidian }
        for asset in ASSETS:
            bp.max_asset_use_per_turn[asset] = max(v.get(asset, 0) for k, v in bp.robot_costs.items())
        blueprints.append(bp)

    for bp in blueprints:
        state = State()
        print('Blueprint', bp.num, bp.go(state, []))


main()
