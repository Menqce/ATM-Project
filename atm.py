import sys
import hashlib

class Account:
    def __init__(self, account_number, pin, balance=0):
        self.account_number = account_number
        self.pin_hash = self.hash_pin(pin)
        self.balance = balance
        self.transaction_history = []

    def hash_pin(self, pin):
        return hashlib.sha256(pin.encode()).hexdigest()

    def verify_pin(self, pin):
        return self.hash_pin(pin) == self.pin_hash

    def check_balance(self):
        return self.balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.transaction_history.append(f"Deposited: £{amount}")
        else:
            raise ValueError("Deposit amount must be positive.")

    def withdraw(self, amount):
        if amount > 0:
            if self.balance >= amount:
                self.balance -= amount
                self.transaction_history.append(f"Withdrew: £{amount}")
            else:
                raise ValueError("Insufficient balance.")
        else:
            raise ValueError("Withdrawal amount must be positive.")

    def get_transaction_history(self):
        return self.transaction_history

class ATM:
    def __init__(self):
        self.accounts = {}

    def create_account(self, account_number, pin, initial_deposit=0):
        if account_number in self.accounts:
            raise ValueError("Account already exists.")
        self.accounts[account_number] = Account(account_number, pin, initial_deposit)

    def authenticate_user(self, account_number, pin):
        if account_number in self.accounts and self.accounts[account_number].verify_pin(pin):
            return self.accounts[account_number]
        else:
            raise ValueError("Invalid account number or PIN.")

    def main_menu(self, account):
        while True:
            print("\nATM Main Menu")
            print("1. Check Balance")
            print("2. Deposit Money")
            print("3. Withdraw Money")
            print("4. View Transaction History")
            print("5. Exit")
            
            try:
                choice = int(input("Select an option: "))
                if choice == 1:
                    print(f"Your balance is: £{account.check_balance()}")
                elif choice == 2:
                    amount = float(input("Enter amount to deposit: "))
                    account.deposit(amount)
                    print("Deposit successful.")
                elif choice == 3:
                    amount = float(input("Enter amount to withdraw: "))
                    account.withdraw(amount)
                    print("Withdrawal successful.")
                elif choice == 4:
                    print("Transaction History:")
                    for transaction in account.get_transaction_history():
                        print(transaction)
                elif choice == 5:
                    print("Service Terminated. Thank you for using our service.")
                    break
                else:
                    print("Invalid option. Please try again.")
            except ValueError as e:
                print(f"Error: {e}. Please enter a valid option.")

    def start(self):
        print("Welcome to Chase Bank")
        while True:
            print("\n1. Create Account")
            print("2. Access Account")
            print("3. Exit")
            
            try:
                choice = int(input("Select an option: "))
                if choice == 1:
                    account_number = input("Enter new account number: ")
                    pin = input("Set a 4-digit PIN: ")
                    initial_deposit = float(input("Enter initial deposit (optional, default is £0): ") or 0)
                    self.create_account(account_number, pin, initial_deposit)
                    print("Account created successfully.")
                elif choice == 2:
                    account_number = input("Enter account number: ")
                    pin = input("Enter 4-digit PIN: ")
                    try:
                        account = self.authenticate_user(account_number, pin)
                        print("Login successful.")
                        self.main_menu(account)
                    except ValueError as e:
                        print(f"Error: {e}")
                elif choice == 3:
                    print("Service Terminated. Goodbye.")
                    sys.exit()
                else:
                    print("Invalid option. Please try again.")
            except ValueError as e:
                print(f"Error: {e}. Please enter a valid option.")

if __name__ == "__main__":
    atm = ATM()
    atm.start()
