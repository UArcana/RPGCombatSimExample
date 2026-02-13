import random

from AbilitySystem import (
    get_primitive_skills_for_weapon,
    get_random_ability_for_weapon,
    get_random_reaction_ability_for_weapon,
)
from Attributes import Attributes, attribute_keys
from EffectApplier import DamageSet
from Weapons import CreateRandomWeapon

MAX_MANA_BASE = 20
MAX_HEALTH_BASE = 100
MAX_HEALTH_MELEE_BONUS = 25

DEBUG_BASE_ATTRIBUTES = 300
DEBUG_RANDOM_ADDITIONAL_ATTRIBUTES = 0


class BattleUnit:

    def __init__(self, name, side, weapon):
        self.name = name
        self.atb = 0.0
        self.weapon = weapon
        self.attributes = Attributes()
        self.mana = self.get_max_mana()
        self.health = self.get_max_health()
        self.side = side
        self.abilities = []
        self.status = []

    def __str__(self):
        return self.name

    def get_mana_regen_per_gamesec(self):
        return 5 + (self.attributes.wis * 0.01)

    def get_max_mana(self):
        return MAX_MANA_BASE + (self.attributes.wis * 0.25)

    def get_max_health(self):
        maxhp = MAX_HEALTH_BASE
        if self.has_melee_weapon():
            maxhp += MAX_HEALTH_MELEE_BONUS
        return maxhp

    def has_melee_weapon(self):
        if self.weapon is None:
            return True

        return self.weapon.get_category() == 'Melee'

    def randomize_attributes(self):
        self.attributes.str = DEBUG_BASE_ATTRIBUTES
        self.attributes.agi = DEBUG_BASE_ATTRIBUTES
        self.attributes.int = DEBUG_BASE_ATTRIBUTES
        self.attributes.wis = DEBUG_BASE_ATTRIBUTES
        self.attributes.spi = DEBUG_BASE_ATTRIBUTES
        self.attributes.end = DEBUG_BASE_ATTRIBUTES
        for _ in range(DEBUG_RANDOM_ADDITIONAL_ATTRIBUTES):
            self.attributes[random.choice(attribute_keys)] += 1

    def is_alive(self):
        return self.health > 0

    def tick(self, duration):
        if duration == 0:
            return

        self.atb += duration

        self.add_mana(self.get_mana_regen_per_gamesec() * (duration / 100))
        for status in self.status:
            status.tick(duration)

    def remove_status_effect(self, status_effect):
        self.status.remove(status_effect)

    def apply_status_effect(self, status_effect):
        self.status.append(status_effect)

    def remove_all_status_effects_of_type(self, status_type):
        for status in self.status:
            if status.type == status_type:
                self.remove_status_effect(status)

    def remove_all_status_effects(self):
        self.status = []

    def full_refresh(self):
        self.health = self.get_max_health()
        self.mana = self.get_max_mana()
        self.atb = 0
        self.remove_all_status_effects()

    def set_dead(self):
        self.health = 0
        self.atb = 0
        self.mana = 0
        self.remove_all_status_effects()

    def damage_health(self, damagesetobj: DamageSet):
        damageset = damagesetobj.damageset
        damagetotal = 0.0
        for element in damageset:
            defstat = 0.0
            if element == "Physical":
                defstat = self.attributes.str * 0.01
            elif element == "Fire" or element == "Water" or element == "Wind" or element == "Earth":
                defstat = self.attributes.int * 0.01
            elif element == "Light" or element == "Dark":
                defstat = self.attributes.spi * 0.01
            damagetotal += damageset[element] / (defstat + 1)
        healthchange = 0.0
        truedamage = max(damagesetobj.truedamage, 0)
        if damagetotal > 0:
            healthchange += self.change_health(damagetotal * -1)
        if truedamage > 0:
            healthchange += self.change_health(max(damagesetobj.truedamage, 0) * -1)
        damagetaken = 0.0
        if healthchange != 0:
            damagetaken = healthchange * -1
        return damagetaken

    def add_health(self, heal):
        return self.change_health(heal)

    def change_health(self, change):
        before_health = self.health
        self.health += change

        if self.health <= 0:
            self.set_dead()
        if self.health > self.get_max_health():
            self.health = self.get_max_health()

        healthchange = self.health - before_health
        return healthchange

    def get_health_percentage(self):
        return self.health / self.get_max_health()

    def damage_mana(self, damage):
        damage = max(damage, 0)
        manachange = self.change_mana(damage * -1)
        damagedealt = manachange * -1
        return damagedealt

    def add_mana(self, amount):
        amount = max(amount, 0)
        return self.change_mana(amount)

    def change_mana(self, change):
        before_mana = self.mana
        self.mana += change
        if self.mana <= 0:
            self.mana = 0
        if self.mana > self.get_max_mana():
            self.mana = self.get_max_mana()

        manachange = self.mana - before_mana
        return manachange

    def is_friendly_to(self, unit):
        return self.side == unit.side

    def get_status_text(self):
        statustext = f"{self.name} ({self.weapon.name})".ljust(25)
        statustext += " - "
        if self.is_alive():
            statustext += f"HP: {self.health:.2f}/{self.get_max_health():.2f}".ljust(
                10)
            statustext += " / "
            statustext += f"MP: {self.mana:.2f}/{self.get_max_mana():.2f}".ljust(10)
            statustext += " / "
            statustext += f"ATB: {self.atb:.2f}".ljust(10)
        else:
            statustext += "DEAD"
        return statustext

    def is_ready_to_act(self):
        return self.atb >= 100.0


unit_counter = 1


def create_random_unit(side):
    unit = BattleUnit(f'{side} Unit {unit_counter}', side, CreateRandomWeapon())
    unit.randomize_attributes()
    unit.abilities.extend(get_primitive_skills_for_weapon(unit.weapon))
    trylimit = 100
    trycounter = 0
    primaryabilitycount = 3
    while (True):
        randomability = get_random_ability_for_weapon(unit.weapon)
        if randomability is not None:
            if not any(ability for ability in unit.abilities
                       if ability.skillbase == randomability.skillbase
                          and ability.element == randomability.element
                          and ability.skillsecondary == randomability.skillsecondary):
                unit.abilities.append(randomability)
                primaryabilitycount -= 1
                trycounter = 0
                if primaryabilitycount == 0:
                    break
                continue
        trycounter += 1
        if trycounter >= trylimit:
            break

    trycounter = 0
    reactionabilitycount = 1
    while (True):
        randomreaction = get_random_reaction_ability_for_weapon(unit.weapon)
        if randomreaction is not None:
            if not any(reaction for reaction in unit.abilities
                       if reaction.skillbase == randomreaction.skillbase):
                unit.abilities.append(randomreaction)
                reactionabilitycount -= 1
                trycounter = 0
                if reactionabilitycount == 0:
                    break
                continue
        trycounter += 1
        if trycounter >= trylimit:
            break
    unit.full_refresh()
    unit.atb = (random.random() * 40) + 10.0
    return unit
