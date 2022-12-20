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
        return ret

    def calc_build_time(self, robot_costs, robot_type):
        robot_build_time = -1
        for ingredient, cost in robot_costs[robot_type].items():
            if cost == 0:
                continue
            if self.robots[ingredient] == 0:
                return None
                
            needed_ticks = max(0, (robot_costs[robot_type][ingredient] - self.assets[ingredient])) // self.robots[ingredient]
            robot_build_time = max(needed_ticks, robot_build_time)
        assert robot_build_time >= 0
        return robot_build_time

    def tick(self):
        for ingredient in ASSETS:
            self.assets[ingredient] += self.robots[ingredient]
        self.current_tick += 1

    def build(self, costs, robot_type):
        for ingredient in costs:
            self.assets[ingredient] -= costs[robot_type][ingredient]
        self.robots[robot_type] += 1

best_so_far = 0
@dataclass
class Blueprint:
    num: int
    robot_costs: dict = field(default_factory=empty_asset_dict)
    max_asset_use_per_turn: dict = field(default_factory=empty_asset_dict)

    def useless_to_build(self, state, candidate):
        if candidate == 'geodes':
            return False

        remaining = 24 - state.current_tick
        if state.robots[candidate] * remaining + state.assets[candidate] >= remaining * self.max_asset_use_per_turn[candidate]:
            return True

        return False

    
    def go(self, current_state, path):
        if current_state.current_tick >= 24:
            print('tick', current_state.current_tick, 'path:', path, current_state.assets['geodes'])

        ret = [ ]
        for next_build in ASSETS:
            state = current_state.copy()
            state.tick()

            if self.useless_to_build(state, next_build):
                continue
            build_ticks = state.calc_build_time(self.robot_costs, next_build)
            if build_ticks is None:
                continue

            for _ in range(build_ticks):
                state.tick()

            if state.current_tick > 24:
                continue

            state.build(self.robot_costs, next_build)
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
        print('Blueprint', bp.num, bp.go(state, [('begin', 0)]))


main()
