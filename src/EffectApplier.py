import time

from Elements import elements_list, get_scale_stat_for_element

target_modifier_types = {"Damage": "DamageTaken", "Heal": "HealReceived"}
modifier_apply_messages = {
    "DamageTaken": {
        "PositiveValue": "Damage against {0} is boosted by {1}",
        "NegativeValue": "Damage against {0} is reduced by {1}",
        "PositiveMultiplier": "{0} is taking {1:.0%} more damage",
        "NegativeMultiplier": "{0} is taking {1:.0%} less damage",
        "PositiveFixedValue": "{0} will take {1} additional damage",
        "NegativeFixedValue": "{0} will take {1} less damage",
        "PositiveTrueValue": "{0} will lose {1} extra health when hit.",
        "NegativeTrueValue": "{0} will lose {1} less health when hit.",
    },
    "HealReceived": {
        "PositiveValue": "Healing against {0} is boosted by {1}",
        "NegativeValue": "Healing against {0} is reduced by {1}",
        "PositiveMultiplier": "{0} is receiving {1:.0%} more healing",
        "NegativeMultiplier": "{0} is receiving {1:.0%} less healing",
        "PositiveFixedValue": "{0} will receive {1} additional healing",
        "NegativeFixedValue": "{0} will receive {1} less healing",
        "PositiveTrueValue": "{0} will gain {1} extra health when healed.",
        "NegativeTrueValue": "{0} will gain {1} less health when healed.",
    },
    "AtbCost": {
        "PositiveValue": "Base Atb costs of {0} are boosted by {1}",
        "NegativeValue": "Base Atb costs of {0} are reduced by {1}",
        "PositiveMultiplier": "{0} had it's Atb costs increased by {1:.0%}",
        "NegativeMultiplier": "{0} had it's Atb costs decreased by {1:.0%}",
        "PositiveFixedValue":
        "{0} will use {1} additional atb when using abilities.",
        "NegativeFixedValue":
        "{0} will use {1} less atb when using abilities.",
        "PositiveTrueValue": "{0} will lose {1} more atb per ability used.",
        "NegativeTrueValue": "{0} will lose {1} less atb per ability used.",
    }
}


class Values:

  def __init__(self,
               amount=0.0,
               fixedamount=0.0,
               trueamount=0.0,
               multiplier=1.0):
    self.amount = amount
    self.fixedamount = fixedamount
    self.trueamount = trueamount
    self.multiplier = multiplier

  def _add_values_from_data(self, data, user=None, ability=None):
    self.amount += data.get("Amount", 0)
    self.fixedamount += data.get("FixedAmount", 0)
    self.trueamount += data.get("TrueAmount", 0)
    self.multiplier *= data.get("Multiplier", 1.0)
    scale = data.get("Scale", {})
    self.amount *= _convert_scale_to_multiplier(scale, user, ability)


class ModifierValues(Values):

  @staticmethod
  def copy(other):
    return ModifierValues(other.amount, other.fixedamount, other.trueamount,
                          other.multiplier)

  @staticmethod
  def create_from_modifier(modifier, user=None, ability=None):
    values = ModifierValues()
    values._add_values_from_data(modifier, user, ability)
    return values

  def __add__(self, other):
    sumamount = self.amount + other.amount
    sumfixedamount = self.fixedamount + other.fixedamount
    sumtrueamount = self.trueamount + other.trueamount
    summultiplier = self.multiplier * other.multiplier
    if isinstance(other, EffectValues):
      return EffectValues(sumamount, sumfixedamount, sumtrueamount,
                          summultiplier)
    else:
      return ModifierValues(sumamount, sumfixedamount, sumtrueamount,
                            summultiplier)


class EffectValues(Values):

  @staticmethod
  def copy(other):
    return EffectValues(other.amount, other.fixedamount, other.trueamount,
                        other.multiplier)

  @staticmethod
  def create_from_effect(effect, user=None, ability=None):
    values = EffectValues()
    values._add_values_from_data(effect, user, ability)
    return values

  def __add__(self, other):
    sumamount = self.amount + other.amount
    sumfixedamount = self.fixedamount + other.fixedamount
    sumtrueamount = self.trueamount + other.trueamount
    summultiplier = self.multiplier * other.multiplier
    return EffectValues(sumamount, sumfixedamount, sumtrueamount,
                        summultiplier)

  def get_resolved_value_without_true_amount(self):
    value = self.amount
    value *= self.multiplier
    value += self.fixedamount
    return value

  def resolve(self):
    return {
        "Value": self.get_resolved_value_without_true_amount(),
        "TrueValue": self.trueamount
    }

  def apply_divide_limit(self, target_count, divide_limit):
    if divide_limit > 0 and target_count > divide_limit:
      self.multiplier *= (divide_limit / target_count)


