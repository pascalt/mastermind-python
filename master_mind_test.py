import unittest
from mastermindgame import MasterMindGame


class MasterMindTest(unittest.TestCase):
    def test_evaluate(self):

        mg = MasterMindGame(10, 6, 4)
        mg.code_played = [[1, 1, 1, 1]]
        mg.secret_code = [1, 1, 1, 1]
        mg.evaluate()
        print(mg.secret_code)
        print(mg.code_played)

        self.assertEqual(mg.nb_right_places, 4)
        self.assertEqual(mg.nb_wrong_places, 0)

        mg = MasterMindGame(10, 6, 4)
        mg.code_played = [[2, 2, 2, 2]]
        mg.secret_code = [1, 1, 1, 1]
        mg.evaluate()
        print(mg.secret_code)
        print(mg.code_played)

        self.assertEqual(mg.nb_right_places, 0)
        self.assertEqual(mg.nb_wrong_places, 0)

        mg = MasterMindGame(10, 6, 4)
        mg.code_played = [[2, 1, 2, 1]]
        mg.secret_code = [1, 2, 1, 2]
        mg.evaluate()
        print(mg.secret_code)
        print(mg.code_played)

        self.assertEqual(mg.nb_right_places, 0)
        self.assertEqual(mg.nb_wrong_places, 4)

        mg = MasterMindGame(10, 6, 4)
        mg.code_played = [[3, 5, 2, 1]]
        mg.secret_code = [5, 3, 2, 6]
        mg.evaluate()
        print(mg.secret_code)
        print(mg.code_played)

        self.assertEqual(mg.nb_right_places, 1)
        self.assertEqual(mg.nb_wrong_places, 2)

        mg = MasterMindGame(10, 6, 4)
        mg.code_played = [[1, 2, 2, 2]]
        mg.secret_code = [1, 3, 3, 3]
        mg.evaluate()
        print(mg.secret_code)
        print(mg.code_played)

        self.assertEqual(mg.nb_right_places, 1)
        self.assertEqual(mg.nb_wrong_places, 0)

        mg = MasterMindGame(10, 6, 4)
        mg.code_played = [[1, 2, 2, 2]]
        mg.secret_code = [1, 1, 3, 3]
        mg.evaluate()
        print(mg.secret_code)
        print(mg.code_played)

        self.assertEqual(mg.nb_right_places, 1)
        self.assertEqual(mg.nb_wrong_places, 0)

        mg = MasterMindGame(10, 6, 4)
        mg.code_played = [[1, 2, 2, 2]]
        mg.secret_code = [5, 1, 3, 3]
        mg.evaluate()
        print(mg.secret_code)
        print(mg.code_played)

        self.assertEqual(mg.nb_right_places, 0)
        self.assertEqual(mg.nb_wrong_places, 1)

        mg = MasterMindGame(10, 6, 4)
        mg.code_played = [[0, 0, 1, 1]]
        mg.secret_code = [2, 0, 5, 0]
        mg.evaluate()
        print(mg.secret_code)
        print(mg.code_played)

        self.assertEqual(mg.nb_right_places, 1)
        self.assertEqual(mg.nb_wrong_places, 1)


if __name__ == '__main__':
    unittest.main()
