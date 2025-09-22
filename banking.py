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

    
    
# BankSystem
class BankSystem:
    def __init__(self, filename="bank.csv"):
        self.filename = filename
        self.customers = {}
        self.load()

    def load(self):
        self.customers = {}
        try:
            with open(self.filename, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    acct_id = row["id"]
                    first = row["first_name"]
                    last = row["last_name"]
                    pw = row["password"]

                    try:
                        checking_bal = float(row.get("checking", 0))
                    except (ValueError, TypeError):
                        checking_bal = 0.0

                    try:
                        savings_bal = float(row.get("savings", 0))
                    except (ValueError, TypeError):
                        savings_bal = 0.0

                    active = row.get("active", "True") == "True"
                    try:
                        overdrafts = int(row.get("overdraft_count", 0))
                    except (ValueError, TypeError):
                        overdrafts = 0

                    cust = Customer(acct_id, first, last, pw, checking_bal, savings_bal, active, overdrafts)
                    self.customers[acct_id] = cust
        except FileNotFoundError:
            print(f"{self.filename} not found. Please create it first.")

    def list_customers(self):
        for c in self.customers.values():
            print(c)

# add customer
    def add_customer(self, account_id, first_name, last_name, password, checking=0.0, savings=0.0,
                    active=True, overdraft_count=0):
        if account_id in self.customers:
           print("❌ Account ID already exists") 
           return None

        new_cust = Customer(account_id, first_name, last_name, password, checking, savings,
                            active, overdraft_count)

        with open(self.filename, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=[
                "id", "first_name", "last_name", "password", "checking", "savings",
                "active", "overdraft_count"
            ])
            if f.tell() == 0:
                writer.writeheader()
            writer.writerow({
                "id": account_id,
                "first_name": first_name,
                "last_name": last_name,
                "password": password,
                "checking": checking,
                "savings": savings,
                "active": active,
                "overdraft_count": overdraft_count
            })
        self.customers[account_id] = new_cust
        print(f"✅ Customer {first_name} {last_name} added successfully!")
        return new_cust

# demo
if __name__ == "__main__":
    bank = BankSystem("bank.csv")
    bank.add_customer("20002", "Hamas", "Alsharari", "H6h5m", 100, 50, True, 0)
    bank.list_customers()