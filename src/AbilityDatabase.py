primitive_skills = {
    "Attack": {
        "UsableWithWeaponCategory": ["Melee"],
        "Category":
            "Primary",
        "TargetType":
            "Enemy",
        "TargetScope":
            "Single",
        "TargetRange":
            "Melee",
        "Reactable":
            False,
        "Effects": [{
            "Type": "Damage",
            "Amount": 8.75,
            "ElementWeight": {
                "WeaponElement": 1.0,
            },
            "Scale": {
                "WeaponScale": 0.01
            }
        }],
        "AtbCost":
            40,
    },
    "Shoot": {
        "UsableWithWeaponCategory": ["Ranged"],
        "Category":
            "Primary",
        "TargetType":
            "Enemy",
        "TargetScope":
            "Single",
        "TargetRange":
            "Any",
        "Reactable":
            False,
        "Effects": [{
            "Type": "Damage",
            "Amount": 11.7,
            "ElementWeight": {
                "WeaponElement": 1.0,
            },
            "Scale": {
                "WeaponScale": 0.01
            }
        }],
        "AtbCost":
            45,
    },
    "Sneak Attack": {
        "UsableWithWeaponCategory": ["MeleeAgile"],
        "Category":
            "Primary",
        "TargetType":
            "Enemy",
        "TargetScope":
            "Single",
        "TargetRange":
            "Any",
        "Reactable":
            False,
        "Effects": [{
            "Type": "Damage",
            "Amount": 14.5,
            "ElementWeight": {
                "WeaponElement": 1.0,
            },
            "Scale": {
                "WeaponScale": 0.01
            }
        }],
        "AtbCost":
            50,
    },
    "Shock": {
        "UsableWithWeaponCategory": ["Elemental"],
        "Category":
            "Primary",
        "TargetType":
            "Enemy",
        "TargetScope":
            "Single",
        "TargetRange":
            "Any",
        "Reactable":
            False,
        "Effects": [{
            "Type": "Damage",
            "Amount": 11.7,
            "ElementWeight": {
                "WeaponElement": 1.0,
            },
            "Scale": {
                "WeaponScale": 0.01
            }
        }],
        "AtbCost":
            50,
    },
    "Beacon": {
        "UsableWithWeaponCategory": ["Spiritual"],
        "Category":
            "Primary",
        "TargetType":
            "Enemy",
        "TargetScope":
            "Single",
        "TargetRange":
            "Any",
        "Reactable":
            False,
        "Effects": [{
            "Type": "Damage",
            "Amount": 10,
            "ElementWeight": {
                "WeaponElement": 1.0,
            },
            "Scale": {
                "WeaponScale": 0.01
            }
        }],
        "AtbCost":
            42,
    },
    "Parry": {
        "UsableWithWeaponCategory": ["Melee", "MeleeAgile"],
        "Category":
            "Guard",
        "Effects": [{
            "Type": "AddModifier",
            "Modifier": {
                "Type": "DamageTaken",
                "Multiplier": 0.75
            }
        }],
        "AtbCost":
            20,
    },
    "Mana Shield": {
        "UsableWithWeaponCategory": ["Spiritual", "Elemental"],
        "Category":
            "Guard",
        "Effects": [{
            "Type": "AddModifier",
            "Modifier": {
                "Type": "DamageTaken",
                "Multiplier": 0.5
            }
        }],
        "ManaCost":
            5,
        "AtbCost":
            5,
    },
    "Deflect": {
        "UsableWithWeaponCategory": ["Ranged", "MeleeAgile"],
        "Category":
            "Guard",
        "Effects": [{
            "Type": "AddModifier",
            "Modifier": {
                "Type": "DamageTaken",
                "Amount": -3,
                "Multiplier": 0.8
            }
        }],
        "AtbCost":
            10,
    }
}

