import random
#import time

from BattleUnitSystem import BattleUnit
from EffectApplier import apply_effect
from TargetingUtilities import *

#RESOLVE_STEP_DELAY = 0.25


class ActionChain:

  def __init__(self, primaryunit, ability, target, battle):
    self.primaryunit = primaryunit
    self.battle = battle
    self.primaryaction = PrimaryAction(primaryunit, ability, target, battle)
    self.actionchain: list[Action] = [self.primaryaction]
    self.resolvedata = {}
    self.create_resolve_data()
    self.primaryaction.update_resolve_target_data(self)

  def create_resolve_data(self):
    for unit in self.battle.allunits:
      self.add_unit_to_resolve_data(unit)

  def add_unit_to_resolve_data(self, unit):
    if unit not in self.resolvedata:
      self.resolvedata[unit] = {"Conditions": [], "Modifiers": []}

  def did_unit_act(self, unit):
    return any(action.user is unit for action in self.actionchain)

  def is_unit_using_primary(self, unit):
    return self.primaryaction.user is unit

  def is_unit_using_reaction(self, unit):
    if self.is_unit_using_primary(unit):
      return False
    return any(action.user is unit for action in self.actionchain)

  def is_unit_guarding(self, unit):
    return any(action.user is unit for action in self.actionchain
               if action.ability.is_guard())

  def display_primary_declare(self):
    self.primaryaction.display_declare_text()

  def get_units_targeted_for_effect_type(self, effecttype):
    units = []
    for unit in self.battle.allunits:
      if "TargetedByEffect" in self.resolvedata[unit]:
        if effecttype in self.resolvedata[unit]["TargetedByEffect"]:
          units.append(unit)
    return units

  def get_units_waiting_to_apply_effect(self, effecttype):
    units = []
    for unit in self.battle.allunits:
      if "WillUseEffect" in self.resolvedata[unit]:
        if effecttype in self.resolvedata[unit]["WillUseEffect"]:
          units.append(unit)

    return units

  def use_reaction(self, unit, ability, target=None):
    if ability.category == "Guard":
      self.actionchain.append(ReactionGuard(unit, ability, self.battle))
    elif ability.category == "Assist":
      self.actionchain.append(
          ReactionAssist(unit, target, ability, self.battle))
    elif ability.category == "Interrupt":
      self.actionchain.append(
          ReactionInterrupt(unit, target, ability, self.battle))

  def resolve_chain(self):
    resolver = ActionResolver(self)
    resolver.resolve()


class ActionResolver:

  def __init__(self, chain):
    self.battle = chain.battle
    self.chain = chain

  def resolve(self):
    resolvechain = []
    resolvechain.extend(self.chain.actionchain)
    resolvechain.sort(key=lambda action: action.get_priority())
    for action in reversed(resolvechain):
      self.battle.display_log("")
      self._resolve_action(action)
      self._resolve_step_wait()

  def _resolve_action(self, action):
    if not action.user.is_alive():
      action.canceled = True
      action.display_user_dead_text()
      return
    self.spend_ability_costs(action)
    if action.canceled:
      action.display_canceled_text()
      return

    action.display_use_text()

    #debugstart
    debug_text = " - TAGS: "
    for effect in action.ability.effects:
      if effect["Type"] == "AddModifier":
        debug_text += f"{effect['Type']}({effect['Modifier']['Type']}) "
      else:
        debug_text += f"{effect['Type']} "
    self.display_log(debug_text)
    #debugend

    for effect in action.ability.effects:
      apply_effect(action, effect, self)

  def display_log(self,logtext):
    self.battle.display_log(logtext)

  def _resolve_step_wait(self):
    #time.sleep(RESOLVE_STEP_DELAY)
    self.battle.wait_step()

  def spend_ability_costs(self, action):
    manacost = action.ability.get_mana_cost_for_unit(action.user)
    atbcost = action.ability.get_atb_cost_for_unit(action.user)

    for modifier in self.get_unit_modifiers_of_type(action.user, "ManaCost"):
      manacost += modifier.get("Amount", 0)
      manacost *= modifier.get("Multiplier", 1)

    for modifier in self.get_unit_modifiers_of_type(action.user, "AtbCost"):
      atbcost += modifier.get("Amount", 0)
      atbcost *= modifier.get("Multiplier", 1)

    atbcost = max(atbcost, 0)
    manacost = max(manacost, 0)

    if action.user.mana < manacost:
      action.canceled = True
      return False

    if action.user.atb < atbcost:
      action.canceled = True
      return False

    action.user.mana -= manacost
    action.user.atb -= atbcost
    return True

  def get_unit_conditions(self, unit):
    return self.chain.resolvedata[unit]["Conditions"]

  def get_unit_modifiers(self, unit):
    return self.chain.resolvedata[unit]["Modifiers"]

  def add_modifier_to_unit(self, unit, modifier):
    self.chain.resolvedata[unit]["Modifiers"].append(modifier)

  def add_condition_to_unit(self, unit, condition):
    self.chain.resolvedata[unit]["Conditions"].append(condition)

  def get_unit_conditions_of_type(self, unit, conditiontype):
    return [
        condition for condition in self.get_unit_conditions(unit)
        if condition["Type"] == conditiontype
    ]

  def get_unit_modifiers_of_type(self, unit, modifiertype):
    return [
        modifier for modifier in self.get_unit_modifiers(unit)
        if modifier["Type"] == modifiertype
    ]


