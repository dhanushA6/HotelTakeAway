from model.menu_manage import *
from model.order_manage import *
import pickle
import wrapper as wp

if __name__ == "__main__":
    with open('menu.pickle', 'rb') as f:
        menus = pickle.load(f)
        f.close()
    
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
        while True:
            print("[1.] Choose Item.")
            print("[2.] Done/Finish")
            item_name = input(f"Enter item name from {selected_menu.capitalize()} menu (or 'done' to finish): ")
            if item_name.lower() == 'done':
                break

            # Check if the item exists in the menu
            item_exists = False
            for item in menu.get_menu_items():
                if item.name.lower() == item_name.lower():
                    item_exists = True
                    qty = int(input(f"Enter quantity for {item.name}: "))
                    wp.additem_to_cart(item, qty)
                    break

            if not item_exists:
                print("Item not found in the menu. Please enter a valid item.")
        
        # Create orders using the OrderFactory
        if wp.cart_items():
            new_order = OrderFactory.create_order(wp.cart_items())
            print("Order created successfully with the following items:")
            new_order.assign_token(generate_unique_token())
            print('-'*60)
            print('Token Number: ', new_order.token)
            # Displaying the order type
            print('Name', ' '*(20-len('Name')), 'Price', 'Qty')
            print('-'*60)
            new_order.display_order()
            print('-'*60)
            # Assigning a token to the order
            print('Total Bill Amount: ',new_order. calculate_bill())
            print('-'*60)
 
            # Choosing a payment strategy
            payment_option = input("Enter payment option (Credit Card / Cash): ")

            if payment_option.lower() == "credit card":
                new_order.set_payment_strategy(CreditCardPayment())
            elif payment_option.lower() == "cash":
                new_order.set_payment_strategy(CashPayment())
            else:
                raise ValueError("Invalid payment option")

            # Making payment
            new_order.make_payment()

            # Displaying order details
            print(f"Order Token: {new_order.token}")
        else:
            print("No item Selected")
    else:
        print("Invalid menu choice")

    
 
    