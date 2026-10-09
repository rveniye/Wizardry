import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.cards import *


##############
# LAND CARDS #
##############

# Basic lands
forest = LandCard(
    name="Forest",
    generic_mana=0,
    sp_mana="",
    description="Tap to add one green mana.",
    effect="tap? gen 1 green",
)

island = LandCard(
    name="Island",
    generic_mana=0,
    sp_mana="",
    description="Tap to add one blue mana.",
    effect="tap? gen 1 blue",
)

mountain = LandCard(
    name="Mountain",
    generic_mana=0,
    sp_mana="",
    description="Tap to add one red mana.",
    effect="tap? gen 1 red",
)


land_of_iridesence = LandCard(
    name="Land of Iridesence",
    generic_mana=0,
    sp_mana="",
    description=(
        "Enters the battlefield tapped."
        "|Tap to add one green, blue, or red mana."
    ),
    effect="entertap; tap? gen 1 green/blue/red",
)

graveyard = LandCard(
    name="Graveyard",
    generic_mana=0,
    sp_mana="",
    description=(
        "When tapped, it generates blue mana correlating "
        "to the number of Skeletons in your graveyard."
    ),
    effect="tap? gen (graveyard count Skeleton) blue",
)


# Dual lands (enter tapped but produce two colors)
tropical_grove = LandCard(
    name="Tropical Grove",
    generic_mana=0,
    sp_mana="",
    description=(
        "Enters the battlefield tapped."
        "|Tap to add one green or blue mana."
    ),
    effect="entertap; tap? gen 1 green/blue",
)

volcanic_peak = LandCard(
    name="Volcanic Peak",
    generic_mana=0,
    sp_mana="",
    description=(
        "Enters the battlefield tapped."
        "|Tap to add one red or blue mana."
    ),
    effect="entertap; tap? gen 1 red/blue",
)

wild_highlands = LandCard(
    name="Wild Highlands",
    generic_mana=0,
    sp_mana="",
    description=(
        "Enters the battlefield tapped."
        "|Tap to add one red or green mana."
    ),
    effect="entertap; tap? gen 1 red/green",
)


# Cost lands
atlantis = LandCard(
    name="Atlantis",
    generic_mana=0,
    sp_mana="",
    description=(
        "Enters the battlefield tapped."
        "|t1b: Generates 2 green mana."
    ),
    effect="entertap; tap? for 1 blue gen 2 green; tap? gen 1 blue",
)

sand_temple = LandCard(
    name="Sand Temple",
    generic_mana=0,
    sp_mana="",
    description=(
        "Enters the battlefield tapped."
        "|t1r: Generates 2 red mana."
    ),
    effect="entertap; tap? for 1 blue gen 2 red; tap? gen 1 blue",
)

dragon_dwelling = LandCard(
    name="Dragon Dwelling",
    generic_mana=0,
    sp_mana="",
    description="Enters battlefield tapped."
                "|t1r: Generates 2 green mana.",
    effect="entertap;",
)

################
# CREATURE CARDS #
################

###################
# Green creatures #
###################
slime = CreatureCard(
    name="Slime",
    generic_mana=1,
    sp_mana="green",
    description="Attacking doesn't cause this creature to tap.",
    att=2,
    end=2,
    effect="vigilant",
)

bigger_slime = CreatureCard(
    name="Bigger Slime",
    generic_mana=2,
    sp_mana="green",
    description=(
        "Attacking doesn't cause this creature to tap."
        "|It's a bigger slime."
    ),
    att=3,
    end=3,
    effect="vigilant",
)

forest_bear = CreatureCard(
    name="Forest Bear",
    generic_mana=1,
    sp_mana="green",
    description=(
        "A powerful bear from the deep forest."
        "|Why does he look like a dog"
    ),
    att=2,
    end=2,
    effect="",
)