class Action:

  def __init__(self, user, target, ability, battle):
    self.user = user
    self.ability = ability
    self.declaredtarget = target
    self.canceled = False
    self.battle = battle
    if self.ability is None:
      return
    self.maintargets = self.get_main_action_targets(target)
    self.update_resolve_target_data(battle.actionchain)
    if ability.reactable:
      self.display_declare_text()

  def get_main_action_targets(self, target):
    return self.get_action_targets(target, self.ability.target_type,
                                   self.ability.target_scope,
                                   self.ability.target_range)

  def get_potential_action_targets(self, target, targettype, targetscope,
                                   targetrange):
    if targetscope == "Random":
      possible_targets = get_possible_targets_of_type(self.user, targettype,
                                                      self.battle)
    else:
      possible_targets = self.get_action_targets(target, targettype,
                                                 targetscope, targetrange)
    if possible_targets is None:
      return []
    else:
      return possible_targets

  def get_action_targets(self, target, targettype, targetscope, targetrange):
    if targetscope == "Single":
      if targettype == "Self":
        return [self.user]
      else:
        return [target]

    elif targetscope == "All":
      candidates = []
      if targettype == "Self":
        return [self.user]
      elif targettype == "Enemy":
        candidates = get_hostile_units(self.user, self.battle)
      elif targettype == "Friendly":
        candidates = get_allied_units(self.user, self.battle)
      elif targettype == "Friendly Except Self":
        candidates = get_allied_units_except_self(self.user, self.battle)
      elif targettype == "Everyone":
        candidates = get_all_units(self.battle)
      elif targettype == "Everyone Except Self":
        candidates = get_all_units_except_self(self.user, self.battle)
      elif targettype == "None":
        return []
      else:
        return None

      if candidates is not None:
        if targetrange == "Melee":
          melees = [unit for unit in candidates if unit.has_melee_weapon()]
          if len(melees) > 0:
            return melees
          else:
            return candidates
        else:
          return candidates

    elif targetscope == "Random":
      candidates = []
      if targettype == "Self":
        return [self.user]
      elif targettype == "Enemy":
        candidates = get_hostile_units(self.user, self.battle)
      elif targettype == "Friendly":
        candidates = get_allied_units(self.user, self.battle)
      elif targettype == "Friendly Except Self":
        candidates = get_allied_units_except_self(self.user, self.battle)
      elif targettype == "Everyone":
        candidates = get_all_units(self.battle)
      elif targettype == "Everyone Except Self":
        candidates = get_all_units_except_self(self.user, self.battle)
      elif targettype == "None":
        return []
      else:
        return None

      if candidates is not None:
        if targetrange == "Melee":
          melees = [unit for unit in candidates if unit.has_melee_weapon()]
          if len(melees) > 0:
            return [random.choice(melees)]
          else:
            return [random.choice(candidates)]
        else:
          return [random.choice(candidates)]
    else:
      return None

  def update_resolve_target_data(self, chain):
    if chain is None:
      return

    for effect in self.ability.effects:
      targettype = effect.get("TargetType", self.ability.target_type)
      targetscope = effect.get("TargetScope", self.ability.target_scope)
      targetrange = effect.get("TargetRange", self.ability.target_range)

      targets = self.get_potential_action_targets(self.declaredtarget,
                                                  targettype, targetscope,
                                                  targetrange)
      if effect["Type"] != "AddModifier":
        if "WillUseEffect" not in chain.resolvedata[self.user]:
          chain.resolvedata[self.user]["WillUseEffect"] = set()
        chain.resolvedata[self.user]["WillUseEffect"].add(effect["Type"])
        if targets is not None:
          for target in targets:
            if "TargetedByEffect" not in chain.resolvedata[target]:
              chain.resolvedata[target]["TargetedByEffect"] = set()
            chain.resolvedata[target]["TargetedByEffect"].add(effect["Type"])
      else:
        if "WillAddModifier" not in chain.resolvedata[self.user]:
          chain.resolvedata[self.user]["WillAddModifier"] = set()
        chain.resolvedata[self.user]["WillAddModifier"].add(
            effect["Modifier"]["Type"])
        if targets is not None:
          for target in targets:
            if "TargetedByModifier" not in chain.resolvedata[target]:
              chain.resolvedata[target]["TargetedByModifier"] = set()
            chain.resolvedata[target]["TargetedByModifier"].add(
                effect["Modifier"]["Type"])

  def get_priority(self):
    return self.ability.priority

  def is_reaction(self):
    return not self.ability.is_primary()

  def display_use_text(self):
    if len(self.maintargets) == 1:
      self.battle.display_log(f"{self.user} used {self.ability} on {self.maintargets[0]}")
    else:
      self.battle.display_log(f"{self.user} used {self.ability}")

  def display_declare_text(self):
    if len(self.maintargets) == 1:
      self.battle.display_log(f"{self.user} is preparing to use {self.ability} on {self.maintargets[0]}")
    else:
      self.battle.display_log(f"{self.user} is preparing to use {self.ability}")

  def display_canceled_text(self):
    self.battle.display_log(f"{self.user} got interrupted and couldn't use {self.ability}")

  def display_user_dead_text(self):
    self.battle.display_log(f"{self.user} is dead and can't use {self.ability}")


