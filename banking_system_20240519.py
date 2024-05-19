import datetime as dt
import tabulate as tb
import os
import pickle
import requests
import time

BANK_NAME = 'Korbl Bank'
BANK_FILE = 'korbl_bank.pkl'
ID_FILE = 'korbl_id.pkl'


class PickleFile:
    def __init__(self, name):
        self.name = name

    def is_exist(self):
        return os.path.exists(self.name)
    
    def save(self, data):
        self.data = data
        with open(self.name, 'wb') as f:
            pickle.dump(self.data, f)

    def load(self):
        with open(self.name, 'rb') as f:
            data = pickle.load(f)
        return data

    def message(self, action):
        if action == 'save':
            return f'{self.name} saved.'
        else:
            return f'{self.name} loaded.'
    
    def __str__(self):
        return f'File Name = {self.name}.'
    
class Bank:
    def __init__(self, name, id):
        self.name = name
        self.new_customer_id = id
        self.customers_list = []
        self.teller_name = 'Korbl'
        self.menu = {
            1: {'title': '(General): Open an Account', 'func': self.open_account},
            2: {'title': '(Normal): Make a Deposit'},
            3: {'title': '(Normal): Make a Withdrawl'},
            4: {'title': '(Normal): Print Bank Statement'},
            5: {'title': '(Checking): Make a Deposit'},
            6: {'title': '(Checking): Issue a Check'},
            7: {'title': '(Checking): Send a Statement'},
            8: {'title': '(Forex): Make a Deposit'},
            9: {'title': '(Forex): Make a Withdrawl'},
        }

        self.account_menu = {
            1: {'title': 'Normal Account (N)'},
            2: {'title': 'Checking Account (C)'},
            3: {'title': 'Forex Account (F)'},
            # 4: {'title': 'Fixed Deposit Account (D)'}
        }
        
    def greeting(self):
        now = dt.datetime.now()
        hour = now.hour
        if hour < 12:
            part_of_day = 'morning'
        elif hour < 5:
            part_of_day = 'afternoon'
        else:
            part_of_day = 'evening'
        return f'Good {part_of_day}. My name is {self.teller_name}.'
    
    def count_customers(self):
        return f'Customers Count = {len(self.customers_list)}'
    
    def show_total_deposits(self):
        total = 0
        for customer in self.customers_list:
            total += customer.find_total_balance()
        return f'Total Deposits = ${total}'
    
    def show_menu(self):
        for key, item in self.menu.items():
            print(f"{key}: {item['title']}")
        print()
        option = input(f'{self.greeting()} How may I help you?: ')
        print()
        if option.isdecimal() and int(option) in self.menu.keys():
            if int(option) == 1:
                self.menu[int(option)]['func'](None)
            elif int(option) == 2:
                accounts = self.check_account('N')
                if accounts:
                    self.deposit_service(accounts)
            elif int(option) == 3:
                accounts = self.check_account('N')
                if accounts:
                    available_accounts = [account for account in accounts if account.balance >= 100]
                    if available_accounts:
                        self.withdrawl_service(available_accounts)
                    else:
                        print('All your Normal Accounts have balance < 100.')
                        to_deposit = input("Would you like to make a deposit ('yes' or 'no')?: ")
                        if to_deposit == 'yes':
                            self.deposit_service(accounts)
            elif int(option) == 4:
                accounts = self.check_account('N')
                if accounts:
                    self.bank_statement_service(accounts)
            elif int(option) == 5:
                accounts = self.check_account('C')
                if accounts:
                    self.deposit_service(accounts)
            elif int(option) == 6:
                accounts = self.check_account('C')
                if accounts:
                    available_accounts = [account for account in accounts if account.balance >= 100]
                    if available_accounts:
                        self.issue_check_service(available_accounts)
                    else:
                        print('All your Checking Accounts have balance < 100.')
                        to_deposit = input("Would you like to make a deposit ('yes' or 'no')?: ")
                        if to_deposit == 'yes':
                            self.deposit_service(accounts)
            elif int(option) == 7:
                accounts = self.check_account('C')
                if accounts:
                    self.bank_statement_service(accounts)
            elif int(option) == 8:
                accounts = self.check_account('F')
                if accounts:
                    self.deposit_service(accounts)
            elif int(option) == 9:
                accounts = self.check_account('F')
                if accounts:
                    self.withdrawl_service(accounts)
                    
    def check_id(self):
        while True:
            customer_id = input("Sure. May I have your Customer ID ('no' for New Customer)?: ")
            print()
            if customer_id == 'no':
                self.add_customer(self.new_customer_id)
                break
            elif customer_id.isdecimal():
                valid_customer_ids = [customer.customer_id for customer in self.customers_list]
                print(valid_customer_ids)
                if not int(customer_id) in valid_customer_ids:
                    print('Your Customer ID is not in our records.')
                    self.add_customer(self.new_customer_id)
                break
        print()
        return self.customers_list[-1].customer_id if customer_id == 'no' else int(customer_id)
    
    def check_account(self, account_code):
        account_codes = {
            'N': 'Normal Account',
            'C': 'Checking Account',
            'F': 'Forex Account',
            # 'D': 'Fixed Deposit Account'
        }
        
        customer_id = self.check_id()
        customer = self.customers_list[customer_id-1]
        account_types = [account.account_type for account in customer.accounts_list]
        if not account_code in account_types:
            account_name = account_codes[account_code]
            print(f"You don't have a {account_name} yet.")
            to_open = input(f"Would you like to open a {account_name} ('yes'/'no')?: ")
            print()
            if to_open == 'yes':
                self.open_account(customer_id)
                return [customer.accounts_list[-1]]
            else:
                return None
        else:
            available_accounts = []
            for account in customer.accounts_list:
                if account.account_type == account_code:
                    available_accounts.append(account)
            return available_accounts
                            
    def open_account(self, customer_id):
        if not customer_id:
            customer_id = self.check_id()
        customer = self.customers_list[customer_id-1]
        customer_name = customer.customer_name
        
        for key, item in self.account_menu.items():
            print(f"{key}: {item['title']}")
        print()
        ac_option = input('Which type of Account would you like to open?: ')
        print()
        if ac_option.isdecimal() and int(ac_option) in self.account_menu.keys():
            account_type = self.account_menu[int(ac_option)]['title'][:-4]
            if int(ac_option) == 1:
                account = Account('N', customer_id, customer_name, balance=0)
            elif int(ac_option) == 2:
                account = CheckingAccount('C', customer_id, customer_name, balance=0, max_number=10, address=customer.home_address)
            elif int(ac_option) == 3:
                account = ForexAccount('F', customer_id, customer_name, balance=0)
            else:
                pass
            time.sleep(2)
            customer.accounts_list.append(account)
            print(f'Your {account_type} is ready. The Account ID is {account.account_id}.\n')
            account.show_info()
            account.show_balance()
        else:
            pass

    def add_customer(self, id):
        message = 'We will have you fill out the Registration Form, please.'
        print(f'{message}')
        print('-' * len(message))
        while True:
            name = input('Name: ')
            if name.replace(' ', '').isalpha():
                customer_name = name.title()
                break
        
        while True:
            district = input('District: ')
            if district.replace(' ', '').isalpha():
                district = district.title()
                break
        
        while True:
            home_address = input('Home Address: ')
            if not home_address.replace(' ', '').isdecimal() and len(home_address) > 0:
                home_address = home_address.title()
                break
        
        customer = Customer(id, customer_name, district, home_address)
        self.customers_list.append(customer)
        
        print("Alright, I'll get that set up for you...")
        time.sleep(2)
        print(f"\nIt's all set up. Your Customer ID is {id}.")
        
        self.new_customer_id += 1
    
    def deposit_service(self, accounts):
        if accounts and len(accounts) == 1:
            account = accounts[0]
            if account.account_type == 'F':
                account.forex_deposit()
            else:
                account.deposit()
        else:
            def print_accounts(accounts):
                for i in range(len(accounts)):
                    if accounts[i].account_type != 'F':
                        print(f'{i+1}: Account ID: {accounts[i].account_id} | Balance: {accounts[i].balance}')
            
            print_accounts(accounts)
            print()
            while True:
                index = input('Which account would you choose?: ')     
                if index.isdecimal() and 0 <= int(index)-1 <= len(accounts)-1:
                    account = accounts[int(index)-1]
                    if account.account_type == 'F':
                        account.forex_deposit()
                    else:
                        account.deposit()
                    next = input("Would you like to make another deposit ('yes' or 'no')?: ")
                    if next == 'no':
                        break
                    else:
                        print_accounts(accounts)
                        print()
    
    def withdrawl_service(self, accounts):
        if accounts and len(accounts) == 1:
            account = accounts[0]
            if account.account_type == 'F':
                account.forex_withdrawl()
            else:
                account.withdrawl()
        else:
            def print_accounts(accounts):
                for i in range(len(accounts)):
                    if accounts[i].account_type != 'F' and accounts[i].balance >= 100:
                        print(f'{i+1}: Account ID: {accounts[i].account_id} | Balance: {accounts[i].balance}')
            
            print_accounts(accounts)
            print()
            while True:
                index = input('Which account would you choose?: ')     
                if index.isdecimal() and 0 <= int(index)-1 <= len(accounts)-1:
                    account = accounts[int(index)-1]
                    if account.account_type == 'F':
                        account.forex_withdrawl()
                    else:
                        account.withdrawl()
                    count = 0
                    for account in accounts:
                        if account.account_type != 'F' and account.balance >= 100:
                            count += 1
                    if count > 0:
                        next = input("Would you like to make another withdrawl ('yes' or 'no')?: ")
                        if next == 'no':
                            break
                        else:
                            print_accounts(accounts)
                            print()
                    else:
                        print('All your Accounts have balance < 100.')
                        to_deposit = input("Would you like to make a deposit ('yes' or 'no')?: ")
                        if to_deposit == 'yes':
                            self.deposit_service(accounts)
    
    def issue_check_service(self, accounts):
        if accounts and len(accounts) == 1:
            checking_account = accounts[0]
            checking_account.issue_check()
        else:
            def print_accounts(accounts):
                for i in range(len(accounts)):
                    if accounts[i].balance >= 100:
                        print(f'{i+1}: Account ID: {accounts[i].account_id} | Balance: {accounts[i].balance}')
            
            print_accounts(accounts)
            print()
            while True:
                index = input('Which account would you choose?: ')     
                if index.isdecimal() and 0 <= int(index)-1 <= len(accounts)-1:
                    accounts[int(index)-1].issue_check()
                    count = 0
                    for account in accounts:
                        if account.balance >= 100:
                            count += 1
                    if count > 0:
                        next = input("Would you like to issue anoher check ('yes' or 'no')?: ")
                        if next == 'no':
                            break
                        else:
                            print_accounts(accounts)
                            print()
                    else:
                        print('All your Checking Accounts have a balance < 100.')
                        to_deposit = input("Would you like to make a deposit ('yes' or 'no')?: ")
                        if to_deposit == 'yes':
                            self.deposit_service(accounts)
    
    def bank_statement_service(self, accounts):
        if accounts:
            for account in accounts:
                account.bank_statement()

    def __str__(self):
        return f'This is {self.name}.'

    def __repr__(self):
        for customer in self.customers_list:
            repr(customer)
            print()
            print(f'Number of Accounts: {customer.count_accounts()}')
            print(f'Total Balance: ${customer.find_total_balance()}\n\n')
        return f'{self.count_customers()} | {self.show_total_deposits()}'

