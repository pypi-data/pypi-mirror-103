# Arrpy #
	
A lightweight module allowing simple manipulation of 2D arrays using base python list objects. Designed for use in pandas-incompatible situations, such as when working in Jython. Allows import and export of spreadsheets, finding the mean across rows or columns, and row extraction.

## download ##
run 'pip install arrpy'

## Import and export ##
	
**open_df**(file, delim_type = "csv", subarray = "col", e = 'utf-8-sig')
Open *file* and return a corresponding list of lists.
*file* is a string denoting the path of the 2D data of interest.
*delim type* is a string denoting the column separators used in *file*. Currently accepts "csv" and "tab".
*subarray* is a string denoting whether the respective subarrays in the list created will correspond to a row or a columns of *file*.
*e* is a string denoting the encoding of the *file*.

**write_csv**(arr, path, subarray = "col")
Write *arr* to *file*.
*arr* is a list of lists.
*file* is a string denoting the path to write to.
*subarray* is a string denoting whether the respective subarrays in *arr* will correspond to a row or column of *file*.

## List manipulation ##

**append_row**(arr, row, base_check = True, deep = True)
Output a new list object with *row* appended to *arr*.
*arr* is a list of lists.
*row* is a list to append to *arr*.
*base_check* is a boolean to determine whether to run a set of basic compatibilty checks on *arr* (type, length, dimension count, and raggedness)
*deep* is a boolean to determine whether to append *row* to a deep (True) or shallow copy of *arr* (False).

**del_row**(arr, row, base_check = True)
Output a new list object with *row* deleted from *arr*.
*arr* is a list of lists.
*row* is an object that is coercible to 0 <= int <= len(arr[0]).
*base_check* is a boolean to determine whether to run a set of basic compatibilty checks on *arr* (type, length, dimension count, and raggedness)

## List processing ##

**avg_col**(arr, base_check = True, dim_check = False)
Outputs the arithmetic mean of the columns (subarrays) of *arr* as a list.
*arr* is a list of lists.
*base_check* is a boolean to determine whether to run a set of basic compatibilty checks on *arr* (type, length, dimension count, and raggedness)
*dim_check* is a boolean to determine whether to check if *arr* has a consistent number of dimensions. This can be slow for larger *arr*.

**avg_row**(arr, base_check = True, dim_check = False)
Outputs the arithmetic mean of the rows (a given index of each subarray) of *arr* as a list.
*arr* is a list of lists.
*base_check* is a boolean to determine whether to run a set of basic compatibilty checks on *arr* (type, length, dimension count, and raggedness)
*dim_check* is a boolean to determine whether to check if *arr* has a consistent number of dimensions. This can be slow for larger *arr*.

**row_extract**(arr, row, base_check = True)
Outputs the selected row (given index of each subarray of *arr*) as a list.
*arr* is a list of lists.
*row* is an object that is coercible to 0 <= int <= len(arr[0]).
*base_check* is a boolean to determine whether to run a set of basic compatibilty checks on *arr* (type, length, dimension count, and raggedness)
*dim_check* is a boolean to determine whether to check if *arr* has a consistent number of dimensions. This can be slow for larger *arr*.

