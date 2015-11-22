#!/usr/bin/env python3
import binascii
import csv
import os.path
import sys
from tkinter.filedialog import askopenfilename, askdirectory
from tkinter.simpledialog import askinteger

def split_csv_file(f, dst_dir, keyfunc):
    csv_reader = csv.reader(f)
    csv_writers = {}
    for row in csv_reader:
        k = keyfunc(row)
        if k not in csv_writers:
            csv_writers[k] = csv.writer(open(os.path.join(dst_dir, k),
                                             mode='w', newline=''))
        csv_writers[k].writerow(row)

def get_args_from_gui():
    input_filename = askopenfilename(
        filetypes=(('CSV', '.csv'),),
        title='Select CSV Input File')
    column = askinteger('Choose Table Column', 'Table column')
    dst_dir = askdirectory(title='Select Destination Directory')
    return (input_filename, column, dst_dir)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        input_filename, column, dst_dir = get_args_from_gui()
    else:
        raise Exception("Invalid number of arguments")
    with open(input_filename, mode='r', newline='') as f:
        split_csv_file(f, dst_dir, lambda r: r[column-1]+'.csv')
        
