target_types = [
    "Enemy", "Friendly", "Friendly Except Self", "Self", "Everyone",
    "Everyone Except Self", "None"
]
target_scopes = ["Single", "All", "Random"]
target_range = ["Melee", "Ranged", "Any"]


def get_hostile_units(unit, battle):
  hostile_units = []
  for target in battle.activeunits:
    if target.side != unit.side and target.is_alive():
      hostile_units.append(target)
  return hostile_units


def get_allied_units(unit, battle):
  allied_units = []
  for target in battle.activeunits:
    if target.side == unit.side and target.is_alive():
      allied_units.append(target)
  return allied_units


def get_allied_units_except_self(unit, battle):
  allied_units = get_allied_units(unit, battle)
  allied_units.remove(unit)
  return allied_units


def get_all_units_except_self(unit, battle):
  all_units = []
  all_units.extend(battle.activeunits)
  all_units.remove(unit)
  return all_units


def get_all_units(battle):
  all_units = []
  all_units.extend(battle.activeunits)
  return all_units


def filter_units_to_range(unitlist, range):
  if range == "Melee":
    return [unit for unit in unitlist if unit.has_melee_weapon()]
  elif range == "Ranged":
    return [unit for unit in unitlist if not unit.has_melee_weapon()]
  else:
    newunitlist = []
    newunitlist.extend(unitlist)
    return newunitlist


def get_hostile_melee_units(unit, battle):
  hostiles = get_hostile_units(unit, battle)
  return filter_units_to_range(hostiles, "Melee")


def get_possible_targets_of_type_in_range(unit, target_type, target_range,
                                          battle):
  
  hostile_melees = get_hostile_melee_units(unit, battle)
  if target_range == "Melee" and len(hostile_melees) > 0:
    if target_type == "Enemy":
      return hostile_melees
    elif target_type == "Everyone":
      targets = []
      targets.extend(hostile_melees)
      targets.extend(get_allied_units(unit, battle))
      return targets
    if target_type == "Everyone Except Self":
      targets = []
      targets.extend(hostile_melees)
      targets.extend(get_allied_units_except_self(unit, battle))
      return targets

  return get_possible_targets_of_type(unit, target_type, battle)


def get_possible_targets_of_type(unit, target_type, battle):
  if target_type == "Self":
    return [unit]
  elif target_type == "Enemy":
    return get_hostile_units(unit, battle)
  elif target_type == "Friendly":
    return get_allied_units(unit, battle)
  elif target_type == "Friendly Except Self":
    return get_allied_units_except_self(unit, battle)
  elif target_type == "Everyone":
    return get_all_units(battle)
  elif target_type == "Everyone Except Self":
    return get_all_units_except_self(unit, battle)
  elif target_type == "None":
    return []
  else:
    return None


def get_reaction_targets(unit, ability, battle):
  targets = get_possible_targets_of_type(unit, ability.target_type, battle)
  if targets is None:
    return []

  if len(targets) == 0:
    return []

  targets = set(targets)

  if ability.requiresactingally:
    allyacted = any(
        battle.actionchain.did_unit_act(ally)
        for ally in get_allied_units(unit, battle))
    if not allyacted:
      return []

  if ability.requiresactingenemy:
    enemyacted = any(
        battle.actionchain.did_unit_act(enemy)
        for enemy in get_hostile_units(unit, battle))
    if not enemyacted:
      return []

  if ability.requireeffecttargetany is not None:
    potentialtargets = set()
    for effect in ability.requireeffecttargetany:
      effecttargets = battle.actionchain.get_units_targeted_for_effect_type(
          effect)
      potentialtargets.update(effecttargets)
    targets = targets.intersection(potentialtargets)

  if ability.requireeffecttargetall is not None:
    potentialtargets = set()
    first = True
    for effect in ability.requireeffecttargetall:
      effecttargets = battle.actionchain.get_units_targeted_for_effect_type(
          effect)
      if first:
        potentialtargets.update(effecttargets)
        first = False
      else:
        potentialtargets = potentialtargets.intersection(effecttargets)
    targets = targets.intersection(potentialtargets)

  if ability.requireeffectuserany is not None:
    potentialtargets = set()
    for effect in ability.requireeffectuserany:
      effecttargets = battle.actionchain.get_units_waiting_to_apply_effect(
          effect)
      potentialtargets.update(effecttargets)
    targets = targets.intersection(potentialtargets)

  if ability.requireeffectuserall is not None:
    potentialtargets = set()
    first = True
    for effect in ability.requireeffectuserall:
      effecttargets = battle.actionchain.get_units_waiting_to_apply_effect(
          effect)
      if first:
        potentialtargets.update(effecttargets)
        first = False
      else:
        potentialtargets = potentialtargets.intersection(effecttargets)
    targets = targets.intersection(potentialtargets)

  if len(targets) == 0:
    return []

  inappropriate_targets = set()
  for target in targets:
    if ability.requirestargetacted and not battle.actionchain.did_unit_act(
        target):
      inappropriate_targets.add(target)
      continue
    if not ability.targetprimary and battle.actionchain.is_unit_using_primary(
        target):
      inappropriate_targets.add(target)
      continue
    if not ability.targetreaction and battle.actionchain.is_unit_using_reaction(
        target):
      inappropriate_targets.add(target)
      continue
    if not ability.targetguard and battle.actionchain.is_unit_guarding(target):
      inappropriate_targets.add(target)
      continue

  targets = targets.difference(inappropriate_targets)

  if len(targets) == 0:
    return []

  return list(targets)


def does_ability_require_target(ability):
  if ability.target_type == "Self" or ability.target_type == "None" or ability.target_scope != "Single":
    return False

  return True
