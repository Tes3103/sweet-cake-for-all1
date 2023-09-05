import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

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
     Get user input figures from the daily sales data
     a while loop will run until it get the valid data figure from the user
     which is a string separated by comma,
    """
    while True:
        print("please enter sales data from the last market day.")
        print("Data should be six figures, and separated by commas.")
        print("Example:50,55,65,40,34,40\n")

        data_str = input("Please enter your data here: ")
    
        sales_data = data_str.split(",")

        if validate_data(sales_data):
            print("Data is valid!")
            break
        
    return sales_data


def validate_data(values):
    """
    Inside the try except statement, converts all string values into intgers.
    if strings cannot be converted into integer, raises value error, 
    or values are not exactly 6
    """
    try:
        [int(value)for value in values]
        if len(values) != 6:
            raise ValueError(
                f"6 values are required, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False
        
    return True


def update_sales_worksheet(data):
    """
    update sales worksheet,add new row with the list data provided.
    """
    print("Updating sales worksheet...\n")
    sales_worksheet = SHEET.worksheet("sales")
    sales_worksheet.append_row(data)
    print("Sales worksheet updated succesfully.\n")


def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate for each value
    surplus is the difference of stock and sales
    positive surplus shows wastage
    negative surplus showes additional sales
    """
    print("Calculating surplus data...\n") 
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]
    print(stock_row)  


def main():
    """
    Run all program function
    """
    data = get_sales_data()   
    sales_data = [int(num) for num in data]
    update_sales_worksheet(sales_data)
    calculate_surplus_data(sales_data)

print("Welcome to Sweet Cake for all1 Data Automation!")
main()
