import os
import time
import logging
import multiprocessing

from BattleSystem import Battle

TEST_MAX_BATTLES_SAFETY_LIMIT = 50000
TEST_FIRST_REPORT_BATTLE_COUNT = 10000
TEST_REPORT_BATTLE_COUNT_CHECKPOINT = 2500
TEST_MODE_SIMULTANEOUS_BATTLE_COUNT = 23

logging.basicConfig(level=logging.INFO)


class StatisticsData:
    def __init__(self):
        self.battle_counter = multiprocessing.Value('i', 0)
        self.battles_finished = multiprocessing.Value('i', 0)
        self.statistics_finished = multiprocessing.Value('b', False)
        self.holdforwriting = multiprocessing.RLock()
        self.ability_queue = multiprocessing.Queue()
        self.weapon_queue = multiprocessing.Queue()


class StatisticsWorkerThread(multiprocessing.Process):
    def __init__(self, data: StatisticsData):
        super().__init__()
        self.data : StatisticsData = data

    def run(self):
        logging.info("Worker started")
        while True:
            time.sleep(0)
            with self.data.battle_counter.get_lock():
                if self.data.battle_counter.value >= TEST_MAX_BATTLES_SAFETY_LIMIT:
                    logging.info("Worker completed tasks")
                    break
                self.data.battle_counter.value += 1
                localcount = self.data.battle_counter.value
            battle = Battle(localcount, True)
            print(f"Starting battle {localcount}\n", end="")
            battle.start_battle()
            with self.data.holdforwriting:
                add_finished_battle_to_statistics(battle, self.data)
            print(f"Finished battle {localcount}\n", end="")
            with self.data.battles_finished.get_lock():
                self.data.battles_finished.value += 1


class StatisticsWriterThread(multiprocessing.Process):
    def __init__(self, data: StatisticsData):
        super().__init__()
        self.data :StatisticsData = data

    def run(self):
        logging.info("Displayer started")
        checkpoint = TEST_FIRST_REPORT_BATTLE_COUNT
        while True:
            time.sleep(0)
            self.get_ability_reports()
            self.get_weapon_reports()
            if checkpoint <= self.data.battles_finished.value:
                checkpoint += TEST_REPORT_BATTLE_COUNT_CHECKPOINT
                with self.data.holdforwriting:
                    print("-- Updating Statistics --\n", end="")
                    write_statistics_to_file("BalanceTest",self.data.battles_finished.value)
                    print("---- Update Finished ----\n", end="")
            if self.data.statistics_finished.value:
                with self.data.holdforwriting:
                    print("---- Updating Final  ----\n", end="")
                    write_statistics_to_file("BalanceTest",self.data.battles_finished.value)
                print("-- Statistics Finished --\n", end="")
                break

    def get_ability_reports(self):
        while not self.data.ability_queue.empty():
            message = self.data.ability_queue.get()
            data = message
            ability = data[0]
            iswinner = data[1]
            write_ability_to_statistics(ability, iswinner)


    def get_weapon_reports(self):
        while not self.data.weapon_queue.empty():
            message = self.data.weapon_queue.get()
            data = message
            weapon = data[0]
            iswinner = data[1]
            write_weapon_to_statistics(weapon, iswinner)

def launch_test_cycles():
    data = StatisticsData()
    writer = StatisticsWriterThread(data=data)
    workers = [StatisticsWorkerThread(data=data) for _ in range(TEST_MODE_SIMULTANEOUS_BATTLE_COUNT)]
    writer.start()
    for worker in workers:
        worker.start()
    for worker in workers:
        worker.join()
    data.statistics_finished.value = True
    writer.join()


battle_count = 0
balance_statistics = {
    "Ability": {},
    "AbilityElement": {},
    "AbilityMod": {},
    "WeaponCategory": {},
    "WeaponType": {},
    "WeaponElement": {}
}


