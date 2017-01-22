#Archaeology
- A separate part of the game, to be used on the generated worlds.
- Won't actually interface with generated worlds at first.
- First steps:
    - You are presented with several documents in one foreign language.
    - Your goal is to translate them.
    - You can enter a word (a string) in the alien language and a word in English.
        - If right, the word will translate itself into english/become a different color.
        - If wrong, nothing will happen.
        - Suffixes will not be automatically translated.
- Goal is generally to discover things about the worlds.
    - Languages
        - Deciphering
        - Grammatical structure (maybe)
    - History
        - Wars
    - Culture
        - Religion
        - Art

#Languages
- Phonetics
    - What sounds does each symbol make?
- Orthography
    - Do we write with letters, pictographs, syllabaries, etc?
- Morphology
    - Separate words for suffixes/prefixes like plural/conjugation
    - Prefix/Suffixes or Helping Word (before/after) for:
        - Plural/singular
        - Negation
        - Converting part of speech (-ive, -ness)
        - Tenses
            - Gerunds
            - Past
            - Present
            - Future
            - Perfect
                - Past
                - Present
                - Future
        - Comparing
            - Superlative/comparative (could be on a per-word basis maybe?)
- Syntax
- Semantics

#Plans
- A structured way for nations and people to have agendas.
- Each plan is a tree, with each node being another plan
- Plans are evaluated top down (as you would expect).
- Each plan has it's own ID, and will be sent a message one it's goals have been completed.
- List of plan components:
    - Nation:
        - Conquer city `city` {conquer_city}
        - Conquer nation `nation` {conquer_nation}
        - Improve income `goal` {increase_income}
            - Create trade agreements {create_trade_agreement}
            - Send caravans (city)
            - Expand city (city)
            - Build buildings (city)
            - Disband soldiers (city)
        - Improve cities {improve_city}
            - Expand city (city)
            - Build buildings (city)
        - Found new city {found_city}
        - Train soldiers `time` `amount` {train_soldier}
        - Merge armies `amount` {merge_army}
            - Send army (city)
    - City:
        - Train soldiers `time` `number` {train_soldier}
        - Disband soldiers `time` `number` {disband_soldier}
        - Send army `number` `location` {send_soldier}
        - Send caravans `time` `number` `location`
        - Expand city `time` `amount`
        - Build buildings `time` `amount` `purpose`
- Example plan:
    - Conquer nation B
        - Build an army
            - Train armies at cities
                - Train 100 soldiers at city 1
                - Train 200 soldiers at city 2
                - Train 300 soldiers at city 3
        - Merge armies
            - Send all soldiers from city 1 to city 2
            - Send all soldiers from city 3 to city 2
        - Send armies to conquer cities
            - Send army from city 2 to attack enemy city

#People
- Generals
- Judges
- Heroes (achilles, cu chulainn, odysseus, et cetera)
    - Fights between heroes to decide the outcome of battles, rather than fighting the whole battle
- Notable People should live in cities, rather than just existing in the nation

#Military
- Officers (centurions, colonels, whatever)
- Specialized units (infiltration, artillery)
- Specialized formations
- Military doctrines

#Battle
- Tactics
- Deploying more than one kind of troop at a time (not all the levies first).
- Morale
- Walls
- Defenses (caltrops, stakes)
- Terrain (hills, rivers, bridges, valleys)

#Natural disasters
- Earthquakes
- Tornadoes
- Droughts/floods

#Art
- Actual content
    - Basic outlines of the work
    - Possibly even simple paintings

#Literature
- Fables
- History
- Theologic

#Non-human life
- Wildlife
- Hunting
- Domesticated animals
- Beasts of burden
- Plants (edible, poisonous, et cetera)
- Randomly generated animals/plants

#Food
- Multiple kinds of food.
- Vegan/Vegetarian/whatever
- Staple foods
- Common foods
- "High class" foods
- Taboo foods (such as dog and horse meat in the US)

#Religion
- Rituals (specific to gods, and the whole religion in general)
    - Sacrifices: Animal, human
- Associate gods with particular representations
    - Animals
    - As people using certain weapons
- Dogmas/teachings/prohibitions

#Celebrations
- Religious
- Independence days/founding days
- Birthdays (probably going to be birth months, on account of how time progresses, but eh) of notable people

#Superstitions
- Lucky days
- Divination
- Random stuff (black cats, walking under ladders, breaking mirrors, et cetera).

#Research
- Weapons/armor available based on research
    - Weapons and armor chosen based on previous effectiveness.
- Buildings available based on research

#Miscellaneous
- Duels between notable people
    - Probably primarily heroes, but eh?
- Assassination plots
- Intellectual movements (great awakening, enlightenment, art movements)
- Saving/loading
