
#Strategy Pattern
# PaymentStrategy classes
class PaymentStrategy:
    def make_payment(self, amount):
        # Abstract method for making payments
        pass
    
class CreditCardPayment(PaymentStrategy):
    def make_payment(self, amount):
        # Implement credit card payment logic
        print(f"Paid ${amount} via Credit Card")

class CashPayment(PaymentStrategy):
    def make_payment(self, amount):
        # Implement cash payment logic
        print(f"Paid ${amount} in Cash")