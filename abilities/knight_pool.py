knight_abilities = [
    # Offensive (1x 1-star, 2x 2-star, 2x 3-star)
    {
        "name": "Slash",
        "type": "Offense",
        "description": "A quick melee attack dealing moderate damage.",
        "cooldown": 3,
        "damage": 120,
        "crit_chance": 0.12,
        "crit_multiplier": 1.5,
        "damage_amp": 0.20,
        "scaling_stat": "strength",
        "stackable": False,
        "stars": 1
    },
    {
        "name": "Shield Bash",
        "type": "Offense",
        "description": "Bashes enemy with shield, dealing damage and stunning.",
        "cooldown": 8,
        "damage": 160,
        "crit_chance": 0.10,
        "crit_multiplier": 1.6,
        "damage_amp": 0.25,
        "stun_duration": 2,
        "scaling_stat": "strength",
        "stackable": False,
        "stars": 2
    },
    {
        "name": "Cleave",
        "type": "Offense",
        "description": "Sweeping attack hitting multiple enemies.",
        "cooldown": 10,
        "damage": 140,
        "crit_chance": 0.13,
        "crit_multiplier": 1.7,
        "damage_amp": 0.30,
        "scaling_stat": "strength",
        "aoe_radius": 5,
        "stackable": False,
        "stars": 2
    },
    {
        "name": "Power Strike",
        "type": "Offense",
        "description": "Powerful heavy strike dealing high damage.",
        "cooldown": 12,
        "damage": 280,
        "crit_chance": 0.18,
        "crit_multiplier": 1.9,
        "damage_amp": 0.35,
        "scaling_stat": "strength",
        "stackable": False,
        "stars": 3
    },
    {
        "name": "Earth Shatter",
        "type": "Offense",
        "description": "Smashes the ground causing AoE damage and knockback.",
        "cooldown": 20,
        "damage": 350,
        "crit_chance": 0.20,
        "crit_multiplier": 2.1,
        "damage_amp": 0.40,
        "scaling_stat": "strength",
        "aoe_radius": 7,
        "stackable": False,
        "stars": 3
    },

    # Defensive (3 total)
    {
        "name": "Shield Wall",
        "type": "Defense",
        "description": "Increases block chance by 50% for 10 seconds.",
        "cooldown": 25,
        "block_chance_percent": 0.50,
        "duration": 10,
        "stackable": False
    },
    {
        "name": "Fortify",
        "type": "Defense",
        "description": "Increases armor by 40% for 12 seconds.",
        "cooldown": 20,
        "armor_percent": 0.40,
        "duration": 12,
        "stackable": False
    },
    {
        "name": "Last Stand",
        "type": "Defense",
        "description": "Reduces damage taken by 50% for 8 seconds.",
        "cooldown": 30,
        "damage_reduction_percent": 0.50,
        "duration": 8,
        "stackable": False
    },

    # Support (3 total)
    {
        "name": "Inspire",
        "type": "Support",
        "description": "Increases strength by 20% for 15 seconds.",
        "cooldown": 30,
        "strength_percent": 0.20,
        "duration": 15,
        "stackable": False
    },
    {
        "name": "Guardian's Blessing",
        "type": "Support",
        "description": "Heals 5% max health instantly.",
        "cooldown": 25,
        "heal_percent": 0.05,
        "stackable": False
    },
    {
        "name": "Battle Cry",
        "type": "Support",
        "description": "Increases attack speed by 15% for 10 seconds.",
        "cooldown": 20,
        "attack_speed_percent": 0.15,
        "duration": 10,
        "stackable": False
    }
]
