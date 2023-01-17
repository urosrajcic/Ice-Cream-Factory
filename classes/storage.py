# It's a class that stores a value.
import datetime
import os
from classes.ingredient import Ingredient


class Storage:
    def __init__(self, name: str, products: dict):
        self.__name = name
        self.__products = products

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def get_products(self):
        return self.__products

    def set_products(self, products):
        self.__products = products

    def add_product(self, product, quantity):
        """
        It adds a product to the cart, and if the product is already in the cart, it adds the quantity to the existing
        quantity.

        :param: product: The product to add to the cart
        :param: quantity: The number of items to add to the cart
        """
        self.__products[product] += quantity

    def take_product(self, product, quantity):
        """
        It takes a product and quantity as arguments, and then subtracts the quantity from the product's value in the
        dictionary.

        :param: product: The product to take from the inventory
        :param: quantity: The amount of the product to take
        """
        self.__products[product] -= quantity

    @staticmethod
    def calculate_min_needed_ingredients(set_of_all_ingredients: set, min_quantity: int, ice_creams: list) -> dict:
        """
        It takes a set of all ingredients, a minimum quantity of ice creams to make, and a list of ice creams, and
        returns a dictionary of ingredients and their quantities

        :param set_of_all_ingredients: a set of all the ingredients that are used in the ice creams
        :type set_of_all_ingredients: set
        :param min_quantity: the minimum number of ice creams you want to make
        :type min_quantity: int
        :param ice_creams: a list of IceCream objects
        :type ice_creams: list
        :return: A dictionary of ingredients and their quantities.
        """
        ingredients = {}
        for ingredient in set_of_all_ingredients:
            ingredients[ingredient.get_name()] = 0
        for ice_cream in ice_creams:
            for ingredient in ice_cream.get_ingredients().keys():
                ingredients[ingredient.get_name()] += ice_cream.get_ingredients()[ingredient] * min_quantity
        ingredients_keys = list(ingredients.keys())
        for ingredient in set_of_all_ingredients:
            if ingredient.get_name() in ingredients_keys:
                ingredients[ingredient] = ingredients[ingredient.get_name()]
                del ingredients[ingredient.get_name()]
        return ingredients

    def make_ingredient_storage_report(self, set_of_all_ingredients: set, quantity: int, ice_creams):
        """
        It takes a set of all ingredients, a quantity of products to be produced, calculates the minimum need of
        ingredients for the production, and then compares it to the current storage of ingredients. If the current
        storage is less than the minimum need, it writes a report to a file.

        :param: set_of_all_ingredients: set -a set of all ingredients that are needed for the production of all products
        :param: quantity: int - the quantity of the product that the user wants to produce
        """
        report = ""
        min_need_ingredients = self.calculate_min_needed_ingredients(set_of_all_ingredients, quantity, ice_creams)
        for ingredient in self.__products.keys():
            if self.__products[ingredient] < min_need_ingredients[ingredient]:
                difference = min_need_ingredients[ingredient] - self.__products[ingredient]
                report += f"Quantity of {ingredient.get_name()} is low, {round(difference, 7)} kg" \
                          f" is needed for minimum production.\n"
                path = os.getcwd() + "\\Reports\\"
                if not os.path.exists(path):
                    os.mkdir(path)
                date = str(datetime.datetime.now()).replace(":", "-").replace(".", "-")
                with open(path + f" Ingredient storage report for trade manager - {date}", "w") as f:
                    f.write(report)
                    f.close()

    def make_ice_cream_storage_report(self, quantity: int):
        """
        It takes a quantity as an argument and checks if the number of ice creams in the storage is less than
        the quantity. If it is, it writes a report to a file.

        :param: quantity: int - the minimum quantity of ice cream that should be in the storage
        """
        report = ""
        for ice_cream in self.__products.keys():
            number_of_ice_creams = self.__products[ice_cream]
            if number_of_ice_creams < quantity:
                difference = quantity - number_of_ice_creams
                report += f"{ice_cream.get_name()} - {int(number_of_ice_creams)}: {int(difference)}" \
                          f" is needed for minimum storage"
                path = os.getcwd() + "\\Reports\\"
                if not os.path.exists(path):
                    os.mkdir(path)
                date = str(datetime.datetime.now()).replace(":", "-").replace(".", "-")
                with open(path + f" Ice cream storage report for production manager  - {date}", "w") as f:
                    f.write(report)
                    f.close()

    def make_report(self):
        """
        It creates a report for the current store, containing the name of the storage and the name and quantity of all
        the products in the store.
        """
        report = f"{self.__name}:\n"
        for product in self.__products.keys():
            if isinstance(product, Ingredient):
                report += f"{product.get_name()} - {self.__products[product]} kg\n"
            else:
                report += f"{product.get_name()} - {self.__products[product]}\n"
        path = os.getcwd() + "\\Reports"
        if not os.path.exists(path):
            os.mkdir(path)
        date = str(datetime.datetime.now()).replace(":", "-").replace(".", "-")
        with open(path + "\\" + f"{self.__name} report - {date}.txt", "w") as f:
            f.write(report)
            f.close()

    def make_file_of_products_and_quantities(self):
        """
        It creates a text file with the name of the store and the word "status" and writes the name of each product and
         the quantity of that product in the store
        """
        text = ""
        for product in self.__products.keys():
            text += f"{product.get_name()} - {round(self.__products[product], 5)}\n"
        with open(f"{self.__name} status.txt", "w") as f:
            f.write(text)
            f.close()

    def read_file_for_products(self):
        """
        It reads the file, splits the text into a list of products and quantities, and then adds the quantities to the
        products
        """
        with open(f"{self.__name} status.txt", "r") as f:
            text = f.read()
            products_and_quantities = text.split("\n")
            for product in self.__products.keys():
                for product_and_quantity in products_and_quantities:
                    name_and_quantity = product_and_quantity.split("-")
                    name = name_and_quantity[0].strip()
                    quantity = name_and_quantity[-1].strip()
                    if product.get_name() == name:
                        self.__products[product] += float(quantity)

    def deliver_ice_cream(self):
        """
        It takes the name of the ice cream and the quantity of it as input, and if the quantity is less than the
        quantity of the ice cream in the dictionary, it prints a message, otherwise it takes the product and makes
        a file of the products and quantities.
        """
        ice_cream_name = input("Select ice cream for delivery (Kapri, King, Kornet, Coko moko): ")
        quantity = int(input("Choose quantity: "))
        for ice_cream in self.__products.keys():
            if ice_cream.get_name() == ice_cream_name:
                if self.__products[ice_cream] < quantity:
                    print("Not enough ice cream for delivery!")
                    continue
                else:
                    self.take_product(ice_cream, quantity)
                    self.make_file_of_products_and_quantities()

    def order_ingredient(self, set_of_all_ingredients: set):
        """
        It takes the name of an ingredient and the quantity of that ingredient, and adds it to the list of ingredients
        that the user has ordered.
        """
        ingredient_name = input("Ingredient: ")
        quantity = float(input("Quantity (kg): "))
        for ingredient in set_of_all_ingredients:
            if ingredient.get_name() == ingredient_name:
                self.add_product(ingredient, quantity)
                self.make_file_of_products_and_quantities()
