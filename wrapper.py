from model.menu_manage import MenuManager
from model.order_manage import *
from model.cart import SingletonMeta, Cart
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



def create_tokens():
    return 100

def create_order( cart_items):
    new_order = OrderFactory.create_order(cart_items)
    order_type = new_order.type
    token_number = create_tokens()
    new_order.token = token_number
    total_amount = new_order.calculate_bill()
    


def additem_to_cart(item, qty):
    try:
        # Try to load the existing cart object
        with open('cart.pkl', 'rb') as file:
            cart = pickle.load(file)
    except FileNotFoundError:
        # If file doesn't exist, create a new cart object
        cart = Cart()

    # Add item to the cart
    cart.add_to_cart(item, qty)
    
    # Save the updated cart object to the file using pickle
    with open('cart.pkl', 'wb') as file:
        pickle.dump(cart, file)
        print('Item Added to cart Successfully')


def make_cart_empty():
    try:
        # Try to load the existing cart object
        with open('cart.pkl', 'rb') as file:
            cart = pickle.load(file)
    except FileNotFoundError:
        # If file doesn't exist, create a new cart object
        cart = Cart()

    cart.orders = {}

    with open('cart.pkl', 'wb') as file:
        pickle.dump(cart, file)
        print('Item Added to cart Successfully')
        
    print("Cart got Empty")


def cart_items():
    try:
        # Try to load the existing cart object
        with open('cart.pkl', 'rb') as file:
            cart = pickle.load(file)
    except FileNotFoundError:
        # If file doesn't exist, create a new cart object
        cart = Cart()
    return cart.get_cart_items()
