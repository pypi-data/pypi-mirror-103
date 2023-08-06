import csv
import re

from arrpy import _checks as checks
from arrpy._basicrows import appender, extractor
    
def avg_col(arr, base_check = True, dim_check = False):
    """Return the arithmetic mean of the given columns (contained subarrays)."""
    checker = checks.ValidCheck(arr)
    if not checker.run_checks(base_check, dim_check):
        return
    width, height = len(arr), len(arr[0])
    avg_arr = []
    for y in range(height):
        temp_arr = []
        for x in range(width):
            temp_arr.append(arr[x][y])
        temp_avg = sum(temp_arr)/len(temp_arr)
        avg_arr.append(temp_avg)
    return avg_arr

def avg_row(arr, base_check = True, dim_check = False):
    """Return the arithmetic mean of the given rows (given index of contained subarrays)."""
    checker = checks.ValidCheck(arr)
    if not checker.run_checks(base_check, dim_check):
        return
    width, height = len(arr), len(arr[0])
    avg_arr = []
    for x in range(width):
        temp_arr = []
        for y in range(height):
            temp_arr.append(arr[x][y])
        temp_avg = sum(temp_arr)/len(temp_arr)
        avg_arr.append(temp_avg)
    return avg_arr

def append_row(arr, row, base_check = True, deep = True):
    """Return a new list of lists with the indicated row (list) appended."""
    checker = checks.ValidCheck(arr)
    if not checker.run_checks(base_check):
        return
    return appender(arr, row, deep)

def del_row(arr, row, base_check = True):
    """Return a new list of lists with the indicated row deleted."""
    checker = checks.ValidCheck(arr)
    if not checker.run_checks(base_check):
        return
    width, height = len(arr), len(arr[0])
    try:
        row = int(row)
    except ValueError:
        print(f"input row index {row} not coercible to type int. Exiting")
        return
    if not 0 <= row < height:
        print(f"row index {row} is invalid for an input array with {width} columns and {height} rows. Exiting")
        return
    arr_out = [[] for i in range(width)]
    for y in range(height):
        if y != row:
            arr_row = extractor(arr, y)
            appender(arr_out, arr_row, deep = False)
    return arr_out

def extract_row(arr, row, base_check = True):
    """Return the indicated row (a list of the values at the given index of all subarrays)."""
    checker = checks.ValidCheck(arr)
    if not checker.run_checks(base_check):
        return
    return extractor(arr, row)


def open_df(file, delim_type = "csv", subarray = "col", e = 'utf-8-sig'):
    """Open the tab or csv file and return it as a list of lists."""
    with open(file,'r', encoding = e) as f:
        file_text = f.read()
    delims = {"csv": "," , "tab": "\t"}
    rows = re.split("\n", file_text)
    #if the last char of the imported file is \n a false extra element will be added to the first column
    #strip this
    if rows[-1] == "":
        rows.pop()
    try:
        if subarray == "col":
            arr = [[] for char in rows[0] if char == delims[delim_type]] + [[]]
            for row in rows:
                cols = re.split(delims[delim_type], row)
                for i, col in enumerate(cols):
                    arr[i].append(col)
        else:
            arr = [re.split(delims[delim_type], row) for row in rows]
    except:
        print("Failed during file parsing. Check that delimitor type and encoding are suitable. Default file type is csv.")
        return
    return arr

def write_csv(arr, file, subarray = "col"):
    """Write the given list of lists as a csv file."""
    with open(file, 'w') as outfile:
        arr_writer = csv.writer(outfile)
        if subarray == "col":
            for i in range(len(arr[0])):
                row = extract_row(arr, i, base_check = False)
                arr_writer.writerow(row)
        else:
            for row in arr:
                arr_writer.writerow(row)

