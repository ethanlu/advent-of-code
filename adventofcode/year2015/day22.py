from adventofcode import Solution

import re


class BattleState(object):
    def __init__(self, player_hp, player_mana, boss_hp, boss_damage, shield_duration, recharge_duration, poison_duration, cast_sequence, total_mana_used):
        self.cast_sequence = list(cast_sequence)
        self.total_mana_used = total_mana_used

        self.player_hp = player_hp
        self.player_mana = player_mana
        self.player_shield_duration = shield_duration
        self.player_recharge_duration = recharge_duration

        self.boss_hp = boss_hp
        self.boss_damage = boss_damage
        self.boss_poison_duration = poison_duration

    @classmethod
    def from_battle_state(cls, state):
        return cls(state.player_hp, state.player_mana, state.boss_hp, state.boss_damage, state.player_shield_duration, state.player_recharge_duration, state.boss_poison_duration, state.cast_sequence, state.total_mana_used)


class Day22(Solution):
    def _init(self):
        boss_stats = 'Hit Points: 58, Damage: 9'
        self.boss_hp = int(re.match('.*Hit Points: (\d+)', boss_stats).group(1))
        self.boss_damage = int(re.match('.*Damage: (\d+)', boss_stats).group(1))

        self.player_hp = 50
        self.player_mana = 500

        self.best_state = None

        self.spellbook = ['magic_missile', 'drain', 'shield', 'poison', 'recharge']
        self.hardmode = False

    def _check_player_victory(self, state):
        if state.boss_hp <= 0:
            print('player won a battle using ' + str(state.total_mana_used) + ' mana!')
            # player won in this state, this state takes over as the best state if its total mana use is less than current best state's total mana use
            if self.best_state is None or self.best_state.total_mana_used > state.total_mana_used:
                print('this state is now best state!')
                self.best_state = state

            return True
        return False

    def _check_boss_victory(self, state):
        if state.player_hp <= 0:
            print('boss won battle')
            return True
        return False

    def _apply_status_effects(self, state):
        # shield effect applied first
        if state.player_shield_duration > 0:
            state.player_shield_duration -= 1

            print('player shield duration is now at ' + str(state.player_shield_duration))

        # recharge effect applied next
        if state.player_recharge_duration > 0:
            state.player_mana += 101
            state.player_recharge_duration -= 1

            print('recharge provides 101 mana to player, player recharge duration is now at ' + str(state.player_recharge_duration))

        # poison effect applied last
        if state.boss_poison_duration > 0:
            state.boss_hp -= 3
            state.boss_poison_duration -= 1

            print('poison deals 3 damage to boss, boss poison duration is now at ' + str(state.boss_poison_duration))

    def _cast_spell(self, state, spell_to_cast):
        if spell_to_cast == 'magic_missile':
            if state.player_mana >= 53:
                state.player_mana -= 53
                state.total_mana_used += 53
                state.boss_hp -= 4
                print('player casts magic missile')
            else:
                return False
        elif spell_to_cast == 'drain':
            if state.player_mana >= 73:
                state.player_mana -= 73
                state.total_mana_used += 73
                state.boss_hp -= 2
                state.player_hp += 2
                print('player casts drain')
            else:
                return False
        elif spell_to_cast == 'shield':
            if state.player_mana >= 113 and state.player_shield_duration <= 0:
                state.player_mana -= 113
                state.total_mana_used += 113
                state.player_shield_duration = 6
                print('player casts shield')
            else:
                return False
        elif spell_to_cast == 'poison':
            if state.player_mana >= 173 and state.boss_poison_duration <= 0:
                state.player_mana -= 173
                state.total_mana_used += 173
                state.boss_poison_duration = 6
                print('player casts poison')
            else:
                return False
        elif spell_to_cast == 'recharge':
            if state.player_mana >= 229 and state.player_recharge_duration <= 0:
                state.player_mana -= 229
                state.total_mana_used += 229
                state.player_recharge_duration = 5
                print('player casts recharge')
            else:
                return False
        else:
            raise Exception('invalid spell ' + spell_to_cast)

        state.cast_sequence.append(spell_to_cast)
        return True

    def _attack(self, state):
        damage = max((state.boss_damage - (7 if state.player_shield_duration > 0 else 0)), 1)
        state.player_hp -= damage
        print('boss attacks for ' + str(damage) + ' damage')

    def _battle(self, state, spell_to_cast):
        ############################################################################################################
        ############################################################################################################
        # player turn
        print('')
        print('--- player turn ---')
        print('player : ' + str(state.player_hp) + ' hp, ' + str(state.player_mana) + ' mana')
        print('boss : ' + str(state.boss_hp) + ' hp')

        # hardmode enabled, player loses one hp
        if self.hardmode:
            state.player_hp -= 1
            if self._check_boss_victory(state):
                return False

        # apply status effects
        self._apply_status_effects(state)
        if self._check_player_victory(state):
            return True

        # player casts spell
        if not self._cast_spell(state, spell_to_cast):
            # player could not cast spell, end this battle as it is invalid
            print('player could not cast ' + str(spell_to_cast))
            return False
        if self._check_player_victory(state):
            return True

        ############################################################################################################
        ############################################################################################################
        # boss turn
        print('')
        print('--- boss turn ---')
        print('player : ' + str(state.player_hp) + ' hp, ' + str(state.player_mana) + ' mana')
        print('boss : ' + str(state.boss_hp) + ' hp')

        # apply status effects
        self._apply_status_effects(state)
        if self._check_player_victory(state):
            return True

        # boss attacks
        self._attack(state)
        if self._check_boss_victory(state):
            return False

        return None

    def _find_cheapest_victory(self, state, spell_to_cast):
        if self.best_state is None or self.best_state.total_mana_used > state.total_mana_used:
            # only run this battle state if there is no known best state or current state's total mana is less than best state's total mana
            battle_outcome = self._battle(state, spell_to_cast)
            if battle_outcome is None:
                # the outcome of battle yield no victory, so recurse to next state
                for spell in self.spellbook:
                    self._find_cheapest_victory(BattleState.from_battle_state(state), spell)
        return None

    def part_one(self):
        self.hardmode = False
        for spell in self.spellbook:
            print('=============================================================================================')
            self._find_cheapest_victory(BattleState(self.player_hp, self.player_mana, self.boss_hp, self.boss_damage, 0, 0, 0, [], 0), spell)

        return (self.best_state.total_mana_used, '->'.join(self.best_state.cast_sequence))

    def part_two(self):
        self.hardmode = True
        for spell in self.spellbook:
            print('=============================================================================================')
            self._find_cheapest_victory(BattleState(self.player_hp, self.player_mana, self.boss_hp, self.boss_damage, 0, 0, 0, [], 0), spell)

        return (self.best_state.total_mana_used, '->'.join(self.best_state.cast_sequence))
