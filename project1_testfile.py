import unittest
import os
import csv
from main import calc_sales_by_shipmode_segment, calc_highvaluepercentage_city_category


class CalculationTests(unittest.TestCase):
    def setUp(self):
        self.column_dict = {
            "Ship Mode": 0, "Segment": 1, "Country": 2, "City": 3, "State": 4,
            "Postal Code": 5, "Region": 6, "Category": 7, "Sub-Category": 8,
            "Sales": 9, "Quantity": 10, "Discount": 11, "Profit": 12 
        }

    def test_calc_sales_by_shipmode_segment_1(self):
        data = [
            {"Ship Mode": "Second Class", "Segment": "Consumer", "Sales": "100.0"},
            {"Ship Mode": "First Class", "Segment": "Consumer", "Sales": "200.0"},
            {"Ship Mode": "Second Class", "Segment": "Corporate", "Sales": "300.0"}
        ]
        expected = {
            "Consumer": {"Second Class": 100.0, "First Class": 200.0},
            "Corporate": {"Second Class": 300.0}
        }
        self.assertEqual(calc_sales_by_shipmode_segment(data, self.column_dict), expected)

    def test_calc_sales_by_shipmode_segment_2(self):
        data = [
            {"Ship Mode": "Standard Class", "Segment": "Corporate", "Country": "United States", "City": "New York City", "State": "New York", "Region": "East", "Category": "Technology", "Sub-Category": "Phones", "Sales": "1029.95"},
            {"Ship Mode": "First Class", "Segment": "Consumer", "Country": "United States", "City": "Troy", "State": "New York", "Region": "East", "Category": "Office Supplies", "Sub-Category": "Storage", "Sales": "208.56"},
            {"Ship Mode": "First Class", "Segment": "Consumer", "Country": "United States", "City": "Troy", "State": "New York", "Region": "East", "Category": "Office Supplies", "Sub-Category": "Paper", "Sales": "32.4"},
            {"Ship Mode": "First Class", "Segment": "Consumer", "Country": "United States", "City": "Troy", "State": "New York", "Region": "East", "Category": "Furniture", "Sub-Category": "Chairs", "Sales": "319.41"},
            {"Ship Mode": "First Class", "Segment": "Consumer", "Country": "United States", "City": "Troy", "State": "New York", "Region": "East", "Category": "Office Supplies", "Sub-Category": "Paper", "Sales": "14.56"},
            {"Ship Mode": "First Class", "Segment": "Consumer", "Country": "United States", "City": "Troy", "State": "New York", "Region": "East", "Category": "Technology", "Sub-Category": "Accessories", "Sales": "30"},
            {"Ship Mode": "First Class", "Segment": "Consumer", "Country": "United States", "City": "Troy", "State": "New York", "Region": "East", "Category": "Office Supplies", "Sub-Category": "Binders", "Sales": "48.48"},
            {"Ship Mode": "First Class", "Segment": "Consumer", "Country": "United States", "City": "Troy", "State": "New York", "Region": "East", "Category": "Office Supplies", "Sub-Category": "Art", "Sales": "1.68"},
            {"Ship Mode": "Standard Class", "Segment": "Consumer", "Country": "United States", "City": "Los Angeles", "State": "California", "Region": "West", "Category": "Technology", "Sub-Category": "Accessories", "Sales": "13.98"},
            {"Ship Mode": "Standard Class", "Segment": "Consumer", "Country": "United States", "City": "Los Angeles", "State": "California", "Region": "West", "Category": "Office Supplies", "Sub-Category": "Binders", "Sales": "25.824"},
            {"Ship Mode": "Standard Class", "Segment": "Consumer", "Country": "United States", "City": "Los Angeles", "State": "California", "Region": "West", "Category": "Office Supplies", "Sub-Category": "Paper", "Sales": "146.73"},
            {"Ship Mode": "Standard Class", "Segment": "Consumer", "Country": "United States", "City": "Los Angeles", "State": "California", "Region": "West", "Category": "Furniture", "Sub-Category": "Furnishings", "Sales": "79.76"}
        ]
        result = calc_sales_by_shipmode_segment(data, self.column_dict)
        self.assertAlmostEqual(result["Consumer"]["First Class"], 655.09, places=2)
        self.assertAlmostEqual(result["Consumer"]["Standard Class"], 266.294, places=2)
        self.assertAlmostEqual(result["Corporate"]["Standard Class"], 1029.95, places=2)

    def test_calc_sales_by_shipmode_segment_empty(self):
        data = []
        expected = {}
        self.assertEqual(calc_sales_by_shipmode_segment(data, self.column_dict), expected)

    def test_calc_sales_by_shipmode_segment_4(self):
        data = [
            {"Ship Mode": "Standard Class", "Segment": "Corporate", "City": "Mesa", "State": "Arizona", "Region": "West", "Category": "Office Supplies", "Sub-Category": "Paper", "Sales": "86.272"},
            {"Ship Mode": "Standard Class", "Segment": "Corporate", "City": "Mesa", "State": "Arizona", "Region": "West", "Category": "Technology", "Sub-Category": "Phones", "Sales": "263.96"},
            {"Ship Mode": "Second Class", "Segment": "Corporate", "City": "Salinas", "State": "California", "Region": "West", "Category": "Office Supplies", "Sub-Category": "Labels", "Sales": "427.42"},
            {"Ship Mode": "First Class", "Segment": "Consumer", "City": "Jackson", "State": "Mississippi", "Region": "South", "Category": "Office Supplies", "Sub-Category": "Paper", "Sales": "19.44"},
            {"Ship Mode": "Standard Class", "Segment": "Consumer", "City": "New York City", "State": "New York", "Region": "East", "Category": "Office Supplies", "Sub-Category": "Art", "Sales": "75.48"},
            {"Ship Mode": "Standard Class", "Segment": "Consumer", "City": "New York City", "State": "New York", "Region": "East", "Category": "Furniture", "Sub-Category": "Furnishings", "Sales": "39.98"}
        ]
        expected = {
            "Corporate": {"Standard Class": 350.232, "Second Class": 427.42},
            "Consumer": {"First Class": 19.44, "Standard Class": 115.46}
        }
        self.assertEqual(calc_sales_by_shipmode_segment(data, self.column_dict), expected)

    def test_calc_sales_by_shipmode_segment_5(self):
        data = [
            {"Ship Mode": "Standard Class", "Segment": "Consumer", "City": "Trenton", "State": "Michigan", "Region": "Central", "Category": "Office Supplies", "Sub-Category": "Binders", "Sales": "58.05"},
            {"Ship Mode": "Standard Class", "Segment": "Consumer", "City": "Trenton", "State": "Michigan", "Region": "Central", "Category": "Office Supplies", "Sub-Category": "Art", "Sales": "56.98"},
            {"Ship Mode": "Standard Class", "Segment": "Consumer", "City": "Trenton", "State": "Michigan", "Region": "Central", "Category": "Furniture", "Sub-Category": "Furnishings", "Sales": "157.74"},
            {"Ship Mode": "Standard Class", "Segment": "Consumer", "City": "Dallas", "State": "Texas", "Region": "Central", "Category": "Office Supplies", "Sub-Category": "Paper", "Sales": "3.528"},
            {"Ship Mode": "Standard Class", "Segment": "Consumer", "City": "Dallas", "State": "Texas", "Region": "Central", "Category": "Office Supplies", "Sub-Category": "Paper", "Sales": "4.624"}
        ]
        expected = {"Consumer": {"Standard Class": 280.922}}
        self.assertEqual(calc_sales_by_shipmode_segment(data, self.column_dict), expected)

    def test_calc_sales_by_shipmode_segment_multiple_segments_6(self):
        data = [
            {"Ship Mode": "Same Day", "Segment": "Corporate", "City": "San Diego", "State": "California", "Region": "West", "Category": "Furniture", "Sub-Category": "Tables", "Sales": "567.12"},
            {"Ship Mode": "Same Day", "Segment": "Home Office", "City": "Smyrna", "State": "Georgia", "Region": "South", "Category": "Technology", "Sub-Category": "Phones", "Sales": "484.83"},
            {"Ship Mode": "Same Day", "Segment": "Home Office", "City": "Smyrna", "State": "Georgia", "Region": "South", "Category": "Office Supplies", "Sub-Category": "Paper", "Sales": "122.97"},
            {"Ship Mode": "Same Day", "Segment": "Home Office", "City": "Smyrna", "State": "Georgia", "Region": "South", "Category": "Office Supplies", "Sub-Category": "Storage", "Sales": "154.44"},
            {"Ship Mode": "Same Day", "Segment": "Consumer", "City": "Redlands", "State": "California", "Region": "West", "Category": "Office Supplies", "Sub-Category": "Paper", "Sales": "19.98"},
            {"Ship Mode": "Same Day", "Segment": "Consumer", "City": "Redlands", "State": "California", "Region": "West", "Category": "Office Supplies", "Sub-Category": "Art", "Sales": "5.04"}
        ]
        expected = {
            "Corporate": {"Same Day": 567.12},
            "Home Office": {"Same Day": 762.24},
            "Consumer": {"Same Day": 25.02}
        }
        self.assertEqual(calc_sales_by_shipmode_segment(data, self.column_dict), expected)

    def test_calc_sales_by_shipmode_segment_bad_data(self):
        data = [
            {"Ship Mode": "Standard Class", "Segment": "Corporate", "City": "Green Bay", "State": "Wisconsin", "Region": "Central", "Category": "Office Supplies", "Sub-Category": "Paper", "Sales": "22.72"},
            {"Ship Mode": "", "Segment": "Consumer", "City": "Los Angeles", "State": "California", "Region": "West", "Category": "Furniture", "Sub-Category": "Furnishings", "Sales": ""},
            {"Ship Mode": "Second Class", "Segment": "Home Office", "City": "Costa Mesa", "State": "California", "Region": "West", "Category": "Technology", "Sub-Category": "Accessories", "Sales": "239.97"},
            {"Ship Mode": "First Class", "Segment": "Corporate", "City": "Houston", "State": "Texas", "Region": "Central", "Category": "Technology", "Sub-Category": "Phones", "Sales": "946.344"},
            {"Ship Mode": "Standard Class", "Segment": "Consumer", "City": "Dallas", "State": "Texas", "Region": "Central", "Category": "Office Supplies", "Sub-Category": "Supplies", "Sales": "51.52"},
            {"Ship Mode": "Second Class", "Segment": "Consumer", "City": "Tulsa", "State": "Oklahoma", "Region": "Central", "Category": "Office Supplies", "Sub-Category": "Binders", "Sales": "42.81"},
            {"Ship Mode": "Second Class", "Segment": "Consumer", "City": "Tulsa", "State": "Oklahoma", "Region": "Central", "Category": "Office Supplies", "Sub-Category": "Paper", "Sales": "12.96"}
        ]
        expected = {
            "Corporate": {"Standard Class": 22.72, "First Class": 946.344},
            "Home Office": {"Second Class": 239.97},
            "Consumer": {"Standard Class": 51.52, "Second Class": 55.77}
        }
        self.assertEqual(calc_sales_by_shipmode_segment(data, self.column_dict), expected)

    # --- High Value Percentage Tests ---

    def test_highvalue_1(self):
        # there are 0 high value sales
        data = [
            {"Ship Mode": "Standard Class", "Segment": "Consumer", "City": "Houston", "State": "Texas", "Region": "Central", "Category": "Office Supplies", "Sub-Category": "Binders", "Sales": "26.046"},
            {"Ship Mode": "Standard Class", "Segment": "Consumer", "City": "Houston", "State": "Texas", "Region": "Central", "Category": "Office Supplies", "Sub-Category": "Storage", "Sales": "32.544"},
            {"Ship Mode": "Standard Class", "Segment": "Consumer", "City": "Houston", "State": "Texas", "Region": "Central", "Category": "Technology", "Sub-Category": "Phones", "Sales": "122.92"}
        ]
        expected = [
            {'city': 'Houston', 'category': 'Office Supplies', 'total_sales': 2, 'high_value_sales': 0, 'high_value_percentage': 0.0},
            {'city': 'Houston', 'category': 'Technology', 'total_sales': 1, 'high_value_sales': 0, 'high_value_percentage': 0.0}
        ]
        self.assertEqual(calc_highvaluepercentage_city_category(data, self.column_dict), expected)

    def test_calc_highvalue_2(self):
        data = [
            {"Ship Mode": "Standard Class", "Segment": "Consumer", "City": "Los Angeles", "State": "California", "Region": "West", "Category": "Technology", "Sub-Category": "Copiers", "Sales": "3359.952"},
            {"Ship Mode": "Standard Class", "Segment": "Consumer", "City": "Los Angeles", "State": "California", "Region": "West", "Category": "Office Supplies", "Sub-Category": "Paper", "Sales": "42.8"},
            {"Ship Mode": "Standard Class", "Segment": "Consumer", "City": "Los Angeles", "State": "California", "Region": "West", "Category": "Technology", "Sub-Category": "Accessories", "Sales": "248.85"}
        ]
        expected = [
            {'city': 'Los Angeles', 'category': 'Technology', 'total_sales': 2, 'high_value_sales': 1, 'high_value_percentage': 50.0},
            {'city': 'Los Angeles', 'category': 'Office Supplies', 'total_sales': 1, 'high_value_sales': 0, 'high_value_percentage': 0.0}
        ]
        self.assertEqual(calc_highvaluepercentage_city_category(data, self.column_dict), expected)

    def test_calc_highvalue_3(self):
        data = [
            {"Ship Mode": "Same Day", "Segment": "Corporate", "City": "San Francisco", "State": "California", "Region": "West", "Category": "Technology", "Sub-Category": "Machines", "Sales": "1919.976"},
            {"Ship Mode": "Second Class", "Segment": "Corporate", "City": "Provo", "State": "Utah", "Region": "West", "Category": "Furniture", "Sub-Category": "Bookcases", "Sales": "1292.94"},
            {"Ship Mode": "First Class", "Segment": "Home Office", "City": "New York City", "State": "New York", "Region": "East", "Category": "Technology", "Sub-Category": "Machines", "Sales": "1704.89"}
        ]
        expected = [
            {'city': 'San Francisco', 'category': 'Technology', 'total_sales': 1, 'high_value_sales': 1, 'high_value_percentage': 100.0},
            {'city': 'Provo', 'category': 'Furniture', 'total_sales': 1, 'high_value_sales': 1, 'high_value_percentage': 100.0},
            {'city': 'New York City', 'category': 'Technology', 'total_sales': 1, 'high_value_sales': 1, 'high_value_percentage': 100.0}
        ]
        self.assertEqual(calc_highvaluepercentage_city_category(data, self.column_dict), expected)

    def test_highvalue_4(self):
        data = [
            {"Ship Mode": "Standard Class", "Segment": "Consumer", "City": "Houston", "State": "Texas", "Region": "Central", "Category": "Furniture", "Sub-Category": "Chairs", "Sales": "1500"},
            {"Ship Mode": "Standard Class", "Segment": "Consumer", "City": "Dallas", "State": "Texas", "Region": "Central", "Category": "Technology", "Sub-Category": "Phones", "Sales": "3000"},
            {"Ship Mode": "Standard Class", "Segment": "Consumer", "City": "Dallas", "State": "Texas", "Region": "Central", "Category": "Furniture", "Sub-Category": "Tables", "Sales": "700"}
        ]
        expected = [
            {'city': 'Houston', 'category': 'Furniture', 'total_sales': 1, 'high_value_sales': 1, 'high_value_percentage': 100.0},
            {'city': 'Dallas', 'category': 'Technology', 'total_sales': 1, 'high_value_sales': 1, 'high_value_percentage': 100.0},
            {'city': 'Dallas', 'category': 'Furniture', 'total_sales': 1, 'high_value_sales': 0, 'high_value_percentage': 0.0}
        ]
        result = calc_highvaluepercentage_city_category(data, self.column_dict)
        self.assertEqual(result, expected)

    def test_highvalue_5(self):
        data = [
            {"Ship Mode": "Standard Class", "Segment": "Consumer", "City": "Houston", "State": "Texas", "Region": "Central", "Category": "Furniture", "Sub-Category": "Chairs", "Sales": "abc"},
            {"Ship Mode": "Standard Class", "Segment": "Consumer", "City": "", "State": "Texas", "Region": "Central", "Category": "Technology", "Sub-Category": "Phones", "Sales": "1500"},
            {"Ship Mode": "Standard Class", "Segment": "Consumer", "City": "Houston", "State": "Texas", "Region": "Central", "Category": "", "Sub-Category": "Storage", "Sales": "2000"}
        ]
        expected = []
        result = calc_highvaluepercentage_city_category(data, self.column_dict)
        self.assertEqual(result, expected)

    def test_highvalue_6(self):
        data = [
            {"Ship Mode": "Standard Class", "Segment": "Consumer", "City": "Houston", "State": "Texas", "Region": "Central", "Category": "Office Supplies", "Sub-Category": "Binders", "Sales": "26.046"},
            {"Ship Mode": "Standard Class", "Segment": "Consumer", "City": "Houston", "State": "Texas", "Region": "Central", "Category": "Office Supplies", "Sub-Category": "Storage", "Sales": "32.544"},
            {"Ship Mode": "Standard Class", "Segment": "Consumer", "City": "Houston", "State": "Texas", "Region": "Central", "Category": "Technology", "Sub-Category": "Phones", "Sales": "122.92"},
            {"Ship Mode": "Standard Class", "Segment": "Consumer", "City": "Houston", "State": "Texas", "Region": "Central", "Category": "Furniture", "Sub-Category": "Chairs", "Sales": "1500"}
        ]
        expected = [
            {'city': 'Houston', 'category': 'Office Supplies', 'total_sales': 2, 'high_value_sales': 0, 'high_value_percentage': 0.0},
            {'city': 'Houston', 'category': 'Technology', 'total_sales': 1, 'high_value_sales': 0, 'high_value_percentage': 0.0},
            {'city': 'Houston', 'category': 'Furniture', 'total_sales': 1, 'high_value_sales': 1, 'high_value_percentage': 100.0}
        ]
        result = calc_highvaluepercentage_city_category(data, self.column_dict)
        self.assertEqual(result, expected)

    def test_highvalue_7(self):
        data = [
            {"Ship Mode": "Standard Class", "Segment": "Consumer", "City": "Chicago", "State": "Illinois", "Region": "Central", "Category": "Technology", "Sub-Category": "Phones", "Sales": "1,500"},
            {"Ship Mode": "Standard Class", "Segment": "Consumer", "City": "Chicago", "State": "Illinois", "Region": "Central", "Category": "Furniture", "Sub-Category": "Chairs", "Sales": "950"},
            {"Ship Mode": "Standard Class", "Segment": "Consumer", "City": "Chicago", "State": "Illinois", "Region": "Central", "Category": "Office Supplies", "Sub-Category": "Paper", "Sales": "NaN"}
        ]
        expected = [
            {'city': 'Chicago', 'category': 'Furniture', 'total_sales': 1, 'high_value_sales': 0, 'high_value_percentage': 0.0}
        ]
        result = calc_highvaluepercentage_city_category(data, self.column_dict)
        self.assertEqual(result, expected)

    def test_highvalue_8(self):
        data = [
            {"Ship Mode": "Standard Class", "Segment": "Consumer", "City": "Boston", "State": "Massachusetts", "Region": "East", "Category": "Technology", "Sub-Category": "Accessories", "Sales": "1000"},
            {"Ship Mode": "Standard Class", "Segment": "Consumer", "City": "Boston", "State": "Massachusetts", "Region": "East", "Category": "Furniture", "Sub-Category": "Tables", "Sales": "1200"}
        ]
        expected = [
            {'city': 'Boston', 'category': 'Technology', 'total_sales': 1, 'high_value_sales': 0, 'high_value_percentage': 0.0},
            {'city': 'Boston', 'category': 'Furniture', 'total_sales': 1, 'high_value_sales': 1, 'high_value_percentage': 100.0}
        ]
        result = calc_highvaluepercentage_city_category(data, self.column_dict)
        self.assertEqual(result, expected)


def main():
    unittest.main(verbosity=2)

if __name__ == '__main__':
    main()



def main():
    unittest.main(verbosity=2)

if __name__ == '__main__':
    main()