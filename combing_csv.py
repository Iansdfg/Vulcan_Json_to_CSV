#  This script combine CSV from json_to_csv.py and manual csv together 
import csv
import os
import pandas as pd
import glob
from json_to_csv import write_array_to_CSV

def add_one_csv_to_table(file_name, table):
    with open(file_name, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
                continue
            table.append(row)

# def combine_csv(file_one, file_two, destination):
#     file_a = pd.read_csv(file_one)
#     file_b = pd.read_csv(file_two)
#     file_b = file_b.dropna(axis=1)
#     merged = file_a.merge(file_b, on='title')
#     merged.to_csv(destination, index=False)

def combine_csv(file_one, file_two, destination):
    combined_csv = pd.concat([pd.read_csv(f) for f in [file_one, file_two]])
    combined_csv.to_csv( destination, index=False, encoding='utf-8-sig')

if __name__ == "__main__":
    manual_table = []
    # add_one_csv_to_table('manual/Joy_10 - Sheet1.csv', manual_table)
    

    files = os.listdir('manual/')
    for one_file in files:
        add_one_csv_to_table('manual/' + one_file, manual_table)

    for row in manual_table:
        print(row)

    write_array_to_CSV(manual_table, 'manual_table.csv')

    combine_csv('json_to_csv.csv', 'manual_table.csv', 'combined.csv')
