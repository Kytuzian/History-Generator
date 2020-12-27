# Installation
You will need Python 3 (tested with 3.8.5, hopefully works with others).
If you're using Windows just go to [https://www.python.org/](https://www.python.org) and download Python 3.
If you are on Linux you may need to install Tkinter separately; on Ubuntu with `apt` you can run `sudo apt install python3-tk`.

Then, all you need to do then is navigate to the place where you downloaded it, and type the following:

```
python history_generator
```

The simulation will then just run. Read the mechanics below for more information.

DISCLAIMER:
None of the below information is guaranteed to be current/accurate at any point, although I will try to update it.

# Mechanics Overview
At the beginning, the game generates a number of nations. Each of these has their own languages (see language below), name, religion, cities, armies in each of those cities, notable people, and works of art.

Nations also have several base stats, a tax rate, morale (revolts will start to occur when this is too low, usually happens when losing a war), army spending (this is an amount that dictates how much money is put into recruiting soldiers).

Cities are founded by nations when they have the money, but can also be obtained by conquest. Every once in a while, nations will go to war with each other, and fight battle when they think they can win. The chance of a nation going to war with another nation increases when the tolerance of their religion is low (affected by both the gods in their religions pantheon, by a base tolerance, and by the various statistics of priests within the nation (although these can also increase the tolerance of the religion)). When a battle begins, a new screen will pop up with circles in the color of the nations, representing each soldier.

Both armies deploy some of their soldiers (the exact number depends on the battle size set in battle.py), in the proportion to each other's army. For example, if one nation has 1000 troops, the other has 10, and the battle size is 350 (as it is at the time of writing), the first nation will deploy 350 troops, and the second nation will deploy only 3, thereby maintaining the 100 to 1 ratio. Soldiers are organized into units (the size of which is determined by the unit type). Units will attempt to maintain their ranks as they move. Ranged units will only move under one of two conditions. One, that they are out of ammunition, and two, if there is an enemy unit that is too close to them. Both of these scenarios will cause the soldiers to switch to their melee weapon.

When melee combat occurs, both soldiers roll for their attack/defense (0 to a max of their strength), with another random roll (0 to their fatigue / 2), and subtract the two. The soldier's weapon affects this, as well as the best material that the nation the soldier is from has researched. This means that while a soldier with a strength of 20 will almost always beat a soldier with a strength of 1, the soldier with a strength of 1 is able to win. After the fight, there is a 1 in the unit's discipline (1 in 5 if the unit has 5 discipline) chance that the unit's fatigue will go up. Therefore, if the soldier with 20 strength has fought a lot, it will become much weaker so a strength 20 soldier cannot simply destroy an entire army (like they used to be able to), although a 20 strength soldier will be able to take out a considerable number of enemies of strength 1. Whichever soldiers loses, loses 1 health, and when their health is 0, they will be removed from their unit and from the army.

For ranged units, there is a counter which determines when they can shoot. It varies from weapon to weapon, and is mostly affected by the square root of their discipline, although it does have a small random component to it. When the projectile is shot, it is directed at a single target, and if it doesn't hit it, it doesn't hit any other soldier either. Assuming it does hit, the projectile will have a base damage of 0 to the strength of unit that shot it. This, however, will be decreased by another random roll of the defending unit, which is a roll of 0 to its fatigue / 2 subtracted by a roll of 0 to its strength. The damage obviously cannot go below 0 or above the original damage roll of the projectile.

