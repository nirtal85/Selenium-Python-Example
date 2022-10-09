import itertools
import os

import xlrd

from globals import dir_global


class ExcelParser:
    def __init__(self, excel_path):
        self.excel_path = os.path.join(dir_global.DATA_FILES_PATH, excel_path)

    def read_from_excel(self, sheet_name):
        rows_val = []
        # read from file
        work_book = xlrd.open_workbook(self.excel_path)
        sheet = work_book.sheet_by_name(sheet_name)

        # get all values, iterating through rows and columns
        num_cols = sheet.ncols  # Number of columns
        for row_idx, col_idx in itertools.product(range(1, sheet.nrows), range(num_cols)):
            cell_obj = sheet.cell(row_idx, col_idx)  # Get cell object by row, col
            # Convert cell to string,split it according to "'" and take the second cell in the array created
            # e.g.: cell_obj == "text:'something'" --> after convert and splitting == "something"
            rows_val.append(str(cell_obj).split("'")[1])
        return rows_val
