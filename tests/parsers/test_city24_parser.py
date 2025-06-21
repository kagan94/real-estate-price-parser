import unittest
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from parsers.city24_parser import City24Parser
from parsers.common import AddressComponents


class TestCity24Parser(unittest.TestCase):
    def setUp(self):
        self.parser = City24Parser()

    def test_parse_address_components(self):
        """Test address parsing with various formats"""
        test_cases = [
            # Simple address without apartment number
            {
                "address": "Tallinn, Lasnamäe linnaosa, Punane tn-15",
                "expected": AddressComponents("Tallinn", "Punane tn 15", None)
            },
            # Address with apartment number in fraction format
            {
                "address": "Tallinn, Põhja-Tallinna linnaosa, Kalaranna tn-8/8",
                "expected": AddressComponents("Tallinn", "Kalaranna tn 8", "8")
            },
            # Address with building number containing letter
            {
                "address": "Tallinn, Kesklinna linnaosa, Pirita tee-26b/4",
                "expected": AddressComponents("Tallinn", "Pirita tee 26b", "4")
            },
            # Address with dash in street name
            {
                "address": "Tallinn, Põhja-Tallinna linnaosa, Uus-Maleva tn-3",
                "expected": AddressComponents("Tallinn", "Uus-Maleva tn 3", None)
            },
            # Address with fraction apartment number
            {
                "address": "Tallinn, Kesklinna linnaosa, Tiiu tn-12/3",
                "expected": AddressComponents("Tallinn", "Tiiu tn 12", "3")
            },
            # Building numbers with letters
            {
                "address": "Tallinn, Kesklinn, Pirita tee-26f",
                "expected": AddressComponents("Tallinn", "Pirita tee 26f", None)
            },
            # Address without dash
            {
                "address": "Tallinn, Kesklinn, Pärnu mnt 123",
                "expected": AddressComponents("Tallinn", "Pärnu mnt 123", None)
            },
            # Edge case: address with neighborhood dash
            {
                "address": "Tallinn, Põhja-Tallinna linnaosa, Põhja pst-23",
                "expected": AddressComponents("Tallinn", "Põhja pst 23", None)
            },
        ]
        
        for i, test_case in enumerate(test_cases):
            with self.subTest(i=i, address=test_case["address"]):
                result = self.parser.parse_address_components(test_case["address"])
                self.assertEqual(result, test_case["expected"])


if __name__ == '__main__':
    unittest.main() 