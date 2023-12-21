class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Cart(metaclass=SingletonMeta):
    def __init__(self):
        self.orders = {}

    def add_to_cart(self, item, qty):
        self.orders[item] = qty

    def get_cart_items(self):
        return self.orders


