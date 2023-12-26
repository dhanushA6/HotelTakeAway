import pickle
import wrapper as wp
class Menu:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def get_items(self):
        return self.items

class MenuBuilder:
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
        cateogry = item_remove.category.capitalize()
        menus = self.menus[cateogry].get_items()
        for item in menus:
            if item.name.lower() == item_remove.lower():
                menus.remove(item)
                self.menus[cateogry].items = menus
                self.save_to_pickle("menus.pickle")
                return True
                break
        return False
        
        

    def get_menu_items(self, menu_type):
        if menu_type in self.menus:
            return self.menus[menu_type].get_items()
        else:
            print(f"Menu type '{menu_type}' not found.")
            return []

    def save_to_pickle(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.menus, file)

    def load_from_pickle(self, filename):
        with open(filename, 'rb') as file:
            self.menus = pickle.load(file)

