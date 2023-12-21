from abc import ABC, abstractmethod
import random
from model.payment import *
from model.menu import *

# Placeholder function for generating a unique token
def generate_unique_token():
    return random.randint(100, 999) 

class Order(ABC):
    def __init__(self, items):
        self.items = items
        self.token = None
        self.is_paid = False
        self.payment_strategy = None

    def assign_token(self, token):
        self.token = token

    def calculate_bill(self):
        total_bill = sum(item.price*qty for item , qty in self.items.items())
        return total_bill

    def set_payment_strategy(self, payment_strategy):
        self.payment_strategy = payment_strategy

    def make_payment(self):
        if not self.payment_strategy:
            raise ValueError("Payment strategy is not set")
        bill_amount = self.calculate_bill()
        self.payment_strategy.make_payment(bill_amount)
        self.is_paid = True

    @abstractmethod
    def display_order(self):
        pass

class NormalOrder(Order):
    def __init__(self, items):
        self.type = 'normal'
        super().__init__(items)

    def display_order(self):
        
        for item, qty in self.items.items():
            print(f'{item.name}', ' '*abs(20 - len(item.name)), f'{item.price}',' '*(5-len(str(item.price))), f'{qty}')
        print("Normal Order:")
class PriorityOrder(Order):
    def __init__(self, items):
        self.type = 'priority'
        super().__init__(items)

    def display_order(self):
        
        for item, qty in self.items.items():
            print(f'{item.name}', ' '*abs(20 - len(item.name)), f'{item.price}',' '*(5-len(str(item.price))), f'{qty}')
        print("Priority Order:")
        
# Factory Method for creating orders
class OrderFactory:
    @staticmethod
    def create_order(items):
        if len(items) <= 3:
            return PriorityOrder(items)
        else:
            return NormalOrder(items)

