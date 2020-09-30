from slimstampen.spacingmodel import SpacingModel, Fact
from utilities.constants import *


class Model:
    m = SpacingModel()

    # Creates an array of multiplication facts from min_table*min_table to max_table*max_table.
    # All multiplication facts in the array are added as facts
    # Index with tables_array["table of ...+1"]["question in table+1"]["tuple content"].
    # E.g. tables_array[2][5][2] will return the answer to 3*6, which is 18.
    min_table = 1
    max_table = 10
    tables_array = []
    counter = 0

    for num1 in range(min_table, max_table + 1):
        one_table_array = []
        for num2 in range(min_table, max_table + 1):
            counter += 1
            table_fact = Fact(fact_id=counter, question=f"{num1} x {num2}", answer=f"{num1 * num2}")
            m.add_fact(table_fact)
            one_table_array.append(table_fact)
        tables_array.append(one_table_array)

    def get_next_fact(self):
        # Get the time for get_new_fact by subtracting the starting time from the current time in milliseconds
        # time.sleep(1); # is a test
        run_time = int(round(time.time() * 1000)) - START_TIME

        next_fact, new = self.m.get_next_fact(current_time=run_time)
        return next_fact


