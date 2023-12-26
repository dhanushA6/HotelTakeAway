import pickle

class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Menu:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def get_items(self):
        return self.items

class MenuBuilder(metaclass=SingletonMeta):
    def __init__(self):
        self.menus = {
            'Breakfast': Menu(),
            'Lunch': Menu(),
            'Snacks': Menu(),
            'TodayMenu': Menu(),
            'Dinner': Menu()
        }

    def add_to_menu(self, menu_type, item):
        if menu_type in self.menus:
            self.menus[menu_type].add_item(item)
        else:
            print(f"Menu type '{menu_type}' not found.")

    def remove_menu(self, item_remove):
        category = item_remove.category.capitalize()
        menus = self.menus[category].get_items()
        for item in menus:
            if item.name.lower() == item_remove.name.lower():
                menus.remove(item)
                self.menus[category].items = menus
                print("Item Removed Successfully")
                break
        return False

    def get_menu_items(self, menu_type):
        if menu_type in self.menus:
            return self.menus[menu_type].get_items()
        else:
            print(f"Menu type '{menu_type}' not found.")
            return []


