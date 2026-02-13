from BattleSystem import Battle
from TestStatistics import launch_test_cycles

STATISTICS_TEST_MODE = True


if __name__ == "__main__":
    if STATISTICS_TEST_MODE:
        launch_test_cycles()
    else:
        battle = Battle(1)
        battle.start_battle()