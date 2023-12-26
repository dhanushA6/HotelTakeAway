from model.menu_manage import MenuManager
from model.order_manage import *
from model.cart import  Cart
from model.orders import Orders
import pickle, os
import random
from datetime import datetime
from model.customer import Customer, MenuObservable
from model.menu_of_the_day import MenuBuilder
# Path Constants
CONFIG_PATH = os.path.dirname(os.path.realpath(__file__))
APP_PATH = os.path.abspath(os.path.join(CONFIG_PATH, '..'))
pickle_name = CONFIG_PATH + "\\menu.pickle"


def add_subscriber(cust):
    try:
        with open("subscribers.pkl", 'rb') as file:
            obj = pickle.load(file)
            file.close()
    except:
        #using Observer Pattern here
        obj = MenuObservable()
        

    if cust.email not in obj.observers:
        obj.add_observer(cust)
        print("Subscriber added Successfully....")

    with open("subscribers.pkl", 'wb') as file :
        pickle.dump(obj, file)
        file.close()
 
       


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
    selected_items = menus[menu_type.capitalize()]
    #selected_items = menu.get_menu_items()
    items_data = []
    for item in selected_items:
        items_data.append(item.get_attrs())
    return items_data

def get_all_menu_items():
    menus = load_menus()
    all_menu_items = {}

    for menu_type, menu_items in menus.items():
        selected_items = menu_items
        items_data = []
        for item in selected_items:
            items_data.append(item.get_attrs())

        all_menu_items[menu_type] = items_data

    return all_menu_items

def dump_data(menus, filename):
    try:
        with open(filename, 'wb') as file:
            pickle.dump(menus, file)
        return True
    except Exception as e:
        print(f"Error saving pickle file: {e}")

#---------------- Cart Section ---------------------------------------

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
    return True

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
    add_subscriber(cust_obj)
    new_order = OrderFactory.create_order(cart_dict, cust_obj)
    return new_order

def create_token():
    return len(get_orders_list()) + 1

def assign_token_and_datetime(new_order):
    generated_token = create_token()
    new_order.token = generated_token
    
    current_datetime = datetime.now()
    current_date = current_datetime.date()
    current_time = current_datetime.time()
    
    format_date = current_date.strftime("%B %d, %Y")
    
    new_order.order_date = format_date
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
        return []
    
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
    
#----------------  Admin Paneld Functionality -----------------------------
def load_menu_data():
    try:
        with open('menu.pickle', 'rb') as f:
            menus = pickle.load(f)
            print("menus data Loaded Successfully")
    except:
        menu_manager = MenuManager()
        breakfast_menu = menu_manager.get_menu("Breakfast")
        dinner_menu = menu_manager.get_menu("Dinner")
        lunch_menu = menu_manager.get_menu("Lunch")
        today_menu = menu_manager.get_menu("TodayMenu")
        dessert_menu = menu_manager.get_menu("Dessert")
        snack_menu = menu_manager.get_menu("Snacks")
        menus = {
        "Breakfast": breakfast_menu.items,
        "Lunch": lunch_menu.items,
        "Snacks": snack_menu.items,
        "TodayMenu": today_menu.items,
        "Dinner": dinner_menu.items,
        "Dessert": dessert_menu.items }    
    return menus

def assign_menu_data():

    menu_manager = MenuManager()
    menus = load_menu_data()

    breakfast_menu = menu_manager.get_menu("Breakfast")
    breakfast_menu.items = menus["Breakfast"]

    dinner_menu = menu_manager.get_menu("Dinner")
    dinner_menu.items = menus["Dinner"]
    
    lunch_menu = menu_manager.get_menu("Lunch")
    lunch_menu.items = menus["Lunch"]

    today_menu = menu_manager.get_menu("TodayMenu")
    today_menu.items = menus["TodayMenu"]

    dessert_menu = menu_manager.get_menu("Dessert")
    dessert_menu.items = menus["Dessert"]

    snack_menu = menu_manager.get_menu("Snacks")
    snack_menu.items = menus["Snacks"]

