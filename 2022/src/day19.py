from __future__ import annotations

import helpers

import itertools
import collections

from dataclasses import dataclass, field, replace
import re

bp_re = re.compile(r'Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.')

ASSETS = [ 'geodes', 'ore', 'clay', 'obsidian' ]

@dataclass
class State:
    assets: dict = field(default_factory=lambda: { asset: 0 for asset in ASSETS })
    robots: dict = field(default_factory=lambda: { asset: 0 for asset in ASSETS })
    cracked_geodes: int = 0

    def __post_init__(self):
        self.robots['ore'] = 1

    def copy(self):
        ret = State()
        ret.assets = self.assets.copy()
        ret.robots = self.robots.copy()
        return ret

    def max_possible_geodes(self, turns_left):
        ret = self.assets['geodes']
        crackers = self.robots['geodes'] + 1
        for i in range(turns_left):
            ret += crackers
            crackers += 1
        return ret

best_so_far = 0
@dataclass
class Blueprint:
    num: int
    robot_costs: dict
    max_asset_use_per_turn: dict
    
    def __init__(self, num):
        self.num = num
        self.robot_costs = { }
        self.max_asset_use_per_turn = {}

    def go(self, current_state, path):
        current_state = current_state.copy()

        turns_left = 24 - len(path)
        print('path:', len(path), path)
        if turns_left == 0:
            print('completed geodes:', current_state.assets['geodes'])
            return [ current_state ]

        global best_so_far
        if best_so_far > current_state.max_possible_geodes(turns_left):
            print('pruning bad outcome', path)
            return [ current_state ]
        else:
            print('max possible geodes', current_state.max_possible_geodes(turns_left))

        for asset in ASSETS:
            current_state.assets[asset] += current_state.robots[asset]

        end_states = []

        for new_robot in ASSETS:
            #print('considering', len(path), new_robot)
            robot_costs = self.robot_costs[new_robot]
            if new_robot != 'geodes' and current_state.robots[new_robot] >= self.max_asset_use_per_turn[new_robot]:
                print('never need to make more', new_robot, current_state.robots[new_robot], self.max_asset_use_per_turn[new_robot])
                continue
            for ore in robot_costs:
                if current_state.assets[ore] < robot_costs[ore]:
                    #print('nope', new_robot, current_state.assets[ore], robot_costs[ore])
                    break
            else:
                new_state = current_state.copy()
                #print('yep', new_robot, new_state.assets[ore], robot_costs[ore])
                for ore, cost in robot_costs.items():
                    new_state.assets[ore] -= cost
                new_state.robots[new_robot] += 1
                if new_state.assets['geodes'] > best_so_far:
                    best_so_far = new_state.assets['geodes']
                    print('new best:', best_so_far)
                end_states.extend(self.go(new_state, path + [ new_robot ]))
        end_states.extend(self.go(current_state.copy(), path + ['wait']))
        return end_states
                
    

def main() -> None:
    lines = helpers.read_input()

    blueprints = []
    for line in lines:
        assert (m := bp_re.match(line)) != None
        num, ore_robot_cost_ore, clay_robot_cost_ore, obsidian_cost_ore, obsidian_cost_clay, geode_cost_ore, geode_cost_obsidian = [ int(v) for v in m.groups()]
        bp = Blueprint(num)
        bp.robot_costs['ore'] = { 'ore': ore_robot_cost_ore }
        bp.robot_costs['clay'] = { 'ore': clay_robot_cost_ore }
        bp.robot_costs['obsidian'] = { 'ore': obsidian_cost_ore, 'clay': obsidian_cost_clay }
        bp.robot_costs['geodes'] = { 'ore': geode_cost_ore, 'obsidian': geode_cost_obsidian }
        for asset in ASSETS:
            bp.max_asset_use_per_turn[asset] = max(v.get(asset, 0) for k, v in bp.robot_costs.items())
        blueprints.append(bp)

    for bp in blueprints:
        state = State()
        print('Blueprint', bp.num, bp.go(state, ['wait']))


main()
