elements_list = [
    "Physical", "Fire", "Water", "Earth", "Wind", "Light", "Dark", "Void"
]


def get_scale_stat_for_element(element):
  if element == "Physical":
    return "str"
  if element == "Fire" or element == "Water" or element == "Earth" or element == "Wind":
    return "int"
  if element == "Light" or element == "Dark":
    return "spi"
  if element == "Void":
    return None
