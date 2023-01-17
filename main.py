import os

from classes.ingredient import Ingredient
from classes.storage import Storage
from classes.ice_cream import IceCream
import production


def main():
    """Create ingredient storage if the file - Ingredient storage status.txt - doesn't exist."""
    start_quantity = 0
    set_of_all_ingredients = Ingredient.create_set_of_ingredients()
    ice_creams = IceCream.create_ice_creams(set_of_all_ingredients)

    minimum_needed_ingredients = Storage.calculate_min_needed_ingredients(set_of_all_ingredients, start_quantity,
                                                                          ice_creams)
    ingredient_storage = Storage("Ingredient storage", minimum_needed_ingredients)
    if os.path.exists("Ingredient storage status.txt"):
        ingredient_storage.read_file_for_products()
    else:
        start_quantity = 100
        starting_ingredients = Storage.calculate_min_needed_ingredients(set_of_all_ingredients, start_quantity,
                                                                        ice_creams)
        ingredient_storage = Storage("Ingredient storage", starting_ingredients)
    ingredient_storage.make_file_of_products_and_quantities()

    """Create ice cream storage if the file - Cold storage status.txt - doesn't exist."""
    start_quantity = 0
    ice_cream_products = {}
    for ice_cream in ice_creams:
        ice_cream_products[ice_cream] = start_quantity
    cold_storage = Storage("Cold storage", ice_cream_products)
    if os.path.exists("Cold storage status.txt"):
        cold_storage.read_file_for_products()
    else:
        start_quantity = 100
        for ice_cream in ice_creams:
            ice_cream_products[ice_cream] = start_quantity
        cold_storage = Storage("Cold storage", ice_cream_products)
    cold_storage.make_file_of_products_and_quantities()

    cold_storage.make_ice_cream_storage_report(quantity=100)
    ingredient_storage.make_ingredient_storage_report(set_of_all_ingredients, quantity=100, ice_creams=ice_creams)

    a = True
    while a:
        menu = input("1. Quantity of ingredients in the Ingredient storage\n"
                     "2. Quantity of ice creams in the Cold storage\n"
                     "3. Produce ice cream\n"
                     "4. Quantity of King and Kapri in the Cold storage\n"
                     "5. Cocoa quantity and number of Čoko-moko\n"
                     "6. Order ingredient\n"
                     "7. Deliver ice cream\n"
                     "8. End\n"
                     "Choose an option: ")
        if menu == "1":
            ingredient_storage.make_report()

        elif menu == "2":
            cold_storage.make_report()

        elif menu == "3":
            ice_cream_name = input("Select ice cream for production (Kapri, King, Kornet, Coko moko): ")
            if ice_cream_name not in ("Kapri", "King", "Kornet", "Coko moko"):
                print("Wrong name.")
                continue
            quantity = int(input("Select the quantity of ice cream: "))
            ingredient_report = production.deliver_ingredients_to_production(ice_cream_name, quantity,
                                                                             ingredient_storage,
                                                                             ice_creams)
            ice_cream_report = production.deliver_ice_creams_to_cold_storage(ice_cream_name,
                                                                             quantity, cold_storage, ingredient_report,
                                                                             ice_creams)
            production.make_production_report(ice_cream_report)

        elif menu == "4":
            report = ""
            for ice_cre in cold_storage.get_products():
                if ice_cre.get_name() == "King":
                    king_quantity = cold_storage.get_products()[ice_cre]
                    report += f"King - {king_quantity}\n"
            for ice_cre in cold_storage.get_products():
                if ice_cre.get_name() == "Kapri":
                    kapri_quantity = cold_storage.get_products()[ice_cre]
                    report += f"Kapri - {kapri_quantity}"
            print(report)

        elif menu == "5":
            report = ""
            for ingredient in ingredient_storage.get_products():
                if ingredient.get_name() == "cocoa":
                    quantity = ingredient_storage.get_products()[ingredient]
                    for ice_cre in cold_storage.get_products():
                        if ice_cre.get_name() == "Coko moko":
                            ingredients = ice_cre.get_ingredients()
                            number_of_ice_cream = quantity // ingredients[ingredient]
                            report += f"cocoa - {quantity} kg, enough for {number_of_ice_cream} Coko moko ice creams."
            print(report)

        elif menu == "6":
            ingredient_storage.order_ingredient(set_of_all_ingredients)

        elif menu == "7":
            cold_storage.deliver_ice_cream()

        elif menu == "8":
            a = False

        else:
            print("Option doesn't exist.")


if __name__ == "__main__":
    main()
