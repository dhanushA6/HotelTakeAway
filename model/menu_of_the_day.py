import pickle

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

# # Usage
# builder = MenuBuilder()
# builder.add_to_menu('Breakfast', 'Cereal')
# builder.add_to_menu('Breakfast', 'Omelette')
# builder.add_to_menu('Lunch', 'Chicken Sandwich')
# builder.add_to_menu('Lunch', 'Pasta')
# builder.add_to_menu('Snacks', 'Chips')
# builder.add_to_menu('TodayMenu', 'Chef Special')
# builder.add_to_menu('Dinner', 'Steak')

# # Save to pickle file
# # builder.save_to_pickle('menu_data.pickle')

# # Create a new instance of MenuBuilder
# builder = MenuBuilder()
# builder.load_from_pickle('menu_data.pickle')
# builder.add_to_menu("Breakfast", "Vadai")
# builder.save_to_pickle('menu_data.pickle')
# new_builder = MenuBuilder()
# # Load data from the pickle file
# new_builder.load_from_pickle('menu_data.pickle')

# # Get items for a specific menu type after loading from pickle
# breakfast_menu = new_builder.get_menu_items('Breakfast')
# print("Breakfast Menu:", breakfast_menu)

# # ... similarly for other menu types
