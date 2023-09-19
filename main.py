import numpy as np
import csv

#convertir CSV to Array
csv_filename = './dataset/dataset_1.csv'
with open(csv_filename) as f:
    reader = csv.reader(f)
    next(reader)
    lst = list(reader)
    print(lst)