def dump_menu_data():
    menu_manager = MenuManager()
    breakfast_menu = menu_manager.get_menu("Breakfast")
    dinner_menu = menu_manager.get_menu("Dinner")
    lunch_menu = menu_manager.get_menu("Lunch")
    today_menu = menu_manager.get_menu("TodayMenu")
    dessert_menu = menu_manager.get_menu("Dessert")
    snack_menu = menu_manager.get_menu("Snacks")
    menus = {
        "Breakfast": breakfast_menu.items,
        "Lunch": lunch_menu.items,
        "Snacks": snack_menu.items,
        "TodayMenu": today_menu.items,
        "Dinner": dinner_menu.items,
        "Dessert": dessert_menu.items
   
    }

    try:
        with open('menu.pickle', 'wb') as file:
            pickle.dump(menus, file)
            print("Data Written Successfully")
    except Exception as e:
        print(f"Error saving menus: {e}")



# function added by henry
def add_item_to_menu(itemName: str, category: str, price: int, desc: str, imageName: str):
    manager = MenuManager()
    assign_menu_data()
    name = itemName.capitalize()
    category = category.capitalize()
    menu = manager.get_menu(category)
    menu.add_item(name, int(price), desc, imageName, category)

    dump_menu_data()
    menus = load_menu_data()
    print(f"Item {name} is added to {category} Successful")
    return True if dump_data(menus, 'menu.pickle') else False

def remove_item_from_menu(itemName: str, category: str):
    manager = MenuManager()
    assign_menu_data()
    name = itemName.capitalize()
    category = category.capitalize()
    menu = manager.get_menu(category)
    menu.delete_item(name)
    dump_menu_data()
    menus = load_menu_data()
    print(f"Item {name} is Removed from {category}")
    return True if dump_data(menus, 'menu.pickle') else False

#feature for showorders data
#This is the Structure of the show_orders_data structure
'''
{
    100: [
        "order_token_1",
        {
            "item_name_1": quantity_1,
            "item_name_2": quantity_2,
            ...
        },
        "customer_name_1",
        "order_type_1",
        "order_time_1"
    ],
    101: [
        "order_token_2",
        {
            "item_name_1": quantity_1,
            "item_name_2": quantity_2,
            ...
        },
        "customer_name_2",
        "order_type_2",
        "order_time_2"
    ]
}

'''

def show_orders_data():
    order_list = get_orders_list()
    show_orders_data = {}
    key = 1000
    for order in order_list:
        order_data = []
        order_data.append(order.token)
        items_data = {}
        for item, qty in order.items.items():
            items_data[item.name] = qty
        order_data.append(items_data)
        order_data.append(order.customer.name)
        order_data.append(order.customer.email)
        order_data.append(order.customer.ph_no)
        order_data.append(order.type)
        order_data.append(order.order_time)

        #Adding the data 's to show_orders_data 
        show_orders_data[key] = order_data
        key += 1
    print("Orderst List data fetched successfully")
    return show_orders_data

def action(key_to_remove):

    if key_to_remove in show_orders_data:
        del show_orders_data[key_to_remove]
        print(f"Entry with key {key_to_remove} removed successfully.")
        return True
    else:
        print(f"Key {key_to_remove} not found in the dictionary.") 
        return False
    



# ------------------- Observer Pattern------------------------------------------
def get_subscribers_data():
    try:
        with open("subscribers.pkl", 'rb') as file:
            subscribers = pickle.load(file)
            file.close()
    except:
        subscribers = []
    return subscribers

#--------------------------------------Menu of the day -------------------------------
def add_item_to_todayMenu(item_add, menu_type):
    builder = MenuBuilder()
    try:
        builder.load_from_pickle('todaymenu.pickle')
    except Exception:
        print("File not Found")

    menu_type_name = menu_type.capitalize()
    builder.add_to_menu(menu_type_name, item_add)
    builder.save_to_pickle('todaymenu.pickle')
    print("Item Added to the Today Menu SuccessFully..")
    return True

def get_todaymenu(menu_type):
    new_builder = MenuBuilder()
    try:
        new_builder.load_from_pickle('todaymenu.pickle')
    except Exception:
        print("File not Found")
    if menu_type.capitalize() in ["Breakfast", "Lunch", "Snacks","TodayMenu", "Dinner"]:
        menu = new_builder.get_menu_items(menu_type)
        print(f"Menu Items of {menu_type} is Retrieved Successfully.. ")
    else:
        print("Invalid Menu Type")
    return menu

#------------------------------------------- end of the Menu of the day------ ----------




    






