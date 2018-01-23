from tech.armor import Armor
from tech.mount import Mount
from tech.weapon import Weapon

# TODO: Reintroduce, once mechanics are clearly defined
# trebuchet = Weapon('Trebuchet', 950, 600, 1.5, 60, 1, 1, 1, reload_time=800/2, ammunition=5, projectile_speed=30, siege_weapon=True, projectile_size=20)
# scorpio = Weapon('Scorpio', 700, 500, 1.5, 40, 1, 1, 1, reload_time=700/2, ammunition=20, projectile_speed=60, siege_weapon=True, projectile_size=7)
# ballista = Weapon('Ballista', 600, 500, 1.5, 42, 1, 1, 1, reload_time=800/2, ammunition=20, projectile_speed=50, siege_weapon=True, projectile_size=9)
# onager = Weapon('Onager', 750, 550, 1.5, 50, 1, 1, 1, reload_time=700/2, ammunition=10, projectile_speed=25, siege_weapon=True, projectile_size=19)
# mortar = Weapon('Mortar', 850, 600, 1.5, 55, 1, 1, 1, reload_time=750/2, ammunition=10, projectile_speed=20, siege_weapon=True, projectile_size=17)
# cannon = Weapon('Cannon', 1000, 650, 1.5, 60, 1, 1, 1, reload_time=1000/2, ammunition=10, projectile_speed=45, siege_weapon=True, projectile_size=18)
# catapult = Weapon('Catapult', 750, 530, 1.5, 60, 1, 1, 1, reload_time=600/2, ammunition=30, projectile_speed=25, siege_weapon=True, projectile_size=19)

# Short
unarmed = Weapon('Unarmed', 0, 5, 0, 1, 1, 1, 1, reload_time=1, armor_pierce=-1)
dagger = Weapon('Dagger', 10, 5, 1.5, 2, 2, 1.1, 1, reload_time=2, armor_pierce=1)
rondel = Weapon('Rondel', 25, 5, 1.6, 3, 1, 1.5, 1, reload_time=2)
dirk = Weapon('Dirk', 25, 5, 1.6, 3, 1, 1.5, 1, reload_time=2)
kopis = Weapon('Kopis', 40, 6, 1.8, 6, 1, 2, 1, reload_time=3, armor_pierce=-1)
shortsword = Weapon('Shortsword', 50, 7, 1.8, 5, 2, 2, 1.1, reload_time=4, armor_pierce=-1)
club = Weapon('Club', 10, 7, 0, 5, 2, 1, 1, reload_time=6)
hammer = Weapon('Hammer', 25, 7, 1.3, 6, 1, 1.5, 0.8, reload_time=5, armor_pierce=1)
mace = Weapon('Mace', 40, 7, 1.5, 6, 1, 1.8, 1.0, reload_time=5, armor_pierce=1)
morning_star = Weapon('Morning Star', 200, 7, 1.5, 8, 0, 2, 0.2, reload_time=10, armor_pierce=1)
tanto = Weapon('Tanto', 25, 5, 1.8, 2, 1, 1.8, 1, reload_time=3)
hatchet = Weapon('Hatchet', 15, 4, 1.8, 2.5, 1, 1.6, 1, reload_time=2, armor_pierce=-1)
falchion = Weapon('Falchion', 40, 5, 1.5, 8, 1, 1.25, 1, reload_time=6, armor_pierce=-1)
cleaver = Weapon('Cleaver', 35, 5, 3, 8, 0, 0.5, 0, reload_time=6, armor_pierce=1)
sickle = Weapon('Sickle', 10, 3, 1.4, 1, 2, 1, 1.25, reload_time=1, armor_pierce=-1)
war_axe = Weapon('War Axe', 50, 8, 1.8, 10, 0, 1.2, 0.5, reload_time=12)
battle_axe = Weapon('Battle Axe', 65, 9, 1.4, 12, 0, 1.0, 0.35, reload_time=14, armor_pierce=1)
knife = Weapon('Knife', 5, 5, 0.45, 1.5, 0.5, 1.5, 0.5, reload_time=1, armor_pierce=-1)
hand_axe = Weapon('Hand Axe', 10, 7, 0.6, 2.2, 0.9, 1.9, 0.9, reload_time=8, armor_pierce=-1)

