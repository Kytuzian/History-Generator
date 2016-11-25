#Installation
You will need Python 2.7 (preinstalled on OS X and some Linux (I think, don't know for sure, but I'm sure you can handle it)). If you're using Windows just go to https://www.python.org/ and get 2.7.

All you need to do then is navigate to the place where you uncompressed it, and type the following:

```
python history_generator.py
```

The simulation will then just run. Read the mechanics below for more information.

DISCLAIMER:
None of the below information is guaranteed to be current/accurate at any point, although I will try to update it.

#Mechanics Overview
At the beginning, the game generates a number of nations. Each of these has their own languages (see language below), name, religion, cities, armies in each of those cities, notable people, and works of art.

Nations also have several base stats, a tax rate, morale (revolts will start to occur when this is too low, usually happens when losing a war), army spending (this is an amount that dictates how much money is put into recruiting soldiers).

Cities are founded by nations when they have the money, but can also be obtained by conquest. Every once in a while, nations will go to war with each other, and fight battle when they think they can win. The chance of a nation going to war with another nation increases when the tolerance of their religion is low (affected by both the gods in their religions pantheon, by a base tolerance, and by the various statistics of priests within the nation (although these can also increase the tolerance of the religion)). When a battle begins, a new screen will pop up with circles in the color of the nations, representing each soldier.

Both armies deploy some of their soldiers (the exact number depends on the battle size set in battle.py), in the proportion to each other's army. For example, if one nation has 1000 troops, the other has 10, and the battle size is 350 (as it is at the time of writing), the first nation will deploy 350 troops, and the second nation will deploy only 3, thereby maintaining the 100 to 1 ratio. Soldiers are organized into units (the size of which is determined by the unit type). Units will attempt to maintain their ranks as they move. Ranged units will only move under one of two conditions. One, that they are out of ammunition, and two, if there is an enemy unit that is too close to them. Both of these scenarios will cause the soldiers to switch to their melee weapon.

When melee combat occurs, both soldiers roll for their attack/defense (0 to a max of their strength), with another random roll (0 to their fatigue / 2), and subtract the two. The soldier's weapon affects this, as well as the best material that the nation the soldier is from has researched. This means that while a soldier with a strength of 20 will almost always beat a soldier with a strength of 1, the soldier with a strength of 1 is able to win. After the fight, there is a 1 in the unit's discipline (1 in 5 if the unit has 5 discipline) chance that the unit's fatigue will go up. Therefore, if the soldier with 20 strength has fought a lot, it will become much weaker so a strength 20 soldier cannot simply destroy an entire army (like they used to be able to), although a 20 strength soldier will be able to take out a considerable number of enemies of strength 1. Whichever soldiers loses, loses 1 health, and when their health is 0, they will be removed from their unit and from the army.

For ranged units, there is a counter which determines when they can shoot. It varies from weapon to weapon, and is mostly affected by the square root of their discipline, although it does have a small random component to it. When the projectile is shot, it is directed at a single target, and if it doesn't hit it, it doesn't hit any other soldier either. Assuming it does hit, the projectile will have a base damage of 0 to the strength of unit that shot it. This, however, will be decreased by another random roll of the defending unit, which is a roll of 0 to its fatigue / 2 subtracted by a roll of 0 to its strength. The damage obviously cannot go below 0 or above the original damage roll of the projectile.

