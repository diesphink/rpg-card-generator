# RPG Card Generator

This is a tool to facilitate my card creation for my table top RPG.

## How to use

### 1. Clone this repo

```bash
git clone https://github.com/diesphink/rpg-card-generator.git
```

### Create virtualenv and install dependencies

This is a python script, perhaps you have all the dependencies, but maybe not. I recommend you install this on a virtualenv, with the following code:

```bash
cd rpg-card-generator
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

If you don't care about virtual environments, just install everyting on requirements.txt:

```bash
pip3 install -r requirements.txt
```

### Edit/create `.toml` files in `input` folder.

The configuration files are in .toml, the syntax can be found here: [https://toml.io/](https://toml.io/en/)

The available main options are:

#### 

```toml
# Default card, has an image on top, a box for description, and plenty of space for extra infos, tags, etc.
["Normal card"]

title = "TItle for the card" # Optional, if undefined, will use the section title ("Normal card" in this case)

image = "path to the 410x210 image" # For normal cards, this is a 410x210 image file

# This is the main text of the card.
# Aditional parsed options:
# - You can insert a blank line between paragraphs to add space
# - You can add **bold** words
# - You can add  - at the start of a line (with surrounding spaces) to make a list
description = """
Long text for **description**.

This is a list:

 - option 1
 - option 2

There's
no problem in breaking lines, it'll be on a continuous
single line
"""

# Optional. Footer information added at the bottom left corner
# Line breaks here will reflect on line breaks on the card
footer = """
Information added
at the bottom left corner
"""

type = "Spell" # Optional. Type of the card, will be added in black on the middle right of the card, below the image

time = "action" # Optional. Time of the activation, if it's bonus, action or reaction, will use colors cyan, blue and red. Everything else will get red color as well.

cost = "ki" # Optional. Cost to use the ability, will be printed in black at the bottom right corner, besides the time information

components = "VSM" # Optional. Adds iconography to mark the magical components: V for verbal, S for somatic and M for material. If a spell has a material cost worth any value, it should be noted in "cost".

fontsize = "4.5" # Optional font size for text in the card, useful for cards with sooo many words. Defaults to 6.

count = 1 # Optional, indicates how many of this card to print
```

```toml
# More simple card, useful to pass around for other players
# Contains title, one image on the full background and a box of text
["Token card"]

token = true # Indicates that this is a token card

title = "TItle for the card" # Optional, if undefined, will use the section title ("Token card" in this case)

image = "path to the 410x630 image" # For token cards, this is a 410x630 image file

type = "Spell effect" # Type of the card, will be added in black on the middle right of the card, below the image

count = 1 # Optional, indicates how many of this card to print
```

```toml
# Cards with just an image
# Are defined if you have not defined a specific type (token, back, sheet, inventory) and there's no description present
['Image card']

image = "path to the 410x630 image" # For image cards, this is a 410x630 image file

count = 1 # Optional, indicates how many of this card to print
```


```toml
# Back of the card
["Back card"]

token = true # Indicates that this is a back card

image = "path to the 410x630 image" # For back cards, this is a 410x630 image file

color = "orange" # Color to add as filter to the image. The options are:
                 # - green
                 # - red
                 # - blue
                 # - yellow
                 # - orange
                 # - teal
                 # - purple
                 # - brown

count = 1 # Optional, indicates how many of this card to print
```

```toml
# Character sheet

[character]

sheet = true # Indicates this is a character sheet card

image = "path to the 1260x1760 image" # For character sheet cards, this is a 1260x1760 image file

title = "Character name, class, etc" # Title of the card

# Attributes of the character. You can change the key names for any text you wish, or translate the values
# The order of the values are:
# - Attribute value
# - Attribute bonus
# - Saving throw
# Negative values must be informed, but the + is optional

[character.attributes]
STR = [12, 1, 1]
DES = [8, -1, -1]
CON = [14, +2, +2]
"???" = [10, 0, 0]
WIS = [10, 0, 0]
CHA = [10, 0, 0]

# Skill values, names and proficiencies, in arrays
[character.skills]

# skill check bonus
skills = [0, 5, 4, 4, 1, 1, 1, 1, 2, 2, 3, 2, 5, 2, 6, 6, 5, 8]

# wether you have proficience with the skill (will make the skill bold)
profic = [0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1]

# Names for the skills (for translation or additional info)
names = [
    'Athletics',
    'Acrobatics',
    'Sleight of hand',
    'Stealth (\faIcon{hotjar}adv)',
    'Arcana',
    'History',
    'Investigation',
    'Nature',
    'Religion',
    'Animal Handling',
    'Insight',
    'Medicine',
    'Perception',
    'Survival',
    'Deception',
    'Intimidation',
    'Performance',
    'Persuasion',
]

# Information for the 9 boxes beneath the character image.
# You can have any information here, if you want to add two values
# you can pass an array, the second value will be added as a callout
# over the main value
[character.boxes]
INIT = "+4"
AC = 14
HP = 30
PROF = "+2"
"H DICE" = "4d8"
SPEED = ["9m", "30ft"]
"SP ATT" = "+6"
"SP SAVE" = 14
"SLOTS" = "5/2"
"ANY" = "VL"

# Proficiencies box
# Every value here will be inserted as a line, with the key in bold text
[character.proficiencies]

title = "Anything else" # You can change the prof box to use it for character abilities, feats, whatever

'\faIcon{comment}Languages' = "Common, elvish."
'\faIcon{gavel}Armor and weapons' = "Light and medium armor, shields, simple and martial weapons."
'\faTools{}Tools' = "Thieves' tools (traps or locks)"

# Attacks box
# Same as above, every value here will be inserted as a line, with the
# key in bold text
[quimera.attacks]

title = "Anything else" # You can change the prof box to use it for character abilities, feats, whatever

"Sword (1h)" = "+6, 1d8+4 slashing"
"Sword (2h)" = "+6, 1d10+4 slashing"
```

```toml
[inventory]

inventory = true # Indicates this is an inventory card

title = "Inventory of **Character**" # Title of the card
image = "path to the 1260x1760 image" # For character sheet cards, this is a 1260x1760 image file

# Every key/value will make a section on the inventory
# For each line in the value, there'll be a line on inventory,
# with a square checkbox at the side
"Backpack" = """
Bedroll
Dagger
Waterskin
"""

"Equipped" = """
Leather armor
Longsword
"""

# Consumables
# For every key/value, there'll be a line, with how many squares as passed in the value at the right side
# If you want to break line for more information on the item, use \\
# Additionally, you can pass GP for how many Gold pieces to start with on the sheet
[inventory.consumables]
'''Potion of climbing
(1h, climb speed 9m, adv on climb)''' = 1
'Potion of healing (2d4+2)' = 10
"Ration" = 5
GP = 336

```

## Execute generate_latex.py

On execution, it will generate an output folder with the necessary contents (images that are used on the files, tex files created)

## Import in overleaf

Execute the bash script open_in_overleaf to easily export the content of that folder to a new project in overleaf.

If you wish, you may instead just create a new project in overleaf and manually import all the files in the output directory