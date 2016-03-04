# Installation
You will need Python 2.7 (preinstalled on OS X and some Linux (I think, don't know for sure, but I'm sure you can handle it)). If you're using Windows just go to [link]https://www.python.org/[/link] and get 2.7.

All you need to do then is navigate to the place where you uncompressed it, and type the following:

```
python history_generator.py
```

The simulation will then just run. Read the mechanics below for more information.

#Planned Features
1. Add a different speed/size to soldiers
2. Morale for armies
3. Generals for armies
4. Alliances, defensive pacts, non-aggression pacts, et cetera
5. Add more resources
6. Add terrain
7. Saving
8. Research

#Mechanics Overview
At the beginning, the game generates a number of nations. Each of these has their own languages (see language below), name, public offices, cities, and army.

Nations also have several base stats, a tax rate, morale (revolts will start to occur when this is too low, usually happens when losing a war), army spending (this is an amount that dictates how much money is put into recruiting soldiers).

Cities are founded by nations when they have the money, but can also be obtained by conquest. Every once in a while, nations will go to war with each other, and fight battle when they think they can win. When a battle begins, a new screen will pop up with little circles in the color of the nations, representing each soldier.

Both armies deploy all of their soldiers. Soldiers are organized into units (the size of which is determined by the unit type). Ranged units do not move, only shoot. However, ranged units will transition to melee once they run out of ammunition or if the enemy units get too close. Melee units will essentially ram themselves into their enemy until one of them dies.

When melee combat occurs, both soldiers roll for their attack/defense (0 to a max of their strength), with another random roll (0 to their fatigue / 2), and subtract the two. This means that while a soldier with a strength of 20 will almost always beat a soldier with a strength of 1, the soldier with a strength of 1 is able to win. After the fight, there is a 1 in the unit's discipline (1 in 5 if the unit has 5 discipline) chance that the unit's fatigue will go up. Therefore, if the soldier with 20 strength has fought a lot, it will become much weaker so a strength 20 soldier cannot simply destroy an entire army (like they used to be able to), although a 20 strength soldier will be able to take out a considerable number of enemies of strength 1. Whichever soldiers loses, loses 1 health, and when their health is 0, they will be removed from their unit/the army.

For ranged units, there is a counter which determines when they can shoot. It goes from 0 to 60, and is incremented a random amount, anywhere from 0 to the square root of the unit's discipline, every step. When the projectile is shot, it is directed at a single target, and if it doesn't hit it, it doesn't hit any other soldier either. Assuming it does hit, the projectile will have a base damage of 0 to the strength of unit that shot it. This, however, will be decreased by another random roll of the defending unit, which is a roll of 0 to its fatigue / 2 subtracted by a roll of 0 to its strength. The damage obviously cannot go below 0 or above the original damage roll of the projectile.

When an army has no more units, the battle will end (they are always fights to the death of the entire army. I know its not entirely realistic, but this is much easier to implement and I plan to implement morale for armies at a later date (if its no longer on the to-do list, assume I've done it and I'm just too lazy to change this description)). The winning (only if the attackers, of course) army conquers a single city from the losers and all of it's production, improvements, et cetera will now contribute to the conquering nation. Additionally, the winners will gain morale, and the losers will lose morale.

#Nation
A group of cities all joined together with armies to attack and trade with other nations.

The nation also shares a common religion (and this doesn't change, there is no conversion yet) and language.

Nations have government offices and people in those offices. Currently, all offices last for life, and they modify the following three stats in varying degrees (the people in office also affect the office, increasing or decreasing the multipliers): tax rate, army spending, and morale.

Nations have a capital city which will give more morale to the enemy when captured. Additionally, when a nation loses its capital, it will lose more morale, but while it owns its capital, it will gain morale every year.

#City
Cities are the building blocks of nations. Each city contains some amount of people, some amount of land (organized into cells), produces and consumes food, and builds buildings.

There are two types of cells. They can either be a "city" cell or a "surrounding" cell. City cells can support 1000 people, and represent the inner part of cities where all the houses, markets, et cetera, are. They look like a square with a border around it. Surrounding cells are the surrounding countryside, where all the farms, and other agricultural buildings are located. They can support 10 people each. Naturally, it takes a lot of surrounding farmland to support one city tile, which is why the vast majority of tiles are surrounding cells.

Cities contain buildings as well. There following are the types of buildings and their associated bonuses/costs:
- Houses: Population capacity: 100, Tax rate: x1.001, Cost: 100
- Farm: Population capacity: 10, Food output: 100, Cost: 200
- Fishery: Population capacity: 5, Food output: 150, Cost: 200
- Ranch: Population capacity: 5, Food output: 200, Cost: 300
- Mine: Population capacity: 20, Money output: 500, Cost: 600
- Market: Tax rate: x1.01, Money output: 1000, Cost: 1500

#Army
A tree of unit types/numbers.

Units have three main stats, strength, health, and discipline. Additionally, they can either be ranged, or not ranged. Discipline only currently affects ranged units (higher disciplines means soldiers will tend to shoot faster).

Ranged unit do not move until they are out of ammo, at which point they switch to melee. If you see projectiles flying through large amounts of enemies, this is because the projectile is only targeting one enemy (runs WAY faster this way). Just imagine it was a really bad shot.

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
- Starting letters (their are the only letters than can appear at the beginning of words)
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