skill_bases = {
    "Bolt": {
        "UsableWithWeaponCategory": ["Melee", "Elemental"],
        "Category":
            "Primary",
        "TargetType":
            "Enemy",
        "TargetScope":
            "Single",
        "TargetRange":
            "Any",
        "Effects": [{
            "Type": "Damage",
            "Amount": (16.8 * 3),
            "ElementWeight": {
                "AbilityElement": 1.0,
            },
            "Scale": {
                "ElementScale": 0.002,
                "int": 0.008
            }
        }],
        "ManaCost":
            5,
        "AtbCost":
            40,
        "ElementNameOverrides": {
            "Physical": "Steel",
            "Water": "Aqua",
            "Earth": "Rock",
            "Air": "Wind",
            "Light": "Holy",
            "Dark": "Shadow",
            "Void": "Chaos"
        }
    },
    "Infusion": {
        "UsableWithWeaponCategory": ["Spiritual", "Elemental"],
        "Category":
            "Primary",
        "TargetType":
            "Enemy",
        "TargetScope":
            "Single",
        "TargetRange":
            "Any",
        "Effects": [{
            "Type": "Damage",
            "Amount": (25 * 3),
            "ElementWeight": {
                "AbilityElement": 1.0,
            },
            "Scale": {
                "WeaponScale": 0.01
            }
        }],
        "ManaCost":
            10,
        "AtbCost":
            50,
        "ElementNameOverrides": {
            "Physical": "Energy",
            "Void": "Chaos"
        }
    },
    "Missile": {
        "UsableWithWeaponCategory": ["Ranged", "Spiritual"],
        "Category":
            "Primary",
        "TargetType":
            "Enemy",
        "TargetScope":
            "Single",
        "TargetRange":
            "Any",
        "Effects": [{
            "Type": "Damage",
            "Amount": (22 * 3),
            "ElementWeight": {
                "AbilityElement": 1.0,
            },
            "Scale": {
                "WeaponScale": 0.005,
                "ElementScale": 0.005
            }
        }],
        "ManaCost":
            5,
        "AtbCost":
            50,
        "ElementNameOverrides": {
            "Physical": "",
            "Fire": "Burning",
            "Water": "Aqua",
            "Earth": "Rock",
            "Air": "Wind",
            "Light": "Holy",
            "Void": "Chaos"
        }
    },
    "Slash": {
        "UsableWithWeaponCategory": ["MeleeAgile", "Melee"],
        "Category":
            "Primary",
        "TargetType":
            "Enemy",
        "TargetScope":
            "Single",
        "TargetRange":
            "Any",
        "Effects": [{
            "Type": "Damage",
            "Amount": (22 * 3),
            "ElementWeight": {
                "AbilityElement": 1.0,
            },
            "Scale": {
                "WeaponScale": 0.008,
                "ElementScale": 0.002
            }
        }],
        "ManaCost":
            5,
        "AtbCost":
            50,
        "ElementNameOverrides": {
            "Physical": "",
            "Fire": "Burning",
            "Water": "Aqua",
            "Earth": "Granite",
            "Air": "Wind",
            "Light": "Holy",
            "Dark": "Shadow",
            "Void": "Chaos"
        }
    },
    "Strike": {
        "UsableWithWeaponCategory": ["Melee", "MeleeAgile"],
        "Category":
            "Primary",
        "TargetType":
            "Enemy",
        "TargetScope":
            "Single",
        "TargetRange":
            "Melee",
        "Effects": [{
            "Type": "Damage",
            "Amount": (21.5 * 3),
            "ElementWeight": {
                "AbilityElement": 1.0,
            },
            "Scale": {
                "WeaponScale": 0.008,
                "ElementScale": 0.002
            }
        }],
        "ManaCost":
            5,
        "AtbCost":
            50,
        "ElementNameOverrides": {
            "Physical": "",
            "Fire": "Burning",
            "Water": "Aqua",
            "Earth": "Rock",
            "Air": "Wind",
            "Light": "Holy",
            "Void": "Chaos"
        }
    },
    "Blessing": {
        "UsableWithWeaponElement": ["Fire", "Water", "Light", "Dark", "Void"],
        "LimitElements": ["Fire", "Water", "Light", "Dark", "Void"],
        "Category": "Primary",
        "TargetType": "Friendly",
        "TargetScope": "Single",
        "TargetRange": "Any",
        "Effects": [{
            "Type": "Heal",
            "Amount": (6 * 3),
            "Scale": {
                "spi": 0.01
            }
        }],
        "ManaCost": 15,
        "AtbCost": 50,
        "ElementNameOverrides": {
            "Water": "Ocean",
            "Light": "Holy",
        }
    },
    "Circle": {
        "UsableWithWeaponElement": ["Water", "Light", "Dark", "Void"],
        "LimitElements": ["Water", "Light", "Dark", "Void"],
        "Category":
            "Primary",
        "TargetType":
            "Friendly",
        "TargetScope":
            "All",
        "TargetRange":
            "Any",
        "Effects": [{
            "Type": "Heal",
            "Amount": (8.25 * 3),
            "Scale": {
                "spi": 0.01
            },
            "DivideLimit": 2
        }],
        "ManaCost":
            25,
        "AtbCost":
            55,
        "ElementNameOverrides": {
            "Water": "Aqua",
            "Light": "Holy",
        }
    }
}

