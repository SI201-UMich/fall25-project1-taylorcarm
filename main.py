# set up files, added samplesuperstore.csv to folder
import csv

#name: Carmela Taylor
#umid: 58771562
#email: carmelat@umich.edu
#collaborators: me!
#GenAI to help debug, explain some function logic, and help with expected values for test cases

# def get_data(file):
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

# dictionary with column names and their positions in the csv
column_dict = {
    "Ship Mode": 0, "Segment": 1, "Country": 2, "City": 3, "State": 4,
    "Postal Code": 5, "Region": 6, "Category": 7, "Sub-Category": 8,
    "Sales": 9, "Quantity": 10, "Discount": 11, "Profit": 12 
}

#calculation 1: which shipping methods are most popular among different types of customers/segments
def calc_sales_by_shipmode_segment(data, column_dict):
    results = {}

    for row in data:
        # get the rows segment, shipping method, and sales amnt
        segment = row['Segment']
        ship_mode = row['Ship Mode']
        sales = row['Sales']

        # checks if any column is blank, then skips
        if segment == "" or ship_mode == "" or sales == "":
            continue

        # make sure sales is a valid number so later it can be made a float (this was a problem in tests)
        if sales.replace('.', '', 1).isdigit() == False:
            continue

        # converts sales to a float
        sales = float(sales)

        # segment is outer key, ship_mode inner, sales is value
        if segment not in results:
            # if segment isn't alr there, create nested dict for it
            results[segment] = {}
        if ship_mode not in results[segment]:
            # if ship mode isn't alr in nested dict, initialize sales value to 0
            results[segment][ship_mode] = 0.0

        #adds the current rows sales to the total sales for this segment and shipping method combo
        results[segment][ship_mode] += sales #was origibally just =, debugging with +=

    # round sales so it passes the tests
    for segment in results:
        for ship_mode in results[segment]:
            results[segment][ship_mode] = round(results[segment][ship_mode], 3)

    return results

#calculation 2 - which product categories are receiving high sales in each city?
def calc_highvaluepercentage_city_category(data, column_dict):
    results = [] # final output is a list of dicts
    counts = {} # dict for total sales and high value counts for each pair of city/category
    highsales_threshold = 1000


    for row in data:
        # get each rows city, category, and sales amnt
        city = row['City']
        category = row['Category']
        sales = row['Sales']

        # same as last calc, skip missing data
        if city == "" or category == "" or sales =="":
            continue
        # skip if sales amnt isn't a valid number
        if sales.replace('.', '', 1).isdigit() == False:
            continue

        sales = float(sales)
        key = (city, category)

        if key not in counts:
            # initialize the dict for city/category pairs if they aren't in it
            counts[key] = {'total': 0, 'high_value': 0}

        counts[key]['total'] += 1 #increment total sales

        if sales > highsales_threshold:
            counts[key]['high_value'] += 1 #increment high values

    # makes list of dictionaries
    for (city, category), values in counts.items():
        total = values['total'] # this is total # of sales for this city/cat
        high_value = values['high_value']
        percentage = (high_value / total) * 100

        #append dictionary to the results (final output)
        results.append({'city': city, 'category': category, 'total_sales': total, 
                            'high_value_sales': high_value, 'high_value_percentage': round(percentage, 2)})

    return results

    #pass

#first output function
def write_shipmode_segment_to_csv(filename, ndict):
    outFile = open(filename, "w")
    csv_writer = csv.writer(outFile) #create writer

    #headers
    csv_writer.writerow(['Segment', 'Ship Mode', 'Total Sales'])

    #ndict is the nested dictionary
    for segment in ndict:
        inner_d = ndict[segment]  # shipping modes for this segment
        for ship_mode in inner_d:
            total_sales = inner_d[ship_mode] # gets the sales total
            out_list = [segment, ship_mode, total_sales] # makes the list for the row in the csv
            csv_writer.writerow(out_list)

    outFile.close()

# second output function
def write_highvaluepercentage_to_csv(filename, listdict):
    outFile = open(filename, "w")
    csv_writer = csv.writer(outFile) #create writer

    csv_writer.writerow(['City', 'Category', 'Total Sales', 'High Value Sales', 'High Value %'])

    # list dict is the list of dictionairies
    for item in listdict:
        # items in the csv row
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
    # reads data
    data = get_data("SampleSuperstore.csv")

    # calcs
    results1 = calc_sales_by_shipmode_segment(data, column_dict)
    results2 = calc_highvaluepercentage_city_category(data, column_dict)

    #write results
    write_shipmode_segment_to_csv("shipmode_segment_results.csv", results1)
    write_highvaluepercentage_to_csv("highvalue_results.csv", results2)

    # message for tests
    print("results written to both CSV files successfully yay!")

# execute main
if __name__ == '__main__':
    main()