import wrapper as wp
from model.menu import MenuItem
from model.customer import MenuObservable
import pickle





# item1 = MenuItem("Chicken Biriyani", 150, "A flavorful Indian rice dish with aromatic basmati rice, chicken, and a blend of spices, cooked to perfection.", "chicken-biriyani.png", "Lunch")
# print(wp.add_item_to_todayMenu(item1, item1.category))
# print(wp.get_todaymenu("Breakfast"))

# for item in wp.get_todaymenu("Lunch"):
#     item.display()

#print(wp.get_orders_list())

# for order in wp.get_orders_list():
#     wp.add_subscriber(order.customer)

# try:
#         with open("subscribers.pkl", 'rb') as file:
#             obj = pickle.load(file)
#             file.close()
# except:
#         #using Observer Pattern here
#         obj = MenuObservable()

# obj.notify_observers("Biriyani")

data = wp.show_orders_data()
print(data)
wp.remove_order_data(1000)
print(wp.show_orders_data())