class DamageSet:

  def __init__(self, element_weights, damage, true_damage=0.0):
    self.element_weights = element_weights
    self.rawdamage = damage
    self.truedamage = true_damage
    self.damageset = {}
    self.recalculate()

  def recalculate(self):
    self.damageset = {}
    for element in elements_list:
      self.damageset[element] = self.rawdamage * self.element_weights.get(
          element, 0.0)

  def deal_to_unit(self, unit):
    return unit.damage_health(self)


class EffectHandler:

  def __new__(cls, action, effect, resolver):
    if cls is EffectHandler:
      if effect["Type"] == "Damage":
        return super().__new__(EffectHandlerDamage)
      if effect["Type"] == "Heal":
        return super().__new__(EffectHandlerHealing)
      if effect["Type"] == "AddModifier":
        return super().__new__(EffectHandlerAddModifier)
      if effect["Type"] == "AtbGain":
        return super().__new__(EffectHandlerAtbGain)
      if effect["Type"] == "AtbLoss":
        return super().__new__(EffectHandlerAtbLoss)
      if effect["Type"] == "ManaGain":
        return super().__new__(EffectHandlerManaGain)
      if effect["Type"] == "ManaLoss":
        return super().__new__(EffectHandlerManaLoss)
      else:
        raise TypeError(
            f"Effect type {effect['Type']} is missing a handler class.")

  def __init__(self, action, effect, resolver):
    self.action = action
    self.effect = effect
    self.effect_type = effect["Type"]
    self.resolver = resolver

  def apply(self):
    self.targets = _get_effect_targets(self.action, self.effect)
    self.actionmodifiers = _get_modifiers_affecting_action_of_type(
        self.action, self.resolver, self.effect_type)
    self.values = EffectValues.create_from_effect(self.effect,
                                                  self.action.user,
                                                  self.action.ability)
    self.divide_limit = self.effect.get("DivideLimit", 0)
    self.element_weights = _get_element_weights_of_effect(
        self.effect, self.action.user, self.action.ability)
    self.values.apply_divide_limit(len(self.targets), self.divide_limit)

    for modifier in self.actionmodifiers:
      self.values += ModifierValues.create_from_modifier(
          modifier, self.action.user, self.action.ability)

  def get_target_specific_values(self, target):
    targetvalues = EffectValues.copy(self.values)
    targetmodtype = _get_target_modifier_type(self.effect_type)
    if targetmodtype is not None:
      targetmodifiers = self.resolver.get_unit_modifiers_of_type(
          target, targetmodtype)

      for modifier in targetmodifiers:
        targetvalues += ModifierValues.create_from_modifier(modifier, target)
    return targetvalues


class EffectHandlerDamage(EffectHandler):

  def apply(self):
    super().apply()

    for target in self.targets:
      targetvalues = self.get_target_specific_values(target)

      targetdamage = targetvalues.resolve()

      damageset = DamageSet(self.element_weights, targetdamage["Value"],
                            targetdamage["TrueValue"])

      damagetaken = damageset.deal_to_unit(target)
      if damagetaken > 0:
        self.resolver.display_log(f"{target.name} took {damagetaken:.2f} damage")
      else:
        self.resolver.display_log(f"{target.name} took no damage")


class EffectHandlerHealing(EffectHandler):

  def apply(self):
    super().apply()

    for target in self.targets:
      targetvalues = self.get_target_specific_values(target)

      targetheal = targetvalues.resolve()

      healamount = target.add_health(targetheal["Value"] +
                                     targetheal["TrueValue"])
      if healamount > 0:
          self.resolver.display_log(f"Healed {target.name} for {healamount:.2f} health")


