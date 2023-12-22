from model.menu_manage import MenuManager
from model.order_manage import *
from model.cart import SingletonMeta, Cart
from model.orders import Orders
import pickle, os
import random
from datetime import datetime
from model.customer import Customer
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
    for item, qty in cart.items():
        total += int(item.price) * int(qty)
    return total

def create_item(name, price, description, img, category, available=True):
    return MenuItem(name, price, description, img, category, available)


def get_cart_item_names():
    cart = load_cart()
    cart_names = []
    cart_dict = cart.get_cart_items()
    for item  in cart_dict:
        cart_names.append(item.name)
    return cart_names

def load_cart():
    try:
        # Try to load the existing cart object
        with open('cart.pkl', 'rb') as file:
            cart = pickle.load(file)
    except FileNotFoundError:
        # If file doesn't exist, create a new cart object
        cart = Cart()
    return cart

#----------------------------- Orders Section-------------------------------------
def push_orders(order):

    try:
        with open('order.pkl', 'rb') as file:
            orders_list = pickle.load(file)
    except FileNotFoundError:
        orders_list = []
    orders_list.append(order)
    with open('order.pkl', 'wb') as file:
        pickle.dump(orders_list, file)
        print('Order Added Successfully')
        file.close()

def create_order(cust_obj):
    cart_obj = load_cart()
    cart_dict = cart_obj.get_cart_items()
    new_order = OrderFactory.create_order(cart_dict, cust_obj)
    return new_order

def create_token():
    return random.randint(100, 999)

def assign_token_and_datetime(new_order):
    generated_token = create_token()
    new_order.token = generated_token
    current_datetime = datetime.now()
    current_date = current_datetime.date()
    current_time = current_datetime.time()
    new_order.order_date = current_date
    new_order.order_time = current_time.strftime("%H:%M:%S")
    print("Token assigned to the order ")

def get_ordered_cart_items(new_order):
    return new_order.items

def get_ordered_bill_total(new_order):
    items = new_order.items
    total = 0
    for item, qty in items.items():
        total += int(item.price) * int(qty)
    return total

def assign_strategy(new_order, payment_strategy):
    if payment_strategy == "paypal":
        paypal = PayPalPayment()
        new_order.payment_strategy = paypal
        print("Paypal Payment Strategy assigned Succesfully")
        return paypal
    elif payment_strategy == "googlepay":
        google_pay = GooglePayPayment()
        new_order.payment_strategy = google_pay
        print("Google pay Payment Strategy assigned Succesfully")
        return google_pay
    elif payment_strategy== "cash": 
        cash = CashPayment()
        new_order.payment_strategy = cash
        print("Cash Payment Strategy assigned Succesfully")
        return cash
    
def make_payment_for_order(payment_obj, new_order):
    bill_total = get_ordered_bill_total(new_order)
    new_order.is_paid = True
    payment_obj.make_payment(bill_total)

def get_orders_list():
    try:
        # Try to load the existing cart object
        with open('order.pkl', 'rb') as file:
            order_list = pickle.load(file)
            file.close()
        return order_list
    except FileNotFoundError:
        # If file doesn't exist, create a new cart object
        print("No Order is Created")
        return False
    
def create_customer(name, ph_no, email):
    return Customer(name, ph_no, email)

def create_payment_obj():
    return PaymentStrategy()

def do_payment(payment_option, new_order):

    if payment_option == "paypal":
                payment_obj = assign_strategy(new_order, payment_option)
                print("Payment Object: ",payment_obj)
                make_payment_for_order(payment_obj, new_order)
    elif payment_option == "googlepay":
        payment_obj = assign_strategy(new_order, payment_option)
        make_payment_for_order(payment_obj, new_order)
    elif payment_option.lower() == "cash":
        payment_obj = assign_strategy(new_order, payment_option)
        make_payment_for_order(payment_obj, new_order)
    else:
        raise ValueError("Invalid payment option")











    