reaction_skills = {
    "Warm Up": {
        "UsableWithWeaponElement": ["Fire"],
        "Category":
            "Assist",
        "SubCategory":
            "Empower",
        "TargetType":
            "Friendly",
        "TargetScope":
            "Single",
        "TargetRange":
            "Any",
        "CanTargetReaction":
            False,
        "RequireEffectUserAny": ["Damage"],
        "Effects": [{
            "Type": "AddModifier",
            "Modifier": {
                "Type": "Damage",
                "Multiplier": 1.435
            }
        }],
        "ManaCost":
            0,
        "AtbCost":
            15,
    },
    "Serenity": {
        "UsableWithWeaponElement": ["Water"],
        "Category":
            "Assist",
        "SubCategory":
            "Empower",
        "TargetType":
            "Friendly",
        "TargetScope":
            "Single",
        "TargetRange":
            "Any",
        "CanTargetGuard":
            True,
        "RequireEffectTargetAny": ["Heal"],
        "Effects": [{
            "Type": "AddModifier",
            "Modifier": {
                "Type": "HealReceived",
                "Multiplier": 1.45
            }
        }],
        "ManaCost":
            2,
        "AtbCost":
            10,
    },
    "Desecrate": {
        "UsableWithWeaponElement": ["Dark"],
        "Category":
            "Interrupt",
        "SubCategory":
            "Disrupt",
        "TargetType":
            "Enemy",
        "TargetScope":
            "Single",
        "TargetRange":
            "Any",
        "CanTargetGuard":
            True,
        "RequireEffectTargetAny": ["Heal"],
        "Effects": [{
            "Type": "AddModifier",
            "Modifier": {
                "Type": "HealReceived",
                "Multiplier": 0.65
            }
        }],
        "ManaCost":
            3,
        "AtbCost":
            10,
    },
    "Rock Shell": {
        "UsableWithWeaponElement": ["Earth"],
        "Category":
            "Assist",
        "SubCategory":
            "Protect",
        "TargetType":
            "Friendly Except Self",
        "TargetScope":
            "Single",
        "TargetRange":
            "Any",
        "CanTargetGuard":
            True,
        "RequireEffectTargetAny": ["Damage"],
        "Effects": [{
            "Type": "AddModifier",
            "Modifier": {
                "Type": "DamageTaken",
                "Multiplier": 0.67
            }
        }],
        "ManaCost":
            2,
        "AtbCost":
            15,
    },
    "War Cry": {
        "UsableWithWeaponElement": ["Physical"],
        "Category":
            "Assist",
        "SubCategory":
            "Empower",
        "TargetType":
            "Friendly Except Self",
        "TargetScope":
            "All",
        "TargetRange":
            "Any",
        "Priority":
            1,
        "CanTargetGuard":
            True,
        "RequiresActingAlly":
            True,
        "Effects": [{
            "Type": "AddModifier",
            "Modifier": {
                "Type": "AtbCost",
                "Multiplier": 0.82
            }
        }],
        "ManaCost":
            15,
        "AtbCost":
            20,
    },
    "Wind Shear": {
        "UsableWithWeaponElement": ["Wind"],
        "Category":
            "Interrupt",
        "SubCategory":
            "Disrupt",
        "TargetType":
            "Enemy",
        "TargetScope":
            "All",
        "TargetRange":
            "Any",
        "Priority":
            1,
        "CanTargetGuard":
            True,
        "RequiresActingEnemy":
            True,
        "Effects": [{
            "Type": "AddModifier",
            "Modifier": {
                "Type": "AtbCost",
                "Multiplier": 1.225
            }
        }],
        "ManaCost":
            10,
        "AtbCost":
            20,
    },
    "Relief": {
        "UsableWithWeaponElement": ["Light"],
        "Category": "Assist",
        "SubCategory": "Protect",
        "TargetType": "Friendly Except Self",
        "TargetScope": "Single",
        "TargetRange": "Range",
        "CanTargetGuard": True,
        "Priority": -1,
        "RequireEffectTargetAny": ["Damage"],
        "Effects": [{
            "Type": "Heal",
            "Amount": (0.87 * 2),
            "Scale": {
                "spi": 0.01
            }
        }],
        "ManaCost": 5,
        "AtbCost": 20,
    },
    "Slam": {
        "UsableWithWeaponCategory": ["Melee"],
        "Category":
            "Interrupt",
        "SubCategory":
            "Interrupt",
        "TargetType":
            "Enemy",
        "TargetScope":
            "Single",
        "TargetRange":
            "Melee",
        "RequiresTargetActed":
            True,
        "Effects": [{
            "Type": "Damage",
            "Amount": (4 * 2),
            "ElementWeight": {
                "WeaponElement": 1.0,
            },
            "Scale": {
                "WeaponScale": 0.01
            }
        }, {
            "Type": "AddModifier",
            "Modifier": {
                "Type": "AtbCost",
                "Multiplier": 1.3
            }
        }],
        "ManaCost":
            10,
        "AtbCost":
            20,
    },
    "Opportunity Shot": {
        "UsableWithWeaponCategory": ["Ranged"],
        "Category":
            "Interrupt",
        "SubCategory":
            "Interrupt",
        "TargetType":
            "Enemy",
        "TargetScope":
            "Single",
        "TargetRange":
            "Range",
        "CanTargetPrimary":
            False,
        "RequiresTargetActed":
            True,
        "Effects": [{
            "Type": "Damage",
            "Amount": (8.1 * 2),
            "ElementWeight": {
                "WeaponElement": 1.0,
            },
            "Scale": {
                "WeaponScale": 0.01
            }
        }],
        "ManaCost":
            2,
        "AtbCost":
            25,
    },
    "Expose": {
        "UsableWithWeaponCategory": ["MeleeAgile"],
        "Category":
            "Interrupt",
        "SubCategory":
            "Disrupt",
        "TargetType":
            "Enemy",
        "TargetScope":
            "Single",
        "TargetRange":
            "Range",
        "CanTargetGuard":
            True,
        "RequireEffectTargetAny": ["Damage"],
        "Effects": [{
            "Type": "AddModifier",
            "Modifier": {
                "Type": "DamageTaken",
                "Multiplier": 1.36
            }
        }],
        "ManaCost":
            0,
        "AtbCost":
            10,
    },
    "Barrier": {
        "UsableWithWeaponCategory": ["Spiritual"],
        "Category":
            "Assist",
        "SubCategory":
            "Protect",
        "TargetType":
            "Friendly Except Self",
        "TargetScope":
            "Single",
        "TargetRange":
            "Range",
        "CanTargetGuard":
            True,
        "RequireEffectTargetAny": ["Damage"],
        "Effects": [{
            "Type": "AddModifier",
            "Modifier": {
                "Type": "DamageTaken",
                "Amount": (-2.77 * 2),
                "Scale": {
                    "WeaponScale": 0.01
                }
            }
        }],
        "ManaCost":
            5,
        "AtbCost":
            15,
    },
    "Enchant": {
        "UsableWithWeaponCategory": ["Elemental"],
        "Category":
            "Assist",
        "SubCategory":
            "Empower",
        "TargetType":
            "Friendly Except Self",
        "TargetScope":
            "Single",
        "TargetRange":
            "Range",
        "RequireEffectUserAny": ["Damage"],
        "Effects": [{
            "Type": "AddModifier",
            "Modifier": {
                "Type": "Damage",
                "Amount": (7.4 * 2),
                "Scale": {
                    "WeaponScale": 0.01
                }
            }
        }],
        "ManaCost":
            5,
        "AtbCost":
            30,
    },
}