vine_elemental = CreatureCard(
    name="Vine Elemental",
    generic_mana=3,
    sp_mana="green",
    description=(
        "Gains +1/+1 when another creature enters the battlefield."
        "|Looks like he's mid boogie"
    ),
    att=2,
    end=3,
    effect="enter? inc att 1; enter? inc end 1",
)

alpha_wolf = CreatureCard(
    name="Alpha Wolf",
    generic_mana=2,
    sp_mana="green",
    description=(
        "Other creatures you control get +1 attack."
        "|Sorry, you're not a sigma"
    ),
    att=3,
    end=2,
    effect="summon? global inc att 1",
)

stone_giant = CreatureCard(
    name="Stone Giant",
    generic_mana=2,
    sp_mana="green",
    description=(
        "Gains +2 to endurance when blocking."
        "|He does not look amused at all..."
    ),
    att=1,
    end=3,
    effect="block? inc end 2",
)

green_wizar = CreatureCard(
    name="Green Wizar",
    generic_mana=1,
    sp_mana="green",
    description=(
        "Gains +1 to attack for each green coloured mana you have "
        "when it enters the battlefield.|The power of green"
    ),
    att=2,
    end=6,
    effect="summon? inc att (mana count green)",
)

king_slime = CreatureCard(
    name="King Slime",
    generic_mana=4,
    sp_mana="green",
    description=(
        "Gives all active slime creatures +1 to attack."
        "|The king of slimes"
    ),
    att=4,
    end=6,
    effect='summon? inc att 1 "Slime"',
)

archer = CreatureCard(
    name="Archer",
    generic_mana=2,
    sp_mana="green",
    description="This creature has reach.|His arrows go pretty far",
    att=2,
    end=3,
    effect="reach",
)

hero = CreatureCard(
    name="Hero",
    generic_mana=3,
    sp_mana="green",
    description="All creatures you control gain +1 to endurance.|So inspiring",
    att=3,
    end=3,
    effect="summon? global inc end 1",
)

##################
# Blue creatures #
##################
skeleton = CreatureCard(
    name="Skeleton",
    generic_mana=2,
    sp_mana="blue",
    description="Haste.\nGains +1 to endurance when blocking.",
    att=2,
    end=2,
    effect="haste; block? inc end 1",
)

skeleton_army = CreatureCard(
    name="Skeleton Army",
    generic_mana=3,
    sp_mana="blue",
    description="Gains +1 to attack for every skeleton in the graveyard.",
    att=2,
    end=2,
    effect="haste; summon? inc att (graveyard count Skeleton)",
)

phantom_warrior = CreatureCard(
    name="Phantom Warrior",
    generic_mana=3,
    sp_mana="blue",
    description="Reach. This creature can block flying creatures.",
    att=2,
    end=3,
    effect="reach",
)

sea_serpent = CreatureCard(
    name="Sea Serpent",
    generic_mana=4,
    sp_mana="blue",
    description="Trample. It's a powerful sea creature.|Ssssss",
    att=5,
    end=5,
    effect="trample",
)

arcane_scholar = CreatureCard(
    name="Arcane Scholar",
    generic_mana=2,
    sp_mana="blue",
    description=(
        "When this creature enters the battlefield, draw a card."
        "|He is smart"
    ),
    att=1,
    end=3,
    effect="summon? draw 1",
)

vergil = CreatureCard(
    name="Vergil",
    generic_mana=5,
    sp_mana="blue",
    description=(
        "The Storm that is Approaching. Cannot be blocked."
        "|Deadbeat Dad"
    ),
    att=6,
    end=6,
    effect="unblockable",
)

blue_wizar = CreatureCard(
    name="Blue Wizar",
    generic_mana=1,
    sp_mana="blue",
    description=(
        "Gains +1 to attack for each blue coloured mana you have "
        "when it enters the battlefield.|The power of blue"
    ),
    att=2,
    end=6,
    effect="summon? inc att (mana count blue)",
)

