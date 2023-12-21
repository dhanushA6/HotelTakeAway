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
    


def add_item_to_cart(item_add, qty):
    try:
        # Try to load the existing cart object
        with open('cart.pkl', 'rb') as file:
            cart = pickle.load(file)
    except FileNotFoundError:
        # If file doesn't exist, create a new cart object
        cart = Cart()
        
    cart_dict = cart.get_cart_items() 
    flag = False 
    for item, q in cart_dict.items():
        # Add  duplicate item to the cart
        if item_add.name == item.name:
            flag = True
            cart_dict[item] = qty
            print("Item qty updated")
            break
    
    # Add new item to the cart
    if not flag:
        print("New Item Added")
        cart_dict[item_add] = qty
        
    with open('cart.pkl', 'wb') as file:
        pickle.dump(cart, file)
        print('Cart item added  and Saved Successfully')
    return True

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

def remove_cart_item(item_to_delete):
    try:
        # Try to load the existing cart object
        with open('cart.pkl', 'rb') as file:
            cart = pickle.load(file)
    except FileNotFoundError:
        # If file doesn't exist, create a new cart object
        cart = Cart()


    cart_dict = cart.get_cart_items()

    for item, qty in cart_dict.items():
        if item_to_delete.name == item.name:
                del cart_dict[item] 
                with open('cart.pkl', 'wb') as file:
                    pickle.dump(cart, file)
                    print('Cart item removed and Saved Successfully')
                break
  



def cart_items():
    try:
        # Try to load the existing cart object
        with open('cart.pkl', 'rb') as file:
            cart = pickle.load(file)
    except FileNotFoundError:
        # If file doesn't exist, create a new cart object
        cart = Cart()
    return cart.get_cart_items()

def get_cart_total():
    cart = cart_items()
    total = 0
    for item in cart:
        total += int(item.price)
    return total

def create_item(name, price, description, img, category, available=True):
    return MenuItem(name, price, description, img, category, available)
