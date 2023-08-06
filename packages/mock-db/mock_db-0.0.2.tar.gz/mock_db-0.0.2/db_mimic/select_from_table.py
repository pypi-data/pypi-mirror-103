import db

# ? select(tablename, columns) -> select values under specified columns from specified table
# * advanced: accept expressions over columns
def select(tablename, columns):
    """
    select values from specified columns
    input: tablename, columns as list of table indices
    computation:
        pull table based on tablename
        select specified columns
        copy into temp table
    output: temp table of selected columns
    """
    if len(columns) < 1:
        print(f"\nSELECT ERROR: Must select at least one column from {tablename}.")
        return

    # determine data types of columns passed in; retrieve accordingly
    column_inputs = [type(x) == str for x in columns]
    if False in column_inputs and True in column_inputs:
        print(
            "\nSELECT ERROR: Invalid selection. Please enter column names OR column indices."
        )
        return

    table = db.get_table(tablename)[1]  #! if switch to dict, [1] ==> ['table']

    if False in column_inputs:  # columns = list of indices
        temp_table = table.iloc[:, columns]
    else:  # columns = list of headers
        temp_table = table.loc[:, columns]

    print(f"Retrieved columns {columns} from {tablename}.")
    return temp_table
