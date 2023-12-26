import wrapper as wp
from model.menu import MenuItem
from model.customer import MenuObservable
import pickle
from model.menu_of_the_day import MenuBuilder


item = MenuItem("Chicken Fried Rice ", 60, "Deep-fried Indian bread, made from unleavened wheat dough, served fluffy and puffed.", "poori.jpg", "Lunch")
data = wp.get_todaymenu()
print(data)
# for item in data["Lunch"]:
#     print(item.name)
# wp.remove_menu(item)
# print(data)
# # # # data2 = wp.get_todaymenu()
# # # # for item in data2["Breakfast"]:
# # # #     print(item.name)




