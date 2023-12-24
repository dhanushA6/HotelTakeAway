from abc import ABC, abstractmethod
from model.menu import MenuItem  # Assuming MenuItem class is imported correctly


# Abstract Factory Method for Menu Creation
class Menu(ABC):
    @abstractmethod
    def get_menu_items(self):
        pass

    @abstractmethod
    def add_item(self, name, price, description, img, category, available=True):
        pass

    @abstractmethod
    def delete_item(self, item_name):
        pass

    @abstractmethod
    def update_item(self, old_item_name, new_item):
        pass


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class BreakfastMenu(metaclass=SingletonMeta):
    def __init__(self):
        self.items = []

    def get_menu_items(self):
        return [item for item in self.items]

    def add_item(self, name, price, description, img, category, available=True):
        new_item = MenuItem(name, price, description, img, category, available)
        self.items.append(new_item)

    def delete_item(self, item_name):
        for item in self.items:
            if item.name.lower() == item_name.lower():
                self.items.remove(item)
                print(f"Item {item.name} is removed from the Menu Successfully")
                break

    def update_item(self, old_item_name, new_item):
        for item in self.items:
            if item.name == old_item_name:
                item.name = new_item.name
                item.price = new_item.price
                item.description = new_item.description
                item.available = new_item.available
                break


class LunchMenu(metaclass=SingletonMeta):
    def __init__(self):
        self.items = []

    def get_menu_items(self):
        return [item for item in self.items]

    def add_item(self, name, price, description, img, category, available=True):
        new_item = MenuItem(name, price, description, img, category, available)
        self.items.append(new_item)

    def delete_item(self, item_name):
        for item in self.items:
            if item.name.lower() == item_name.lower():
                self.items.remove(item)
                print(f"Item {item.name} is removed from the Menu Successfully")
                break

    def update_item(self, old_item_name, new_item):
        for item in self.items:
            if item.name == old_item_name:
                item.name = new_item.name
                item.price = new_item.price
                item.description = new_item.description
                item.available = new_item.available
                break


class SnacksMenu(metaclass=SingletonMeta):
    def __init__(self):
        self.items = []

    def get_menu_items(self):
        return [item for item in self.items]

    def add_item(self, name, price, description, img, category, available=True):
        new_item = MenuItem(name, price, description, img, category, available)
        self.items.append(new_item)

    def delete_item(self, item_name):
        for item in self.items:
            if item.name.lower() == item_name.lower():
                self.items.remove(item)
                print(f"Item {item.name} is removed from the Menu Successfully")
                break

    def update_item(self, old_item_name, new_item):
        for item in self.items:
            if item.name == old_item_name:
                item.name = new_item.name
                item.price = new_item.price
                item.description = new_item.description
                item.available = new_item.available
                break


class TodayMenu(metaclass=SingletonMeta):
    def __init__(self):
        self.items = []

    def get_menu_items(self):
        return [item for item in self.items]

    def add_item(self, name, price, description, img, category, available=True):
        new_item = MenuItem(name, price, description, img, category, available)
        self.items.append(new_item)

    def delete_item(self, item_name):
        for item in self.items:
            if item.name.lower() == item_name.lower():
                self.items.remove(item)
                print(f"Item {item.name} is removed from the Menu Successfully")
                break

    def update_item(self, old_item_name, new_item):
        for item in self.items:
            if item.name == old_item_name:
                item.name = new_item.name
                item.price = new_item.price
                item.description = new_item.description
                item.available = new_item.available
                break


class DinnerMenu(metaclass=SingletonMeta):
    def __init__(self):
        self.items = []

    def get_menu_items(self):
        return [item for item in self.items]

    def add_item(self, name, price, description, img, category, available=True):
        new_item = MenuItem(name, price, description, img, category, available)
        self.items.append(new_item)

    def delete_item(self, item_name):
        for item in self.items:
            if item.name.lower() == item_name.lower():
                self.items.remove(item)
                print(f"Item {item.name} is removed from the Menu Successfully")
                break

    def update_item(self, old_item_name, new_item):
        for item in self.items:
            if item.name == old_item_name:
                item.name = new_item.name
                item.price = new_item.price
                item.description = new_item.description
                item.available = new_item.available
                break


class DessertMenu(metaclass=SingletonMeta):
    def __init__(self):
        self.items = []

    def get_menu_items(self):
        return [item for item in self.items]

    def add_item(self, name, price, description, img, category, available=True):
        new_item = MenuItem(name, price, description, img, category, available)
        self.items.append(new_item)

    def delete_item(self, item_name):
        for item in self.items:
            if item.name.lower() == item_name.lower():
                self.items.remove(item)
                print(f"Item {item.name} is removed from the Menu Successfully")
                break

    def update_item(self, old_item_name, new_item):
        for item in self.items:
            if item.name == old_item_name:
                item.name = new_item.name
                item.price = new_item.price
                item.description = new_item.description
                item.available = new_item.available
                break


class MenuManager(metaclass=SingletonMeta):
    def __init__(self):
        self.menus = {
            "Breakfast": BreakfastMenu(),
            "Lunch": LunchMenu(),
            "Snacks": SnacksMenu(),
            "TodayMenu": TodayMenu(),
            "Dessert": DessertMenu(),
            "Dinner": DinnerMenu()
        }

    def get_menu(self, menu_type):
        return self.menus.get(menu_type)
