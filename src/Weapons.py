import random

from Attributes import Attributes
from Elements import elements_list

weapon_categories = {
    "Melee": ["Sword", "Axe", "Spear"],
    "Elemental": ["Staff", "Orb"],
    "Spiritual": ["Relic", "Grimoire"],
    "Ranged": ["Bow", "Crossbow"],
    "MeleeAgile": ["Dagger", "Scythe"]
}


class Weapon:

  def __init__(self, type, element):
    self.type = type
    self.element = element
    self.associated_stats = Attributes()
    self.name = self.get_name()

  def get_category(self):
    for category in weapon_categories:
      if self.type in weapon_categories[category]:
        return category
    return None

  def get_name(self):
    if self.element == "Physical":
      return self.type

    elementname = self.element
    if self.element == "Light":
      elementname = "Holy"
    return f"{elementname} {self.type}"

  def get_scale(self):
    scale = {}
    if self.get_category() == "Melee":
      scale["str"] = 0.8
    if self.get_category() == "Ranged":
      scale["agi"] = 0.8
    if self.get_category() == "Spiritual":
      scale["spi"] = 0.8
    if self.get_category() == "Elemental":
      scale["int"] = 0.8
    if self.get_category() == "MeleeAgile":
      scale["str"] = 0.16
      scale["agi"] = 0.64

    if self.element == "Physical":
      if "str" in scale:
        scale["str"] += 0.2
      else:
        scale["str"] = 0.2
    if self.element == "Fire" or self.element == "Water" or self.element == "Wind" or self.element == "Earth":
      if "int" in scale:
        scale["int"] += 0.2
      else:
        scale["int"] = 0.2
    if self.element == "Light" or self.element == "Dark":
      if "spi" in scale:
        scale["spi"] += 0.2
      else:
        scale["spi"] = 0.2

    return scale


def CreateRandomWeapon():
  weapon_category = random.choice(list(weapon_categories.keys()))
  weapon_type = random.choice(weapon_categories[weapon_category])
  weapon_element = None
  while (True):
    weapon_element = random.choice(elements_list)
    if weapon_type == "Dagger" and weapon_element == "Light":
      continue
    if weapon_type == "Scythe" and weapon_element == "Light":
      continue
    if weapon_element == "Void":
      continue
    break
  weapon = Weapon(weapon_type, weapon_element)
  return weapon
