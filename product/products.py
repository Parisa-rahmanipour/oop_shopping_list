import json

class Product:
    """
    this class is about products and it
    have only instance methods which works with
    file that contain products information
    """
    @staticmethod
    def get_categories(info_file, category):
        """
        this method read dict of specific category from json file
        and it shows name and price of that specific category
        """
        with open(info_file, 'r+') as file:
            info_dict=json.load(file)
            if category in info_dict.keys():
                for key, value in info_dict[category].items():
                    print('{}  :  {}$'.format(key, value))

    @staticmethod
    def check_available_products(info_file):
        """
        this method get name of each product from json file
        and add it to a list and it returns the list
        """
        with open(info_file, 'r+') as file:
            info_dict=json.load(file)
            products=list()
            for key, value in info_dict['VEGETABLES'].items():
                products.append(key)
            for key, value in info_dict['FRUITS'].items():
                products.append(key)
            for key, value in info_dict['SUPERMARKET'].items():
                products.append(key)
        return products

    @staticmethod
    def get_products_dict(info_file):
        """
        this method reads all dicts of 3 categories and unpack it inside one dict
        to help finding price of each product for facture
        """
        with open(info_file, 'r+') as file:
            info_dict=json.load(file)
            products_info = {**info_dict['VEGETABLES'], **info_dict['FRUITS'], **info_dict['SUPERMARKET']}
        return products_info
