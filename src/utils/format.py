try:
    from pint import Quantity
except ImportError:
    # Define a dummy Quantity class if pint is not installed
    class Quantity:
        pass


def replace_all (string, *chars, **chars_):
    string_new = string

    # Process dict items (take priority)
    for char, char_new in chars_:
        while char in string_new:
            string_new = string_new.replace(char, char_new)
    
    # Process list items
    for char in chars:
        while char in string_new:
            string_new = string_new.replace(char, '')
    
    return string_new.strip()

def format_quantity (quantity: Quantity, type_: type = float) -> str:
    try:
        value = type_(quantity.magnitude)
        unit_formatted = replace_all(str(quantity.units), ' ** ', ' ')
        return f'[{unit_formatted}] {value}'
    except:
        return str(quantity)  # Dummy return