# Medium
pick = Weapon('Pick', 20, 7, 2.2, 4, 1, 1, 1, reload_time=8, armor_pierce=1)
macuahuitl = Weapon('Macuahuitl', 60, 9, 3.0, 6, 1.25, 1.5, 1, reload_time=8)
katana = Weapon('Katana', 125, 11, 2.4, 7, 0.25, 2, 0.25, reload_time=4, armor_pierce=-1)
sabre = Weapon('Sabre', 50, 9, 1.8, 7, 0.5, 2.35, 1, reload_time=3)
rapier = Weapon('Rapier', 100, 10, 1.5, 5, 0, 5, 0.2, reload_time=5, armor_pierce=1)
arming_sword = Weapon('Arming Sword', 100, 8, 2, 6, 3, 2, 1.1, reload_time=5)
bastard_sword = Weapon('Bastard Sword', 150, 12, 2.3, 7, 2, 2, 1.5, reload_time=6)
claymore = Weapon('Claymore', 200, 15, 2.5, 10, 1, 2.5, 0.5, reload_time=7, armor_pierce=1)
bill = Weapon('Bill', 50, 12, 1.5, 6, 4, 1.5, 1.5, reload_time=8, armor_pierce=1)
flail = Weapon('Flail', 50, 12, 1.2, 6, 0, 2, 0.5, reload_time=12, armor_pierce=1)
falx = Weapon('Falx', 75, 14, 1.8, 8, 1, 2, 0.8, reload_time=7, armor_pierce=-1)
great_axe = Weapon('Great Axe', 100, 14, 1.4, 10, 0, 2, 0.5, reload_time=10)
war_hammer = Weapon('War hammer', 250, 14, 1.6, 15, 0, 2, 0, reload_time=13, armor_pierce=1)
short_spear = Weapon('Short Spear', 50, 10, 1.2, 5, 2, 1.8, 1.2, reload_time=9, armor_pierce=1)
scimitar = Weapon('Scimitar', 80, 10, 2.0, 5, 0, 2, 0.5, reload_time=4, armor_pierce=-1)
estoc = Weapon('Estoc', 175, 12, 2.2, 8, 2, 1, 1.5, reload_time=8)
gladius = Weapon('Gladius', 120, 8, 1.8, 7, 1, 2, 1.5, reload_time=7)
daikatana = Weapon('Dai Katana', 220, 12, 1.8, 7, 0, 2.5, 0.5, reload_time=8, armor_pierce=-1)
nodachi = Weapon('No Dachi', 250, 14, 1.9, 8, 0, 3, 0.5, reload_time=10, armor_pierce=-1)
maul = Weapon('Maul', 235, 13, 1.4, 12, 0, 2, 0.5, reload_time=11)
short_voulge = Weapon('Short Voulge', 140, 13, 1.7, 8, 1, 1.4, 1.2, reload_time=10)
zweihander = Weapon('Zweihander', 350, 14, 2.0, 10, 0.2, 2, 0.5, reload_time=9, armor_pierce=1)
flamberge = Weapon('Flamberge', 320, 14, 2.0, 9, 0.5, 2.5, 0.2, reload_time=8)
clamshell = Weapon('Clamshell', 300, 14, 2.0, 8, 3, 1.7, 1.2, reload_time=8, armor_pierce=-1)
longsword = Weapon('Longsword', 160, 14, 2.0, 8, 2.5, 1, 1, reload_time=7)
goedendag = Weapon('Goedendag', 20, 11, 1.1, 4, 2, 1.5, 1, reload_time=7, armor_pierce=1)

