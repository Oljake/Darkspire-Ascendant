mysticmage_abilities = [
    # Offensive (1x 1-star, 2x 2-star, 2x 3-star)
    {
        "name": "Arcane Bolt",
        "type": "Offense",
        "description": "Shoots a bolt of pure arcane energy.",
        "cooldown": 4,
        "damage": 95,
        "crit_chance": 0.12,
        "crit_multiplier": 1.6,
        "damage_amp": 0.2,
        "scaling_stat": "intelligence",
        "stackable": False,
        "stars": 1
    },
    {
        "name": "Mystic Surge",
        "type": "Offense",
        "description": "Unleashes a surge of arcane energy damaging multiple foes.",
        "cooldown": 9,
        "damage": 135,
        "crit_chance": 0.14,
        "crit_multiplier": 1.7,
        "damage_amp": 0.28,
        "scaling_stat": "intelligence",
        "aoe_radius": 5,
        "stackable": False,
        "stars": 2
    },
    {
        "name": "Mind Pierce",
        "type": "Offense",
        "description": "Damages and silences an enemy for 3 seconds.",
        "cooldown": 8,
        "damage": 70,
        "crit_chance": 0.11,
        "crit_multiplier": 1.5,
        "damage_amp": 0.25,
        "silence_duration": 3,
        "scaling_stat": "intelligence",
        "stackable": False,
        "stars": 2
    },
    {
        "name": "Ethereal Blast",
        "type": "Offense",
        "description": "A powerful arcane blast that pierces through enemies.",
        "cooldown": 12,
        "damage": 270,
        "crit_chance": 0.18,
        "crit_multiplier": 1.85,
        "damage_amp": 0.35,
        "scaling_stat": "intelligence",
        "stackable": False,
        "stars": 3
    },
    {
        "name": "Astral Nova",
        "type": "Offense",
        "description": "Summons a nova of astral energy dealing massive AoE damage.",
        "cooldown": 20,
        "damage": 360,
        "crit_chance": 0.21,
        "crit_multiplier": 2.1,
        "damage_amp": 0.4,
        "scaling_stat": "intelligence",
        "aoe_radius": 7,
        "stackable": False,
        "stars": 3
    },

    # Defensive (3 total)
    {
        "name": "Mana Shield",
        "type": "Defense",
        "description": "Converts damage taken to mana loss for 10 seconds.",
        "cooldown": 20,
        "duration": 10,
        "mana_absorb_percent": 0.75,
        "stackable": False
    },
    {
        "name": "Mystic Veil",
        "type": "Defense",
        "description": "Reduces magic damage taken by 30% for 12 seconds.",
        "cooldown": 25,
        "magic_damage_reduction_percent": 0.30,
        "duration": 12,
        "stackable": False
    },
    {
        "name": "Ethereal Step",
        "type": "Defense",
        "description": "Quick teleport that increases evasion by 25% for 5 seconds.",
        "cooldown": 18,
        "evasion_percent": 0.25,
        "duration": 5,
        "stackable": False
    },

    # Support (3 total)
    {
        "name": "Arcane Focus",
        "type": "Support",
        "description": "Increases mana regeneration by 20% for 15 seconds.",
        "cooldown": 30,
        "mana_regen_percent": 0.20,
        "duration": 15,
        "stackable": False
    },
    {
        "name": "Concentration",
        "type": "Support",
        "description": "Increases spell critical chance by 12% for 12 seconds.",
        "cooldown": 25,
        "crit_chance_percent": 0.12,
        "duration": 12,
        "stackable": False
    },
    {
        "name": "Focus Aura",
        "type": "Support",
        "description": "Increases cast speed by 18% for 10 seconds.",
        "cooldown": 30,
        "cast_speed_percent": 0.18,
        "duration": 10,
        "stackable": False
    }
]
