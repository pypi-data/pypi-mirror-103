import db

# ? filter(tablename, condition) -> select all entries from specified table where condition == True
# * advanced: accept multiple conditions
def filter(tablename, condition):
    table = db.get_table(tablename)[1]
    print(f"\n\nFiltering '{tablename}' for col {condition}")
    if ">=" in condition:
        cond = condition.split(">=")
        col = cond[0].strip()
        val = cond[-1]
        if db.is_int(col):  # col is int
            col = int(col)
            if db.is_float(val):
                val = float(val)
                temp_table = table[table.iloc[:, col] >= val]  # val is float
                return temp_table
            elif db.is_int(val):
                val = int(val)
                temp_table = table[table.iloc[:, col] >= val]  # val is int
                return temp_table
            else:
                temp_table = table[table.iloc[:, col] >= val.strip()]  # val is str
                return temp_table
        else:  # col is str
            if db.is_float(val):
                val = float(val)
                temp_table = table[table.loc[:, col] >= val]  # val is float
                return temp_table
            elif db.is_int(val):
                val = int(val)
                temp_table = table[table.loc[:, col] >= val]  # val is int
                return temp_table
            else:
                temp_table = table[table.loc[:, col] >= val.strip()]  # val is str
                return temp_table

    elif ">" in condition:
        cond = condition.split(">")
        col = cond[0].strip()
        val = cond[-1]
        if db.is_int(col):  # col is int
            col = int(col)
            if db.is_float(val):
                val = float(val)
                temp_table = table[table.iloc[:, col] > val]  # val is float
                return temp_table
            elif db.is_int(val):
                val = int(val)
                temp_table = table[table.iloc[:, col] > val]  # val is int
                return temp_table
            else:
                temp_table = table[table.iloc[:, col] > val.strip()]  # val is str
                return temp_table
        else:  # col is str
            if db.is_float(val):
                val = float(val)
                temp_table = table[table.loc[:, col] > val]  # val is float
                return temp_table
            elif db.is_int(val):
                val = int(val)
                temp_table = table[table.loc[:, col] > val]  # val is int
                return temp_table
            else:
                temp_table = table[table.loc[:, col] > val.strip()]  # val is str
                return temp_table

    elif "<=" in condition:
        cond = condition.split("<=")
        col = cond[0].strip()
        val = cond[-1]
        if db.is_int(col):  # col is int
            col = int(col)
            if db.is_float(val):
                val = float(val)
                temp_table = table[table.iloc[:, col] <= val]  # val is float
                return temp_table
            elif db.is_int(val):
                val = int(val)
                temp_table = table[table.iloc[:, col] <= val]  # val is int
                return temp_table
            else:
                temp_table = table[table.iloc[:, col] <= val.strip()]  # val is str
                return temp_table
        else:  # col is str
            if db.is_float(val):
                val = float(val)
                temp_table = table[table.loc[:, col] <= val]  # val is float
                return temp_table
            elif db.is_int(val):
                val = int(val)
                temp_table = table[table.loc[:, col] <= val]  # val is int
                return temp_table
            else:
                temp_table = table[table.loc[:, col] <= val.strip()]  # val is str
                return temp_table

    elif "<" in condition:
        cond = condition.split("<")
        col = cond[0].strip()
        val = cond[-1]
        if db.is_int(col):  # col is int
            col = int(col)
            if db.is_float(val):
                val = float(val)
                temp_table = table[table.iloc[:, col] < val]  # val is float
                return temp_table
            elif db.is_int(val):
                val = int(val)
                temp_table = table[table.iloc[:, col] < val]  # val is int
                return temp_table
            else:
                temp_table = table[table.iloc[:, col] < val.strip()]  # val is str
                return temp_table
        else:  # col is str
            if db.is_float(val):
                val = float(val)
                temp_table = table[table.loc[:, col] < val]  # val is float
                return temp_table
            elif db.is_int(val):
                val = int(val)
                temp_table = table[table.loc[:, col] < val]  # val is int
                return temp_table
            else:
                temp_table = table[table.loc[:, col] < val.strip()]  # val is str
                return temp_table
    elif "==" in condition:
        cond = condition.split("==")
        col = cond[0].strip()
        val = cond[-1]
        if db.is_int(col):  # col is int
            col = int(col)
            if db.is_float(val):
                val = float(val)
                temp_table = table[table.iloc[:, col] == val]  # val is float
                return temp_table
            elif db.is_int(val):
                val = int(val)
                temp_table = table[table.iloc[:, col] == val]  # val is int
                return temp_table
            else:
                temp_table = table[table.iloc[:, col] == val.strip()]  # val is str
                return temp_table
        else:  # col is str
            if db.is_float(val):
                val = float(val)
                temp_table = table[table.loc[:, col] == val]  # val is float
                return temp_table
            elif db.is_int(val):
                val = int(val)
                temp_table = table[table.loc[:, col] == val]  # val is int
                return temp_table
            else:
                temp_table = table[table.loc[:, col] == val.strip()]  # val is str
                return temp_table
    elif "=" in condition:
        cond = condition.split("=")
        col = cond[0].strip()
        val = cond[-1]
        if db.is_int(col):  # col is int
            col = int(col)
            if db.is_float(val):
                val = float(val)
                temp_table = table[table.iloc[:, col] == val]  # val is float
                return temp_table
            elif db.is_int(val):
                val = int(val)
                temp_table = table[table.iloc[:, col] == val]  # val is int
                return temp_table
            else:
                temp_table = table[table.iloc[:, col] == val.strip()]  # val is str
                return temp_table
        else:  # col is str
            if db.is_float(val):
                val = float(val)
                temp_table = table[table.loc[:, col] == val]  # val is float
                return temp_table
            elif db.is_int(val):
                val = int(val)
                temp_table = table[table.loc[:, col] == val]  # val is int
                return temp_table
            else:
                temp_table = table[table.loc[:, col] == val.strip()]  # val is str
                return temp_table
    else:
        print("Invalid condition argumen. Cannot perform filter.")
        return table
