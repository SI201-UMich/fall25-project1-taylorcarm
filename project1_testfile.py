import unittest
import os
import csv
from main import calc_sales_by_shipmode_segment

class CalculationTests(unittest.TestCase):
    def setUp(self):
        self.column_dict = {
            "Ship Mode": 0, "Segment": 1, "Country": 2, "City": 3, "State": 4,
            "Postal Code": 5, "Region": 6, "Category": 7, "Sub-Category": 8,
            "Sales": 9, "Quantity": 10, "Discount": 11, "Profit": 12 
        }

    def test_calc_sales_by_shipmode_segment_1(self):
        data = [
            ["Second Class", "Consumer", "", "", "", "", "", "", "", "100.0", "", "", ""],
            ["First Class", "Consumer", "", "", "", "", "", "", "", "200.0", "", "", ""],
            ["Second Class", "Corporate", "", "", "", "", "", "", "", "300.0", "", "", ""],
        ]
        expected = {
            "Consumer": {"Second Class": 100.0, "First Class": 200.0},
            "Corporate": {"Second Class": 300.0}
        }
        self.assertEqual(calc_sales_by_shipmode_segment(data, self.column_dict), expected)


def main():
    unittest.main(verbosity=2)

if __name__ == '__main__':
    main()