# Long
polehammer = Weapon('Polehammer', 100, 15, 1.0, 8, 2, 2, 1, reload_time=11, armor_pierce=1)
staff = Weapon('Staff', 20, 7, 1.0, 1, 1, 2, 2, reload_time=7)
spear = Weapon('Spear', 40, 20, 1.0, 4, 4, 1.5, 1.5, reload_time=7, armor_pierce=1)
pike = Weapon('Pike', 80, 25, 1.0, 5, 5, 1.5, 1.5, reload_time=9, armor_pierce=1)
sarissa = Weapon('Sarissa', 160, 35, 1.0, 7, 3, 2, 2, reload_time=12)
halberd = Weapon('Halberd', 140, 20, 1.0, 8, 2, 2, 1, reload_time=12, armor_pierce=1)
poleaxe = Weapon('Poleaxe', 90, 14, 1.0, 6, 2, 2, 1, reload_time=10, armor_pierce=-1)
bardiche = Weapon('Bardiche', 120, 15, 0.8, 10, 1, 1, 0.6, reload_time=11, armor_pierce=1)
voulge = Weapon('Voulge', 105, 15, 0.9, 8, 1, 1.5, 0.8, reload_time=9)
naginata = Weapon('Naginata', 220, 14, 2, 4, 0.5, 3, 1.5, reload_time=8, armor_pierce=-1)
war_spear = Weapon('War Spear', 170, 18, 1.4, 8, 0.3, 0.5, 0.5, reload_time=11)
sledgehammer = Weapon('Sledgehammer', 150, 14, 0.6, 20, 0.6, 2, 0.3, reload_time=13)
glaive = Weapon('Glaive', 100, 16, 0.8, 9, 0.6, 1.5, 1.5, reload_time=8)
lance = Weapon('Lance', 180, 23, 1.5, 9, 1, 2, 1, reload_time=11, armor_pierce=1)

# Shields
shield = Weapon('Shield', 10, 3, 1.5, 1, 5, 1, 2, reload_time=10, shield=True)
leather_shield = Weapon('Leather Shield', 20, 3, 0.5, 1.5, 6, 1, 2, reload_time=10, shield=True)
wooden_shield = Weapon('Wooden Shield', 35, 3, 0.5, 2, 8, 1, 2, reload_time=10, shield=True)
buckler = Weapon('Buckler', 50, 3, 2, 1.5, 3, 1, 5, reload_time=8, shield=True)
round_shield = Weapon('Round Shield', 100, 3, 2, 1.5, 10, 1, 4, reload_time=10, shield=True)
kite_shield = Weapon('Kite Shield', 150, 3, 1.5, 1, 12, 1, 3, reload_time=12, shield=True)
heater_shield = Weapon('Heater Shield', 70, 3, 1.5, 3, 8, 1, 4, reload_time=10, shield=True)
board_shield = Weapon('Board Shield', 125, 3, 1, 1, 15, 1, 2.5, reload_time=13, shield=True)
tower_shield = Weapon('Tower Shield', 150, 3, 1.5, 0.5, 20, 1, 2, reload_time=18, shield=True)
pavise = Weapon('Pavise Shield', 200, 3, 1.5, 0.75, 25, 1, 2, reload_time=15, shield=True)

all_melee_weapons = [unarmed, pick, hatchet, macuahuitl, falchion, sabre, cleaver, sickle, katana, war_axe, battle_axe,
                     knife, hand_axe, war_hammer, short_spear, scimitar, estoc, gladius, daikatana, nodachi, maul,
                     short_voulge, zweihander, flamberge, clamshell, longsword, goedendag, bardiche, voulge, naginata,
                     war_spear, sledgehammer, glaive, lance, tanto, halberd, poleaxe, great_axe, rapier, polehammer,
                     kopis, mace, falx, club, hammer, dagger, rondel, dirk, shortsword, bastard_sword, claymore, spear,
                     staff, bill, pike, sarissa, flail, morning_star]