skill_elemental_effects = {
    "Physical": {
        "DefaultScaleModifier": 0.8,
        "AddedScale": {
            "str": 0.002
        },
    },
    "Fire": {
        "DefaultScaleModifier": 0.8,
        "AddedScale": {
            "int": 0.002
        }
    },
    "Water": {
        "DefaultScaleModifier": 0.8,
        "AddedScale": {
            "int": 0.002
        }
    },
    "Earth": {
        "DefaultScaleModifier": 0.8,
        "AddedScale": {
            "int": 0.002
        }
    },
    "Wind": {
        "DefaultScaleModifier": 0.8,
        "AddedScale": {
            "int": 0.002
        }
    },
    "Light": {
        "DefaultScaleModifier": 0.8,
        "AddedScale": {
            "spi": 0.002
        }
    },
    "Dark": {
        "DefaultScaleModifier": 0.8,
        "AddedScale": {
            "spi": 0.002
        }
    },
    "Void": {}
}

skill_secondary_effects = {
    "Powerful": {
        "AppliesTo": ["Bolt", "Infusion", "Missile", "Slash", "Strike"],
        "Modifiers": [
            {
                "Type": "Damage",
                "Multiplier": 1.3
            },
            {
                "Type": "Heal",
                "Multiplier": 1.3
            },
            {
                "Type": "AtbCost",
                "Multiplier": 1.10
            },
        ]
    },
    "Greater": {  # should not apply to moves below 10 mana cost
        "AppliesTo": ["Infusion", "Blessing", "Circle"],
        "Modifiers": [
            {
                "Type": "Damage",
                "Multiplier": 1.22
            },
            {
                "Type": "Heal",
                "Multiplier": 1.22
            },
            {
                "Type": "ManaCost",
                "Multiplier": 1.2
            },
        ]
    },
    "Swift": {
        "AppliesTo":
            ["Bolt", "Infusion", "Slash", "Strike", "Blessing", "Circle"],
        "Modifiers": [
            {
                "Type": "Damage",
                "Multiplier": 0.87
            },
            {
                "Type": "Heal",
                "Multiplier": 0.87
            },
            {
                "Type": "AtbCost",
                "Multiplier": 0.8
            },
        ]
    },
    "Lesser": {  # should not apply to moves below 10 mana cost
        "AppliesTo": ["Infusion", "Blessing", "Circle"],
        "Modifiers": [
            {
                "Type": "Damage",
                "Multiplier": 1.05
            },
            {
                "Type": "Heal",
                "Multiplier": 1.05
            },
            {
                "Type": "ManaCost",
                "Multiplier": 0.5
            },
        ]
    },
    "Crushing": {
        "AppliesTo": ["Bolt", "Infusion", "Strike"],
        "Modifiers": [{
            "Type": "ManaCost",
            "Amount": 5
        }],
        "Effects": [{
            "Type": "AtbLoss",
            "Amount": 7.5,
            "DivideLimit": 1
        }],
    },
    "Motivating": {
        "AppliesTo": ["Blessing", "Circle"],
        "Modifiers": [{
            "Type": "ManaCost",
            "Amount": 5
        }],
        "Effects": [{
            "Type": "AtbGain",
            "Amount": 3.2,
            "DivideLimit": 1
        }],
    },
    "Invigorating": {
        "AppliesTo": ["Bolt", "Infusion", "Missile", "Slash", "Strike"],
        "Modifiers": [{
            "Type": "AtbCost",
            "Multiplier": 1.1
        }, {
            "Type": "ManaCost",
            "Multiplier": 1.1
        }],
        "Effects": [{
            "TargetType": "Self",
            "TargetScope": "Single",
            "TargetRange": "Any",
            "Type": "Heal",
            "Amount": 3,
            "Scale": {
                "spi": 0.01
            }
        }],
    }
}
