# set up files, added samplesuperstore.csv to folder
import csv

def get_data(file):
    data = []
    # inFile = open(file)
    # csv_file = csv.reader(inFile)

    # headers = next(csv_file)
    # for row in csv_file:
    #     data.append(row)

    # inFile.close()
    # return headers, data #chat explained why i need to return headers
    with open(file) as fn:
        csv_file = csv.reader(fn)
        headers = next(csv_file)
        for row in csv_file:
            data.append(row)
    return data

column_dict = {
    "Ship Mode": 0, "Segment": 1, "Country": 2, "City": 3, "State": 4,
    "Postal Code": 5, "Region": 6, "Category": 7, "Sub-Category": 8,
    "Sales": 9, "Quantity": 10, "Discount": 11, "Profit": 12 
}

def calc_sales_by_shipmode_segment(data, column_dict):
    results = {}

    for row in data:
        segment = row[column_dict['Segment']]
        ship_mode = row[column_dict['Ship Mode']]
        sales = row[column_dict['Sales']]

        # checks if any column is blank, then skips
        if segment == "" or ship_mode == "" or sales == "":
            continue

        # make sure sales is a valid number so later i can be made a float
        if sales.replace('.', '', 1).isdigit() == False:
            continue

        sales = float(sales)

        # segment is outer key, ship_mode inner, sales is value
        if segment not in results:
            results[segment] = {}
        if ship_mode not in results[segment]:
            results[segment][ship_mode] = 0.0

        results[segment][ship_mode] += sales #was origibally just =, debugging with +=

    # round sales so it passes the tests
    for segment in results:
        for ship_mode in results[segment]:
            results[segment][ship_mode] = round(results[segment][ship_mode], 3)

    return results
    #pass