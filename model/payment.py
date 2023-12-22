# PaymentStrategy classes
class PaymentStrategy:
    def make_payment(self, amount):
        # Abstract method for making payments
        pass
    
class PayPalPayment(PaymentStrategy):
    def __init__(self, payment_type = "PayPal"):
        self.payment_type = payment_type
    def make_payment(self, amount):
        # Implement PayPal payment logic
        print(f"Paid ${amount} using PayPal")

class GooglePayPayment(PaymentStrategy):
    def __init__(self, payment_type = "GooglePay"):
        self.payment_type = payment_type
    def make_payment(self, amount):
        # Implement Google Pay payment logic
        print(f"Paid ${amount} using Google Pay")

class CashPayment(PaymentStrategy):
    def __init__(self, payment_type = "Cash"):
        self.payment_type = payment_type
        
    def make_payment(self, amount):
        # Implement cash payment logic
        print(f"Paid ${amount} in Cash")