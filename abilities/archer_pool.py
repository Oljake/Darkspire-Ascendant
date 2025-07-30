archer_abilities = [
    # Offensive (1x 1-star, 2x 2-star, 2x 3-star)
    {
        "name": "Quick Shot",
        "type": "Offense",
        "description": "Shoots a quick arrow dealing moderate damage.",
        "cooldown": 3,
        "damage": 110,
        "crit_chance": 0.12,
        "crit_multiplier": 1.5,
        "damage_amp": 0.18,
        "scaling_stat": "dexterity",
        "stackable": False,
        "stars": 1
    },
    {
        "name": "Piercing Arrow",
        "type": "Offense",
        "description": "Shoots an arrow that pierces through enemies.",
        "cooldown": 7,
        "damage": 140,
        "crit_chance": 0.15,
        "crit_multiplier": 1.7,
        "damage_amp": 0.25,
        "scaling_stat": "dexterity",
        "stackable": False,
        "stars": 2
    },
    {
        "name": "Volley",
        "type": "Offense",
        "description": "Fires multiple arrows in an arc dealing AoE damage.",
        "cooldown": 10,
        "damage": 120,
        "crit_chance": 0.14,
        "crit_multiplier": 1.6,
        "damage_amp": 0.3,
        "scaling_stat": "dexterity",
        "aoe_radius": 6,
        "stackable": False,
        "stars": 2
    },
    {
        "name": "Explosive Arrow",
        "type": "Offense",
        "description": "Shoots an explosive arrow causing AoE damage.",
        "cooldown": 15,
        "damage": 260,
        "crit_chance": 0.18,
        "crit_multiplier": 1.9,
        "damage_amp": 0.35,
        "scaling_stat": "dexterity",
        "aoe_radius": 7,
        "stackable": False,
        "stars": 3
    },
    {
        "name": "Rain of Arrows",
        "type": "Offense",
        "description": "Calls down a rain of arrows hitting multiple enemies.",
        "cooldown": 22,
        "damage": 320,
        "crit_chance": 0.20,
        "crit_multiplier": 2.0,
        "damage_amp": 0.4,
        "scaling_stat": "dexterity",
        "aoe_radius": 8,
        "stackable": False,
        "stars": 3
    },

    # Defensive (3 total)
    {
        "name": "Evasive Roll",
        "type": "Defense",
        "description": "Quick roll increasing dodge chance by 30% for 3 seconds.",
        "cooldown": 15,
        "dodge_percent": 0.30,
        "duration": 3,
        "stackable": False
    },
    {
        "name": "Camouflage",
        "type": "Defense",
        "description": "Blend with the environment reducing aggro for 10 seconds.",
        "cooldown": 25,
        "aggro_reduction_percent": 0.50,
        "duration": 10,
        "stackable": False
    },
    {
        "name": "Quick Reflexes",
        "type": "Defense",
        "description": "Increases movement speed by 20% for 8 seconds.",
        "cooldown": 20,
        "move_speed_percent": 0.20,
        "duration": 8,
        "stackable": False
    },

    # Support (3 total)
    {
        "name": "Sharpshooter",
        "type": "Support",
        "description": "Increases critical hit chance by 15% for 12 seconds.",
        "cooldown": 30,
        "crit_chance_percent": 0.15,
        "duration": 12,
        "stackable": False
    },
    {
        "name": "Rapid Shot",
        "type": "Support",
        "description": "Increases attack speed by 20% for 10 seconds.",
        "cooldown": 25,
        "attack_speed_percent": 0.20,
        "duration": 10,
        "stackable": False
    },
    {
        "name": "Steady Aim",
        "type": "Support",
        "description": "Increases accuracy by 20% for 15 seconds.",
        "cooldown": 30,
        "accuracy_percent": 0.20,
        "duration": 15,
        "stackable": False
    }
]
