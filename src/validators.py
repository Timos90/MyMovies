import datetime

def validate_int_input(prompt, error_message="Invalid input. Please enter a valid number."):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print(error_message)

def validate_float_input(prompt, min_value=None, max_value=None, error_message="Invalid input. Please enter a valid number."):
    while True:
        try:
            value = float(input(prompt))
            if (min_value is not None and value < min_value) or (max_value is not None and value > max_value):
                print(f"{error_message}: Please enter a value between {min_value} and {max_value}.")
            else:
                return value
        except ValueError:
            print(f"{error_message}: Please enter a valid number.")

def validate_date_input(prompt, error_message="Invalid input. Please enter a valid date (YYYY-MM-DD)."):
    while True:
        try:
            date_str = input(prompt)
            return datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            print(error_message)
