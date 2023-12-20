# from model.menu_manage import MenuManager
# from model.order_manage import *
import pickle, os

# Path Constants
CONFIG_PATH = os.path.dirname(os.path.realpath(__file__))
APP_PATH = os.path.abspath(os.path.join(CONFIG_PATH, '..'))
pickle_name = CONFIG_PATH + "\\menu.pickle"

def load_menus():
    try:
        with open(pickle_name, 'rb') as file:
            menus = pickle.load(file)
        return menus
    except FileNotFoundError:
        print("Menu file not found.")
    except Exception as e:
        print(f"Error loading menus: {e}")

def get_menu_items(menu_type):
    menus = load_menus()
    if menu_type.capitalize() not in menus:
        return False
    menu = menus[menu_type.capitalize()]
    selected_items = menu.get_menu_items()
    items_data = []
    for item in selected_items:
        items_data.append(item.get_attrs())
    return items_data

def dump_menus(menus):
    try:
        with open('all_menus.pkl', 'wb') as file:
            pickle.dump(menus, file)
    except Exception as e:
        print(f"Error saving menus: {e}")
