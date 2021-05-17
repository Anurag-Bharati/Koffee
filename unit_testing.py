import unittest

import level_generator
from main import level_data

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



