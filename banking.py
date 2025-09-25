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
    def deposit(self, amount):
        if amount <= 0:
            print("❌ Deposit amount must be positive")
            return
        self.balance += amount
        if self.balance >= 0 and not self.active:
            self.active = True
            self.overdraft_count = 0
            print(f"♻️ Account reactivated!")
        print(f"✅ Deposited {amount}. New balance: {self.balance}")

    def withdraw(self, amount):
        if amount > 100:
            print("❌ Cannot withdraw more than $100 at once")
            return
        if self.balance - amount < -100:
            print("❌ Withdrawal denied: balance cannot go below -100")
            return
        self.balance -= amount
        if self.balance < 0:
            self.balance -= 35
            self.overdraft_count += 1
            if self.overdraft_count >= 2:
                self.active = False
        print(f"✅ Withdraw {amount}. New balance: {self.balance}")


class SavingsAccount(Account):
    def deposit(self, amount):
        if amount <= 0:
            print("❌ Deposit amount must be positive")
            return
        self.balance += amount
        if self.balance >= 0 and not self.active:
            self.active = True
            self.overdraft_count = 0
            print(f"♻️ Account reactivated!")
        print(f"✅ Deposited {amount}. New balance: {self.balance}")

    def withdraw(self, amount):
        if amount > 100:
           print("❌ Cannot withdraw more than $100 at once")
           return
        if self.balance - amount < -100:
            print("❌ Withdrawal denied: balance cannot go below -100")
            return
        self.balance -= amount
        if self.balance < 0:
            self.balance -= 35
            self.overdraft_count += 1
            if self.overdraft_count >= 2:
                self.active = False
        print(f"✅ Withdraw {amount}. New balance: {self.balance}")


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


# authenticate, logout
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

# internal transfers
    def transfer_internal(self, cust, from_acc, to_acc, amount):
        if from_acc == to_acc:
            print("❌ Cannot transfer to the same account") 
            return 

        if from_acc == "checking":
            from_account = cust.checking
        else:
            from_account = cust.savings

        if to_acc == "checking":
            to_account = cust.checking
        else:
            to_account = cust.savings

        if amount > from_account.balance + 100:
            print("❌ Not enough funds for this transfer")
            return 

        from_account.withdraw(amount)
        to_account.deposit(amount)
        self.save()
        print(f"✅ Transferred {amount} from {from_acc} to {to_acc}")

# external transfers
    def transfer_external(self, from_cust, to_account_id, from_acc, to_acc, amount):
        to_cust = self.customers.get(to_account_id)
        if not to_cust:
            print("❌ Destination account not found")
            return

        if from_acc == "checking":
            from_account = from_cust.checking
        else:
            from_account = from_cust.savings

        if to_acc == "checking":
            to_account = to_cust.checking
        else:
            to_account = to_cust.savings

        if amount > from_account.balance + 100:
            print("❌ Not enough funds for this transfer")
            return

        from_account.withdraw(amount)

        if not from_account.active:
            print(f"❌ Transfer canceled: {from_acc} account of {from_cust.account_id} is deactivated due to overdraft")
            return

        to_account.deposit(amount)
        self.save()
        print(f"✅ Transferred {amount} from {from_cust.account_id} ({from_acc}) to {to_cust.account_id} ({to_acc})")

    
if __name__ == "__main__":
    bank = BankSystem("bank.csv")

    print("Welcome to ACME Bank!")

    while True:
        have_account = input("Do you have an account? (yes/no): ").lower()
        if have_account in ["yes", "no"]:
            break
        print("❌ Please answer 'yes' or 'no' only.")

    if have_account == "no":
        print("Let's create your account.")
        account_id = input("Enter a new account ID: ")
        first_name = input("First Name: ")
        last_name = input("Last Name: ")
        password = input("Password: ")
        checking = float(input("Initial Checking Balance (0 if none): "))
        savings = float(input("Initial Savings Balance (0 if none): "))
        bank.add_customer(account_id, first_name, last_name, password, checking, savings)
     
    print("\n--- Login ---")
    login_id = input("Enter your account ID: ")
    login_pw = input("Enter your password: ")
    cust = bank.authenticate(login_id, login_pw)

    if cust:
        while True:
            print("\nWhat do you want to do?")
            print("1. Deposit")
            print("2. Withdraw")
            print("3. Transfer Internal (checking <-> savings)")
            print("4. Transfer External (to another customer)")
            print("5. Logout")
            choice = input("Enter choice (1-5):")

            
            if choice == "1":
                while True:
                    acc_type = input("Deposit to 'checking' or 'savings': ").lower()
                    if acc_type in ["checking", "savings"]:
                        break
                    print("❌ Please enter 'checking' or 'savings' only.")
                amount = float(input("Amount to deposit: "))
                if acc_type == "checking":
                    cust.checking.deposit(amount)
                else:
                    cust.savings.deposit(amount)

            elif choice == "2":
                while True:
                    acc_type = input("Withdraw from 'checking' or 'savings': ").lower()
                    if acc_type in ["checking", "savings"]:
                        break
                    print("❌ Please enter 'checking' or 'savings' only.")
                amount = float(input("Amount to withdraw: "))
                if acc_type == "checking":
                    cust.checking.withdraw(amount)
                else:
                    cust.savings.withdraw(amount)

            elif choice == "3":
                while True:
                    from_acc = input("Transfer from 'checking' or 'savings': ").lower()
                    if from_acc in ["checking", "savings"]:
                        break
                    print("❌ Please enter 'checking' or 'savings' only.")
                while True:
                    to_acc = input("Transfer to 'checking' or 'savings': ").lower()
                    if to_acc in ["checking", "savings"]:
                        break
                    print("❌ Please enter 'checking' or 'savings' only.")
                amount = float(input("Amount to transfer: "))
                bank.transfer_internal(cust, from_acc, to_acc, amount)

            elif choice == "4":
                to_id = input("Enter destination account ID: ")
                while True:
                    from_acc = input("Transfer from 'checking' or 'savings': ").lower()
                    if from_acc in ["checking", "savings"]:
                        break
                    print("❌ Please enter 'checking' or 'savings' only.")
                while True:
                    to_acc = input("Transfer to 'checking' or 'savings': ").lower()
                    if to_acc in ["checking", "savings"]:
                        break
                    print("❌ Please enter 'checking' or 'savings' only.")
                amount = float(input("Amount to transfer: "))
                bank.transfer_external(cust, to_id, from_acc, to_acc, amount)

            elif choice == "5":
                cust = bank.logout(cust)
                break

            else:
                print("Invalid choice, try again.")