mind_sorcerer = CreatureCard(
    name="Mind Sorcerer",
    generic_mana=2,
    sp_mana="blue",
    description=(
        "An evil sorcerer from the lands between. Draw 1 card when "
        "he enters the battlefield.|He reads your mind"
    ),
    att=3,
    end=4,
    effect="summon? draw 1",
)

wanderer = CreatureCard(
    name="Wanderer",
    generic_mana=2,
    sp_mana="blue",
    description=(
        "Flying. A powerful wizar forgotten to time. His true "
        "ability is unknown.|What's his name again?"
    ),
    att=3,
    end=4,
    effect="flying",
)

mind_flayer = CreatureCard(
    name="Mind Flayer",
    generic_mana=4,
    sp_mana="blue",
    description=(
        "A mind-controlling illithid that yearns for dominance. "
        "Create an intellect devourer when summoned."
    ),
    att=5,
    end=5,
    effect='summon? create 1 "Intellect Devourer"',
)

#################
# Red creatures #
#################
goblin_raider = CreatureCard(
    name="Goblin Raider",
    generic_mana=1,
    sp_mana="red",
    description="Haste. This creature can attack the turn it enters.",
    att=2,
    end=1,
    effect="haste",
)

fire_elemental = CreatureCard(
    name="Fire Elemental",
    generic_mana=3,
    sp_mana="red",
    description="Gains +1 attack when attacking.",
    att=3,
    end=2,
    effect="attack? inc att 1",
)

dragon_whelp = CreatureCard(
    name="Dragon Whelp",
    generic_mana=2,
    sp_mana="red",
    description=(
        "Flying. This baby dragon will grow to be quite terrifying."
    ),
    att=3,
    end=2,
    effect="flying",
)

berserker = CreatureCard(
    name="Berserker",
    generic_mana=2,
    sp_mana="red",
    description="Gains +2 attack when attacking, but -1 endurance.",
    att=2,
    end=3,
    effect="attack? inc att 2; attack? dec end 1",
)

imp = CreatureCard(
    name="Imp",
    generic_mana=1,
    sp_mana="red",
    description="Flying. A very evil creature.",
    att=2,
    end=2,
    effect="flying",
)

sazael_the_great = CreatureCard(
    name="Sazael the Great",
    generic_mana=4,
    sp_mana="red",
    description=(
        "Flying, trample, and gains +2 when attacking."
        "|This dragon is pretty great."
    ),
    att=5,
    end=5,
    effect="flying; trample; attack? inc att 2",
)

red_wizar = CreatureCard(
    name="Red Wizar",
    generic_mana=1,
    sp_mana="red",
    description=(
        "Gains +1 to attack for each red coloured mana you have "
        "when it enters the battlefield.|The power of red"
    ),
    att=2,
    end=6,
    effect="summon? inc att (mana count red)",
)

intellect_devourer = CreatureCard(
    name="Intellect Devourer",
    generic_mana=1,
    sp_mana="red",
    description=(
        "Haste. A repulsive creature that harnesses the intellect "
        "of others.|Not that it'd get much from you"
    ),
    att=2,
    end=2,
    effect="haste",
)



# Green creatures
green_creatures = [
    slime,
    bigger_slime,
    forest_bear,
    vine_elemental,
    alpha_wolf,
    stone_giant,
    green_wizar,
    king_slime,
    archer,
    hero,
]

# Blue creatures
blue_creatures = [
    skeleton,
    skeleton_army,
    phantom_warrior,
    sea_serpent,
    arcane_scholar,
    vergil,
    blue_wizar,
    mind_sorcerer,
    wanderer,
    mind_flayer,
]

# Red creatures
red_creatures = [
    goblin_raider,
    fire_elemental,
    dragon_whelp,
    berserker,
    imp,
    sazael_the_great,
    red_wizar,
    intellect_devourer,
]

# Spell cards
spells = []

# Land cards
lands = [
    forest,
    island,
    mountain,
    land_of_iridesence,
    graveyard,
    tropical_grove,
    volcanic_peak,
    wild_highlands,
    atlantis,
    sand_temple,
    dragon_dwelling,
]
