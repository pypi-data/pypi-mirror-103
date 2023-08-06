"""arrpy is a 2D array manipulation module.

arrpy is a lightweight module allowing simple manipulation of 2D arrays using base
python list objects. Designed for use in pandas-incompatible situations, such
as when working in Jython. Allows import and export of spreadsheets, finding
the mean across rows or columns, and row extraction.

Functions:
- avg_col returns the arithmetic mean of the given columns as a list.
- avg_row returns the arithmetic mean of the given rows as a list.
- append_row appends the given list to a list of lists.
- del_row removes the indicated row from a list of lists.
- extract_row returns the indicated row from a list of lists.
- open_df opens the indicated file and returns a list of lists.
- write_csv saves a lists of lists as a csv.
"""

from arrpy.listprocessor import (
avg_col,
avg_row,
append_row,
del_row,
extract_row,
open_df,
write_csv
)