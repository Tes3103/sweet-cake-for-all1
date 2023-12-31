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
     Get user input figures from the daily sales data
     a while loop will run until it get the valid data figure from the user
     which is a string separated by comma,
    """
    while True:
        print("please enter sales data from the last market day.")
        print("Data should be six figures, and separated by commas.")
        print("Example:50,55,65,40,34,40\n")

        data_str = input("Please enter your sales data here:\n")

        sales_data = data_str.split(",")

        if validate_data(sales_data):
            print("Data is valid!")
            break

    return sales_data


def validate_data(values):
    """
    Inside the try except statement, converts all string values into intgers.
    if strings cannot be converted into integer,raises value error,or values
    are not exactly 6 positive numbers.
    """
    try:
        [int(value)for value in values]
        if len(values) != 6:
            raise ValueError(
                f"6 values are required, you provided {len(values)}"
            )
        for value in values:
            if int(value) < 0:
                raise ValueError(
                    f"6 values should be greater than 0")
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False
    return True


def update_worksheet(data, worksheet):
    """
    receives a lsit of integers to be inserted to a worksheet
    update the specified worksheet with the data provided.
    """
    print(f"Updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} Work sheet updated successfully!\n")
    print(f"{worksheet} please click the below link to view the update\n")
    print(f"{worksheet} https://tinyurl.com/24wwjfce\n")


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
    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    return surplus_data


def get_last_5_entries_sales():
    """
    Collects columens of data from sales worksheet, collecting
    the last five entries for each cake and returns the data as
    list of lists
    """
    sales = SHEET.worksheet("sales")
    columns = []
    for ind in range(1, 7):
        column = sales.col_values(ind)
        columns.append(column[-5:])
    return columns


def calculate_stock_data(data):
    """
    calculate teh average stock for each item type adding 25%
    """
    print("Calculating stock data...\n")
    new_stock_data = []

    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column)/5
        stock_num = average * 2.5
        new_stock_data.append(round(stock_num))
    return new_stock_data


def main():
    """
    Run all program function
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, "surplus")
    sales_columns = get_last_5_entries_sales()
    stock_data = calculate_stock_data(sales_columns)
    update_worksheet(stock_data, "stock")


if __name__ == "__main__":
    print("Welcome to Sweet Cake for all1 Data Automation!")
    main()