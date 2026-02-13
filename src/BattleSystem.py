import os
import random
import time

from ActionSystem import ActionChain
from BattleUnitAI import get_ai_command
from BattleUnitSystem import create_random_unit

BATTLE_TICK_SPEED = 0.1

DEBUG_ALLIES_COUNT = 4
DEBUG_ENEMIES_COUNT = 4
DEBUG_AUTO_MODE = True
DEBUG_WAIT_STEP = 1
DEBUG_WAIT_AFTER_RESOLVE = 6



class Battle:

    def __init__(self, battleid, statisticsmode = False):
        self.statisticsmode = statisticsmode
        self.battleid = battleid
        self.starttime = 0
        self.allunits = []
        self.activeunits = []
        self.playercontrolledunits = []
        self.battlesecs = 0
        self.actionchain: ActionChain | None = None
        self.create_units()

    def create_units(self):
        for i in range(DEBUG_ALLIES_COUNT):
            unit = create_random_unit("Allied")
            unit.name = "Ally" + str(i)
            self.add_unit_to_battle(unit)
        for i in range(DEBUG_ENEMIES_COUNT):
            unit = create_random_unit("Enemy")
            unit.name = "Enemy" + str(i)
            self.add_unit_to_battle(unit)

    def add_unit_to_battle(self, unit):
        self.activeunits.append(unit)
        self.allunits.append(unit)

    def check_battle_finished(self):
        sides = []
        for unit in self.activeunits:
            if unit.side not in sides:
                sides.append(unit.side)
        return len(sides) <= 1

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_real_seconds(self):
        print(f"Time Elapsed: {round(time.time() - self.starttime, 2)}")

    def display_battle_seconds(self):
        print(f"Battle Seconds: {round(self.battlesecs / 100, 2)}")

    def display_battle_id(self):
        print(f"Battle Id: {self.battleid}")

    def tick(self):
        self.battlesecs += BATTLE_TICK_SPEED
        for unit in self.activeunits:
            unit.tick(BATTLE_TICK_SPEED)

    def get_ready_units(self):
        return [unit for unit in self.activeunits if unit.is_ready_to_act()]

    def display_unit_statuses(self):
        for unit in self.allunits:
            print(unit.get_status_text())

    def display_empty_line(self):
        self.display_log("")

    def display_log(self,logtext):
        if not self.statisticsmode:
            print(logtext + "\n", end="")

    def reset_actionchain(self):
        self.actionchain = None

    def get_reactions(self):
        all_done = False
        while (not all_done):
            self.wait_step()
            all_done = True
            shuffledunits = []
            shuffledunits.extend(self.activeunits)
            random.shuffle(shuffledunits)
            for unit in shuffledunits:
                if not self.actionchain.did_unit_act(unit):
                    if unit in self.playercontrolledunits:
                        pass  # TODO
                    else:
                        acted = get_ai_command(unit, self)
                        if acted:
                            all_done = False

    def use_primary_ability(self, user, ability, target):
        self.actionchain = ActionChain(user, ability, target, self)
        if ability.reactable:
            self.get_reactions()
        self.actionchain.resolve_chain()
        if ability.reactable:
            self.wait_post_resolve()
        else:
            self.wait_step()
        self.reset_actionchain()

    def play_turn(self, unit):
        if unit in self.playercontrolledunits:
            pass  # TODO
        else:
            get_ai_command(unit, self)

    def play_unit_turns(self):
        nextunit = max(self.get_ready_units(), key=lambda unit: unit.atb)
        self.play_turn(nextunit)

    def start_battle(self):
        self.display_log("Battle Start!")
        self.starttime = time.time()
        while not self.check_battle_finished():
            self.battle_turn()
        self.display_log("Battle End!")

    def wait_step(self):
        if not self.statisticsmode:
            time.sleep(DEBUG_WAIT_STEP)

    def wait_post_resolve(self):
        if not self.statisticsmode:
            time.sleep(DEBUG_WAIT_AFTER_RESOLVE)

    def update_active_units(self):
        for unit in self.activeunits:
            if not unit.is_alive():
                self.activeunits.remove(unit)

    def battle_turn(self):
        self.update_active_units()
        if len(self.get_ready_units()) > 0:
            if not self.statisticsmode:
                self.clear_screen()
                self.display_battle_id()
                self.display_real_seconds()
                self.display_battle_seconds()
                self.display_empty_line()
                self.display_unit_statuses()
                self.display_empty_line()
            self.play_unit_turns()
        else:
            self.tick()
