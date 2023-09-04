import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('sweet_cake_for_all1')

def get_sales_data():
    """
     the user input figures from the daily sales data
    """
    print("please enter sales data from from the last market day.")
    print("Data should be six figures, and separated by commas.")
    print("Example:50,55,65,40,34,40\n")

    data_str = input("Please enter your data here: ")
    print(f"the data provided is {data_str}")

get_sales_data()   



