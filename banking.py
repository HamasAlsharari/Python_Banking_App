import csv

# Base Classes
class Account:
    def __init__(self, balance=0.0, active=True, overdraft_count=0):
        self.balance = float(balance)
        self.active = bool(active)
        self.overdraft_count = int(overdraft_count)
    
    def __str__(self):
        return f"Balance: {self.balance:.2f}, Active: {self.active}, Overdrafts: {self.overdraft_count}"

class CheckingAccount(Account):
        pass

class SavingsAccount(Account):
        pass

class Customer:
    def __init__(self, account_id, first_name, last_name, password, checking_balance=0.0, savings_balance=0.0,
                active=True, overdraft_count=0):
        self.account_id = str(account_id)
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.checking = CheckingAccount(checking_balance, active, overdraft_count)
        self.savings = SavingsAccount(savings_balance, active, overdraft_count)

    def __str__(self):
        return f"{self.account_id} - {self.first_name} {self.last_name}"

# Demo
if __name__ == "__main__":
    demo = Customer("10001", "William", "Hartnell", "4fg56", 100, 500, True, 0)
    print(demo)
    print(demo.checking)
    print(demo.savings)


