import gspread
from datetime import date
from random import randint

# Initialize the service account and spreadsheet variables
sa = None
sh = None

def initialize_google_sheet():
    global sa, sh
    try:
        sa = gspread.service_account(filename="service_account.json")
        sh = sa.open("DailyQuotes")
    except:
        sa = None
        sh = None

def get_data_from_google_sheet():
    global sa, sh
    if sa is None or sh is None:
        initialize_google_sheet()

    try:
        if sa is None or sh is None:
            return ["Please Check Your Internet", f"-{randint(1, 25)}-"]

        wks = sh.get_worksheet(0)
        
        d = date.today()
        all_dates = wks.col_values(1)

        try:
            row_index = all_dates.index(str(d))
            row_index += 1

            b_value = wks.cell(row_index, 2).value
            c_value = wks.cell(row_index, 3).value
            
            return [b_value, c_value]
            
        except ValueError:
            return ["Error On Our Side", "..."]
        
    except:
        sa = None
        sh = None
        return ["Please Check Your Internet", f"-{randint(1, 25)}-"]

# b_value, c_value = get_data_from_google_sheet()
# if b_value and c_value:
#     print("Value in B column:", b_value)
#     print("Value in C column:", c_value)