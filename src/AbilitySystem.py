import random

from AbilityDatabase import (
    primitive_skills,
    reaction_skills,
    skill_bases,
    skill_elemental_effects,
    skill_secondary_effects,
)
from Elements import elements_list
from TargetingUtilities import get_possible_targets_of_type, get_reaction_targets
from Weapons import weapon_categories


class PrimitiveAbility:

  def __init__(self, primitive_skill):
    self.skillbase = primitive_skill
    self.read_base_skill_data()
    self.name = self.get_name()

  def __str__(self):
    return self.name

  def read_base_skill_data(self):
    database = self.get_database()

    if self.skillbase in database:
      data = database[self.skillbase]
    else:
      exceptionmessage = f"Missing skill data for skill: {self.skillbase} \n"
      raise Exception(exceptionmessage)

    self.category = data.get("Category", "Primary")

    if self.is_guard():
      self.target_type = data.get("TargetType", "Self")
    else:
      self.target_type = data.get("TargetType", "Enemy")

    self.target_scope = data.get("TargetScope", "Single")
    self.target_range = data.get("TargetRange", "Any")

    self.priority = data.get("Priority", 0)

    self.base_atb_cost = data.get("AtbCost", 0)
    self.base_mana_cost = data.get("ManaCost", 0)

    self.effects = []
    self.effects.extend(data.get("Effects", []))
    self.modifiers = []
    self.modifiers.extend(data.get("Modifiers", []))

    self.reactable = data.get("Reactable", True)

  def get_mana_cost(self):
    manacost = self.base_mana_cost
    for modifier in self.modifiers:
      if modifier["Type"] == "ManaCost":
        manacost += modifier.get("Amount", 0)
        manacost *= modifier.get("Multiplier", 1.0)
    return manacost

  def get_mana_cost_for_unit(self, unit):
    return self.get_mana_cost()

  def get_atb_cost(self):
    atbcost = self.base_atb_cost
    for modifier in self.modifiers:
      if modifier["Type"] == "AtbCost":
        atbcost += modifier.get("Amount", 0)
        atbcost *= modifier.get("Multiplier", 1.0)
    return atbcost

  def get_atb_cost_for_unit(self, unit):
    atbcost = self.get_atb_cost()
    atbdivider = 0
    atbscaler = 0
    if self.is_damage():
      atbdivider += 100
      atbscaler += unit.attributes.agi
    if self.is_healing():
      atbdivider += 100
      atbscaler += unit.attributes.spi
    if not self.is_healing() and not self.is_damage(
    ) and self.has_added_effects():
      atbdivider += 100
      atbscaler += unit.attributes.spi

    if atbscaler > 0:
      atbcost /= (atbscaler / atbdivider) + 1

    atbcost = max(atbcost, 0)
    return atbcost

  def get_name(self):
    return self.skillbase

  def get_database(self):
    return primitive_skills

  def is_healing(self):
    return any(effect["Type"] == "Heal" for effect in self.effects)

  def is_damage(self):
    return any(effect["Type"] == "Damage" for effect in self.effects)

  def is_primary(self):
    return self.category == "Primary"

  def is_guard(self):
    return self.category == "Guard"

  def is_interrupt(self):
    return self.category == "Interrupt"

  def is_assist(self):
    return self.category == "Assist"

  def has_added_effects(self):
    return any(effect["Type"] != "Damage" and effect["Type"] != "Heal"
               for effect in self.effects)

  def is_single_target(self):
    return self.target_scope == "Single" or self.target_scope == "Random"

  def can_be_used(self, unit, battle):
    if unit.mana < self.get_mana_cost_for_unit(unit):
      return False

    if battle.actionchain is None:
      if self.is_primary():
        if not unit.is_ready_to_act():
          return False

        if self.target_type == "None":
          return True

        targets = get_possible_targets_of_type(unit, self.target_type, battle)

        if len(targets) == 0:
          return False

        return True
    else:
      if self.is_guard():
        targets = battle.actionchain.get_units_targeted_for_effect_type(
            "Damage")
        if unit in targets and unit.atb >= self.get_atb_cost_for_unit(unit):
          return True

    return False


class ReactionAbility(PrimitiveAbility):

  def __init__(self, reaction_name):
    self.skillbase = reaction_name
    self.read_base_skill_data()
    self.name = self.get_name()

  def read_base_skill_data(self):
    super().read_base_skill_data()
    database = self.get_database()

    if self.skillbase in database:
      data = database[self.skillbase]
    else:
      exceptionmessage = f"Missing skill data for skill: {self.skillbase} \n"
      raise Exception(exceptionmessage)

    self.category = data.get("Category", "Interrupt")
    self.subcategory = data.get("SubCategory", None)

    self.targetprimary = data.get("CanTargetPrimary", True)
    self.targetreaction = data.get("CanTargetReaction", True)
    self.targetguard = data.get("CanTargetGuard", False)

    self.requiresactingenemy = data.get("RequiresActingEnemy", False)
    self.requiresactingally = data.get("RequiresActingAlly", False)
    self.requirestargetacted = data.get("RequiresTargetActed", False)

    self.requireeffecttargetany = data.get("RequireEffectTargetAny", None)
    self.requireeffecttargetall = data.get("RequireEffectTargetAll", None)
    self.requireeffectuserany = data.get("RequireEffectUserAny", None)
    self.requireeffectuserall = data.get("RequireEffectUserAll", None)

  def get_database(self):
    return reaction_skills

  def get_name(self):
    return self.skillbase

  def can_be_used(self, unit, battle):
    if battle.actionchain is None:
      return False

    if unit.mana < self.get_mana_cost_for_unit(unit):
      return False

    if unit.atb < self.get_atb_cost_for_unit(unit):
      return False

    targets = get_reaction_targets(unit, self, battle)

    if len(targets) == 0:
      return False

    return True


