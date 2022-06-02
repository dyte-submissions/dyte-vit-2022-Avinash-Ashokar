import csv
import pandas as pd

def writeCSVFiles(fields, newCSVFile):
    with open("output.csv", 'w') as csvfile: 
        csvwriter = csv.writer(csvfile) 
        csvwriter.writerow(fields) 
        csvwriter.writerows(newCSVFile)

    file = "output.csv"
    df = pd.read_csv(file)
    pd.options.display.max_columns = len(df.columns)
    if (len(fields) == 4):
        df.drop(df.columns[[1]], axis=1, inplace=True)
    else:
        df.drop(df.columns[[1]], axis=1, inplace=True)
        df.drop(df.columns[[2]], axis=1, inplace=True)
        df.drop(df.columns[[1]], axis=1, inplace=True)
    print()
    print(df)
    print("\nDetailed table can be viewed from output.csv file.")