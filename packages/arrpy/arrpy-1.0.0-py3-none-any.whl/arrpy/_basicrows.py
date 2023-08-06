"""as the del_row function of listprocessor depends on the appender and
extractor functions (for appending and extracting rows), make them available
in a separate file to ensure that they are always available to the
listprocessor functions regardless of import method.
"""
from copy import deepcopy

def appender(arr, row, deep = True):
    """Return a new array with the indicated row added."""
    width = len(arr)
    if deep:
        arr_out = deepcopy(arr)
    else:
        arr_out = arr[:]
    if type(row) != list:
        print("Input row was not of type 'list'. Exiting")
        return
    if len(row) != width:
        print(f"column count {width} does not match row length of {len(row)}. Exiting")
        return
    for x in range(width):
        arr_out[x].append(row[x])
    return arr_out

def extractor(arr, row):
    """Return the indicated row (the given index of all subarrays)."""
    width, height = len(arr), len(arr[0])
    try:
        row = int(row)
    except ValueError:
        print(f"input row index {row} not coercive to type int. Exiting")
        return
    if not 0 <= row < height:
        print(f"row index {row} is invalid for an input array with {width} columns and {height} rows. Exiting")
        return
    row_out = []
    for x in range(width):
        row_out.append(arr[x][row])
    return row_out
    