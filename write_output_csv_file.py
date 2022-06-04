import csv
import pandas as pd

def display_output_as_a_table(table_header_names, package_name):
    df = pd.read_csv(package_name+".csv")
    
    # The below Spaghetti code is being written to properly display table in the terminal. Please don't judge me.
    # I sacrificed some columns to get this
    if (len(table_header_names) == 4):
        df.drop(df.columns[[1]], axis=1, inplace=True)
    else:
        df.drop(df.columns[[1]], axis=1, inplace=True)
        df.drop(df.columns[[2]], axis=1, inplace=True)
        df.drop(df.columns[[1]], axis=1, inplace=True)
    print()
    
    if (df.empty):
        print("Table for " + package_name)
        print("It's not funny kid. The package \"" + package_name + "\" is not present in the given repositories.")
    else:
        print("Table for " + package_name)
        print(df)
        print("\nDetailed table can be viewed from "+package_name+".csv file.")

def write_output_csv_file(table_header_names, output_csv_file_values, package_name):
    with open(package_name+".csv", 'w') as csv_file: 
        csv_writer = csv.writer(csv_file) 
        csv_writer.writerow(table_header_names) 
        csv_writer.writerows(output_csv_file_values)

    display_output_as_a_table(table_header_names, package_name)