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
        # test that it returns a nested dictionary with the segment, shipping class, and sale
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

    def test_calc_sales_by_shipmode_segment_2(self):
        # check that it adds the data from multiple rows
        data = [
            ["Standard Class","Corporate","United States","New York City","New York","10024","East","Technology","Phones","1029.95","5","0","298.6855"],
            ["First Class","Consumer","United States","Troy","New York","12180","East","Office Supplies","Storage","208.56","6","0","52.14"],
            ["First Class","Consumer","United States","Troy","New York","12180","East","Office Supplies","Paper","32.4","5","0","15.552"],
            ["First Class","Consumer","United States","Troy","New York","12180","East","Furniture","Chairs","319.41","5","0.1","7.098"],
            ["First Class","Consumer","United States","Troy","New York","12180","East","Office Supplies","Paper","14.56","2","0","6.9888"],
            ["First Class","Consumer","United States","Troy","New York","12180","East","Technology","Accessories","30","2","0","3.3"],
            ["First Class","Consumer","United States","Troy","New York","12180","East","Office Supplies","Binders","48.48","4","0.2","16.362"],
            ["First Class","Consumer","United States","Troy","New York","12180","East","Office Supplies","Art","1.68","1","0","0.84"],
            ["Standard Class","Consumer","United States","Los Angeles","California","90004","West","Technology","Accessories","13.98","2","0","6.1512"],
            ["Standard Class","Consumer","United States","Los Angeles","California","90004","West","Office Supplies","Binders","25.824","6","0.2","9.3612"],
            ["Standard Class","Consumer","United States","Los Angeles","California","90004","West","Office Supplies","Paper","146.73","3","0","68.9631"],
            ["Standard Class","Consumer","United States","Los Angeles","California","90004","West","Furniture","Furnishings","79.76","4","0","22.3328"]
        ]
        expected = {
            "Corporate": {"Standard Class": 1029.95},
            "Consumer": {"First Class": 655.09, "Standard Class": 266.294}
        }
        #self.assertEqual(calc_sales_by_shipmode_segment(data, self.column_dict), expected)
        result = calc_sales_by_shipmode_segment(data, self.column_dict)
        self.assertAlmostEqual(result["Consumer"]["First Class"], 655.09, places=2)
        self.assertAlmostEqual(result["Consumer"]["Standard Class"], 266.294, places=2)
        self.assertAlmostEqual(result["Corporate"]["Standard Class"], 1029.95, places=2)

    def test_calc_sales_by_shipmode_segment_empty(self):
        # checks if the data is empty
        data = []
        expected = {}
        self.assertEqual(calc_sales_by_shipmode_segment(data, self.column_dict), expected)


def main():
    unittest.main(verbosity=2)

if __name__ == '__main__':
    main()