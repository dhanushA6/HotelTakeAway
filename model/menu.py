#class to create the item
class MenuItem:
    def __init__(self, name, price, description, img, available=True):
        self.name = name
        self.price = price
        self.description = description
        self.available = available
        self.img = img

    def display(self):
        print(f'{self.name}', ' '*(20-len(self.name)) ,
        f'{self.price}', ' '*(5-len(str(self.price))) ,
        f'{self.description}', ' '*(25- len(self.description)), f'{self.available}')

    def get_attrs(self):
        return [self.name, self.price, self.description,  self.img, self.available]