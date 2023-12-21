from model.menu_manage import *
from model.order_manage import *
import pickle

if __name__ == "__main__":
    with open('menu.pickle', 'rb') as f:
        menus = pickle.load(f)
    
    breakfast_menu = menus["Breakfast"]
    lunch_menu = menus["Lunch"]
    # snacks_menu = menus["Snacks"]
    # drinks_menu = menus["Drinks"]
    # dessert_menu = menus["Dessert"]
    
    # for item in breakfast_menu.get_menu_items():
    #     item.display()

    # # Adding items to Breakfast menu
    menu_manager = MenuManager()
    # breakfast_menu = menu_manager.get_menu("Breakfast")
    # breakfast_menu.add_item("Poori", 30, "Deep-fried Indian bread, made from unleavened wheat dough, served fluffy and puffed.", "poori.jpg")
    # breakfast_menu.add_item("Idly", 8, "Steamed, spongy rice and urad dal dumplings, a staple in South Indian cuisine", "Idly.jpg")
    # breakfast_menu.add_item("Dosa", 40, "Thin, crispy fermented rice and urad dal crepe, a versatile dish in Indian cuisine.", "plain-dosa.jpg")
    # breakfast_menu.add_item("Vadai", 10, "Deep-fried lentil fritters, typically made with urad dal or chana dal, enjoyed as a savory snack.", "medhu-vadai.jpg")
    # breakfast_menu.add_item("Pongal", 40, "South Indian rice dish cooked with lentils, black pepper, cumin, and ghee, often garnished with cashews.", "rava-pongal.jpg")
    # breakfast_menu.add_item("Upma", 35, "A savory South Indian dish made from dry-roasted semolina, typically seasoned with mustard seeds, curry leaves, and vegetables.", "upma.jpg")
    

    # # Adding items to Lunch menu
    # lunch_menu = menu_manager.get_menu("Lunch")
    # lunch_menu.add_item("Chicken Biriyani", 150, "A flavorful Indian rice dish with aromatic basmati rice, chicken, and a blend of spices, cooked to perfection.", "chicken-biriyani.png")
    # lunch_menu.add_item("Full Meals", 80, "A comprehensive and wholesome Indian meal that includes a variety of dishes such as rice, chapati, curry, dal, vegetables, and sometimes dessert, providing a balanced dining experience.", "meals.jpg")
    # lunch_menu.add_item("Mutton Biriyani", 200, "Fragrant and spiced rice preparation with tender mutton, creating a delicious and hearty Indian meal.", "mutton-biriyani.jpg")
    # lunch_menu.add_item("Sandwich", 160, "A versatile and convenient meal, typically consisting of layers of ingredients such as bread, vegetables, cheese, and meats.", "sandwich.jpg")
    # lunch_menu.add_item("Sambar Rice", 30, "A comforting South Indian dish where rice is combined with sambar, a tangy and spicy lentil-based vegetable stew.", "sambar.jpg")
    # lunch_menu.add_item("Veg Fried Rice", 80, "Stir-fried rice with mixed vegetables, often seasoned with soy sauce and spices, creating a flavorful and quick vegetarian dish.", "veg-fried-rice.jpg")
    # lunch_menu.add_item("Curd Rice", 30, "A simple South Indian dish combining rice with yogurt, often tempered with mustard seeds, curry leaves, and green chillies.", "curd-rice.jpg")
    # lunch_menu.add_item("Pizza", 100, "Oven-baked flatbread topped with tomato sauce, cheese, and various toppings, a popular Italian dish enjoyed worldwide.", "pizza.jpg")

    # # Adding items to Snacks menu
    # snacks_menu = menu_manager.get_menu("Snacks")
    # snacks_menu.add_item("Nachos", 8.99, "Loaded nachos")
    # snacks_menu.add_item("Popcorn", 3.49, "Buttered popcorn")
    # snacks_menu.add_item("Mozzarella Sticks", 7.99, "Crispy mozzarella sticks")
    # snacks_menu.add_item("Chicken Wings", 9.99, "Spicy chicken wings")
    # snacks_menu.add_item("Hummus and Pita", 6.49, "Creamy hummus with pita bread")

    # # Adding items to Drinks menu
    # drinks_menu = menu_manager.get_menu("Drinks")
    # drinks_menu.add_item("Coffee", 3.49, "Hot brewed coffee")
    # drinks_menu.add_item("Tea", 2.99, "Assam black tea")
    # drinks_menu.add_item("Milkshake", 4.99, "Chocolate milkshake")
    # drinks_menu.add_item("Smoothie", 5.49, "Mixed berry smoothie")
    # drinks_menu.add_item("Soda", 2.29, "Assorted soft drinks")

    # # Adding items to Dessert menu
    # dessert_menu = menu_manager.get_menu("Dessert")
    # dessert_menu.add_item("Cake", 7.99, "Chocolate cake")
    # dessert_menu.add_item("Ice Cream", 4.49, "Vanilla ice cream")
    # dessert_menu.add_item("Cheesecake", 8.99, "New York-style cheesecake")
    # dessert_menu.add_item("Fruit Tart", 6.49, "Fresh fruit tart")
    # dessert_menu.add_item("Brownie", 5.99, "Fudgy chocolate brownie")

    menus = {
        "Breakfast": menu_manager.get_menu("Breakfast"),
        "Lunch": menu_manager.get_menu("Lunch"),
        "Snacks": menu_manager.get_menu("Snacks"),
        "Drinks": menu_manager.get_menu("Drinks"),
        "Dinner": menu_manager.get_menu("Dinner"),
        "Dessert": menu_manager.get_menu("Dessert")
    }
   
    # try:
    #     with open('menu.pickle', 'wb') as file:
    #         pickle.dump(menus, file)
    # except Exception as e:
    #     print(f"Error saving menus: {e}")

    
    selected_menu = input("Enter menu type to order (Breakfast / Lunch / Snacks / Drinks / Dinner / Dessert): ")

    if selected_menu.lower() in ["breakfast", "lunch", "snacks", "drinks", "dinner", "dessert"]:
        # Get the selected menu
        menu = menus[selected_menu.capitalize()]
        print(f"Items in {selected_menu.capitalize()} Menu:")
        selected_items = menu.get_menu_items()
        print('-'*60)
        print('Name', ' '*(16), 'Price  ', 'Description', ' '*(25-len('description')), 'Availability')
        print(menus)
        for item in selected_items:
            print("Hi")
            item.display()
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

    
 
    