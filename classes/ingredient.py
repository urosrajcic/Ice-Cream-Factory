# It creates a class called Ingredient.
class Ingredient:
    def __init__(self, name: str, price_per_kg: int):
        self.__name = name
        self.__price_per_kg = price_per_kg

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def get_price(self):
        return self.__price_per_kg

    def set_price(self, price):
        self.__price_per_kg = price

    def __str__(self):
        return f"{self.__name} - {self.__price_per_kg}"

    @staticmethod
    def create_set_of_ingredients() -> set:
        """
        It reads the ingredients from the file and returns a set of ingredients.
        :return: A set of Ingredient objects
        """
        with open("Ingredients.txt", "r") as f:
            text = f.read()
            set_of_all_ingredients = set()
            ingredients = text.split("\n")
            for ingredient in ingredients:
                name_and_price = ingredient.split("-")
                name = name_and_price[0]
                price = name_and_price[1]
                set_of_all_ingredients.add(Ingredient(name.strip(), int(price.strip())))
        return set_of_all_ingredients