weapon_list = [tanto, halberd, poleaxe, great_axe, rapier, polehammer, mace, falx, shortsword, bastard_sword, claymore,
               spear, staff, pike, sarissa, flail, morning_star, bill]

sidearm_list = [unarmed, shield, leather_shield, wooden_shield, buckler, round_shield, kite_shield, heater_shield,
                board_shield, tower_shield, pavise, pick, hatchet, falchion, sabre, cleaver, sickle, knife, hand_axe,
                tanto, dagger, club, mace, kopis, hammer, rondel, dirk, staff, shortsword, spear, arming_sword]

basic_weapon_list = [katana, macuahuitl, falchion, sabre, war_axe, battle_axe, goedendag, short_spear, short_voulge,
                     club, mace, hammer, staff, shortsword, spear]

sling = Weapon('Sling', 15, 250, 0, 3, 1, 1.8, 1, reload_time=60, ammunition=25, projectile_speed=7, armor_pierce=-1,
               projectile_size=2)
javelin = Weapon('Javelin', 100, 125, 0.5, 6, 2, 1.5, 1, reload_time=20, ammunition=3, projectile_speed=5,
                 armor_pierce=1, projectile_size=10)
atlatl = Weapon('Atlatl', 150, 175, 0.5, 8, 1, 2.0, 1, reload_time=70, ammunition=8, projectile_speed=6)
shortbow = Weapon('Shortbow', 75, 300, 0.5, 4, 1, 2, 1, reload_time=70, ammunition=15, projectile_speed=10,
                  projectile_size=6)
bow = Weapon('Bow', 125, 350, 0.5, 5, 1, 2, 1, reload_time=80, ammunition=15, projectile_speed=12, projectile_size=8)
longbow = Weapon('Longbow', 200, 400, 0.5, 6, 1, 2.5, 1, reload_time=90, ammunition=15, projectile_speed=14,
                 armor_pierce=1, projectile_size=9)
crossbow = Weapon('Crossbow', 250, 450, 1.5, 10, 1, 1, 1, reload_time=120, ammunition=15, projectile_speed=20,
                  armor_pierce=1, projectile_size=4)
sling_staff = Weapon('Sling Staff', 60, 300, 0, 5, 2, 2, 1, reload_time=60, ammunition=20, projectile_speed=12,
                     armor_pierce=-1, projectile_size=2)
throwing_knives = Weapon('Throwing Knives', 5, 100, 0, 3, 0, 1.8, 1, reload_time=50, ammunition=5, projectile_speed=6,
                         armor_pierce=-1, projectile_size=1)
throwing_axes = Weapon('Throwing Axes', 60, 100, 0, 10, 0, 1.8, 1, reload_time=70, ammunition=3, projectile_speed=5,
                       armor_pierce=-1, projectile_size=3)
throwing_daggers = Weapon('Throwing Daggers', 20, 90, 0, 4, 0, 1.8, 1, reload_time=50, ammunition=5, projectile_speed=6,
                          armor_pierce=-1, projectile_size=2)
jarid = Weapon('Jarids', 60, 150, 0, 4, 0, 1.8, 1, reload_time=60, ammunition=10, projectile_speed=6, armor_pierce=1,
               projectile_size=10)
stones = Weapon('Stones', 0, 80, 0, 1, 0, 1.8, 1, reload_time=30, ammunition=100, projectile_speed=3, armor_pierce=-1,
                projectile_size=1)
darts = Weapon('Darts', 3, 80, 0, 2, 0, 1.8, 1, reload_time=20, ammunition=30, projectile_speed=5, armor_pierce=1,
               projectile_size=1)
pila = Weapon('Pila', 100, 200, 0, 12, 0, 2, 1, reload_time=10, ammunition=3, projectile_speed=6, armor_pierce=1,
              projectile_size=12)
