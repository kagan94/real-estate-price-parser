import os
import sys
import unittest

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from parsers.kvee_parser import KvEeParser
from parsers.common import AddressComponents


class TestKvEeParser(unittest.TestCase):
    def setUp(self):
        self.parser = KvEeParser()

    def test_parse_address_components(self):
        """Test address parsing with various KvEe formats"""
        test_cases = [
            # Simple address without apartment number
            {
                "address": "Tallinn, Lasnamäe, Punane tn 27",
                "expected": AddressComponents("Tallinn", "Punane tn 27", None)
            },
            # Address with apartment number (space before dash)
            {
                "address": "Tallinn, Lasnamäe, Punane tn 21-1",
                "expected": AddressComponents("Tallinn", "Punane tn 21", "1")
            },
            # Address with extra neighborhood part
            {
                "address": "Tallinn, Lasnamäe, Varraku peatus, Punane tn 65",
                "expected": AddressComponents("Tallinn", "Punane tn 65", None)
            },
            # Address with apartment number and extra parts
            {
                "address": "Tallinn, Haabersti, Pikaliiva, Pikaliiva tn 5-26",
                "expected": AddressComponents("Tallinn", "Pikaliiva tn 5", "26")
            },
            # Address with fraction building number
            {
                "address": "Tallinn, Mustamäe, Uus-mustamäe, Aiandi 16/2-29",
                "expected": AddressComponents("Tallinn", "Aiandi 16/2", "29")
            },
            # Address with simple building number
            {
                "address": "Tallinn, Kesklinn, J. Kunderi tn 17",
                "expected": AddressComponents("Tallinn", "J. Kunderi tn 17", None)
            },
            # Address with dash in street name
            {
                "address": "Tallinn, Põhja-Tallinna linnaosa, Uus-Maleva tn 3",
                "expected": AddressComponents("Tallinn", "Uus-Maleva tn 3", None)
            },
            # Address with multiple extra parts
            {
                "address": "Tallinn, Kesklinn, Old Town, Vene tn 12-3",
                "expected": AddressComponents("Tallinn", "Vene tn 12", "3")
            },
            # Address with building number containing letters
            {
                "address": "Tallinn, Kesklinn, Pärnu mnt 26b-15",
                "expected": AddressComponents("Tallinn", "Pärnu mnt 26b", "15")
            },
            # Address with dash
            {
                "address": "Tallinn, Lasnamäe, Narva-test mnt 174b/2",
                "expected": AddressComponents("Tallinn", "Narva-test mnt 174b", "2")
            },
        ]

        for i, test_case in enumerate(test_cases):
            with self.subTest(i=i, address=test_case["address"]):
                result = self.parser.parse_address_components(test_case["address"])
                self.assertEqual(result, test_case["expected"])


if __name__ == '__main__':
    unittest.main()
