import os
import datetime
from classes.storage import Storage


def deliver_ingredients_to_production(name: str, quantity: int, ingredient_storage: "Storage", ice_creams: list) -> str:
    """
    It takes the name of an ice cream, the quantity of ice creams to be produced, the ingredient storage and the list
    of ice creams and returns a report of the ingredients that were taken from the storage

    :param: name: str - the name of the ice cream
    :param: quantity: the number of ice creams you want to produce
    :param: ingredient_storage: Storage
    :param: ice_creams: list of IceCream objects
    :return: A string.
    """

    report = ""
    for ice_cream in ice_creams:
        if ice_cream.get_name() == name:
            report += f"{name}:\n"
            for ingredient in ice_cream.get_ingredients().keys():
                amount_of_ingredient_in_ice_cream = ice_cream.get_ingredients()[ingredient]
                amount_of_ingredient_in_storage = ingredient_storage.get_products()[ingredient]
                if amount_of_ingredient_in_ice_cream * quantity <= amount_of_ingredient_in_storage:
                    ingredient_storage.take_product(ingredient, amount_of_ingredient_in_ice_cream * quantity)
                    ingredient_storage.make_file_of_products_and_quantities()
                    report += f"{ingredient.get_name()} - {amount_of_ingredient_in_ice_cream * quantity}\n"
                else:
                    print("There are not enough ingredients for that ice cream.")

    return report


def deliver_ice_creams_to_cold_storage(name: str, quantity: int, cold_storage: "Storage",
                                       report: str, ice_creams: list) -> str:
    """
     > This function takes in a name, quantity, cold storage, report, and a list of ice creams. It then iterates through
      the list of ice creams and if the name of the ice cream matches the name passed in, it adds the ice cream to the
      cold storage and updates the report.

     :param: name: str = the name of the ice cream
     :param: quantity: int
     :param: cold_storage: the storage object that we want to add the ice creams to
     :param: report: str
     :param: ice_creams: list
     :return: A string
     """
    for ice_cream in ice_creams:
        if ice_cream.get_name() == name:
            cold_storage.add_product(ice_cream, quantity)
            cold_storage.make_file_of_products_and_quantities()
            report += f"\n{ice_cream.get_name()} produced = {quantity}"
        else:
            pass
    return report


def make_production_report(report: str):
    """
    It creates a folder called "Reports" in the current working directory, and then creates a file in that folder with
    the current date and time in the name, and writes the report to that file.

    :param: report: str
    """
    path = os.getcwd() + "\\Reports\\"
    if not os.path.exists(path):
        os.mkdir(path)
    date = str(datetime.datetime.now()).replace(":", "-").replace(".", "-")
    with open(path + f" Production report - {date}", "w") as f:
        f.write(report)
        f.close()
