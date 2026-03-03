# Args: List of arguments that can be passed to a function. They are defined with an asterisk (*) before the parameter name.
def world_cup_titles(country, *lista):
    print('Country: ', country)
    for title in lista:
        print('year: ', title)

world_cup_titles('Brasil', '1958', '1962', '1970', '1994', '2002')
world_cup_titles('Espanha', '2010')

# Kwargs: Dictionary of keyword arguments that can be passed to a function. They are defined with two asterisks (**) before the parameter name.
def calculate_price(value, **dicio):
    tax_percentage = dicio.get('tax_percentage')
    discount = dicio.get('discount')
    if tax_percentage:
        value += value * (tax_percentage / 100)
    if discount:
        value -= discount
    return value

final_price = calculate_price(100.0)
print(final_price)
final_price = calculate_price(100.0, discount=5.0)
print(final_price)
final_price = calculate_price(100.0, tax_percentage=7)
print(final_price)
