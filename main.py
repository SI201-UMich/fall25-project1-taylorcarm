# set up files, added samplesuperstore.csv to folder
import csv

#name: Carmela Taylor
#umid: 58771562
#email: carmelat@umich.edu
#collaborators: Kristen May & Katia Hemphill 
#GenAI to help debug, explain some function logic, and help with expected values for test cases

# def get_data(file):
#     data = []
#     # inFile = open(file)
#     # csv_file = csv.reader(inFile)

#     # headers = next(csv_file)
#     # for row in csv_file:
#     #     data.append(row)

#     # inFile.close()
#     # return headers, data #chat explained why i need to return headers
#     with open(file) as fn:
#         csv_file = csv.reader(fn)
#         headers = next(csv_file)
#         for row in csv_file:
#             data.append(row)
#     return data

def get_data(file):
    with open(file) as fn:
        csv_reader = csv.DictReader(fn)
        data = [row for row in csv_reader]
    return data

column_dict = {
    "Ship Mode": 0, "Segment": 1, "Country": 2, "City": 3, "State": 4,
    "Postal Code": 5, "Region": 6, "Category": 7, "Sub-Category": 8,
    "Sales": 9, "Quantity": 10, "Discount": 11, "Profit": 12 
}

def calc_sales_by_shipmode_segment(data, column_dict):
    results = {}

    # for row in data:
    #     if isinstance(row, dict):
    #         segment = row.get('Segment', "")
    #         ship_mode = row.get('Ship Mode', "")
    #         sales = row.get('Sales', "")
    #     else:
    #         segment = row[column_dict['Segment']]
    #         ship_mode = row[column_dict['Ship Mode']]
    #         sales = row[column_dict['Sales']]

    for row in data:
        # segment = row[column_dict['Segment']]
        # ship_mode = row[column_dict['Ship Mode']]
        # sales = row[column_dict['Sales']]
        # for dictionaries:
        # segment = row['Segment']
        # ship_mode = row['Ship Mode']
        # sales = row['Sales']
        if isinstance(row, dict):
            segment = row.get('Segment', "")
            ship_mode = row.get('Ship Mode', "")
            sales = row.get('Sales', "")
        else:
            segment = row[column_dict['Segment']]
            ship_mode = row[column_dict['Ship Mode']]
            sales = row[column_dict['Sales']]

        # checks if any column is blank, then skips
        if segment == "" or ship_mode == "" or sales == "":
            continue

        # make sure sales is a valid number so later it can be made a float (this was a problem in tests)
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

def calc_highvaluepercentage_city_category(data, column_dict):
    results = []
    counts = {}
    highsales_threshold = 1000


    for row in data:
        # city = row[column_dict['City']]
        # category = row[column_dict['Category']]
        # sales = row[column_dict['Sales']]

        # for dictionaries
        # city = row['City']
        # category = row['Category']
        # sales = row['Sales']

        if isinstance(row, dict):
            city = row.get('City', "")
            category = row.get('Category', "")
            sales = row.get('Sales', "")
        else:
            city = row[column_dict['City']]
            category = row[column_dict['Category']]
            sales = row[column_dict['Sales']]

        if city == "" or category == "" or sales =="":
            continue
        if sales.replace('.', '', 1).isdigit() == False:
            continue

        sales = float(sales)
        key = (city, category)

        if key not in counts:
            counts[key] = {'total': 0, 'high_value': 0}

        counts[key]['total'] += 1

        if sales > highsales_threshold:
            counts[key]['high_value'] += 1

    for (city, category), values in counts.items():
        total = values['total']
        high_value = values['high_value']
        percentage = (high_value / total) * 100

        results.append({'city': city, 'category': category, 'total_sales': total, 
                            'high_value_sales': high_value, 'high_value_percentage': round(percentage, 2)})

    return results

    #pass

def write_shipmode_segment_to_csv(filename, ndict):
    outFile = open(filename, "w")
    csv_writer = csv.writer(outFile)

    csv_writer.writerow(['Segment', 'Ship Mode', 'Total Sales'])

    for segment in ndict:
        inner_d = ndict[segment]  
        for ship_mode in inner_d:
            total_sales = inner_d[ship_mode]
            out_list = [segment, ship_mode, total_sales]
            csv_writer.writerow(out_list)

    outFile.close()

def write_highvaluepercentage_to_csv(filename, listdict):
    outFile = open(filename, "w")
    csv_writer = csv.writer(outFile)

    csv_writer.writerow(['City', 'Category', 'Total Sales', 'High Value Sales', 'High Value %'])

    for item in listdict:
        out_list = [
            item['city'],
            item['category'],
            item['total_sales'],
            item['high_value_sales'],
            item['high_value_percentage']
        ]
        csv_writer.writerow(out_list)

    outFile.close()

def main():
    data = get_data("SampleSuperstore.csv")

    results1 = calc_sales_by_shipmode_segment(data, column_dict)
    results2 = calc_highvaluepercentage_city_category(data, column_dict)

    write_shipmode_segment_to_csv("shipmode_segment_results.csv", results1)
    write_highvaluepercentage_to_csv("highvalue_results.csv", results2)

    print("Results written to both CSV files successfully!")

if __name__ == '__main__':
    main()