recurve_bow = Weapon('Recurve Bow', 200, 320, 0.8, 7, 1, 3, 1, reload_time=75, ammunition=15, projectile_speed=14,
                     armor_pierce=1, projectile_size=7)
war_bow = Weapon('War Bow', 185, 350, 0.5, 8, 0.5, 2, 0.5, reload_time=80, ammunition=15, projectile_speed=13,
                 armor_pierce=1, projectile_size=8)
self_bow = Weapon('Self Bow', 145, 300, 0.5, 6, 1, 2, 1, reload_time=70, ammunition=15, projectile_speed=12,
                  armor_pierce=-1, projectile_size=6)
hunting_bow = Weapon('Hunting Bow', 105, 280, 0.3, 4, 1, 2.5, 1, reload_time=60, ammunition=15, projectile_speed=10,
                     armor_pierce=-1, projectile_size=4)
arbalest = Weapon('Arbalest', 300, 500, 1.5, 12, 1, 1, 1, reload_time=150, ammunition=15, projectile_speed=30,
                  armor_pierce=1, projectile_size=4)
hunting_crossbow = Weapon('Hunting Crossbow', 200, 400, 1.5, 8, 1, 1, 1, reload_time=100, ammunition=15,
                          projectile_speed=15, armor_pierce=-1, projectile_size=2)
flintlock_pistol = Weapon('Flintlock Pistol', 400, 200, 1.5, 20, 1, 1, 1, reload_time=170, ammunition=15,
                          projectile_speed=30, projectile_size=1)
flintlock_rifle = Weapon('Flintlock Rifle', 600, 380, 1.5, 33, 1, 1, 1, reload_time=250, ammunition=15,
                         projectile_speed=50, armor_pierce=1, projectile_size=1)
matchlock_rifle = Weapon('Matchlock Rifle', 650, 400, 1.5, 35, 1, 1, 1, reload_time=270, ammunition=15,
                         projectile_speed=50, armor_pierce=1, projectile_size=1)
blunderbuss = Weapon('Blunderbuss', 550, 200, 1.5, 50, 1, 1, 1, reload_time=300, ammunition=15, projectile_speed=30,
                     projectile_size=2)
arquebus = Weapon('Arquebus', 700, 400, 1.5, 40, 1, 1, 1, reload_time=300, ammunition=15, projectile_speed=45,
                  armor_pierce=1, projectile_size=1)
musket = Weapon('Musket', 1000, 500, 1.5, 50, 1, 1, 1, reload_time=320, ammunition=15, projectile_speed=60,
                armor_pierce=1, projectile_size=1)

all_ranged_weapons = [musket, arquebus, blunderbuss, matchlock_rifle, flintlock_rifle, flintlock_pistol, arbalest,
                      hunting_crossbow, recurve_bow, war_bow, self_bow, hunting_bow, throwing_knives, throwing_axes,
                      throwing_daggers, jarid, stones, darts, atlatl, sling, shortbow, longbow, javelin, bow, crossbow,
                      sling_staff]

ranged_weapon_list = [musket, arquebus, blunderbuss, matchlock_rifle, flintlock_rifle, flintlock_pistol, arbalest,
                      hunting_crossbow, recurve_bow, war_bow, self_bow, hunting_bow, throwing_knives, throwing_axes,
                      throwing_daggers, jarid, stones, darts, sling, atlatl, javelin, shortbow, longbow, bow, crossbow,
                      sling_staff]

basic_ranged_weapon_list = [hunting_crossbow, hunting_bow, throwing_knives, throwing_axes, throwing_daggers, jarid,
                            stones, darts, sling, javelin, shortbow, bow]

