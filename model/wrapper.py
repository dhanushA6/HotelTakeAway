from menu_manage import *
from order_manage import *
import pickle


def load_menus():
    try:
        with open('all_menus.pkl', 'rb') as file:
            menus = pickle.load(file)
    except FileNotFoundError:
        print("Menu file not found.")
        menus = {}
    except Exception as e:
        print(f"Error loading menus: {e}")
    return menus

def get_menu_items(menus, menu_type):
    if menu_type not in menus:
        return False
    menu = menus[menu_type.capitalize()]
    selected_items = menu.get_menu_items()
    return selected_items

def dump_menus(menus):
    try:
        with open('all_menus.pkl', 'wb') as file:
            pickle.dump(menus, file)
    except Exception as e:
        print(f"Error saving menus: {e}")


