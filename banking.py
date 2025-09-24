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

    def save(self):
        with open(self.filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=[
                "id", "first_name", "last_name", "password", "checking", "savings",
                "active", "overdraft_count"
            ])
            writer.writeheader()
            for cust in self.customers.values():
                writer.writerow({
                    "id": cust.account_id,
                    "first_name": cust.first_name,
                    "last_name": cust.last_name,
                    "password": cust.password,
                    "checking": cust.checking.balance,
                    "savings": cust.savings.balance,
                    "active": cust.checking.active,
                    "overdraft_count": cust.checking.overdraft_count
                })
       
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
        self.customers[account_id] = new_cust
        self.save()
        print(f"✅ Customer {first_name} {last_name} added successfully!")
        return new_cust


# authenticate, deposit, withdraw
    def authenticate(self, account_id, password):
        cust = self.customers.get(account_id)
        if cust and cust.password == password:
            print(f"✅ Welcome {cust.first_name} {cust.last_name}")
            return cust
        print("❌ Invalid credentials")
        return None

    def logout(self, cust):
        print(f"✅ {cust.first_name} {cust.last_name} logged out")
        cust = None
        return cust

    def deposit(self, cust, account_type, amount):
        if amount <= 0:
            print("❌ Deposit amount must be positive")
            return
        acct = cust.checking if account_type == "checking" else cust.savings
        acct.balance += amount

        if acct.balance >= 0 and not acct.active:
            acct.active = True
            acct.overdraft_count = 0
            print(f"♻️ Account {account_type} reactivated!")

        print(f"✅ Deposited {amount} to {account_type}. New balance: {acct.balance}")

    def withdraw(self, cust, account_type, amount):
        acct = cust.checking if account_type == "checking" else cust.savings
        if amount > 100:
            print("❌ Cannot withdraw more than $100 at once")
            return
        if acct.balance - amount < -100:
            print("❌ Withdrawal denied: balance cannot go below -100")
            return 
        acct.balance -= amount
        if acct.balance < 0:
            acct.balance -= 35
            acct.overdraft_count += 1
            if acct.overdraft_count >= 2:
                acct.active = False
        print(f"✅ Withdraw {amount} from {account_type}. New balance: {acct.balance}")

# internal transfers
    def transfer_internal(self, cust, from_acc, to_acc, amount):
        if from_acc == to_acc:
            print("❌ Cannot tranfer to the same account") 
            return 
        from_account = cust.checking if from_acc == "checking" else cust.savings
        to_account = cust.checking if to_acc == "checking" else cust.savings

        if amount > from_account.balance + 100:
            print("❌ Not enough funds for this transfer")
            return 
        
        self.withdraw(cust, from_acc, amount)
        self.deposit(cust, to_acc, amount)
        print(f"✅ Transferred {amount} from {from_acc} to {to_acc}")

# external transfers
    def transfer_external(self, from_cust, to_account_id, from_acc, to_acc, amount):
        to_cust = self.customers.get(to_account_id)
        if not to_cust:
            print("❌ Destination account not found")
            return

        from_account = from_cust.checking if from_acc == "checking" else from_cust.savings

        if amount > from_account.balance + 100:
            print("❌ Not enough funds for this transfer")
            return

        self.withdraw(from_cust, from_acc, amount)

        if not from_account.active:
            print(f"❌ Transfer canceled: {from_acc} account of {from_cust.account_id} is deactivated due to overdraft")
            return

        self.deposit(to_cust, to_acc, amount)

        print(f"✅ Transferred {amount} from {from_cust.account_id} ({from_acc}) to {to_cust.account_id}({to_acc})")


if __name__ == "__main__":
    bank = BankSystem("bank.csv")
    cust1 = bank.authenticate("20002", "H6h5m")
    cust2 = bank.customers.get("10001")
    if cust1 and cust2:
        bank.transfer_external(cust1, "10001", "checking", "checking", 10)
        bank.save()
        print("Cust1 Checking:", cust1.checking.balance)
        print("Cust2 Checking:", cust2.checking.balance)