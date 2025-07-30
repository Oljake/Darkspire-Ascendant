firemage_abilities = [
    # Offensive (1x 1-star, 2x 2-star, 2x 3-star)
    {
        "name": "Fireball",
        "type": "Offense",
        "description": "Launches a fireball dealing moderate damage.",
        "cooldown": 4,
        "damage": 100,
        "crit_chance": 0.1,
        "crit_multiplier": 1.5,
        "damage_amp": 0.2,
        "scaling_stat": "intelligence",
        "stackable": False,
        "stars": 1
    },
    {
        "name": "Flame Wave",
        "type": "Offense",
        "description": "Sends a wave of fire dealing AoE damage.",
        "cooldown": 8,
        "damage": 140,
        "crit_chance": 0.12,
        "crit_multiplier": 1.6,
        "damage_amp": 0.25,
        "scaling_stat": "intelligence",
        "aoe_radius": 5,
        "stackable": False,
        "stars": 2
    },
    {
        "name": "Ignite",
        "type": "Offense",
        "description": "Sets target on fire causing damage over time.",
        "cooldown": 6,
        "damage": 30,
        "dot_damage": 20,
        "dot_duration": 6,
        "crit_chance": 0.1,
        "crit_multiplier": 1.4,
        "damage_amp": 0.2,
        "scaling_stat": "intelligence",
        "stackable": True,
        "stars": 2
    },
    {
        "name": "Greater Fireball",
        "type": "Offense",
        "description": "Launches a large fireball dealing high damage.",
        "cooldown": 10,
        "damage": 250,
        "crit_chance": 0.15,
        "crit_multiplier": 1.8,
        "damage_amp": 0.35,
        "scaling_stat": "intelligence",
        "stackable": False,
        "stars": 3
    },
    {
        "name": "Meteor Strike",
        "type": "Offense",
        "description": "Calls down a meteor causing massive AoE damage.",
        "cooldown": 18,
        "damage": 350,
        "crit_chance": 0.2,
        "crit_multiplier": 2.0,
        "damage_amp": 0.4,
        "scaling_stat": "intelligence",
        "aoe_radius": 7,
        "stackable": False,
        "stars": 3
    },

    # Defensive (3 total)
    {
        "name": "Flame Shield",
        "type": "Defense",
        "description": "Creates a shield that absorbs damage and burns attackers.",
        "cooldown": 20,
        "shield_amount": 300,
        "reflect_percent": 0.15,
        "duration": 10,
        "stackable": False
    },
    {
        "name": "Heat Barrier",
        "type": "Defense",
        "description": "Increases fire resistance by 30% for 12 seconds.",
        "cooldown": 25,
        "fire_resist_percent": 0.30,
        "duration": 12,
        "stackable": False
    },
    {
        "name": "Phoenix Rebirth",
        "type": "Defense",
        "description": "Revives player with 30% health upon death (1 min cooldown).",
        "cooldown": 60,
        "revive_health_percent": 0.3,
        "stackable": False
    },

    # Support (3 total)
    {
        "name": "Ember's Blessing",
        "type": "Support",
        "description": "Increases fire damage by 15% for 15 seconds.",
        "cooldown": 30,
        "damage_amp_percent": 0.15,
        "duration": 15,
        "stackable": False
    },
    {
        "name": "Quickened Flames",
        "type": "Support",
        "description": "Increases cast speed by 20% for 12 seconds.",
        "cooldown": 25,
        "cast_speed_percent": 0.20,
        "duration": 12,
        "stackable": False
    },
    {
        "name": "Vital Spark",
        "type": "Support",
        "description": "Regenerates 3% max health per second for 8 seconds.",
        "cooldown": 35,
        "health_regen_percent": 0.03,
        "duration": 8,
        "stackable": False
    }
]