class Customer:
    def __init__(self, id, customer_name, district, home_address):
        self.customer_id = id
        self.customer_name = customer_name
        self.district = district
        self.home_address = home_address
        self.accounts_list = []
    
    def count_accounts(self):
        return len(self.accounts_list)
    
    def find_total_balance(self):
        total = 0
        for account in self.accounts_list:
            total += account.balance
        return total
    
    def __str__(self):
        return f'Customer ID: {self.customer_id} | Customer Name: {self.customer_name}'
        
    def __repr__(self):
        print(f'Customer ID: {self.customer_id}')
        print(f'Customer Name: {self.customer_name}')
        print('Accounts:')
        for account in self.accounts_list:
            print(f'Account ID: {account.account_id}', end=' | ')
            print(f'Account Type: {account.account_type} | Balance: {account.balance}')
            print(account.transactions_list)
        return ''

class Account:
    def __init__(self, account_type, customer_id, customer_name, balance=0):
        BANK_PREFIX = '011'
        time_stamp = dt.datetime.timestamp(dt.datetime.now())
        digits = str(int(time_stamp * (10 ** 6) % (10 ** 9))) # 攞 9 位數字
        self.account_id = f'{BANK_PREFIX}-{digits[:6]}-{digits[-3:]}'
        self.account_type = account_type
        self.customer_id = customer_id
        self.customer_name = customer_name
        self.balance = balance
        self.transactions_list = [['DateTime', 'Withdrawl', 'Deposit', 'Balance']]
        
    def show_info(self):
        account_types = {
            'N': 'Normal Account',
            'C': 'Checking Account',
            'F': 'Forex Account',
            # 'D': 'Fixed Deposit Account'
        }
        
        print(f'Account ID: {self.account_id}')
        print(f'Account Type: {account_types[self.account_type]}')
        print(f'Customer ID: {self.customer_id}')
        print(f'Customer Name: {self.customer_name}')
        print(f'Balance: ${self.balance}\n')
    
    def show_balance(self):
        print(f'Balance: ${self.balance}\n')

    def deposit(self):
        while True:
            amount = input('How much would you like to deposit?: $')
            if amount.isdecimal():
                amount = int(amount)
                if amount % 100 == 0:
                    now = dt.datetime.now()
                    datetime_str = now.strftime('%Y-%m-%d %H:%M:%S')
                    if self.account_type == 'N':
                        self.transactions_list.append([datetime_str, '', amount, self.balance + amount])
                    elif self.account_type == 'C':
                        self.transactions_list.append([datetime_str, '', '', amount, self.balance + amount])
                    self.balance += amount
                    print(f'${amount} is deposited into Account ID {self.account_id}')
                    break
                else:
                    print('Only denomination of 100 is accepted.')
                    deposit_amount = amount // 100 * 100
                    returned_amount = amount % 100
                    now = dt.datetime.now()
                    datetime_str = now.strftime('%Y-%m-%d %H:%M:%S')
                    if self.account_type == 'N':
                        self.transactions_list.append([datetime_str, '', amount, self.balance + deposit_amount])
                    elif self.account_type == 'C':
                        self.transactions_list.append([datetime_str, '', '', amount, self.balance + deposit_amount])
                    self.balance += deposit_amount
                    print(f'${deposit_amount} is deposited into Account ID {self.account_id}')
                    print(f'${returned_amount} is returned.')
                    break
        self.show_balance()
    
    def forex_deposit(self):
        
        while True:
            self.show_currencies()
            
            currency = input('Selected a Currency: ')
            
            is_valid = False
            for row in self.accepted_currencies:
                if currency in row:
                    is_valid = True
            if is_valid:
                break
        
        while True:
            amount = input('How much would you like to deposit?: $')
            
            # rates = {
            #     'AUD': 1.5014, 'BGN': 1.8036, 'BRL': 5.1314, 'CAD': 1.3633, 'CHF': 0.9088,
            #     'CNY': 7.227, 'CZK': 22.798, 'DKK': 6.8808, 'EUR': 0.92217, 'GBP': 0.79016,
            #     'HKD': 7.8015, 'HUF': 357.43, 'IDR': 15968, 'ILS': 3.718, 'INR': 83.35,
            #     'ISK': 138.6, 'JPY': 155.81, 'KRW': 1357.02, 'MXN': 16.681, 'MYR': 4.6875,
            #     'NOK': 10.7276, 'NZD': 1.6369, 'PHP': 57.69, 'PLN': 3.9331, 'RON': 4.588,
            #     'SEK': 10.7479, 'SGD': 1.3472, 'THB': 36.295, 'TRY': 32.262, 'ZAR': 18.2652
            # }
            
            api_url = 'https://api.frankfurter.app/latest'
            params_dict = {
                'from': 'USD'
            }
            response = requests.get(api_url, params_dict)
            results = response.json()
            rates = results['rates']
            
            if amount.isdecimal():
                amount = int(amount)
                if amount % 100 == 0:
                    now = dt.datetime.now()
                    datetime_str = now.strftime('%Y-%m-%d %H:%M:%S')
                    converted_amount = round((amount / rates['HKD']) * rates[currency], 2)
                    self.portfolio_dict[currency] = self.portfolio_dict.get(currency, 0) + converted_amount
                    
                    self.transactions_list.append(
                        [datetime_str, currency, '', converted_amount, self.portfolio_dict[currency]]
                    )
                    print(f"${converted_amount} of {currency} is deposited into Account ID {self.account_id}'s Portfolio.\n")
                    break
                else:
                    print('Only denomination of 100 is accepted.')
                    deposit_amount = amount // 100 * 100
                    returned_amount = amount % 100
                    
                    now = dt.datetime.now()
                    datetime_str = now.strftime('%Y-%m-%d %H:%M:%S')
                    converted_amount = round((deposit_amount / rates['HKD']) * rates[currency], 2)
                    
                    self.transactions_list.append(
                        [datetime_str, currency, '', converted_amount, self.portfolio_dict[currency] + converted_amount]
                    )
                    self.portfolio_dict[currency] += converted_amount
                    print(f"${converted_amount} of {currency} is deposited into Account ID {self.account_id}'s portfolio.")
                    print(f'HKD {returned_amount} is returned.\n')
                    break
        self.show_summary()
        print()
        
    def overdraft_protection(self, amount, payee=None):
        if amount <= self.balance:
            now = dt.datetime.now()
            datetime_str = now.strftime('%Y-%m-%d %H:%M:%S')
            if self.account_type == 'N':
                self.transactions_list.append([datetime_str, amount, '', self.balance - amount])
                print(f'${amount} is withdrawn from Account ID {self.account_id}')
            elif self.account_type == 'C':
                self.transactions_list.append([datetime_str, payee, amount, '', self.balance - amount])
                print(f'$A check of ${amount} is issued to {payee}')
            self.balance -= amount
        else:
            new_amount = self.balance
            print(f'${amount} exceeds the account balance ${self.balance}')
            now = dt.datetime.now()
            datetime_str = now.strftime('%Y-%m-%d %H:%M:%S')
            if self.account_type == 'N':
                self.transactions_list.append([datetime_str, new_amount, '', self.balance - new_amount])
                print(f'Only ${new_amount} is withdrawn from Account ID {self.account_id}')
            elif self.account_type == 'C':
                self.transactions_list.append([datetime_str, payee, amount, '', self.balance - new_amount])
                print(f'A check of only ${new_amount} is issued to {payee}')
            self.balance -= new_amount

    def forex_overdraft_protection(self, currency, amount):
        # rates = {
        #     'AUD': 1.5014, 'BGN': 1.8036, 'BRL': 5.1314, 'CAD': 1.3633, 'CHF': 0.9088,
        #     'CNY': 7.227, 'CZK': 22.798, 'DKK': 6.8808, 'EUR': 0.92217, 'GBP': 0.79016,
        #     'HKD': 7.8015, 'HUF': 357.43, 'IDR': 15968, 'ILS': 3.718, 'INR': 83.35,
        #     'ISK': 138.6, 'JPY': 155.81, 'KRW': 1357.02, 'MXN': 16.681, 'MYR': 4.6875,
        #     'NOK': 10.7276, 'NZD': 1.6369, 'PHP': 57.69, 'PLN': 3.9331, 'RON': 4.588,
        #     'SEK': 10.7479, 'SGD': 1.3472, 'THB': 36.295, 'TRY': 32.262, 'ZAR': 18.2652
        # }
        
        api_url = 'https://api.frankfurter.app/latest'
        params_dict = {
            'from': 'USD'
        }
        response = requests.get(api_url, params_dict)
        results = response.json()
        rates = results['rates']
        
        amount = float(amount)
        if amount > self.portfolio_dict[currency]:
            amount = self.portfolio_dict[currency]
        now = dt.datetime.now()
        datetime_str = now.strftime('%Y-%m-%d %H:%M:%S')
        converted_amount = round((amount / rates[currency]) * rates['HKD'], 1)
        self.transactions_list.append(
            [datetime_str, currency, amount, '', self.portfolio_dict[currency] - amount]
        )
        self.portfolio_dict[currency] -= amount
        print(f'{currency} {amount} is withdrawn from Account ID {self.account_id} and converted into HKD {converted_amount}')
        
    def withdrawl(self):
        while True:
            amount = input('How much would you like to withdrawl?: $')
            if amount.isdecimal():
                amount = int(amount)
                if amount % 100 == 0:
                    self.overdraft_protection(amount)
                    break
                else:
                    print('Only denomination of 100 is accepted.')
                    amount = amount // 100 * 100
                    self.overdraft_protection(amount)
                    break
        self.show_balance()
    
    def forex_withdrawl(self):
        print('Your Portfolio:')
        self.show_summary()
        
        while True:
            self.show_currencies()
            user_currency = input('Select a Currency: ')
            if user_currency in self.portfolio_dict.keys():
                break
        
        while True:
            amount = input('How much would you like to withdrawl?: $')
            print()
            
            if amount.isdecimal():
                self.forex_overdraft_protection(user_currency, amount)
                break
            
        self.show_summary()
        print()
        
    def issue_check(self):
        while True:
            payee = input("Who's the payee?: ")
            if payee.replace(' ', '').isalpha():
                break
        while True:
            amount = input('How much would you like send to the payee?: $')
            if amount.isdecimal():
                amount = int(amount)
                if amount % 100 == 0:
                    if payee:
                        self.overdraft_protection(amount, payee)
                    else:
                        self.overdraft_protection(amount)
                    break
                else:
                    print('Only denomination of 100 is accepted.')
                    amount = amount // 100 * 100
                    if payee:
                        self.overdraft_protection(amount, payee)
                    else:
                        self.overdraft_protection(amount)
                    break
        self.show_balance()
    
    def bank_statement(self):
        account_types = {
            'N': 'Normal Account',
            'C': 'Checking Account',
            'F': 'Forex Account',
            # 'D': 'Fixed Deposit Account'
        }
                                          
        print(f'Customer ID: {self.customer_id}')
        print(f'Customer Name: {self.customer_name}')
        print(f'Account ID: {self.account_id} ({account_types[self.account_type]})')
        print(tb.tabulate(self.transactions_list, headers='firstrow', stralign='right', numalign='right', tablefmt='grid'))
        print()
        
    def __str__(self):
        return f'Account ID: {self.account_id} | Account Type: {self.account_type}'
    
    def __repr__(self):
        return f'Account ID: {self.account_id} | Account Type: {self.account_type}'

