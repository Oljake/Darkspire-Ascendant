# test.py

from fire_mage_pool import firemage_abilities
from dark_mage_pool import darkmage_abilities
from mystic_mage_pool import mysticmage_abilities
from archer_pool import archer_abilities
from knight_pool import knight_abilities

# Combine all abilities pools into one master pool
all_abilities = (
    firemage_abilities +
    darkmage_abilities +
    mysticmage_abilities +
    archer_abilities +
    knight_abilities
)

# Optional: print total count
print(f"Total abilities pooled: {len(all_abilities)}")

# Example: print all offensive abilities from all classes
offensive_abilities = [ab for ab in all_abilities if ab["type"] == "Offense"]
print(f"Total offensive abilities: {len(offensive_abilities)}")
for ability in offensive_abilities:
    print(f"- {ability['name']} ({ability.get('stars', 'N/A')} stars)")
