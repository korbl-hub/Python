import random
import string
import typing

lowercases = list(string.ascii_lowercase)
uppercases = list(string.ascii_uppercase)
digits = list(string.digits)
symbols = list(string.punctuation)

def get_decimal(message, min_value, max_value=None):
    input_ok = False
    while not input_ok:
        value = input(message)
        if value.isdecimal() and int(value) >= min_value:
            if max_value is None:
                input_ok = True
            else:
                input_ok = int(value) <= max_value
    return int(value)
    
def get_current_settings(settings=None):
    DEFAULT_SETTINGS = settings = [1, 1, 1, 1, 8]
    if not settings:
        settings = DEFAULT_SETTINGS
    return settings

def print_current_settings(settings):
    # Min Lowercases, Min Uppercases, Min Digits, Min Symbols, Min Length
    print("Current Settings: ")
    print(f"Minimum Count of Lowercases = {settings[0]}")
    print(f"Minimum Count of Uppercases = {settings[1]}")
    print(f"Minimum Count of Digits = {settings[2]}")
    print(f"Minimum Count of Symbols = {settings[3]}")
    print(f"Minimum Password Length = {settings[4]}")

def update_settings(settings):
    DEFAULT_MIN_LENGTH = 8
    settings.clear()
    # Min Lowercases, Min Uppercases, Min Digits, Min Symbols, Min Length
    settings.append(get_decimal("Enter number of lowercases (Minimum 1): ", 1))
    settings.append(get_decimal("Enter number of uppercases (Minimum 1): ", 1))
    settings.append(get_decimal("Enter number of digits (Minimum 1): ", 1))
    settings.append(get_decimal("Enter number of symbols (Minimum 1): ", 1))
    min_password_length = settings[0] + settings[1] + settings[2] + settings[3]
    if min_password_length < DEFAULT_MIN_LENGTH:
        min_password_length = DEFAULT_MIN_LENGTH
    settings.append(get_decimal(f"Enter password length (Minimum {min_password_length}): ", min_password_length))
    return settings

def draw_chars(source, required_count):
    count = 0
    chars = []
    while count < required_count:
        index = random.randint(0, len(source) - 1)
        chars.append(source[index])
        count += 1
    return chars
    
def generate_password(settings):
    # Min Lowercases, Min Uppercases, Min Digits, Min Symbols, Min Length
    lowercases_in_password = draw_chars(lowercases, settings[0])
    uppercases_in_password = draw_chars(uppercases, settings[1])
    digits_in_password = draw_chars(digits, settings[2])
    symbols_in_password = draw_chars(symbols, settings[3])
    
    drawn_chars_count = settings[0] + settings[1] + settings[2] + settings[3]
    remained_chars_count = settings[4] - drawn_chars_count
    
    pool = lowercases + uppercases + digits + symbols
    remained_chars_in_password = draw_chars(pool, remained_chars_count)
    
    password = []
    password.extend(lowercases_in_password + uppercases_in_password)
    password.extend(digits_in_password + symbols_in_password)
    password.extend(remained_chars_in_password)
    return password

def shuffle_password(password):
    new_password:typing.List[str] = []
    while len(password) > 0:
        old_index = random.randint(0, len(password) - 1)
        char = password.pop(old_index)
        if len(new_password) == 0:
            new_password.append(char)
        else:
            new_index = random.randint(0, len(new_password) - 1)
            new_password.insert(new_index, char)
    return new_password

def pass_fail(current, required):
    if current >= required:
        symbol = ">="
        result = "Pass"
    else:
        symbol = "<"
        result = "Fail"
    return [symbol, result]
        
def check_password(settings):
    password = input("Enter your password: ")
    
    lowercase_count = 0
    uppercase_count = 0
    digit_count = 0
    symbol_count = 0
    
    for char in password:
        if char.islower():
            lowercase_count += 1
        elif char.isupper():
            uppercase_count += 1
        elif char.isdecimal():
            digit_count += 1
        else:
            symbol_count += 1

    # Min Lowercases, Min Uppercases, Min Digits, Min Symbols, Min Length
    symbol1, result1 = pass_fail(lowercase_count, settings[0])
    print(f"Check Lowercases: {lowercase_count} {symbol1} {settings[0]} | Result: {result1}")
    symbol2, result2 = pass_fail(uppercase_count, settings[1])
    print(f"Check Uppercases: {uppercase_count} {symbol2} {settings[1]} | Result: {result2}")
    symbol3, result3 = pass_fail(digit_count, settings[2])
    print(f"Check Digits: {digit_count} {symbol3} {settings[2]} | Result: {result3}")
    symbol4, result4 = pass_fail(symbol_count, settings[3])
    print(f"Check Symbols: {symbol_count} {symbol4} {settings[3]} | Result: {result4}")
    symbol5, result5 = pass_fail(len(password), settings[4])
    print(f"Check Password Length: {len(password)} {symbol5} {settings[4]} | Result: {result5}")
    
def print_menu():
    menu = [
        "Print Current Settings",
        "Update Settings",
        "Generate Password",
        "Check Password",
        "Quit"
    ]
    index = 0
    print()
    while index < len(menu):
        print(f"{index+1}: {menu[index]}")
        index += 1

def main():
    settings = get_current_settings()
    password = ""
    print("Password Generator")
    while True:
        print_menu()
        print()
        option = get_decimal("Select an option: ", 1, 5)
        print()
        if option == 1:
            print_current_settings(settings)
        elif option == 2:
            settings = update_settings(settings)
        elif option == 3:
            password_list = generate_password(settings)
            password = "".join(shuffle_password(password_list))
            print(f"Your new password is: {password}")
        elif option == 4:
            check_password(settings)
        elif option == 5:
            break
            
main()