def write_ability_to_statistics(ability, iswinner):
    if ability.skillbase not in balance_statistics["Ability"]:
        balance_statistics["Ability"][ability.skillbase] = {"Used": 0, "Wins": 0}

    balance_statistics["Ability"][ability.skillbase]["Used"] += 1
    if iswinner:
        balance_statistics["Ability"][ability.skillbase]["Wins"] += 1

    try:
        if ability.element not in balance_statistics["AbilityElement"]:
            balance_statistics["AbilityElement"][ability.element] = {
                "Used": 0,
                "Wins": 0
            }

        balance_statistics["AbilityElement"][ability.element]["Used"] += 1
        if iswinner:
            balance_statistics["AbilityElement"][ability.element]["Wins"] += 1
    except AttributeError:
        pass

    try:
        if ability.skillsecondary not in balance_statistics["AbilityMod"]:
            balance_statistics["AbilityMod"][ability.skillsecondary] = {
                "Used": 0,
                "Wins": 0
            }

        balance_statistics["AbilityMod"][ability.skillsecondary]["Used"] += 1
        if iswinner:
            balance_statistics["AbilityMod"][ability.skillsecondary]["Wins"] += 1
    except AttributeError:
        pass


def add_ability_to_statistics(ability, iswinner, data: StatisticsData):
    data.ability_queue.put([ability, iswinner])


def write_weapon_to_statistics(weapon, iswinner):
    if weapon.type not in balance_statistics["WeaponType"]:
        balance_statistics["WeaponType"][weapon.type] = {"Used": 0, "Wins": 0}

    balance_statistics["WeaponType"][weapon.type]["Used"] += 1
    if iswinner:
        balance_statistics["WeaponType"][weapon.type]["Wins"] += 1

    if weapon.element not in balance_statistics["WeaponElement"]:
        balance_statistics["WeaponElement"][weapon.element] = {
            "Used": 0,
            "Wins": 0
        }

    balance_statistics["WeaponElement"][weapon.element]["Used"] += 1
    if iswinner:
        balance_statistics["WeaponElement"][weapon.element]["Wins"] += 1

    if weapon.get_category() not in balance_statistics["WeaponCategory"]:
        balance_statistics["WeaponCategory"][weapon.get_category()] = {
            "Used": 0,
            "Wins": 0
        }

    balance_statistics["WeaponCategory"][weapon.get_category()]["Used"] += 1
    if iswinner:
        balance_statistics["WeaponCategory"][weapon.get_category()]["Wins"] += 1


def add_weapon_to_statistics(weapon, iswinner, data: StatisticsData):
    data.weapon_queue.put([weapon, iswinner])


def add_unit_to_statistics(unit, iswinner, data):
    for ability in unit.abilities:
        add_ability_to_statistics(ability, iswinner, data)
    add_weapon_to_statistics(unit.weapon, iswinner, data)


def get_winner_side_of_battle(battle):
    sides = []
    for unit in battle.activeunits:
        if unit.side not in sides:
            sides.append(unit.side)
    if len(sides) == 1:
        return sides[0]
    else:
        raise Exception("A battle went into statistics report without finishing!")


def add_finished_battle_to_statistics(battle, data):
    global battle_count
    battle_count += 1
    winnerside = get_winner_side_of_battle(battle)
    for unit in battle.allunits:
        add_unit_to_statistics(unit, unit.side == winnerside, data)


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def write_statistics_to_file(filename, battle_count):
    with open("Statistics/" + filename + ".txt", "w") as statistics_file:
        statistics_file.write(time.ctime() + "\n")
        statistics_file.write(" -- Balance Statistics --\n\n")
        statistics_file.write(f" (In {battle_count} battles)\n\n")
        for statisticcategory in balance_statistics:
            statistics_file.write(f" {statisticcategory}:\n")
            sortedresultlist = []
            for entry in balance_statistics[statisticcategory]:
                entrydata = balance_statistics[statisticcategory][entry]
                sortedresultlist.append({
                    "Entry": entry,
                    "WR": entrydata['Wins'] / entrydata['Used'],
                    "Used": entrydata["Used"]
                })

            sortedresultlist.sort(key=lambda x: x["WR"], reverse=True)
            for result in sortedresultlist:
                statistics_file.write(
                    f"{result['Entry']}: WR:{result['WR']:.2%} Used:{result['Used']}\n"
                )
            statistics_file.write("\n")
