import unittest

import sidereal.ships

class ShipCreationTestCase(unittest.TestCase):
    def test_json_creation(self):
        # Tests the ship creation
        ship = sidereal.ships.Ship.create_from_json(sidereal.ships._examplejson)
        self.assertEqual(ship.mass,5000)

_loader = unittest.TestLoader()
suite = _loader.loadTestsFromTestCase(ShipCreationTestCase)


if __name__=='__main__':
    unittest.main()

