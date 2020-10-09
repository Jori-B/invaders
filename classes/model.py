import random
from slimstampen.spacingmodel import SpacingModel, Fact
from utilities.constants import *


class Model:
    m = SpacingModel()

    # Creates an array of multiplication facts from min_table*min_table to max_table*max_table.
    # All multiplication facts in the array are added as facts
    # Index with tables_array["table of ...+1"]["question in table+1"]["tuple content"].
    # E.g. tables_array[2][5][2] will return the answer to 3*6, which is 18.
    list_of_tables = [7,8,13,14,16]
    times = range(2,9 + 1)
    tables_array = []
    counter = 0

    for num1 in list_of_tables:
        one_table_array = []
        for num2 in times:
            counter += 1
            table_fact = Fact(fact_id=counter, question=f"{num1} x {num2}", answer=f"{num1 * num2}", question2=f"{num2} x {num1}")
            one_table_array.append(table_fact)
        tables_array.append(one_table_array)

    random_table = random.sample(range(0, (len(tables_array) * len(one_table_array)) - 1),
                                 k=len(tables_array) * len(one_table_array) - 1)
    for i in range(0,(len(tables_array)*len(one_table_array)) - 1):
        m.add_fact(tables_array[random_table[i] % len(list_of_tables)][random_table[i] % len(times)])

    def get_count_seen_facts(self, current_time):
        return self.m.count_seen_facts(current_time)

    def get_next_fact(self):
        # Get the time for get_new_fact by subtracting the starting time from the current time in milliseconds
        # time.sleep(1); # is a test
        run_time = int(round(time.time() * 1000)) - START_TIME

        next_fact, new = self.m.get_next_fact(current_time=run_time)
        return next_fact