class PrimaryAction(Action):

  def __init__(self, user, ability, target: list[BattleUnit], battle):
    super().__init__(user, target, ability, battle)


class ReactionInterrupt(Action):

  def display_declare_text(self):
    if self.ability.subcategory == "Interrupt":
      if len(self.maintargets) == 1:
        self.battle.display_log(f"{self.user} is preparing to interrupt {self.maintargets[0]} with {self.ability}")
      else:
        self.battle.display_log(f"{self.user} is preparing to interrupt with {self.ability}")
    elif self.ability.subcategory == "Disrupt":
      if len(self.maintargets) == 1:
        self.battle.display_log(f"{self.user} is preparing to disrupt {self.maintargets[0]} with {self.ability}")
      else:
        self.battle.display_log(f"{self.user} is preparing to disrupt with {self.ability}")
    else:
      if len(self.maintargets) == 1:
        self.battle.display_log(f"{self.user} is preparing to interrupt {self.maintargets[0]} with {self.ability}")
      else:
        self.battle.display_log(f"{self.user} is preparing to interrupt with {self.ability}")


class ReactionAssist(Action):

  def display_declare_text(self):
    if self.ability.subcategory == "Protect":
      if len(self.maintargets) == 1:
        self.battle.display_log(f"{self.user} is preparing to protect {self.maintargets[0]} with {self.ability}")
      else:
        self.battle.display_log(f"{self.user} is preparing to protect with {self.ability}")
    elif self.ability.subcategory == "Empower":
      if len(self.maintargets) == 1:
        self.battle.display_log(f"{self.user} is preparing to empower {self.maintargets[0]} with {self.ability}")
      else:
        self.battle.display_log(f"{self.user} is preparing to empower with {self.ability}")
    else:
      if len(self.maintargets) == 1:
        self.battle.display_log(f"{self.user} is preparing to assist {self.maintargets[0]} with {self.ability}")
      else:
        self.battle.display_log(f"{self.user} is preparing to assist with {self.ability}")


class ReactionGuard(Action):

  def __init__(self, user, ability, battle):
    super().__init__(user, [], ability, battle)

  def get_priority(self):
    return self.ability.priority + 0.8

  def display_use_text(self):
    self.battle.display_log(f"{self.user} is guarding with {self.ability}")

  def display_declare_text(self):
    self.battle.display_log(f"{self.user} is preparing to guard with {self.ability}")