When an army has no more units, the battle will end (they are always fights to the death of the entire army. I know it's not entirely realistic, but this is much easier to implement and I plan to implement morale for armies at a later date (if its no longer on the to-do list, assume I've done it and I'm just too lazy to change this description)). The winning (only if the attackers, of course) army conquers a single city from the losers and all of it's production, improvements, et cetera will now contribute to the conquering nation. Additionally, the winners will gain morale, and the losers will lose morale.

#Weapons and Armor
Weapons have several stats: attack, defense, a material multiplier, and both attack and defense skill multipliers. To calculate the attack with a weapon, the user first calculates the effective attack from the weapon. This is done by taking the material multiplier of the weapon and multiplying it by the strength of the material the weapon is made out of. Then the weapon's attack is a random number from 0 to the weapon's effective attack. Then the soldier's strength is multiplied by the attack skill multiplier, and the two values are added.

The process is the same for defense, except with defense values instead of attack values.

For armor, the process is also the same, and armor, naturally, does not contribute to attack.

#Nation
A group of cities all joined together with armies to attack and carvans to trade with other nations.
The nation also shares a common religion (and this doesn't change, there is no conversion yet) and language.
Nations also have a collection of notable people, and a collection of works of art.

Nations have a capital city which will give more morale to the enemy when captured. Additionally, when a nation loses its capital, it will lose more morale, but while it owns its capital, it will gain morale every year.

Nations also have a technology level. The full tech tree is described in the Tech section.

#Notable People
Notable people can be any of the following:

- General: Currently no purpose.
- Priest: Can increase of decrease the tolerance of the nation's religio.
- Oracle: Currently no purpose.
- Artist: Creates works of art: both drawings and statues.
- Writer: Creates works of literature (which counts as art): plays, novels, essays, and poems.
- Composer: Creates works of art: both songs and musicals.
- Philosopher: Creates works of art: just essays.
- Scientist: Increases the nation's research rate.
- Revolutionary: Decreases the morale of the nation, increasing the chance for a rebellion.
- Hero: Currently no purpose.
- Administrator: Increase the tax rate.

#Art
This includes literature, music, as well as "normal" visual arts (paintings, statues, et cetera).

See the Art Detail section for...details about art.

- Drawings
    - Paintings
    - Frescoes
    - Woodblock prints
    - Sketches
- Statues
- Plays
- Musicals
- Essays
- Poems

#City
Cities are the building blocks of nations. Each city contains some amount of people, some amount of land (organized into cells), produces and consumes food and other resources (leather, cloth, metal, and wood), and builds buildings.

Cells can only contain a certain number of buildings in them, although this limit can be increased by researches (see the Tech section for more details). Cells by default can contain a total of 100.

Cities contain buildings as well. There following are the types of buildings and their associated bonuses/costs:


| Name          	| Population 	| Tax Score 	| Food 	| Wood 	| Leather 	| Cloth 	| Metal 	| Money 	| Caravan Chance 	| Size 	| Cost 	| Research Rate 	|
|---------------	|------------	|-----------	|------	|------	|---------	|-------	|-------	|-------	|----------------	|------	|------	|---------------	|
| House         	| 10         	| 10        	|      	|      	|         	|       	|       	|       	|                	| 5    	| 50   	|               	|
| Farm          	| 5          	|           	| 60   	|      	|         	|       	|       	|       	|                	| 20   	| 200  	|               	|
| Tavern        	| 5          	|           	|      	|      	|         	|       	|       	| 1200  	|                	| 50   	| 500  	|               	|
| Fishery       	| 2          	|           	| 125  	|      	|         	|       	|       	|       	|                	| 40   	| 200  	|               	|
| Ranch         	| 2          	|           	| 125  	|      	|         	|       	|       	|       	|                	| 50   	| 300  	|               	|
| Hunting Lodge 	| 2          	|           	| 50   	|      	|         	|       	|       	|       	|                	| 20   	| 50   	|               	|
| Leatherworker 	| 2          	|           	|      	|      	| 5       	|       	|       	| 200   	|                	| 5    	| 300  	|               	|
| Weaver        	| 2          	|           	|      	|      	|         	| 5     	|       	| 200   	|                	| 5    	| 300  	|               	|
| Woodcutter    	| 2          	|           	|      	| 5    	|         	|       	|       	| 200   	|                	| 50   	| 300  	|               	|
| Mine          	| 8          	|           	|      	|      	|         	|       	| 3     	| 1000  	|                	| 90   	| 1000 	|               	|
| Library       	| 4          	|           	|      	|      	|         	|       	|       	|       	|                	| 90   	| 1000 	| 2             	|
| Lab           	| 2          	|           	|      	|      	|         	|       	|       	|       	|                	| 75   	| 1000 	| 5             	|
| Market        	|            	| 100       	|      	|      	|         	|       	|       	| 1000  	|                	| 60   	| 1500 	|               	|
| Caravansary   	| 5          	|           	|      	|      	|         	|       	|       	|       	| 20             	| 90   	| 2000 	|               	|

#Army
A tree of unit types/numbers.

Units have three main stats, strength, health, and discipline. Additionally, they can either be ranged, or not ranged. Discipline only currently affects ranged units (higher disciplines means soldiers will tend to shoot faster).

Ranged unit do not move until they are out of ammo, or when their targets are too close to them (as in, charging them), at which point they switch to melee. If you see projectiles flying through large amounts of enemies, this is because the projectile is only targeting one enemy (runs WAY faster this way). Just imagine it was a really bad shot, although this should be relatively rare, as soldiers should aim ahead.

Each weapon and armor has it's own stats, which are listed in the Weapons section below.

#Weapons and Armor


| Name          | Cost | Range | Material Multiplier | Attack | Defense | Attack Multiplier | Defense Mutliplier | Reload Time | Ammo | Projectile Speed |
|---------------|------|-------|---------------------|--------|---------|-------------------|--------------------|-------------|------|------------------|
| Unarmed       | 0    | 5     | 0                   | 1      | 1       | 1                 | 1                  | 1           |      |                  |
| Dagger        | 10   | 5     | 1.5                 | 2      | 2       | 1.1               | 1                  | 2           |      |                  |
| Rondel        | 25   | 5     | 1.6                 | 3      | 1       | 1.5               | 1                  | 2           |      |                  |
| Dirk          | 25   | 5     | 1.6                 | 3      | 1       | 1.5               | 1                  | 2           |      |                  |
| Kopis         | 40   | 6     | 1.8                 | 6      | 1       | 2                 | 1                  | 3           |      |                  |
| Shortsword    | 50   | 7     | 1.8                 | 5      | 2       | 2                 | 1.1                | 4           |      |                  |
| Club          | 10   | 7     | 0                   | 5      | 2       | 1                 | 1                  | 6           |      |                  |
| Hammer        | 25   | 7     | 1.3                 | 6      | 1       | 1.5               | 0.8                | 5           |      |                  |
| Mace          | 40   | 7     | 1.5                 | 6      | 1       | 1.8               | 1                  | 5           |      |                  |
| Axe           | 30   | 7     | 1.8                 | 8      | 2       | 2.5               | 0.8                | 7           |      |                  |
| Morning Star  | 200  | 7     | 1.5                 | 8      | 0       | 2                 | 0.2                | 10          |      |                  |
| Sword         | 100  | 10    | 2                   | 6      | 3       | 2                 | 1.1                | 5           |      |                  |
| Bastard Sword | 150  | 12    | 2.3                 | 7      | 2       | 2                 | 1.5                | 6           |      |                  |
| Claymore      | 200  | 15    | 2.5                 | 10     | 1       | 2.5               | 0.5                | 7           |      |                  |
| Bill          | 50   | 12    | 1.5                 | 6      | 4       | 1.5               | 1.5                | 8           |      |                  |
| Flail         | 50   | 12    | 1.2                 | 6      | 0       | 2                 | 0.5                | 12          |      |                  |
| Falx          | 75   | 14    | 1.8                 | 8      | 1       | 2                 | 0.8                | 7           |      |                  |
| Polehammer    | 100  | 15    | 1                   | 8      | 2       | 2                 | 1                  | 11          |      |                  |
| Staff         | 10   | 15    | 0                   | 3      | 3       | 2                 | 2                  | 7           |      |                  |
| Spear         | 40   | 20    | 1                   | 4      | 4       | 1.5               | 1.5                | 7           |      |                  |
| Pike          | 80   | 25    | 1                   | 5      | 5       | 1.5               | 1.5                | 9           |      |                  |
| Sarissa       | 160  | 35    | 1                   | 7      | 3       | 2                 | 2                  | 12          |      |                  |
| Sling         | 15   | 250   | 0                   | 3      | 1       | 1.8               | 1                  | 60          | 25   | 7                |
| Javelin       | 100  | 125   | 0.5                 | 6      | 2       | 1.5               | 1                  | 20          | 3    | 5                |
| Atlatl        | 150  | 175   | 0.5                 | 8      | 1       | 2                 | 1                  | 70          | 8    | 6                |
| Shortbow      | 75   | 300   | 0.5                 | 4      | 1       | 2                 | 1                  | 70          | 15   | 10               |
| Bow           | 125  | 350   | 0.5                 | 5      | 1       | 2                 | 1                  | 80          | 15   | 12               |
| Longbow       | 200  | 400   | 0.5                 | 6      | 1       | 2.5               | 1                  | 90          | 15   | 14               |
| Crossbow      | 250  | 450   | 1.5                 | 10     | 1       | 1                 | 1                  | 200         | 15   | 20               |
| Sling Staff   | 60   | 300   | 0                   | 5      | 2       | 2                 | 1                  | 60          | 20   | 12               |
| Cloth Armor   | 100  |       | 0                   |        | 2       |                   | 0.5                |             |      |                  |
| Padded Armor  | 200  |       | 0                   |        | 3       |                   | 0.5                |             |      |                  |
| Leather Armor | 300  |       | 0                   |        | 4       |                   | 0.4                |             |      |                  |
| Wood Armor    | 300  |       | 0                   |        | 5       |                   | 0.3                |             |      |                  |
| Chainmail     | 1000 |       | 1                   |        | 8       |                   | 0.25               |             |      |                  |
| Plate         | 2000 |       | 2                   |        | 12      |                   | 0.15               |             |      |                  |
|               |      |       |                     |        |         |                   |                    |             |      |                  |

#Religion
Religions can be either monotheistic or polytheistic, but this affects nothing game mechanics wise.
A monotheistic religion will only have one god (of "everything"), but a polytheistic religion will have some random number of gods, whose domains can be any of the following (and they can have up to 4 domains): fire, wind, water, air, lightning, death, children, fertility, harvest, wisdom, war, smithing, animals, earth, rivers. Each god will have an importance score, ranging from 0 (so unimportant it literally affects nothing) to 10 (it pretty much determines the outlook of the entire religion).

The domains of a religion's gods affects the nation's tolerance. For example, a religion who reveres a death god, a war god, and a fire god, especially ones with high importance, will be less tolerant than another religion which reveres important gods of peace, wisdom, and knowledge. However, a religion could revere a god of lesser importance of peace and a god of greater importance of war, making the religion more moderate. Below is a list of all the tolerant domains, and all the intolerant domains. Many domains currently affect nothing, and are entirely neutral.

Tolerant: 'peace', 'wisdom', 'children', 'knowledge'
Intolerant: 'war', 'fire', 'death', 'lightning', 'wind'

The only important statistic of a religion is its tolerance. A religion has a base tolerance anywhere from 1 to 100. This is then modified by the god's domains. More tolerant religions will be less likely to start holy wars (but not normal wars) with other nations, and will be more likely to start trade agreements with other nations. They are also more likely to take the names of captured cities as their own.

Additionally, religions change over time. A god that was once known as a war god can also become a fire god (or even a peace god), even losing his original domain of war although. Pantheons can also gain more gods (unless it's a monotheistic religion, and religions don't switch from monotheism to polytheism or vice versa, at the moment) and lose gods.

#Language
I'm no linguist, so the way the languages are created is probably not at all right, but here it is:

Each language has a list of:
- Letters (letters can appear more than once to change their frequency)
- Starting letters (these are the only letters than can appear at the beginning of words)
- Ending letters (same as above, but for the end)
- Letter sections (such as 'ae' or 'or', just combinations of letters that should appear commonly)
- Vowels. This is just a list of all of the vowels in the letters we chose before
- A vowel frequency. This is just how commonly vowels appear in words
- Names (first and last). These are just like normal words, except they're saved. New names are occasionally generated

Steps to create a new word:

1. Input a rough length for the word (e.g. 10 could produce or a word that's 11 letters or 9 or whatever, just roughly 10
2. Choose a starting letter from the above list. This is the first letter of the word
3. Fill the middle of the words with either vowels or a letter section.
4. End the word with one of the letters in the ending letters list

#Art Details
Each art type has an associated list of possible titles/subjects (they're the same thing, at the moment).
The possibilities are listed below.

Every word will either be a tag (enclosed in angle brackets), or some text not enclosed in angle brackets. Text that is not enclosed in angle brackets is simply whatever it says (for example 'hello' is just 'hello').

Note: If anyone is interested in contributing to the lists of words, that would be pretty swell.
Tags (most randomly choose between the options):

- `<paint>`
    - A type of paint, currently one of: tempera, oil, watercolor.
- `<medium>`
    - An artistic medium, such as canvas, wood, paper, et cetera.
- `<sketch>`
    - Either pencil or charcoal (sketching materials).
- `<material>`
    - A material that statues are commonly made of out (marble, wood, bronze)
- `<animal>`
    - An animal. This list is not extensive, and will frequently be extended.
- `<nature>`
    - Something that is not an animal in nature (includes things like wind, the ocean, and trees).
- `<philosophy>`
    - Philosophies (modernism, stoicism). Also not an extensive list.
- `<notable_person>`
    - A notable person from the same country as the artist.
- `<notable_person_role>`
    - A notable person from the same country as the artist, and also their role (ex. John the writer)
- `<god>`
    - A god from the pantheon of the artist's home country.
- `<name>`
    - A randomly generated name, created from the language of the artist's home country.
- `<art>`
    - A work of art from the artist's home country, not necessarily created by the artist himself, with the title in quotes.
- `<art_creator>`
    - Same as <art>, except includes the creator's name (ex. Botticelli's 'Birth of Venus', Dali's 'Persistence of Memory')
- `<place>`
    - The name of some city in the world.
- `<nation_place>`
    - The name of some city in the artists home country.
- `<n>`
    - A noun. This list is not extensive.
- `<v>`
    - A present tense verb, conjugated for singular subjects (ex. speaks, rather thank speak, spoke, spoken)
- `<prep>`
    - A preposition (in, with, around). Not extensive.
- `<ppart>`
    - A past participle (spoken, talked, sung). Not extensive.
- `<gerund>`
    - A gerund. (speaking, talking, singing). Not extensive.
- `<adj>`
    - An adjective.
- `<article>`
    - An article (definite or indefinite).
- `<indef>`
    - An indefinite article ('a' or 'an' depending on the first letter of the next word.)
- `<cap>`
    - Capitalizes the first letter of the next word.
- `<option1|option2|option3>`
    - Chooses one of the options.
- `<option1,option2,option3>`
    - Chooses at least one of the options. Options can be left empty, to leave a chance to choose nothing (`<option1,,option2>`).

For example:
`<cap><article> <Tale|Story> of <notable_person|god|notable_person_role|place>`

Will generate an article, capitalize the first letter, then choose either 'Tale' or 'Story', then choose a notable person, god, notable person and their role, or a city from the world. It doesn't actually execute in that order, but that's not particularly important.

This could generate (assuming Zeus is in the gods list, Robin Hood is in the notable person list, or London is in the place list):
The Tale of Zeus OR
A Story of Robin Hood OR
The Story of London

The possible titles for art are listed below:

- Landscape
    - `<cap><nature>`
- Portrait
    - `<cap><god|notable_person|notable_person_role>`
- Allegorical
    - `<cap><taste|touch|smell|hearing|sight>`
- Statue
    - `<cap><god|animal|notable_person|notable_person_role>`
- Song
    - `<cap><animal|nature|n|god|name|notable_person|notable_person_role>`
- Musical
    - `<Sir,> <name>`
    - `The <Tale|Story|Song> of <notable_person|god|notable_person_role|place>`
    - `The <Song|Story> of the <cap><animal>`
    - `<name|notable_person|notable_person_role> in <place>`
    - `<name|notable_person|notable_person_role>`
    - `The <cap><n> of <name|notable_person|notable_person_role>`
- Play
    - `The Tale of <notable_person|god|notable_person_role>`
    - `The Story of the <cap><animal>`
    - `<name|notable_person|notable_person_role>`
    - `The <cap><n> of <name|notable_person|notable_person_role|place>`
- Novel
    - `<cap><article> <Tale|Story> of <notable_person|god|notable_person_role|place>`
    - `The Story of the <cap><animal>`
    - `<cap><article> <adj,> <cap><n>`
    - `<cap><article> <gerund,> <cap><n>`
    - `<name|notable_person|notable_person_role>`
    - `<cap><place>`
    - `The <cap><n> of <name|notable_person|notable_person_role>`
    - `<name|notable_person|notable_person_role> with <name|notable_person|notable_person_role>`
- Essay
    - `<On|Concerning> the <cap><animal|nature|philosophy>`
    - `A Critique of <cap><philosophy|art>`
    - `<cap><philosophy> in <cap><art|art_creator|philosophy|art>`
    - `<Defending|Against> <cap><art|art_creator|philosophy>`
    - `The <Rise|Fall> of <cap><philosophy>`
    - `Letter from <place>`
- Poem
    - `<cap><animal|nature>`
    - `<Ode|Song> <on|to> <notable_person|god|place>`
    - `<Ode|Song> <on|to> <article> <animal|nature>`
    - `<cap><gerund> <indef> <cap><n>`
    - `<cap><article> <adj,> <cap><n>`
    - `<name|notable_person|notable_person_role>`
    - `The <cap><n> of <name|notable_person|notable_person_role>`
