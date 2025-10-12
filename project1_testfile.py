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

    def test_calc_sales_by_shipmode_segment_mixed(self):
        # check three different shipping modes and different segments
        data = [
            ["Standard Class", "Corporate", "United States", "Mesa", "Arizona", "85204", "West", "Office Supplies", "Paper", "86.272", "4", "0.2", "31.2736"],
            ["Standard Class", "Corporate", "United States", "Mesa", "Arizona", "85204", "West", "Technology", "Phones", "263.96", "5", "0.2", "23.0965"],
            ["Second Class", "Corporate", "United States", "Salinas", "California", "93905", "West", "Office Supplies", "Labels", "427.42", "14", "0", "196.6132"],
            ["First Class", "Consumer", "United States", "Jackson", "Mississippi", "39212", "South", "Office Supplies", "Paper", "19.44", "3", "0", "9.3312"],
            ["Standard Class", "Consumer", "United States", "New York City", "New York", "10024", "East", "Office Supplies", "Art", "75.48", "2", "0", "19.6248"],
            ["Standard Class", "Consumer", "United States", "New York City", "New York", "10024", "East", "Furniture", "Furnishings", "39.98", "2", "0", "9.995"]
        ]

        expected = {
            "Corporate": {"Standard Class": 350.232, "Second Class": 427.42},
            "Consumer": {"First Class": 19.44, "Standard Class": 115.46}
        }
        self.assertEqual(calc_sales_by_shipmode_segment(data, self.column_dict), expected)

    def test_calc_sales_by_shipmode_segment_summing_multiple(self):
        # check all same segment and shipping mode
        data = [
            ["Standard Class", "Consumer", "United States", "Trenton", "Michigan", "48183", "Central", "Office Supplies", "Binders", "58.05", "3", "0", "26.703"],
            ["Standard Class", "Consumer", "United States", "Trenton", "Michigan", "48183", "Central", "Office Supplies", "Art", "56.98", "7", "0", "22.792"],
            ["Standard Class", "Consumer", "United States", "Trenton", "Michigan", "48183", "Central", "Furniture", "Furnishings", "157.74", "11", "0", "56.7864"],
            ["Standard Class", "Consumer", "United States", "Dallas", "Texas", "75220", "Central", "Office Supplies", "Paper", "3.528", "1", "0.2", "1.1466"],
            ["Standard Class", "Consumer", "United States", "Dallas", "Texas", "75220", "Central", "Office Supplies", "Paper", "4.624", "1", "0.2", "1.6762"]
        ]

        expected = {
            "Consumer": {"Standard Class": 280.922}  # 58.05 + 56.98 + 157.74 + 3.528 + 4.624
        }
        self.assertEqual(calc_sales_by_shipmode_segment(data, self.column_dict), expected)

    def test_calc_sales_by_shipmode_segment_multiple_segments_varied(self):
        # mized segments, same shipping mode
        data = [
            ["Same Day", "Corporate", "United States", "San Diego", "California", "92105", "West", "Furniture", "Tables", "567.12", "10", "0.2", "-28.356"],
            ["Same Day", "Home Office", "United States", "Smyrna", "Georgia", "30080", "South", "Technology", "Phones", "484.83", "3", "0", "126.0558"],
            ["Same Day", "Home Office", "United States", "Smyrna", "Georgia", "30080", "South", "Office Supplies", "Paper", "122.97", "3", "0", "60.2553"],
            ["Same Day", "Home Office", "United States", "Smyrna", "Georgia", "30080", "South", "Office Supplies", "Storage", "154.44", "3", "0", "1.5444"],
            ["Same Day", "Consumer", "United States", "Redlands", "California", "92374", "West", "Office Supplies", "Paper", "19.98", "1", "0", "9.3906"],
            ["Same Day", "Consumer", "United States", "Redlands", "California", "92374", "West", "Office Supplies", "Art", "5.04", "3", "0", "1.26"]
        ]
       
        expected = {
            "Corporate": {"Same Day": 567.12},
            "Home Office": {"Same Day": 762.24},  # 484.83 + 122.97 + 154.44
            "Consumer": {"Same Day": 25.02}       # 19.98 + 5.04
        }
        self.assertEqual(calc_sales_by_shipmode_segment(data, self.column_dict), expected)

    def test_calc_sales_by_shipmode_segment_with_bad_data(self):
        # missing data
        data = [
            ["Standard Class", "Corporate", "United States", "Green Bay", "Wisconsin", "54302", "Central", "Office Supplies", "Paper", "22.72", "4", "0", "10.224"],
            ["", "Consumer", "United States", "Los Angeles", "California", "90036", "West", "Furniture", "Furnishings", "", "2", "0", "5.4"],  # Missing ship mode + sales
            ["Second Class", "Home Office", "United States", "Costa Mesa", "California", "92627", "West", "Technology", "Accessories", "239.97", "3", "0", "26.3967"],
            ["First Class", "Corporate", "United States", "Houston", "Texas", "77041", "Central", "Technology", "Phones", "946.344", "7", "0.2", "118.293"],
            ["Standard Class", "Consumer", "United States", "Dallas", "Texas", "75220", "Central", "Office Supplies", "Supplies", "51.52", "5", "0.2", "-10.948"],
            ["Second Class", "Consumer", "United States", "Tulsa", "Oklahoma", "74133", "Central", "Office Supplies", "Binders", "42.81", "3", "0", "20.1207"],
            ["Second Class", "Consumer", "United States", "Tulsa", "Oklahoma", "74133", "Central", "Office Supplies", "Paper", "12.96", "2", "0", "6.2208"]
        ]
        
        expected = {
            "Corporate": {"Standard Class": 22.72, "First Class": 946.344},
            "Home Office": {"Second Class": 239.97},
            "Consumer": {"Standard Class": 51.52, "Second Class": 55.77}  # 42.81 + 12.96
        }
        self.assertEqual(calc_sales_by_shipmode_segment(data, self.column_dict), expected)

def main():
    unittest.main(verbosity=2)

if __name__ == '__main__':
    main()