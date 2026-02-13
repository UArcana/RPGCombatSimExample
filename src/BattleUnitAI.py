import random

from TargetingUtilities import (
  does_ability_require_target,
  get_allied_units,
  get_possible_targets_of_type_in_range,
  get_reaction_targets,
)

HEAL_INTEREST_THRESHOLD = 0.9


def get_viable_healing_abilities(unit, abilities, battle):
  healabilities = [ability for ability in abilities if ability.is_healing()]
  if len(healabilities) == 0:
    return []

  alliesneedheal = get_allies_in_need_of_healing(unit, battle)
  if len(alliesneedheal) == 0:
    return []

  viable_healabilities = set()
  for ability in healabilities:
    for effect in ability.effects:
      if effect["Type"] != "Heal":
        continue

      effecttargettype = effect.get("TargetType", ability.target_type)

      if effecttargettype == "Self" and unit in alliesneedheal:
        viable_healabilities.add(ability)
      if effecttargettype == "Friendly Except Self" or effecttargettype == "All Except Self":
        allieswithoutself = [ally for ally in alliesneedheal if ally != unit]

        if len(allieswithoutself) > 0:
          viable_healabilities.add(ability)
      else:
        viable_healabilities.add(ability)
  return list(viable_healabilities)


def is_unit_in_need_of_healing(unit):
  return unit.get_health_percentage() <= HEAL_INTEREST_THRESHOLD


def get_allies_in_need_of_healing(unit, battle, targetlist=None):
  if targetlist is None:
    targetlist = get_allied_units(unit, battle)
  damagedallies = [
      ally for ally in targetlist if is_unit_in_need_of_healing(ally)
  ]
  return damagedallies


def find_suitable_healing_target(unit, ability, battle, potentialtargets=None):
  if ability.target_type == "Self":
    if is_unit_in_need_of_healing(unit):
      return unit
    else:
      return None
  alliesneedheal = get_allies_in_need_of_healing(unit, battle,
                                                 potentialtargets)
  if len(alliesneedheal) == 0:
    return None

  if ability.target_type == "Friendly":
    return min(alliesneedheal, key=lambda ally: ally.get_health_percentage())

  if ability.target_type == "Friendly Except Self" or ability.target_type == "All Except Self":
    allieswithoutself = [ally for ally in alliesneedheal if ally != unit]
    if len(allieswithoutself) == 0:
      return None

    return min(allieswithoutself,
               key=lambda ally: ally.get_health_percentage())
  return None


def find_suitable_attack_target(potentialtargets):
  return min(potentialtargets,
             key=lambda hostile: hostile.get_health_percentage())


def get_ai_command(unit, battle):
  chosen_ability = decide_ability_to_use(unit, battle)
  if chosen_ability is None:
    return False

  if chosen_ability.is_primary():
    return issue_primary_ability(unit, chosen_ability, battle)
  else:
    issue_reaction_ability(unit, chosen_ability, battle)

  return True


def issue_primary_ability(unit, ability, battle):
  target = None
  if does_ability_require_target(ability):
    decided_target = decide_target_for_primary_ability(unit, ability, battle)
    if decided_target is not None:
      target = decided_target
    else:
      return False

  battle.use_primary_ability(unit, ability, target)
  return True

def issue_reaction_ability(unit, ability, battle):
  target = None
  if does_ability_require_target(ability):
    targets = get_reaction_targets(unit, ability, battle)
    if len(targets) > 0:
      target = random.choice(targets)
    else:
      return False

  battle.actionchain.use_reaction(unit, ability, target)
  return True


def decide_ability_to_use(unit, battle):
  usable_abilities = [
      ability for ability in unit.abilities
      if ability.can_be_used(unit, battle)
  ]
  viablehealabilities = get_viable_healing_abilities(unit, usable_abilities,
                                                     battle)

  if len(viablehealabilities) > 0:
    return random.choice(viablehealabilities)
  else:
    other_abilities = []
    for ability in usable_abilities:
      if any(effect for effect in ability.effects if effect["Type"] != "Heal"):
        other_abilities.append(ability)

    if len(other_abilities) > 0:
      return random.choice(other_abilities)

    return None


def decide_target_for_primary_ability(unit, ability, battle):
  targets = get_possible_targets_of_type_in_range(unit, ability.target_type,
                                                  ability.target_range, battle)
  if targets is None:
    return None

  if len(targets) == 0:
    return None

  if ability.is_healing():
    healtarget = find_suitable_healing_target(unit, ability, battle, targets)
    if healtarget is not None:
      return healtarget

  if ability.is_damage():
    attacktarget = find_suitable_attack_target(targets)
    return attacktarget

  return random.choice(targets)
