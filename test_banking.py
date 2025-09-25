import unittest
from banking import BankSystem

class TestBank(unittest.TestCase):
    def setUp(self):
        self.bank = BankSystem("bank.csv")

        if "3001" not in self.bank.customers:
            self.bank.add_customer("3001", "Unit", "Test", "pw123", 100, 50)

    def test_add_customer(self):
        c = self.bank.add_customer("3002", "New", "Customer", "pw123")
        self.assertIsNotNone(c)
        self.assertEqual(c.first_name, "New")
        self.assertEqual(c.checking.balance, 0)

    def test_deposit(self):
        cust = self.bank.customers["3001"]
        old = cust.checking.balance
        cust.checking.deposit(50)
        self.assertEqual(cust.checking.balance, old + 50)

    def test_withdraw_limit(self):
        cust = self.bank.customers["3001"]
        cust.checking.withdraw(500)
        self.assertTrue(cust.checking.balance >= -100)

if __name__ == "__main__":
    unittest.main()
