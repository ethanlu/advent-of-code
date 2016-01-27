from itertools import combinations

import re

input = 'Hit Points: 100,Damage: 8,Armor: 2'

class Day21(object):
    def __init__(self, boss_stats):
        self.boss_hp = int(re.match('.*Hit Points: (\d+)', boss_stats).group(1))
        self.boss_damage = int(re.match('.*Damage: (\d+)', boss_stats).group(1))
        self.boss_armor = int(re.match('.*Armor: (\d+)', boss_stats).group(1))

        self.hp = 100
        self.damage = 0
        self.armor = 0

        self.store = {'weapons': {'dagger': {'cost': 8, 'damage': 4, 'armor': 0},
                                  'shortsword': {'cost': 10, 'damage': 5, 'armor': 0},
                                  'warhammer': {'cost': 25, 'damage': 6, 'armor': 0},
                                  'longsword': {'cost': 40, 'damage': 7, 'armor': 0},
                                  'greataxe': {'cost': 74, 'damage': 8, 'armor': 0}
                                 },
                      'armor': {'leather': {'cost': 13, 'damage': 0, 'armor': 1},
                                'chainmail': {'cost': 31, 'damage': 0, 'armor': 2},
                                'splintmail': {'cost': 53, 'damage': 0, 'armor': 3},
                                'bandedmail': {'cost': 75, 'damage': 0, 'armor': 4},
                                'platemail': {'cost': 102, 'damage': 0, 'armor': 5}
                               },
                      'rings': {'damage+1': {'cost': 25, 'damage': 1, 'armor': 0},
                                'damage+2': {'cost': 50, 'damage': 2, 'armor': 0},
                                'damage+3': {'cost': 100, 'damage': 3, 'armor': 0},
                                'defense+1': {'cost': 20, 'damage': 0, 'armor': 1},
                                'defense+2': {'cost': 40, 'damage': 0, 'armor': 2},
                                'defense+3': {'cost': 80, 'damage': 0, 'armor': 3}
                               }
                      }

    def _all_possible_gear_stats(self, allowed_equipment_slot):
        gear_setup = []

        possible_weapons = list(combinations(self.store['weapons'].keys(), allowed_equipment_slot['weapons'])) if allowed_equipment_slot['weapons'] else []
        possible_armors = [('',)] + list(combinations(self.store['armor'].keys(), allowed_equipment_slot['armor'])) if allowed_equipment_slot['armor'] else []
        possible_rings = [('',)] + list(combinations(self.store['rings'].keys(), allowed_equipment_slot['rings'])) if allowed_equipment_slot['rings'] else []

        for weapon in possible_weapons:
            for armor in possible_armors:
                for rings in possible_rings:
                    gear = {'gear': {'weapon': weapon,
                                     'armor': armor,
                                     'rings': rings},
                            'cost': (self.store['weapons'][weapon[0]]['cost']) +
                                    (self.store['armor'][armor[0]]['cost'] if armor[0] else 0) +
                                    (self.store['rings'][rings[0]]['cost'] if len(rings) > 0 and rings[0] else 0) +
                                    (self.store['rings'][rings[1]]['cost'] if len(rings) > 1 and rings[1] else 0),
                            'damage': (self.store['weapons'][weapon[0]]['damage']) +
                                      (self.store['armor'][armor[0]]['damage'] if armor[0] else 0) +
                                      (self.store['rings'][rings[0]]['damage'] if len(rings) > 0 and rings[0] else 0) +
                                      (self.store['rings'][rings[1]]['damage'] if len(rings) > 1 and rings[1] else 0),
                            'armor': (self.store['weapons'][weapon[0]]['armor']) +
                                     (self.store['armor'][armor[0]]['armor'] if armor[0] else 0) +
                                     (self.store['rings'][rings[0]]['armor'] if len(rings) > 0 and rings[0] else 0) +
                                     (self.store['rings'][rings[1]]['armor'] if len(rings) > 1 and rings[1] else 0)}

                    gear_setup.append(gear)

        return gear_setup

    def _battle(self, player, boss):
        while True:
            # player gets first trike
            boss['hp'] -= max(player['damage'] - boss['armor'], 1)
            #print '\t\t PLAYER ATTACKS! ==> boss hp : ' + str(boss['hp']) + ', player hp : ' + str(player['hp'])

            if boss['hp'] <= 0:
                print '\t\t PLAYER WINS! ==> boss hp : ' + str(boss['hp']) + ', player hp : ' + str(player['hp'])
                break

            player['hp'] -= max(boss['damage'] - player['armor'], 1)
            #print '\t\t BOSS ATTACKS!   ==> boss hp : ' + str(boss['hp']) + ', player hp : ' + str(player['hp'])

            if player['hp'] <= 0:
                print '\t\t BOSS WINS! ==> boss hp : ' + str(boss['hp']) + ', player hp : ' + str(player['hp'])
                break

        return player['hp'] > 0

    def part_one(self):
        allowed_equipment_slots = [{'weapons': 1, 'armor': 0, 'rings': 0},
                                   {'weapons': 1, 'armor': 0, 'rings': 1},
                                   {'weapons': 1, 'armor': 0, 'rings': 2},
                                   {'weapons': 1, 'armor': 1, 'rings': 0},
                                   {'weapons': 1, 'armor': 1, 'rings': 1},
                                   {'weapons': 1, 'armor': 1, 'rings': 2}]

        cheapest_victory = 0
        for allowed_equipment_slot in allowed_equipment_slots:
            print 'trying setup : ' + str(allowed_equipment_slot)
            for gear_stats in self._all_possible_gear_stats(allowed_equipment_slot):
                print '\t gears : ' + str(gear_stats)
                gear_cost = gear_stats['cost']
                boss = {'hp': self.boss_hp, 'damage': self.boss_damage, 'armor': self.boss_armor}
                player = {'hp': self.hp, 'damage': self.damage + gear_stats['damage'], 'armor': self.armor + gear_stats['armor']}

                if self._battle(player, boss) and (cheapest_victory == 0 or cheapest_victory > gear_cost):
                    cheapest_victory = gear_cost

        return cheapest_victory

    def part_two(self):
        allowed_equipment_slots = [{'weapons': 1, 'armor': 0, 'rings': 0},
                                   {'weapons': 1, 'armor': 0, 'rings': 1},
                                   {'weapons': 1, 'armor': 0, 'rings': 2},
                                   {'weapons': 1, 'armor': 1, 'rings': 0},
                                   {'weapons': 1, 'armor': 1, 'rings': 1},
                                   {'weapons': 1, 'armor': 1, 'rings': 2}]

        costliest_defeat = 0
        for allowed_equipment_slot in allowed_equipment_slots:
            print 'trying setup : ' + str(allowed_equipment_slot)
            for gear_stats in self._all_possible_gear_stats(allowed_equipment_slot):
                print '\t gears : ' + str(gear_stats)
                gear_cost = gear_stats['cost']
                boss = {'hp': self.boss_hp, 'damage': self.boss_damage, 'armor': self.boss_armor}
                player = {'hp': self.hp, 'damage': self.damage + gear_stats['damage'], 'armor': self.armor + gear_stats['armor']}

                if not self._battle(player, boss) and (costliest_defeat == 0 or costliest_defeat < gear_cost):
                    costliest_defeat = gear_cost

        return costliest_defeat
