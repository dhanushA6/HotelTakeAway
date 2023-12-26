class MenuObservable:
    def __init__(self):
        self.observers = {}

    def add_observer(self, observer):
        self.observers.append(observer)

    def remove_observer(self, observer):
        self.observers.remove(observer)

    def notify_observers(self, new_item):
        for observer in self.observers:
            observer.update(new_item)



class Customer:
    def __init__(self, name, phone_number, email):
        self.name = name
        self.phone_number = phone_number
        self.email = email

    def update(self, new_item):
        print(f"Hi {self.name}, a new item '{new_item}' has been added to the menu!")


