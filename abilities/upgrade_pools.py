upgrade_pools = {
    "mage": [
        # Offensive Abilities
        {  # Ability
            "name": "Fireball",
            "type": "Offense",
            "stat": None,
            "value": None,
            "stackable": False
        },
        {  # Ability
            "name": "Greater Fireball",
            "type": "Offense",
            "stat": None,
            "value": None,
            "prerequisite": "Fireball",
            "stackable": False
        },
        # Defense
        {  # Increases defence by 12%
            "name": "Magic Armor",
            "type": "Defense",
            "stat": "Defense",
            "value": "12%",
            "stackable": True
        },
        {  # Lets you use short teleport
            "name": "Dash",
            "type": "Utility",
            "stat": None,
            "value": None,
            "stackable": False
        },
    ],

    "archer": [
        {
            "name": "Piercing Arrow",
            "type": "Offense",
            "stat": None,
            "value": None,
            "stackable": False
        },
        {
            "name": "Rapid Shot",
            "type": "Offense",
            "stat": "Attack Speed",
            "value": "10%",
            "stackable": False
        },
        {
            "name": "Evasion",
            "type": "Defense",
            "stat": "Defense",
            "value": 8,
            "stackable": True
        },
        {
            "name": "Hawk Eye",
            "type": "Support",
            "stat": "Attack",
            "value": 5,
            "stackable": False
        },
        {
            "name": "Agility Boost",
            "type": "Utility",
            "stat": "Speed",
            "value": "5%",
            "stackable": True
        }
    ],

    "knight": [
        {
            "name": "Heavy Armor",
            "type": "Defense",
            "stat": "Defense",
            "value": "10%",
            "stackable": True
        },
        {
            "name": "Heavy Sword",
            "type": "Offense",
            "stat": "Attack",
            "value": "10%",
            "stackable": True
        },
        {
            "name": "Swift Sword",
            "type": "Offense",
            "stat": "Attack Speed",
            "value": "5%",
            "stackable": True
        },
        {
            "name": "Fortitude",
            "type": "Support",
            "stat": "Health Regen",
            "value": "20%",
            "stackable": True
        },
        {
            "name": "Health Boost",
            "type": "Support",
            "stat": "Health",
            "value": "10%",
            "stackable": True
        },
    ]
}
