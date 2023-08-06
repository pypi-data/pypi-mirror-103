from db_mimic import db

# * create_table test
db.create_table("test", "test_data.csv")
# db.create_table("greenhouse", "greenhouse-gas-emissions.csv")
# db.create_table("err_table", "wrong_type") # returns error for wrong data type

# * select test
db.show(db.select("test", [0, 1, 2]), 5)  # indices
# db.show(db.select("test", ["region", "units", "gas"]), 6)  # col ndb.s
# db.show(db.select("test", ["as", 234, "asdf", 456, 34]), 5)  # ndb.s & indices
# db.show(db.select("test", []), 4)  # no cols selected
# db.show(
#     db.select("greenhouse", [0, 1, 2, 3, 4, 5, 6]), len(db.get_table("greenhouse")[1])
# )
# db.show(db.select("greenhouse", [0, 1, 2, 3, 4, 5, 6]), 20)


# db.show(db.get_table("greenhouse")[1], 10)
# db.show(db.get_table("test")[1], 10)
# * filter test
# ? testing col == int; val == int, float, string
# db.show(db.filter("test", "5 > 2009"), 6)  # * works
# db.show(db.filter("test", "5 < 2009"), 6)  # * works
# db.show(db.filter("test", "5 == 2009"), 6)  # * works
# db.show(db.filter("test", "5 = 2009"), 6)  # * works
# db.show(db.filter("test", "5 >= 2009"), 6)  # * works
# db.show(db.filter("test", "5 <= 2009"), 6)  # * works
# db.show(db.filter("greenhouse", "anzsic_descriptor = Total"), 45)

# db.show(db.filter("test", "0 > Gisborne"), 6)  # * works
# db.show(db.filter("test", "0 < Gisborne"), 6)  # * works
# db.show(db.filter("test", "0 == Gisborne"), 6)  # * works
# db.show(db.filter("test", "0 = Gisborne"), 6)  # * works
# db.show(db.filter("test", "0 >= Gisborne"), 6)  # * works
# db.show(db.filter("test", "0 <= Gisborne"), 6)  # * works

# db.show(db.filter("test", "6 > 850.0"), 6)  # * works
# db.show(db.filter("test", "6 < 850.0"), 6)  # * works
# db.show(db.filter("test", "6 == 1471.69"), 6)  # * works
# db.show(db.filter("test", "6 = 1471.69"), 6)  # * works
# db.show(db.filter("test", "6 >= 850.0"), 6)  # * works
# db.show(db.filter("test", "6 <= 850.0"), 6)  # * works

# # ? testing col == str; val == int, float, string
# db.show(db.filter("test", "year > 2009"), 6)  # * works
# db.show(db.filter("test", "year < 2009"), 6)  # * works
# db.show(db.filter("test", "year == 2009"), 6)  # * works
# db.show(db.filter("test", "year = 2009"), 6)  # * works
# db.show(db.filter("test", "year >= 2009"), 6)  # * works
# db.show(db.filter("test", "year <= 2009"), 6)  # * works

# db.show(db.filter("test", "data_val > 1605.5"), 6)  # * works
# db.show(db.filter("test", "data_val < 1605.5"), 6)  # * works
# db.show(db.filter("test", "data_val == 811.63"), 6)
# db.show(db.filter("test", "data_val = 811.63"), 6)
# db.show(db.filter("test", "data_val >= 1605.5"), 6)  # * works
# db.show(db.filter("test", "data_val <= 1605.5"), 6)  # * works

# db.show(db.filter("test", "region > Gisborne"), 6)  # * works
# db.show(db.filter("test", "region < Gisborne"), 6)  # * works
# db.show(db.filter("test", "region == Gisborne"), 6)  # * works
# db.show(db.filter("test", "region = Gisborne"), 6)  # * works
# db.show(db.filter("test", "region >= Gisborne"), 6)  # * works
# db.show(db.filter("test", "region <= Gisborne"), 6)  # * works


# * show test
temp_table = db.filter("test", "6 < 1605.0")
db.show(temp_table, 8)

# * additional
# print(db.select(db.filter("test", "year > 2009"), [0, 2, 5])) #! not chainable because .filter returns DataFrdb. & .select accepts just tablendb.