class EffectHandlerAddModifier(EffectHandler):

  def apply(self):
    modifier = self.effect["Modifier"]

    targets = _get_effect_targets(self.action, self.effect)

    for target in targets:
      self.resolver.add_modifier_to_unit(target, modifier)
      self._display_text_messages(target, modifier)

  def _display_text_messages(self, target, modifier):
    modifiervalues = ModifierValues.create_from_modifier(
        modifier, self.action.user, self.action.ability)
    modifiertexts = modifier_apply_messages.get(modifier["Type"], None)
    messages_to_display = []
    if modifiertexts is not None:
      if modifiervalues.amount > 0:
        messages_to_display.append({
            "Text":
            modifiertexts.get("PositiveValue", None),
            "Value":
            modifiervalues.amount
        })
      elif modifiervalues.amount < 0:
        messages_to_display.append({
            "Text":
            modifiertexts.get("NegativeValue", None),
            "Value":
            modifiervalues.amount * -1
        })

      if modifiervalues.fixedamount > 0:
        messages_to_display.append({
            "Text":
            modifiertexts.get("PositiveFixedValue", None),
            "Value":
            modifiervalues.fixedamount
        })
      elif modifiervalues.fixedamount < 0:
        messages_to_display.append({
            "Text":
            modifiertexts.get("NegativeFixedValue", None),
            "Value":
            modifiervalues.fixedamount * -1
        })

      if modifiervalues.trueamount > 0:
        messages_to_display.append({
            "Text":
            modifiertexts.get("PositiveTrueValue", None),
            "Value":
            modifiervalues.trueamount
        })
      elif modifiervalues.trueamount < 0:
        messages_to_display.append({
            "Text":
            modifiertexts.get("NegativeTrueValue", None),
            "Value":
            modifiervalues.trueamount * -1
        })

      if modifiervalues.multiplier > 1.0:
        messages_to_display.append({
            "Text":
            modifiertexts.get("PositiveMultiplier", None),
            "Value":
            modifiervalues.multiplier - 1.0
        })
      elif modifiervalues.multiplier < 1.0:
        messages_to_display.append({
            "Text":
            modifiertexts.get("NegativeMultiplier", None),
            "Value":
            1.0 - modifiervalues.multiplier
        })
      for message in messages_to_display:
        self._display_formated_text_message(message["Text"], target,
                                            message["Value"])

  def _display_formated_text_message(self, message, target, value):
    if message is None:
      return
    self.resolver.display_log(message.format(target.name, value))


class EffectHandlerAtbGain(EffectHandler):

  def apply(self):
    super().apply()

    for target in self.targets:
      targetvalues = self.get_target_specific_values(target)

      targetatb = targetvalues.resolve()

      atbamount = max(targetatb["Value"] + targetatb["TrueValue"], 0)
      target.atb += atbamount
      if atbamount > 0:
        self.resolver.display_log(f"{target.name} gained {atbamount:.2f} ATB")


class EffectHandlerAtbLoss(EffectHandler):

  def apply(self):
    super().apply()

    for target in self.targets:
      targetvalues = self.get_target_specific_values(target)

      targetatb = targetvalues.resolve()

      atbamount = max(targetatb["Value"] + targetatb["TrueValue"], 0)
      target.atb -= atbamount
      if atbamount > 0:
        self.resolver.display_log(f"{target.name} lost {atbamount:.2f} ATB")


def apply_effect(action, effect, resolver):
  handler = EffectHandler(action, effect, resolver)
  handler.apply()


def _get_target_modifier_type(effect_type):
  return target_modifier_types.get(effect_type, None)


def _convert_scale_to_multiplier(scale, unit=None, ability=None):
  totalscale = 1.0
  for attribute in scale:
    if attribute == "WeaponScale":
      try:
        weaponscale = unit.weapon.get_scale()
        for weaponattribute in weaponscale:
          totalscale += weaponscale[weaponattribute] * scale[
              "WeaponScale"] * unit.attributes[weaponattribute]
      except:
        pass
      continue
    if attribute == "ElementScale":
      try:
        scalestat = get_scale_stat_for_element(ability.element)
        totalscale += scale["ElementScale"] * unit.attributes[scalestat]
      except:
        pass
      continue
    totalscale += scale[attribute] * unit.attributes[attribute]
  return totalscale


def _get_effect_targets(action, effect):
  targettype = effect.get("TargetType", action.ability.target_type)
  targetscope = effect.get("TargetScope", action.ability.target_scope)
  targetrange = effect.get("TargetRange", action.ability.target_range)
  targets = action.get_action_targets(action.declaredtarget, targettype,
                                      targetscope, targetrange)
  return targets


def _get_element_weights_of_effect(effect, unit, ability):
  try:
    raw_element_weights = effect.get("ElementWeight", {ability.element: 1.0})
  except AttributeError:
    raw_element_weights = effect.get("ElementWeight", {"WeaponElement": 1.0})

  element_weights = {}
  for element in raw_element_weights:
    modifiedelement = element
    if modifiedelement == "WeaponElement":
      modifiedelement = unit.weapon.element

    if modifiedelement == "AbilityElement":
      modifiedelement = ability.element

    if modifiedelement in element_weights:
      element_weights[modifiedelement] += raw_element_weights[element]
    else:
      element_weights[modifiedelement] = raw_element_weights[element]
  return element_weights


def _get_modifiers_affecting_action_of_type(action, resolver, type):
  modifiers = [mod for mod in action.ability.modifiers if mod["Type"] == type]
  modifiers.extend(resolver.get_unit_modifiers_of_type(action.user, type))
  return modifiers
