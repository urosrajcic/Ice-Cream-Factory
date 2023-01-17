import os
import datetime


# It creates a class called IceCream.
class IceCream:
    def __init__(self, name: str, recipe: str, ingredients: dict, serving_size: str,
                 production_date: datetime, price: float):
        self.__name = name
        self.__recipe = recipe
        self.__ingredients = ingredients
        self.__serving_size = serving_size
        self.__production_date = production_date
        self.__price = price

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def get_recipe(self):
        return self.__recipe

    def set_recipe(self, recipe):
        self.__recipe = recipe

    def get_ingredients(self):
        return self.__ingredients

    def set_ingredients(self, ingredients):
        self.__ingredients = ingredients

    def get_serving_size(self):
        return self.__serving_size

    def set_serving_size(self, size):
        self.__serving_size = size

    def get_production_date(self):
        return self.__production_date

    def set_production_date(self, date):
        self.__production_date = date

    def get_price(self):
        return self.__price

    def set_price(self, price):
        self.__price = price

    def __str__(self):
        return f"{self.__name}, {self.__price}"

    @staticmethod
    def read_recipe() -> dict:
        """
        It reads all the files in the Ice creams folder and returns a dictionary with the ice cream name as the key and
        the recipe as the value.
        :return: A dictionary of ice cream names and their recipes.
        """
        path = os.getcwd() + "\\Ice creams"
        ice_creams = os.listdir(path)
        recipes = {}
        for ice_cream in ice_creams:
            with open(path + "\\" + ice_cream, "r") as f:
                text = f.read()
                recipe_list = text.split("\n")
                index = recipe_list.index("Recipe:")
                from functools import reduce
                recipe = reduce(lambda x, y: x + "\n" + y, recipe_list[index + 1:])
                recipes[ice_cream.replace(".txt", "")] = recipe
        return recipes

    @staticmethod
    def read_ingredients(set_of_all_ingredients: set) -> dict:
        """
        It reads the files in the Ice creams folder, and returns a dictionary with the ice cream names as keys and the
        ingredients as values

        :param: set_of_all_ingredients: a set of all ingredients in storage
        :return: A dictionary with the names of the ice creams as keys and a dictionary with the ingredients as keys and
         the quantity of the ingredients as values.
        """
        ice_cream_names_and_ingredients = {}
        path = os.getcwd() + "\\Ice creams"
        ice_creams = os.listdir(path)
        for ice_cream in ice_creams:
            with open(path + "\\" + ice_cream, "r") as f:
                recipe = f.read()
                ingredients_list = recipe.split("\n")
                list_with_number_of_ice_cream = ingredients_list[0].split(" ")
                number = [int(num) for num in list_with_number_of_ice_cream if num.isnumeric()]
                index_start = ingredients_list.index("Ingredients:")
                index_end = ingredients_list.index("Recipe:")
                ingredients = {}
                for ingredient in ingredients_list[index_start + 1: index_end]:
                    name_and_quantity = ingredient.split(":")
                    name = name_and_quantity[0].strip("-")
                    quantity_and_measure = name_and_quantity[1].strip().split(" ")
                    quantity = quantity_and_measure[0]
                    for obj_ingredient in set_of_all_ingredients:
                        if obj_ingredient.get_name() == name:
                            ingredients[obj_ingredient] = float(quantity) / number[0]
                ice_cream_names_and_ingredients[ice_cream.replace(".txt", "")] = ingredients
        return ice_cream_names_and_ingredients

    @staticmethod
    def calculate_ice_cream_serving_size(set_of_all_ingredients: set):
        """
        It takes a set of all ingredients, reads the ingredients from the file, calculates the serving size of each ice
        cream, and returns a dictionary of ice creams and their serving sizes.

        :param: set_of_all_ingredients: a set of all the ingredients in the ice cream
        :return: A dictionary with the ice cream names as keys and the serving sizes as values.
        """
        ice_creams_and_serving_sizes = {}
        dict_of_ice_cream_and_ingredients = IceCream.read_ingredients(set_of_all_ingredients)
        for ice_cream in dict_of_ice_cream_and_ingredients.keys():
            serving_size = 0
            list_of_quantities = list(dict_of_ice_cream_and_ingredients[ice_cream].values())
            for quantity in list_of_quantities:
                serving_size += quantity
            ice_creams_and_serving_sizes[ice_cream] = str(round(serving_size * 1000)) + " g"
        return ice_creams_and_serving_sizes

    @staticmethod
    def calculate_ice_cream_price(set_of_all_ingredients: set) -> dict:
        """
        It takes a set of ingredients and returns a dictionary of ice creams and their prices.

        :param: set_of_all_ingredients: a set of all ingredients
        :return: A dictionary with the name of the ice cream as a key and the price as a value.
        """
        ice_creams_and_prices = {}
        dict_of_ice_cream_and_ingredients = IceCream.read_ingredients(set_of_all_ingredients)
        for ice_cream in dict_of_ice_cream_and_ingredients.keys():
            obj_ingredients = list(dict_of_ice_cream_and_ingredients[ice_cream].keys())
            price = 0
            for obj in obj_ingredients:
                for ingredient in set_of_all_ingredients:
                    if ingredient.get_name() == obj.get_name():
                        quantity = dict_of_ice_cream_and_ingredients[ice_cream][obj]
                        price_for_ingredients = ingredient.get_price() * quantity
                        price += price_for_ingredients
            ice_creams_and_prices[ice_cream] = round(price * 14 / 10)
        return ice_creams_and_prices

    @staticmethod
    def create_ice_creams(set_of_all_ingredients):
        """
        It creates a list of ice cream objects.
        :return: A list of ice cream objects
        """
        ice_creams = []
        path = os.getcwd() + "\\Ice creams"
        ice_creams_names = os.listdir(path)
        ingredients = IceCream.read_ingredients(set_of_all_ingredients)
        recipes = IceCream.read_recipe()
        prices = IceCream.calculate_ice_cream_price(set_of_all_ingredients)
        serving_size = IceCream.calculate_ice_cream_serving_size(set_of_all_ingredients)
        for name in ice_creams_names:
            ice_creams.append(IceCream(name.replace(".txt", ""), recipes[name.replace(".txt", "")],
                                       ingredients[name.replace(".txt", "")], serving_size[name.replace(".txt", "")],
                                       datetime.datetime.now(), prices[name.replace(".txt", "")]))
        return ice_creams
