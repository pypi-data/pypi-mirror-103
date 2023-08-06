import db
import pandas as pd
from datetime import datetime as dt


def create_table(tablename, filename, has_headers=True):
    """
    creates table, tablename, from file, filename
    file MUST be .csv

    input: desired name of table, filename to be imported
        optional: has_headers default is True & first row of file will be treated as headers for table if set to False, first row of file will be the first row of data in the table
    computation:
        extract headers from .csv
        loop through all row of file, creating new table entry for each row
    output: table
    """
    # require .csv file
    filetype = filename[-3:]
    if filetype != "csv":
        print("not a valid filetype, must pass in a .csv")
        return

    # create meta_data
    # created_at =
    # open and read in file
    if has_headers == True:
        table = pd.read_csv(filename, header=0)
    else:
        table = pd.read_csv(filename, header=None)
    # add table to meta_data
    # todo: change to dictionary to access from key instead of index?
    # todo ==> meta_data[tablename] = {has_headers: boolean, table: pd.df, created_at: dt.now()}
    db.meta_data[tablename] = [has_headers, table, dt.now()]

    # confirm successful table creation & addition to meta_data
    print(f"table: '{tablename}' successfully created.")
    return table


if __name__ == "__main__":
    create_table(tablename, has_headers)