class CheckingAccount(Account):
    def __init__(self, account_type, customer_id, customer_name, balance, max_number, address):
        super().__init__(account_type, customer_id, customer_name, balance)
        self.max_number = max_number
        self.address = address
        self.transactions_list = [['DateTime', 'Payee', 'Amount', 'Deposit', 'Balance']]
    
    def __str__(self):
        return f'Account ID: {self.account_id} | Account Type: {self.account_type}'
    
    def __repr__(self):
        return f'Account ID: {self.account_id} | Account Type: {self.account_type}'

class ForexAccount(Account):
    def __init__(self, account_type, customer_id, customer_name, balance):
        super().__init__(account_type, customer_id, customer_name, balance)
        self.portfolio_dict = dict()
        self.transactions_list = [['DateTime', 'Currency', 'Withdrawl', 'Deposit', 'Balance']]
        self.accepted_currencies = [
            ['AUD', 'BGN', 'BRL', 'CAD', 'CHF', 'CNY', 'CZK', 'DKK', 'EUR', 'GBP'],
            ['HKD', 'HUF', 'IDR', 'ILS', 'INR', 'ISK', 'JPY', 'KRW', 'MXN', 'MYR'],
            ['NOK', 'NZD', 'PHP', 'PLN', 'RON', 'SEK', 'SGD', 'THB', 'TRY', 'ZAR']
        ]
        
    def show_currencies(self):
        accepted_currencies = [
            ['AUD', 'BGN', 'BRL', 'CAD', 'CHF', 'CNY', 'CZK', 'DKK', 'EUR', 'GBP'],
            ['HKD', 'HUF', 'IDR', 'ILS', 'INR', 'ISK', 'JPY', 'KRW', 'MXN', 'MYR'],
            ['NOK', 'NZD', 'PHP', 'PLN', 'RON', 'SEK', 'SGD', 'THB', 'TRY', 'ZAR']
        ]
        
        print(tb.tabulate(accepted_currencies, tablefmt='simple'))
        print()
        
    def show_summary(self):
        summary = [(currency, amount) for (currency, amount) in self.portfolio_dict.items()]
        print(tb.tabulate(summary, headers=['Currency', 'Amount'], tablefmt='rst'))
    
    def __str__(self):
        return f'Account ID: {self.account_id} | Account Type: {self.account_type}'
    
    def __repr__(self):
        return f'Account ID: {self.account_id} | Account Type: {self.account_type}'


def main():
    bank_file = PickleFile(BANK_FILE)
    is_bank_file_exist = bank_file.is_exist()
    # print(f"Is Bank File '{BANK_FILE}' exist?: {is_bank_file_exist}")
    if not is_bank_file_exist:
        bank = Bank(BANK_NAME, 1)
        bank_file.save(bank)
        # print(bank_file.message('save') + '\n')
    else:
        bank_file = PickleFile(BANK_FILE)
        bank = bank_file.load()
        # print(bank_file.message('load') + '\n')
    # print(repr(bank) + '\n')
    print(f'{BANK_NAME} - Banking System\n')
    while True:
        bank.show_menu()
        bank_file.save(bank)

main()