cloth_armor = Armor('Cloth Armor', 100, 0, 2, 0.5)
padded_armor = Armor('Padded Armor', 200, 0, 3, 0.5)
leather_armor = Armor('Leather Armor', 300, 0, 4, 0.4)
wood_armor = Armor('Wood Armor', 300, 0, 5, 0.3)
chainmail = Armor('Chaimail', 1000, 1, 8, 0.25)
plate = Armor('Plate', 2000, 2, 12, 0.15, heavy=True)
gambeson = Armor('Gambeson', 600, 1, 5, 0.35)
hauberk = Armor('Hauberk', 1300, 2, 9, 0.30)
lamellar = Armor('Lamellar', 1700, 2, 10, 0.25, heavy=True)
tunic = Armor('Tunic', 80, 0, 2, 0.45)
robe = Armor('Robe', 50, 0, 1, 1)
fur_coat = Armor('Fur Coat', 10, 0, 1, 0.5)
jerkin = Armor('Jerkin', 100, 0, 3, 0.25)
linen_shirt = Armor('Linen', 20, 0, 0, 0.75)
aketon = Armor('Aketon', 70, 0, 2.5, 0.35)
tabard = Armor('Tabard', 60, 0, 1.5, 1.5)
ragged_armor = Armor('Ragged Armor', 10, 0, 0, 0.5)
tribal_wrappings = Armor('Tribal Wrappings', 5, 0, 0, 0.25)
lorica = Armor('Lorica', 500, 2, 7, 0.50)
byrnie = Armor('Byrnie', 600, 1.7, 8, 0.75, heavy=True)
brigandine = Armor('Brigandine', 1500, 2, 11, 0.25)
corrazina = Armor('Corrazina', 1600, 2, 11, 0.50, heavy=True)
scale_armor = Armor('Scale Armor', 1800, 1.5, 12, 0, heavy=True)
coat_plate = Armor('Coat of Plates', 1900, 2, 11, 0.25, heavy=True)
cuir_bouilli = Armor('Cuir Bouilli', 1700, 2, 9, 0.45, heavy=True)

armor_list = [lorica, byrnie, brigandine, corrazina, scale_armor, coat_plate, cuir_bouilli, tunic, robe, fur_coat,
              jerkin, linen_shirt, aketon, tabard, ragged_armor, tribal_wrappings, gambeson, hauberk, lamellar,
              cloth_armor, padded_armor, leather_armor, wood_armor, chainmail, plate]

basic_armor_list = [tunic, robe, fur_coat, jerkin, linen_shirt, aketon, tabard, ragged_armor, tribal_wrappings,
                    gambeson, cloth_armor, leather_armor, wood_armor, padded_armor]

mount_none = Mount('None', 0, 0, 0, 0, 0, 0)
camel = Mount('Camel', 200, 5 / 2, 1, 0, 0.2, 0.2)
donkey = Mount('Donkey', 100, 3 / 2, 0, 1, 0.1, 0.3)
rouncey = Mount('Rouncey', 300, 6 / 2, 1, 1, 0.2, 0.1)
horse = Mount('Donkey', 400, 7 / 2, 3, 1, 0.2, 0.2)
destrier = Mount('Destrier', 500, 8 / 2, 1, 3, 0.3, 0.3)
courser = Mount('Courser', 600, 10 / 2, 2, 1, 0.4, 0.3)
cataphract = Mount('Cataphract', 1200, 4 / 2, 2, 5, 0.5, 1.3, heavy=True)
charger = Mount('Charger', 1500, 7 / 2, 5, 2, 1.4, 0.4, heavy=True)
warhorse = Mount('Warhorse', 1300, 5 / 2, 3, 3, 1.4, 1.3, heavy=True)
barded_warhorse = Mount('Barded Warhorse', 1800, 4 / 2, 2, 4, 1.3, 1.4, heavy=True)
elephant = Mount('Elephant', 2000, 3 / 2, 7, 7, 1.8, 2.3, heavy=True)

basic_mount_list = [camel, donkey, rouncey, horse]

mount_list = [camel, donkey, rouncey, horse, destrier, courser, cataphract, charger, warhorse, barded_warhorse,
              elephant]
