import unittest

import level_generator
import main
from main import level_data
import IO

actualNumber = 0


def var_collector(level_list):

    global actualNumber
    in_row = 0
    for row in level_list:
        in_col = 0
        for numbers in row:
            if numbers == 7:
                actualNumber += 1
            in_col += 1
        in_row += 1
    return actualNumber


class TestMain(unittest.TestCase):

    def test_slimeCount(self):

        var_collector(level_data)

        self.assertEqual(level_generator.slime_quantity, actualNumber)

        print(f"{level_generator.slime_quantity} entity's were loaded and the map has {actualNumber}. ")

    def test_ifSprites(self): # Checks if sprite group is empty
        self.assertEqual(main.cleanup(), True)

    def test_ifKnightAlive(self):   # PLayer should not load initially so this test should fail
        status = main.renderer()
        self.assertEqual(False, status)

    def test_ifStartingLevel(self): # Starting level should be one so this test should fail
        level = main.current_level
        actual = 2
        self.assertEqual(actual, level)

    def test_ifData_stored(self): # Loads data from save.txt unpickle it searches and returns same
        actualList =[2,1,1,8]
        IO.init("anurag")
        data = IO.start([main.score, main.coin, main.coffee, main.timePlayed])
        self.assertListEqual(data, actualList)