class Ability(PrimitiveAbility):

  def __init__(self, skillbase, element, secondary):
    self.skillbase = skillbase
    self.element = element
    self.skillsecondary = secondary
    self.read_base_skill_data()
    self.read_element_data()
    self.read_secondary_data()
    self.name = self.get_name()

  def read_element_data(self):
    if self.element in skill_elemental_effects:
      data = skill_elemental_effects[self.element]
    else:
      exceptionmessage = f"Missing element data for skill: {self.skillbase} \n"
      exceptionmessage += f"Element: {self.element}\n"
      exceptionmessage += "Skill marked as primitive: False"
      raise Exception(exceptionmessage)

    for effect in self.effects:
      if "Scale" in effect:
        for stat in effect["Scale"]:
          effect["Scale"][stat] *= effect["Scale"][stat] * data.get(
              "DefaultScaleModifier", 1.0)

        for stat in data.get("AddedScale", {}):
          if stat in effect["Scale"]:
            effect["Scale"][stat] += data["AddedScale"][stat]
          else:
            effect["Scale"][stat] = data["AddedScale"][stat]

  def read_secondary_data(self):
    if self.skillsecondary in skill_secondary_effects:
      data = skill_secondary_effects[self.skillsecondary]
    else:
      exceptionmessage = f"Missing secondary data for skill: {self.skillbase} \n"
      exceptionmessage += f"Secondary: {self.skillsecondary}\n"
      exceptionmessage += "Skill marked as primitive: False"
      raise Exception(exceptionmessage)

    if "Modifiers" in data:
      self.modifiers.extend(data["Modifiers"])

    if "Effects" in data:
      self.effects.extend(data["Effects"])

  def get_name(self):
    elementnameoverrides = skill_bases[self.skillbase].get(
        "ElementNameOverrides", [])
    elementname = elementnameoverrides.get(self.element, self.element)
    name = self.skillsecondary + " "
    if elementname != "":
      name += elementname + " "
    name += self.skillbase
    return name

  def get_database(self):
    return skill_bases


def get_primitive_skills_for_weapon(weapon):
  weaponcategory = weapon.get_category()
  matchingprimitives = [
      name for name in primitive_skills
      if weaponcategory in primitive_skills[name]["UsableWithWeaponCategory"]
  ]
  skillset = []
  for skillname in matchingprimitives:
    skillset.append(PrimitiveAbility(skillname))

  return skillset


def get_random_ability_for_weapon(weapon):
  weaponcategory = weapon.get_category()
  weaponelement = weapon.element
  matchingskillnames = []
  for skillname in skill_bases:
    categorylimit = skill_bases[skillname].get("UsableWithWeaponCategory",
                                               weapon_categories.keys())
    elementlimit = skill_bases[skillname].get("UsableWithWeaponElement",
                                              elements_list)
    if weaponcategory in categorylimit and weaponelement in elementlimit:
      matchingskillnames.append(skillname)

  if len(matchingskillnames) == 0:
    return None

  decidedskillname = random.choice(matchingskillnames)

  matchingelements = skill_bases[decidedskillname].get(
      "LimitElements", list(skill_elemental_effects.keys()))
  if "Void" in matchingelements:
    matchingelements.remove("Void")

  if len(matchingelements) == 0:
    return None

  decidedelement = random.choice(matchingelements)

  secondarynames = []
  for secondaryname in skill_secondary_effects:
    if decidedskillname in skill_secondary_effects[secondaryname]["AppliesTo"]:
      secondarynames.append(secondaryname)

  if len(secondarynames) == 0:
    return None

  decidedsecondary = random.choice(secondarynames)

  return Ability(decidedskillname, decidedelement, decidedsecondary)


def get_random_reaction_ability_for_weapon(weapon):
  weaponcategory = weapon.get_category()
  weaponelement = weapon.element
  matchingskillnames = []
  for skillname in reaction_skills:
    categorylimit = reaction_skills[skillname].get("UsableWithWeaponCategory",
                                                   weapon_categories.keys())
    elementlimit = reaction_skills[skillname].get("UsableWithWeaponElement",
                                                  elements_list)
    if weaponcategory in categorylimit and weaponelement in elementlimit:
      matchingskillnames.append(skillname)

  if len(matchingskillnames) == 0:
    return None

  decidedskillname = random.choice(matchingskillnames)

  return ReactionAbility(decidedskillname)
