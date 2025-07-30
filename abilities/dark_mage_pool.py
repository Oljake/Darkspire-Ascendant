darkmage_abilities = [
    # Offensive (1x 1-star, 2x 2-star, 2x 3-star)
    {
        "name": "Shadow Bolt",
        "type": "Offense",
        "description": "Fires a bolt of dark energy.",
        "cooldown": 5,
        "damage": 90,
        "crit_chance": 0.1,
        "crit_multiplier": 1.5,
        "damage_amp": 0.2,
        "scaling_stat": "intelligence",
        "stackable": False,
        "stars": 1
    },
    {
        "name": "Dark Pulse",
        "type": "Offense",
        "description": "Emits a pulse of dark energy damaging enemies around you.",
        "cooldown": 9,
        "damage": 130,
        "crit_chance": 0.13,
        "crit_multiplier": 1.7,
        "damage_amp": 0.3,
        "scaling_stat": "intelligence",
        "aoe_radius": 6,
        "stackable": False,
        "stars": 2
    },
    {
        "name": "Corrupting Touch",
        "type": "Offense",
        "description": "Inflicts target with corruption dealing damage over time.",
        "cooldown": 7,
        "damage": 40,
        "dot_damage": 25,
        "dot_duration": 7,
        "crit_chance": 0.11,
        "crit_multiplier": 1.5,
        "damage_amp": 0.25,
        "scaling_stat": "intelligence",
        "stackable": True,
        "stars": 2
    },
    {
        "name": "Shadowflame",
        "type": "Offense",
        "description": "Burns enemies with shadow fire, causing heavy damage.",
        "cooldown": 11,
        "damage": 270,
        "crit_chance": 0.18,
        "crit_multiplier": 1.9,
        "damage_amp": 0.4,
        "scaling_stat": "intelligence",
        "stackable": False,
        "stars": 3
    },
    {
        "name": "Nether Blast",
        "type": "Offense",
        "description": "Explodes dark energy dealing massive AoE damage.",
        "cooldown": 20,
        "damage": 360,
        "crit_chance": 0.22,
        "crit_multiplier": 2.2,
        "damage_amp": 0.45,
        "scaling_stat": "intelligence",
        "aoe_radius": 8,
        "stackable": False,
        "stars": 3
    },

    # Defensive (3 total)
    {
        "name": "Shadow Veil",
        "type": "Defense",
        "description": "Grants invisibility for 6 seconds.",
        "cooldown": 30,
        "duration": 6,
        "stackable": False
    },
    {
        "name": "Dark Pact",
        "type": "Defense",
        "description": "Absorbs damage equal to 20% of max health for 12 seconds.",
        "cooldown": 25,
        "shield_amount_percent": 0.20,
        "duration": 12,
        "stackable": False
    },
    {
        "name": "Cursed Armor",
        "type": "Defense",
        "description": "Increases damage reduction by 35% for 10 seconds.",
        "cooldown": 30,
        "damage_reduction_percent": 0.35,
        "duration": 10,
        "stackable": False
    },

    # Support (3 total)
    {
        "name": "Soul Link",
        "type": "Support",
        "description": "Shares 20% of damage taken with a summoned shadow for 15 seconds.",
        "cooldown": 40,
        "damage_share_percent": 0.20,
        "duration": 15,
        "stackable": False
    },
    {
        "name": "Dark Empowerment",
        "type": "Support",
        "description": "Increases dark damage dealt by 18% for 15 seconds.",
        "cooldown": 30,
        "damage_amp_percent": 0.18,
        "duration": 15,
        "stackable": False
    },
    {
        "name": "Umbral Recovery",
        "type": "Support",
        "description": "Restores 4% max health per second for 6 seconds.",
        "cooldown": 35,
        "health_regen_percent": 0.04,
        "duration": 6,
        "stackable": False
    }
]