When an army has no more units, the battle will end (they are always fights to the death of the entire army. I know it's not entirely realistic, but this is much easier to implement and I plan to implement morale for armies at a later date (if its no longer on the to-do list, assume I've done it and I'm just too lazy to change this description)). The winning (only if the attackers, of course) army conquers a single city from the losers and all of it's production, improvements, et cetera will now contribute to the conquering nation. Additionally, the winners will gain morale, and the losers will lose morale.

# Weapons and Armor
Weapons have several stats: attack, defense, a material multiplier, and both attack and defense skill multipliers. To calculate the attack with a weapon, the user first calculates the effective attack from the weapon. This is done by taking the material multiplier of the weapon and multiplying it by the strength of the material the weapon is made out of. Then the weapon's attack is a random number from 0 to the weapon's effective attack. Then the soldier's strength is multiplied by the attack skill multiplier, and the two values are added.

The process is the same for defense, except with defense values instead of attack values.

For armor, the process is also the same, and armor, naturally, does not contribute to attack.

# Nation
A group of cities all joined together with armies to attack and carvans to trade with other nations.
The nation also shares a common religion (and this doesn't change, there is no conversion yet) and language.
Nations also have a collection of notable people, and a collection of works of art.

Nations have a capital city which will give more morale to the enemy when captured. Additionally, when a nation loses its capital, it will lose more morale, but while it owns its capital, it will gain morale every year.

Nations also have a technology level. The full tech tree is described in the Tech section.

# Notable People
Notable people can be any of the following:

- General: Currently no purpose.
- Priest: Can increase of decrease the tolerance of the nation's religion.
- Oracle: Creates prophesies.
- Artist: Creates works of art: both drawings and statues.
- Writer: Creates works of literature (which counts as art): plays, novels, essays, poems, and myths.
- Composer: Creates works of art: both songs and musicals.
- Philosopher: Creates works of art: just essays.
- Scientist: Increases the nation's research rate.
- Revolutionary: Decreases the morale of the nation, increasing the chance for a rebellion.
- Hero: Currently no purpose.
- Administrator: Increase the tax rate.

# Art
This includes literature, music, as well as "normal" visual arts (paintings, statues, et cetera).

See the Art Detail section for more information.

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

# City
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

# Battles
There are four main components of battles: soldiers, projectiles, units, and the battle itself.
- Soldiers
    - Each soldier belongs to a unit (see below for more details).
    - Each soldier has a name, health, strength, two weapons, a type of armor, a discipline, a fatigue, and an ammunition.
    - Targeting
        - Just randomly choose a target from the targeted unit until it dies, then choose a new one
    - Reloading
        - All weapons have a cooldown (which can be found in the table below).
        - For ranged units this is the frequency that they can shoot.
        - For melee units this is how quickly they can swing their weapons.
        - The reload rate is partially random, and is affected by the discipline of the unit, but is mostly constant.
        - The exact formula is as follows: The reload counter increases by half of the square root of the discipline plus a random number (either 0 or 1) plus one.
    - The line that comes out of each soldier shows it's melee weapon range (if it's using a ranged weapon, the line will not show, so you can tell what mode they're in).
    - Step
        - Melee
            - When a soldier attacks or defends with a melee weapon, several factors go in it.
            - This is their fatigue, the weapon they're using, the material of that weapon (currently just the best material available to the empire) and their strength.
            - If they're defending, then it also includes the armor they're using/the material of that armor.
            - The fatigue loss is a number from 0 to half the fatigue.
            - See the section on weapons and armor for the corresponding numbers (it's in the section about research/technology).
            - Finally the base attack is the weapon's skill multiplier times a random number from 0 to the soldier's strength.
            - The reasoning is that this would allow even the best soldier to fail to kill a weaker one (as they would in real life).
            - Their resulting value is the sum of all the factors minus the fatigue loss.
            - If that value is 0, then their actual result is a random number that is either 0 or 1.
            - If the attack value is greater than the defense value, then the defending soldier will lose one health, if it is the same, then nothing will happen.
            - After each attack/defense, the soldier has a 1 in their discipline value chance to increase their fatigue by 1.
        - Ranged
            - If the unit is in range and fully reloaded, then they will launch a projectile (see the projectile section for more details).
            - The position of their target in the future is calculated exactly (assuming their don't change direction, of course).
            - They lose one ammo for each projectile launched.
            - When a soldier is hit by a projectile, they use their ranged defense, not their melee defense.
            - This is different only in that the weapon defense doesn't count (because generally speaking, it's very difficult to like, cut an arrow or crossbow bolt out of the air, and you're never going to poke a sling stone out of the air with a spear).
            - The strength of a ranged attack depends on all the same things as the strength of a melee attack, except that it is halved at the end, so that ranged weapons aren't TOO powerful.
- Projectiles
    - Each projectile basically has a speed, a radius, and a strength.
    - In order to make the simulation faster, they also have a range of time that they cannot do damage, this half the anticipated time it takes to get to the target, and twice the anticipated time it takes to get to the taget. For example, if it should take about 10 seconds to get to the target, then they don't check for hits for the first five seconds or any time after twenty seconds.
    - You might exclaim, but what if it hits a different soldier/unit? Well it doesn't matter, because projectiles only target one soldier, and ignore all others. This accounts for projectiles you see flying through the soldiers. It's unfortunate, but it's way too slow to check collisions with every unit at every point, so I don't really know what else to do. A consequence of this is that, if the unit the projectile is targeting dies, the projectile itself will simply disappear (in case you've been seeing that and wondering what that's all about).
    - When a projectile hits a soldier, the damage done is equal to the projectile's strength.
    - However, this is reduced by the defense of the soldier that it hits, calculated using the ranged defense mentioned above.
    - The defending soldier's fatigue will increase, in the same way that it does for melee attacks.
- Units
    - Each unit has a speed, a number of soldiers, and a certain arrangement of their ranks, and that's pretty much it.
    - The main function of a unit is to provide targeting for their soldiers, and to keep them moving in those nice ranks rather than becoming a blob of people.
    - The close combat range is 50 by default, this means that s
    - Units will periodically, but randomly, switch targets to the closest unit to them. This is because while at the beginning of the battle, the closet unit might be some ranged unit far away, but now there's a group of people with swords charging at the unit, and that's probably just a tad more pressing. However, it doesn't happen every step because that slows it down more, and it's barely noticable.
- Battle
    - There is only one control, the battle speed, which controls the number of milliseconds between each step. Generally, however, you will reach a point at which decreasing the time between steps doesn't actually speed up the battle (especially in larger battles), this is due to the simulation taking up too much time to calculate each new step.
    - Battles are always between two armies, and always continue until the entirety of one side is killed.
    - Each battle always takes place in a city, there are no battles in the field (while this isn't entirely realistic, it is easier, and I believe most battles in history did take place at cities, rather than in the field in any case).
    - I plan to add fortifications and such for the defenders in the future, but for now, there is no difference between the two sides.
    - Set up
        - At the beginning of the battle, units are randomly placed on their side (either the top half or bottom half) of the field (the screen).
        - The number of troops placed depends on the battle size (the default is 350), because having thousands of soldiers on the screen at once only serves to add to the lag of battles.
        - This doesn't mean that each side gets 350, because the number deploy is proportional to the total number of troops that each nation brought. Obviously it wouldn't be fair if a nation bringing only 350 troops got to fight the 350 troops of their enemy who actually had another 10000 in reserve, because one side should vastly outnumber the other.
        - The battle size is calculated by letting the larger side just automatically have 350 troops out, and then the smaller side is 350 times the ratio of the size of the armies. For example, if one nation has 500 soldiers and the other 1000, the side with 1000 gets to have 350 troops out a time, and the side with 500 gets to have half of that, 175.
        - Soldiers are deployed from the lowest tiers up (because obviously losing peasants isn't nearly as bad as losing, like, important people).
    - Every step the following things happen, in order:
        - The projectiles for each side are handled.
        - The units (and therefore the soldiers) for each side are handled (this include movements, attacking, targeting, and the like).
        - Then the game checks if there should be more reinforcements added to the battle for either side, and if there should, it does it.
        - Finally, if all the soldiers on one side are dead, then the battle is over.
    - When the battle ends, if the attackers won, they incorporate the city into their empire and send back the levied troops to their city of origin (we'll discuss movies armies in a future video).
    - If the defenders won, their levies simply rejoin the rest of the population.

- Stats
    - The simulation keeps track of several stats for each battle, troop type, and weapon.
    - These stats will be used in the future by the AI to make decisions on which weapons they want their soldiers to wield.
    - For battles, this is the troops brought by each side, the number of troops killed, the projectiles launched and the projectiles hit, and the number of melee attacks won.
    - For troop types, it is the number of melee attacks made, the number of melee attacks won, the number of enemies killed, the number of soldiers that died, and the numbers of projectiles launched and hit.
    - For weapons, it is just the attacks made, the attacks won, and the number of soldiers killed. However, attacks in this case can be either melee or ranged, depending on the type of the weapon.
- Optimization
    - This is one of the slowest parts of the simulation at the moment, so if anyone has any ideas about optimization or wants to actually contribute to the code, that'd be great.

# Weapons and Armor


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

# Religion
Religions can be either monotheistic or polytheistic, but this affects nothing game mechanics wise.
A monotheistic religion will only have one god (of "everything"), but a polytheistic religion will have some random number of gods, whose domains can be any of the following (and they can have up to 4 domains): fire, wind, water, air, lightning, death, children, fertility, harvest, wisdom, war, smithing, animals, earth, rivers. Each god will have an importance score, ranging from 0 (so unimportant it literally affects nothing) to 10 (it pretty much determines the outlook of the entire religion).

The domains of a religion's gods affects the nation's tolerance. For example, a religion who reveres a death god, a war god, and a fire god, especially ones with high importance, will be less tolerant than another religion which reveres important gods of peace, wisdom, and knowledge. However, a religion could revere a god of lesser importance of peace and a god of greater importance of war, making the religion more moderate. Below is a list of all the tolerant domains, and all the intolerant domains. Many domains currently affect nothing, and are entirely neutral.

Tolerant: 'peace', 'wisdom', 'children', 'knowledge'
Intolerant: 'war', 'fire', 'death', 'lightning', 'wind'

The only important statistic of a religion is its tolerance. A religion has a base tolerance anywhere from 1 to 100. This is then modified by the god's domains. More tolerant religions will be less likely to start holy wars (but not normal wars) with other nations, and will be more likely to start trade agreements with other nations. They are also more likely to take the names of captured cities as their own.

Additionally, religions change over time. A god that was once known as a war god can also become a fire god (or even a peace god), even losing his original domain of war although. Pantheons can also gain more gods (unless it's a monotheistic religion, and religions don't switch from monotheism to polytheism or vice versa, at the moment) and lose gods.

# Language
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

# Art Details
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
