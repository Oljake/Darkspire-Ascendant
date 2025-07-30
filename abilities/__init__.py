ability_pool = {

    "fire_mage": [
        # Offensive abilities (1x 1-star, 2x 2-star, 2x 3-star)
        {
            "name": "Firebolt",  # 1-star
            "type": "Offense",
            "description": "Quick fire projectile causing light burn.",
            "rarity": 1,
            "cooldown": 2,
            "damage": 35,
            "crit_chance": 0.1,
            "crit_multiplier": 1.5,
            "damage_amp": 0.15,
            "scaling_stat": "Intelligence",
            "tags": ["Projectile", "Fire"],
            "stackable": False
        },
        {
            "name": "Flame Wave",  # 2-star
            "type": "Offense",
            "description": "Cone of fire that knocks back and burns enemies.",
            "rarity": 2,
            "cooldown": 6,
            "damage": 70,
            "crit_chance": 0.15,
            "crit_multiplier": 1.6,
            "damage_amp": 0.2,
            "scaling_stat": "Intelligence",
            "tags": ["AoE", "Fire", "Knockback"],
            "stackable": False
        },
        {
            "name": "Scorching Ring",  # 2-star
            "type": "Offense",
            "description": "Burst of fire damages all nearby enemies.",
            "rarity": 2,
            "cooldown": 8,
            "damage": 65,
            "crit_chance": 0.15,
            "crit_multiplier": 1.6,
            "damage_amp": 0.18,
            "scaling_stat": "Intelligence",
            "tags": ["AoE", "Fire"],
            "stackable": False
        },
        {
            "name": "Greater Fireball",  # 3-star
            "type": "Offense",
            "description": "Charged fire orb explodes for heavy AoE damage.",
            "rarity": 3,
            "cooldown": 12,
            "damage": 140,
            "crit_chance": 0.2,
            "crit_multiplier": 1.75,
            "damage_amp": 0.25,
            "scaling_stat": "Intelligence",
            "tags": ["AoE", "Fire"],
            "stackable": False
        },
        {
            "name": "Meteor Drop",  # 3-star
            "type": "Offense",
            "description": "Summons a meteor that deals massive AoE fire damage.",
            "rarity": 3,
            "cooldown": 18,
            "damage": 180,
            "crit_chance": 0.25,
            "crit_multiplier": 1.8,
            "damage_amp": 0.3,
            "scaling_stat": "Intelligence",
            "tags": ["AoE", "Fire", "Impact"],
            "stackable": False
        },

        # Defensive abilities
        {
            "name": "Flame Shield",
            "type": "Defense",
            "description": "Reduces incoming damage by 25% and burns melee attackers.",
            "cooldown": 15,
            "effect": {"damage_reduction": 0.25, "burn_on_hit": True, "duration": 8},
            "stackable": False
        },
        {
            "name": "Cauterize",
            "type": "Defense",
            "description": "Instantly removes debuffs and restores 20% health.",
            "cooldown": 20,
            "effect": {"cleanse": True, "heal_percent": 0.2},
            "stackable": False
        },
        {
            "name": "Molten Armor",
            "type": "Defense",
            "description": "Increases defense by 20% and burns attackers on hit.",
            "cooldown": 25,
            "effect": {"defense_buff": 0.2, "burn_on_hit": True, "duration": 10},
            "stackable": False
        },

        # Support abilities (only buff you)
        {
            "name": "Ember Heart",
            "type": "Support",
            "description": "Increases fire damage by 20% for 12 seconds.",
            "cooldown": 30,
            "effect": {"fire_damage_buff": 0.2, "duration": 12},
            "stackable": False
        },
        {
            "name": "Pyro Conduit",
            "type": "Support",
            "description": "Each hit has a 30% chance to ignite enemies for 5 seconds.",
            "cooldown": 35,
            "effect": {"ignite_chance": 0.3, "ignite_duration": 5},
            "stackable": False
        },
        {
            "name": "Blazing Trail",
            "type": "Support",
            "description": "Increase movement speed by 15% when moving through fire.",
            "cooldown": 40,
            "effect": {"move_speed_buff": 0.15, "duration": 15},
            "stackable": False
        }
    ],


    "dark_mage": [
        # Offensive
        {
            "name": "Shadow Spike",  # 1-star
            "type": "Offense",
            "description": "Fast projectile causing bleed over time.",
            "rarity": 1,
            "cooldown": 2,
            "damage": 30,
            "crit_chance": 0.12,
            "crit_multiplier": 1.5,
            "damage_amp": 0.14,
            "scaling_stat": "Intelligence",
            "tags": ["Projectile", "Bleed", "Dark"],
            "stackable": False
        },
        {
            "name": "Spectral Blades",  # 2-star
            "type": "Offense",
            "description": "Summons homing blades that slice enemies.",
            "rarity": 2,
            "cooldown": 7,
            "damage": 60,
            "crit_chance": 0.15,
            "crit_multiplier": 1.6,
            "damage_amp": 0.19,
            "scaling_stat": "Intelligence",
            "tags": ["Homing", "Dark"],
            "stackable": False
        },
        {
            "name": "Necrotic Nova",  # 2-star
            "type": "Offense",
            "description": "AoE damage that applies decay debuff.",
            "rarity": 2,
            "cooldown": 9,
            "damage": 65,
            "crit_chance": 0.15,
            "crit_multiplier": 1.6,
            "damage_amp": 0.2,
            "scaling_stat": "Intelligence",
            "tags": ["AoE", "Decay", "Dark"],
            "stackable": False
        },
        {
            "name": "Abyssal Storm",  # 3-star
            "type": "Offense",
            "description": "Damaging storm that weakens enemy healing.",
            "rarity": 3,
            "cooldown": 14,
            "damage": 140,
            "crit_chance": 0.18,
            "crit_multiplier": 1.75,
            "damage_amp": 0.25,
            "scaling_stat": "Intelligence",
            "tags": ["AoE", "Dark", "Debuff"],
            "stackable": False
        },
        {
            "name": "Soul Eruption",  # 3-star
            "type": "Offense",
            "description": "Detonates debuffed enemies for extra AoE damage.",
            "rarity": 3,
            "cooldown": 16,
            "damage": 170,
            "crit_chance": 0.22,
            "crit_multiplier": 1.8,
            "damage_amp": 0.3,
            "scaling_stat": "Intelligence",
            "tags": ["AoE", "Dark", "Explosion"],
            "stackable": False
        },

        # Defensive
        {
            "name": "Veil of Shadows",
            "type": "Defense",
            "description": "Reduces visibility and chance to be hit by 20% for 8 seconds.",
            "cooldown": 12,
            "effect": {"evasion_buff": 0.2, "duration": 8},
            "stackable": False
        },
        {
            "name": "Dark Armor",
            "type": "Defense",
            "description": "Reduces damage taken by 25% and reflects 10% damage back for 10 seconds.",
            "cooldown": 18,
            "effect": {"damage_reduction": 0.25, "reflect_percent": 0.1, "duration": 10},
            "stackable": False
        },
        {
            "name": "Fade Step",
            "type": "Defense",
            "description": "Blink a short distance, avoiding damage briefly.",
            "cooldown": 10,
            "effect": {"invulnerability_duration": 1, "blink_distance": 8},
            "stackable": False
        },

        # Support
        {
            "name": "Soul Leech",
            "type": "Support",
            "description": "Drain 15% of damage dealt as health for 12 seconds.",
            "cooldown": 20,
            "effect": {"lifesteal": 0.15, "duration": 12},
            "stackable": False
        },
        {
            "name": "Dark Pact",
            "type": "Support",
            "description": "Sacrifice 10% HP to boost damage by 30% for 10 seconds.",
            "cooldown": 25,
            "effect": {"hp_cost": 0.1, "damage_buff": 0.3, "duration": 10},
            "stackable": False
        },
        {
            "name": "Mark of the End",
            "type": "Support",
            "description": "Mark enemy, increasing damage taken by 20% for 15 seconds.",
            "cooldown": 30,
            "effect": {"enemy_damage_taken_increase": 0.2, "duration": 15},
            "stackable": False
        }
    ],


    "mystic_mage": [
        # Offensive
        {
            "name": "Arcane Missile",  # 1-star
            "type": "Offense",
            "description": "Shoots a magic missile with moderate magic damage.",
            "rarity": 1,
            "cooldown": 2,
            "damage": 40,
            "crit_chance": 0.1,
            "crit_multiplier": 1.5,
            "damage_amp": 0.17,
            "scaling_stat": "Intelligence",
            "tags": ["Projectile", "Arcane"],
            "stackable": False
        },
        {
            "name": "Mystic Wave",  # 2-star
            "type": "Offense",
            "description": "Arcane energy wave that damages and silences enemies for 2 seconds.",
            "rarity": 2,
            "cooldown": 7,
            "damage": 70,
            "crit_chance": 0.15,
            "crit_multiplier": 1.6,
            "damage_amp": 0.2,
            "scaling_stat": "Intelligence",
            "tags": ["AoE", "Arcane", "Silence"],
            "stackable": False
        },
        {
            "name": "Ethereal Barrage",  # 2-star
            "type": "Offense",
            "description": "Rapid arcane blasts to a single target.",
            "rarity": 2,
            "cooldown": 5,
            "damage": 75,
            "crit_chance": 0.16,
            "crit_multiplier": 1.65,
            "damage_amp": 0.22,
            "scaling_stat": "Intelligence",
            "tags": ["Single-target", "Arcane"],
            "stackable": False
        },
        {
            "name": "Astral Storm",  # 3-star
            "type": "Offense",
            "description": "Summons arcane meteors that rain down, AoE damage.",
            "rarity": 3,
            "cooldown": 14,
            "damage": 150,
            "crit_chance": 0.2,
            "crit_multiplier": 1.8,
            "damage_amp": 0.3,
            "scaling_stat": "Intelligence",
            "tags": ["AoE", "Arcane", "Impact"],
            "stackable": False
        },
        {
            "name": "Time Rift",  # 3-star
            "type": "Offense",
            "description": "Damages enemies and slows their attack speed for 8 seconds.",
            "rarity": 3,
            "cooldown": 16,
            "damage": 120,
            "crit_chance": 0.22,
            "crit_multiplier": 1.8,
            "damage_amp": 0.28,
            "scaling_stat": "Intelligence",
            "tags": ["AoE", "Arcane", "Slow"],
            "stackable": False
        },

        # Defensive
        {
            "name": "Mana Barrier",
            "type": "Defense",
            "description": "Converts 25% of incoming damage to mana loss instead of health.",
            "cooldown": 20,
            "effect": {"damage_to_mana_percent": 0.25, "duration": 10},
            "stackable": False
        },
        {
            "name": "Arcane Ward",
            "type": "Defense",
            "description": "Absorbs 100 damage for 12 seconds.",
            "cooldown": 25,
            "effect": {"damage_absorption": 100, "duration": 12},
            "stackable": False
        },
        {
            "name": "Phantom Veil",
            "type": "Defense",
            "description": "Increases dodge chance by 20% for 10 seconds.",
            "cooldown": 18,
            "effect": {"dodge_buff": 0.2, "duration": 10},
            "stackable": False
        },

        # Support
        {
            "name": "Arcane Focus",
            "type": "Support",
            "description": "Increases Intelligence by 15% for 15 seconds.",
            "cooldown": 30,
            "effect": {"intelligence_buff": 0.15, "duration": 15},
            "stackable": False
        },
        {
            "name": "Spell Haste",
            "type": "Support",
            "description": "Reduces cooldowns of all spells by 20% for 12 seconds.",
            "cooldown": 35,
            "effect": {"cooldown_reduction": 0.2, "duration": 12},
            "stackable": False
        },
        {
            "name": "Meditation",
            "type": "Support",
            "description": "Regenerates 5% mana per second for 10 seconds.",
            "cooldown": 25,
            "effect": {"mana_regen_percent": 0.05, "duration": 10},
            "stackable": False
        }
    ],


    "archer": [
        # Offensive
        {
            "name": "Piercing Arrow",  # 1-star
            "type": "Offense",
            "description": "Arrow that pierces through enemies, dealing moderate damage.",
            "rarity": 1,
            "cooldown": 2,
            "damage": 40,
            "crit_chance": 0.12,
            "crit_multiplier": 1.5,
            "damage_amp": 0.18,
            "scaling_stat": "Dexterity",
            "tags": ["Projectile", "Piercing"],
            "stackable": False
        },
        {
            "name": "Multi-Shot",  # 2-star
            "type": "Offense",
            "description": "Shoots 3 arrows in a cone, each dealing 50% damage.",
            "rarity": 2,
            "cooldown": 7,
            "damage": 35,
            "crit_chance": 0.15,
            "crit_multiplier": 1.6,
            "damage_amp": 0.2,
            "scaling_stat": "Dexterity",
            "tags": ["AoE", "Projectile"],
            "stackable": False
        },
        {
            "name": "Explosive Arrow",  # 2-star
            "type": "Offense",
            "description": "Arrow explodes on impact dealing AoE damage.",
            "rarity": 2,
            "cooldown": 9,
            "damage": 75,
            "crit_chance": 0.15,
            "crit_multiplier": 1.7,
            "damage_amp": 0.22,
            "scaling_stat": "Dexterity",
            "tags": ["AoE", "Projectile", "Explosion"],
            "stackable": False
        },
        {
            "name": "Rain of Arrows",  # 3-star
            "type": "Offense",
            "description": "Rains down arrows dealing AoE damage over 5 seconds.",
            "rarity": 3,
            "cooldown": 15,
            "damage": 140,
            "crit_chance": 0.2,
            "crit_multiplier": 1.75,
            "damage_amp": 0.28,
            "scaling_stat": "Dexterity",
            "tags": ["AoE", "Projectile"],
            "stackable": False
        },
        {
            "name": "Snipe",  # 3-star
            "type": "Offense",
            "description": "Powerful single-target shot with high crit chance.",
            "rarity": 3,
            "cooldown": 10,
            "damage": 160,
            "crit_chance": 0.3,
            "crit_multiplier": 2.0,
            "damage_amp": 0.3,
            "scaling_stat": "Dexterity",
            "tags": ["Single-target", "Projectile"],
            "stackable": False
        },

        # Defensive
        {
            "name": "Evasive Roll",
            "type": "Defense",
            "description": "Rolls away quickly increasing dodge chance by 25% for 5 seconds.",
            "cooldown": 15,
            "effect": {"dodge_buff": 0.25, "duration": 5},
            "stackable": False
        },
        {
            "name": "Camouflage",
            "type": "Defense",
            "description": "Become invisible for 6 seconds or until attacking.",
            "cooldown": 20,
            "effect": {"invisibility_duration": 6},
            "stackable": False
        },
        {
            "name": "Sharpened Reflexes",
            "type": "Defense",
            "description": "Reduces damage taken by 20% for 8 seconds.",
            "cooldown": 18,
            "effect": {"damage_reduction": 0.2, "duration": 8},
            "stackable": False
        },

        # Support
        {
            "name": "Focus Shot",
            "type": "Support",
            "description": "Increases crit chance by 20% for 10 seconds.",
            "cooldown": 25,
            "effect": {"crit_chance_buff": 0.2, "duration": 10},
            "stackable": False
        },
        {
            "name": "Quick Draw",
            "type": "Support",
            "description": "Reduces cooldowns of all archery abilities by 15% for 12 seconds.",
            "cooldown": 30,
            "effect": {"cooldown_reduction": 0.15, "duration": 12},
            "stackable": False
        },
        {
            "name": "Steady Aim",
            "type": "Support",
            "description": "Increases damage by 15% for 15 seconds.",
            "cooldown": 30,
            "effect": {"damage_buff": 0.15, "duration": 15},
            "stackable": False
        }
    ],


    "knight": [
        # Offensive
        {
            "name": "Heavy Slash",  # 1-star
            "type": "Offense",
            "description": "Powerful melee strike with moderate damage.",
            "rarity": 1,
            "cooldown": 3,
            "damage": 50,
            "crit_chance": 0.1,
            "crit_multiplier": 1.5,
            "damage_amp": 0.15,
            "scaling_stat": "Strength",
            "tags": ["Melee"],
            "stackable": False
        },
        {
            "name": "Shield Bash",  # 2-star
            "type": "Offense",
            "description": "Bashes enemy, stunning for 2 seconds.",
            "rarity": 2,
            "cooldown": 7,
            "damage": 40,
            "crit_chance": 0.12,
            "crit_multiplier": 1.6,
            "damage_amp": 0.18,
            "scaling_stat": "Strength",
            "tags": ["Melee", "Stun"],
            "stackable": False
        },
        {
            "name": "Whirlwind",  # 2-star
            "type": "Offense",
            "description": "Spin attack hitting all nearby enemies.",
            "rarity": 2,
            "cooldown": 10,
            "damage": 65,
            "crit_chance": 0.15,
            "crit_multiplier": 1.6,
            "damage_amp": 0.22,
            "scaling_stat": "Strength",
            "tags": ["AoE", "Melee"],
            "stackable": False
        },
        {
            "name": "Crushing Blow",  # 3-star
            "type": "Offense",
            "description": "Heavy blow dealing massive damage to single target.",
            "rarity": 3,
            "cooldown": 12,
            "damage": 140,
            "crit_chance": 0.2,
            "crit_multiplier": 1.75,
            "damage_amp": 0.28,
            "scaling_stat": "Strength",
            "tags": ["Single-target", "Melee"],
            "stackable": False
        },
        {
            "name": "Earthquake Slam",  # 3-star
            "type": "Offense",
            "description": "Slam the ground, damaging and slowing enemies in AoE.",
            "rarity": 3,
            "cooldown": 16,
            "damage": 130,
            "crit_chance": 0.18,
            "crit_multiplier": 1.7,
            "damage_amp": 0.3,
            "scaling_stat": "Strength",
            "tags": ["AoE", "Melee", "Slow"],
            "stackable": False
        },

        # Defensive
        {
            "name": "Dash",
            "type": "Defense/Support",
            "description": "Quick dash that slightly boosts movement and avoids damage for 1 second.",
            "cooldown": 12,
            "effect": {"move_speed_buff": 0.3, "invulnerability_duration": 1},
            "stackable": False
        },
        {
            "name": "Fortify",
            "type": "Defense",
            "description": "Increases defense by 30% for 10 seconds.",
            "cooldown": 20,
            "effect": {"defense_buff": 0.3, "duration": 10},
            "stackable": False
        },
        {
            "name": "Shield Wall",
            "type": "Defense",
            "description": "Blocks all damage for 2 seconds (perfect block).",
            "cooldown": 25,
            "effect": {"block_all_damage_duration": 2},
            "stackable": False
        },

        # Support
        {
            "name": "Battle Cry",
            "type": "Support",
            "description": "Increases attack damage by 20% for 12 seconds.",
            "cooldown": 30,
            "effect": {"damage_buff": 0.2, "duration": 12},
            "stackable": False
        },
        {
            "name": "Adrenaline Rush",
            "type": "Support",
            "description": "Increases attack speed by 25% for 8 seconds.",
            "cooldown": 25,
            "effect": {"attack_speed_buff": 0.25, "duration": 8},
            "stackable": False
        },
        {
            "name": "Last Stand",
            "type": "Support",
            "description": "Regenerates 5% health per second for 10 seconds.",
            "cooldown": 40,
            "effect": {"health_regen_percent": 0.05, "duration": 10},
            "stackable": False
        }
    ]

}
