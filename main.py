from model.menu_manage import *
from model.order_manage import *
from model.customer import Customer
import pickle
import wrapper as wp
from datetime import datetime

if __name__ == "__main__":
    with open('menu.pickle', 'rb') as f:
        menus = pickle.load(f)
        f.close()
    
        order_list = wp.get_orders_list()
        print("Order List: ", order_list)
        if order_list:
            for order in order_list:
                print(order.order_time)
                print(order.order_date)

    
    
    menu_manager = MenuManager()
    
    selected_menu = input("Enter menu type to order (Breakfast / Lunch ): ")
    
    if selected_menu.lower() in ["breakfast", "lunch", "snacks", "drinks", "dinner", "dessert"]:
        # Get the selected menu
        menu = menus[selected_menu.capitalize()]
        print(f"Items in {selected_menu.capitalize()} Menu:")
        selected_items = menu.get_menu_items()
        print('-'*60)
        print('Name', ' '*(16), 'Price  ', 'Description', ' '*(25-len('description')), 'Availability')
        for item in selected_items:
            item.display()
        print('-'*60)
  
        # Ask for item and quantity
        #order_items = {}
        print("[1.] one to add to cart ")
        print("[2.] To reomove front the cart ")
        ch = int(input("Enter your choice : "))
        if ch == 1:
            while True:
            
                item_name = input(f"Enter item name from {selected_menu.capitalize()} menu (or 'done' to finish): ")
                if item_name.lower() == 'done':
                    break

                # Check if the item exists in the menu
                item_exists = False
                for item in menu.get_menu_items():
                    if item.name.lower() == item_name.lower():
                        item_exists = True
                        qty = int(input(f"Enter quantity for {item.name}: "))
                        wp.add_item_to_cart(item, int(qty))
                        break

                if not item_exists:
                    print("Item not found in the menu. Please enter a valid item.")
        elif ch == 2:
            while True:
            
                item_name = input(f"Enter item name to remove front cart ")
                if item_name.lower() == 'done':
                    break

                # Check if the item exists in the menu
                item_exists = False
                for item in menu.get_menu_items():
                    if item.name.lower() == item_name.lower():
                        item_exists = True
                        #qty = int(input(f"Enter quantity for {item.name}: "))
                        print("I am here ")
                        wp.remove_cart_item(item)
                        break

                if not item_exists:
                    print("Item not found in the menu. Please enter a valid item.")


        
        # Create orders using the OrderFactory
        if wp.cart_items():
            
            print("Enter the Customer Details:  ")
            name = input("Enter the name: ").capitalize()
            ph_no = int(input("Enter your ph_no Number: "))
            email = input("Enter your email: ")

            cust = wp.create_customer(name, ph_no, email)

            new_order =wp.create_order(cust)
            wp.assign_token_and_datetime(new_order)
            print('-'*60)
            print('Token Number: ', new_order.token)
            # Displaying the order type
            print('Name', ' '*(20-len('Name')), 'Price', 'Qty')
            print('-'*60)
            new_order.display_order()
            print('-'*60)
            # Assigning a token to the order
            print('Total Bill Amount: ', wp.get_ordered_bill_total(new_order))
            print('-'*60)


 
            # Choosing a payment strategy
            payment_option = input("Enter payment option (PayPal / GooglePay/Cash): ").lower()
            payment = wp.create_payment_obj()
            wp.do_payment(payment_option, new_order)
            wp.push_orders(new_order)

            # Displaying order details
            print(f"Order Token: {new_order.token}")
        else:
            print("No item Selected")
    else:
        print("Invalid menu choice")

    
 
    