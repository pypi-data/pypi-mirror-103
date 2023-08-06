def get_table(tablename):
    return meta_data[tablename]


def show(table, rows):
    if not isinstance(table, pd.DataFrame):
        print("\nSHOW ERROR: No table to show.")
        return
    print(f"\nShowing {rows} rows from table.")
    if len(table) < rows:
        print(f"This table contains fewer than {rows} rows.")
    print(
        tabulate(
            table.head(rows),
            headers="keys",
            tablefmt="fancy_grid",
            showindex="always",
        )
    )
    return table


def is_float(val):
    """
    method to determine if string is a float
    input: string
    computation: try to cast to float
    output: boolean (True = string can be cast to float)
    """
    try:
        float(val)
    except:
        return False
    return True


def is_int(val):
    """
    method to determine if string is a int
    input: string
    computation: try to cast to int
    output: boolean (True = string can be cast to int)
    """
    try:
        int(val)
    except:
        return False
    return True
