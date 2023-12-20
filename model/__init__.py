from menu_manage import *
#from ord_priority import *
from order_manage import *


if __name__ == "__main__":
    # Adding items to Breakfast menu
    menu_manager = MenuManager()
    breakfast_menu = menu_manager.get_menu("Breakfast")
    breakfast_menu.add_item("Pancakes", 7.99, "Fluffy pancakes")
    breakfast_menu.add_item("Omelette", 6.49, "Cheese and veggie omelette")
    breakfast_menu.add_item("French Toast", 8.99, "Buttery French toast")
    breakfast_menu.add_item("Waffles", 9.99, "Crispy waffles")
    breakfast_menu.add_item("Fruit Bowl", 4.99, "Assorted fresh fruits")

    # Adding items to Lunch menu
    lunch_menu = menu_manager.get_menu("Lunch")
    lunch_menu.add_item("Salad", 6.99, "Caesar salad")
    lunch_menu.add_item("Sandwich", 7.49, "Club sandwich")
    lunch_menu.add_item("Pasta", 10.99, "Spaghetti carbonara")
    lunch_menu.add_item("Soup", 5.99, "Tomato basil soup")
    lunch_menu.add_item("Pizza", 12.99, "Margherita pizza")

    # Adding items to Snacks menu
    snacks_menu = menu_manager.get_menu("Snacks")
    snacks_menu.add_item("Nachos", 8.99, "Loaded nachos")
    snacks_menu.add_item("Popcorn", 3.49, "Buttered popcorn")
    snacks_menu.add_item("Mozzarella Sticks", 7.99, "Crispy mozzarella sticks")
    snacks_menu.add_item("Chicken Wings", 9.99, "Spicy chicken wings")
    snacks_menu.add_item("Hummus and Pita", 6.49, "Creamy hummus with pita bread")

        # Adding items to Drinks menu
    drinks_menu = menu_manager.get_menu("Drinks")
    drinks_menu.add_item("Coffee", 3.49, "Hot brewed coffee")
    drinks_menu.add_item("Tea", 2.99, "Assam black tea")
    drinks_menu.add_item("Milkshake", 4.99, "Chocolate milkshake")
    drinks_menu.add_item("Smoothie", 5.49, "Mixed berry smoothie")
    drinks_menu.add_item("Soda", 2.29, "Assorted soft drinks")



    # Adding items to Dessert menu
    dessert_menu = menu_manager.get_menu("Dessert")
    dessert_menu.add_item("Cake", 7.99, "Chocolate cake")
    dessert_menu.add_item("Ice Cream", 4.49, "Vanilla ice cream")
    dessert_menu.add_item("Cheesecake", 8.99, "New York-style cheesecake")
    dessert_menu.add_item("Fruit Tart", 6.49, "Fresh fruit tart")
    dessert_menu.add_item("Brownie", 5.99, "Fudgy chocolate brownie")

   

    selected_menu = input("Enter menu type to order (Breakfast / Lunch / Snacks / Drinks / Dinner / Dessert): ")

    if selected_menu.lower() in ["breakfast", "lunch", "snacks", "drinks", "dinner", "dessert"]:
        # Get the selected menu
        menu = menu_manager.get_menu(selected_menu.capitalize())
        print(f"Items in {selected_menu.capitalize()} Menu:")
        selected_items = menu_manager.get_menu(selected_menu.capitalize()).get_menu_items()
        print('-'*60)
        print('Name', ' '*(16), 'Price  ', 'Description', ' '*(25-len('description')), 'Availability')

        for item in selected_items:
            item_display = ItemDisplay(item)
            item_display.display()
        print('-'*60)

        # Ask for item and quantity
        order_items = {}
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
                    order_items[item] = qty
                    break

            if not item_exists:
                print("Item not found in the menu. Please enter a valid item.")

        # Create orders using the OrderFactory
        if order_items:
            new_order = OrderFactory.create_order(order_items)
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

    
 
    