class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class MenuObservable(metaclass=SingletonMeta):
    def __init__(self):
        self.observers = {}

    def add_observer(self, observer):
        self.observers[observer.email] = observer

    def remove_observer(self, observer):
        del self.observers[observer.email]

    def notify_observers(self, new_item):
        for observer_email in self.observers:
            self.observers[observer_email].update(new_item)



class Customer:
    def __init__(self, name, phone_number, email):
        self.name = name
        self.ph_no = phone_number
        self.email = email

    def update(self, new_item):
        print(f"Hi {self.name}, a new item '{new_item}' has been added to the menu!")


