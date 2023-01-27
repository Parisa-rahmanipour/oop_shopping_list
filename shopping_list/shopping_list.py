class ShoppingList:
    """
    this class is about our shopping basket
    and it define basket as a list which have items inside
    """

    def __init__(self):
        self.items = list()

    def show(self):
        """
        this method shows the item in basket
        """
        print(self.items)

    def add_item(self, item):
        """
        this item checks if item is not available in our basket
        then it add it to basket
        """
        if item not in self.items:
            self.items.append(item)
        else:
            print('this item already exist in our list')

    def delete_item(self, item):
        """
        this method checks if item is inside our basket, delete the item
        """
        if item in self.items:
            self.items.remove(item)
            print(f'{item} have been removed from your list')
        else:
            print('this item is not available in your list')

    def search_item(self, item):
        """
        this method checks if an item exist in our basket or not
        """
        if item in self.items:
            print(f'{item} exist in your list')
        else:
            print(f'{item} does not exist in your list')
