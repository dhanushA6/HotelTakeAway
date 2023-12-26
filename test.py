import wrapper as wp
from model.menu import MenuItem
from model.customer import MenuObservable
import pickle
from model.menu_of_the_day import MenuBuilder

# print(wp.get_todaymenu())
# for item in wp.get_todaymenu()["Lunch"]:
#     print(item.category)
# Adding items to different menus
# print(wp.get_menu_items("Breakfast"))
#---------------------------------------------------
# items = wp.get_menu_items("Breakfast")
# menu_builder = MenuBuilder()
# for item in items:
#         menu_builder.add_to_menu("Breakfast", item[-1])
#         menu_builder.save_to_pickle('menus.pickle')
# new_menu_builder = MenuBuilder()
# new_menu_builder.load_from_pickle('menus.pickle')
# breakfast_items = new_menu_builder.get_menu_items('Breakfast')
# for item in breakfast_items:
#         print(item.name)
# for item in breakfast_items:
#         if item.name == "Poori":
#                 new_menu_builder.remove_menu(item)
#                 break
# print("#"*40)
# new_menu_builder = MenuBuilder()
# new_menu_builder.load_from_pickle('menus.pickle')
# breakfast_items = new_menu_builder.get_menu_items('Breakfast')
# for item in breakfast_items:
#         print(item.name)

# new_menu_builder = MenuBuilder()
# breakfast_items = new_menu_builder.get_menu_items('Breakfast')
# for item in breakfast_items:
#         print(item.name)

data = wp.get_todaymenu()
for list, value in data.items():
    print(list, value)


#-----------------------------------------------------------
# print("Breakfast Item: ",breakfast_items)
# new_menu_builder.remove_menu()

# menu_builder = MenuBuilder()
# menu_builder.add_to_menu('Breakfast', 'Pancakes')
# menu_builder.add_to_menu('Breakfast', 'Eggs')
# menu_builder.add_to_menu('Lunch', 'Salad')
# menu_builder.add_to_menu('Lunch', 'Sandwich')
# menu_builder.add_to_menu('Dinner', 'Steak')

# # Saving menus to a pickle file
# menu_builder.save_to_pickle('menus.pickle')

# # Creating a new instance of MenuBuilder to load the menus from the pickle file
# new_menu_builder = MenuBuilder()
# new_menu_builder.load_from_pickle('menus.pickle')

# # Retrieving items from a specific menu
# breakfast_items = new_menu_builder.get_menu_items('Breakfast')
# print("Breakfast Menu:")
# # for item in breakfast_items:
# #     print(item)
# print(breakfast_items)


# # # ... similarly for other menu types



