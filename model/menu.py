#class to create the item
class MenuItem:
    def __init__(self, name, price, description, available = True):
        self.name = name
        self.price = price
        self.description = description
        self.available = available

class ItemDisplay:
    def __init__(self, item_object):
        self.item = item_object
        self.name = item_object.name
        self.price = item_object.price
        self.description = item_object.description
        self.available = item_object.available
    def display(self):
        print(f'{self.name}', ' '*(20-len(self.name)) ,
        f'{self.price}', ' '*(5-len(str(self.price))) ,
        f'{self.description}', ' '*(25- len(self.description)), f'{self.available}')