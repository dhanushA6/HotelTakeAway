#class to create the item
class MenuItem:
    def __init__(self, name, price, description, available = True):
        self.name = name
        self.price = price
        self.description = description
        self.available = available

    def display(self):
        print(f'{self.name}', ' '*(20-len(self.name)) ,
        f'{self.price}', ' '*(5-len(str(self.price))) ,
        f'{self.description}', ' '*(25- len(self.description)), f'{self.available}')