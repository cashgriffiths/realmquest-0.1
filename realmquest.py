import random
import Classes.player as p
import Classes.enemy as e
import Classes.weapon as weapon
import Classes.spell as spell
import gameplay_functions as play
global loot_rooms


# def check_exit_loss(choice):
#     if choice == "exit":
#         return "exit"
#     elif choice == "loss":
#         print("Returning to main menu...\n")
#         open("level_data.txt", "w").close()
#         open("player_data.txt", "w").close()
#         menu()


def check_level(level, temp, i, j):
    # check adjacent rooms to avoid generating adjacent loot rooms
    # check left
    if len(temp) > 1 and temp[j - 1] in {"l-bt", "l-m", "l-c", "l"}:
        return True
    # check above
    if len(level) > 0 and level[i - 1][j] in {"l-bt", "l-m", "l-c", "l"}:
        return True
    return False


def generate_room(l, w, adj_loot):
    global loot_rooms
    random.seed()
    val = random.random()
    # loot room
    if val < 0.25:
        # loot rooms should only make up less than 20% of level
        if loot_rooms / (l * w) >= 0.25 or adj_loot:
            return "b"
        loot_rooms += 1
        random.seed()
        val = random.random()
        # trapped room
        if val < 0.1:
            random.seed()
            val = random.random()
            # booby trapped loot room
            if val < 0.5:
                return "l-bt"
            # mimic trapped loot room
            else:
                return "l-m"
        # loot room with choice
        # elif 0.8 > val > 0.6:
        #     return "l-c"
        # regular loot room
        else:
            return "l"
    # basic room
    else:
        random.seed()
        val = random.random()
        if val < 0.1:
            return "w"
        return "b"


def generate_level(l, w, x, y):
    # empty level array
    level = []
    # top wall
    top = []
    for i in range(w):
        top.append("-")
    for i in range(l):
        # store each row in temp array
        temp = []
        for j in range(w):
            temp.append(generate_room(l, w, check_level(level, temp, i, j)))
        # append each row of level
        level.append(temp)
    level.insert(0, top)
    # left and right walls
    for i in range(0, len(level)):
        level[i].insert(0, "|")
        level[i].append("|")
    # bottom wall
    bottom = []
    for i in range(w + 2):
        bottom.append("-")
    level.append(bottom)
    # boss
    random.seed()
    xb = random.randint(1, x + 1)
    level[1][xb] = "!"
    # starting position
    level[y + 2][x] = "s"
    level[y + 1][x] = "b"
    return level


def new_game():
    global loot_rooms
    # clear files for new game
    open("level_data.txt", "w").close()
    open("player_data.txt", "w").close()
    loot_rooms = 0
    # generate length and width of level. min length/width of 7, max of 10. One square unit is one room
    random.seed()
    l = random.randint(5, 7)
    w = random.randint(5, 7)
    # starting position
    # random distance from left side, not including edges
    x = random.randint(1, w - 1)
    # bottom row
    y = l - 1
    # 2d array representing level
    # level is l units tall and w units wide, starting position at x, y
    level = generate_level(l, w, x, y)
    # blank "map" for player
    player_map = []
    top = []
    for m in range(w + 2):
        top.append("-")
    player_map.append(top)
    for i in range(l):
        temp = []
        for j in range(w):
            temp.append("?")
        player_map.append(temp)
    for k in range(1, l + 1):
        player_map[k].insert(0, "|")
        player_map[k].append("|")
    bottom = []
    for n in range(w + 2):
        bottom.append("-")
    player_map.append(bottom)
    player_map[1][level[1].index("!")] = "!"
    player_map[y + 2][x] = "s"
    player_map[y + 1][x] = "b"
    player = p.Player(25, 0,
                      {"Basic Sword": weapon.Weapon(5, 10, 1, "none", 5, 0),
                       "Heavy Club": weapon.Weapon(7, 10, 2, "none", 5, 0)},
                      {"Fireball": spell.Spell(16, 10, 6, "none", 0),
                       "Ice Spikes": spell.Spell(11, 10, 4, "none", 0)},
                      {"Health Potion": 3}, {})
    play_game(x, y + 2, level, player_map, player, "start", "none")


def save_game(level, player_map, player, x1, y1, last_pos, enemy):
    print("Saving game...\n\n")
    # open data file to write information
    level_data = open("level_data.txt", "w")
    # store level information
    level_data.write("LEVEL:\n")
    for i in level:
        for j in i:
            level_data.write(str(j) + " ")
        level_data.write("\n")
    level_data.write("CURRENT_POS:\n" + str(x1) + " " + str(y1) + "\n")
    level_data.write("LAST_POS:\n" + last_pos)
    level_data.write("\nENEMY:\n")
    if enemy == "none":
        level_data.write("none")
    else:
        level_data.write(str(enemy.hp) + ",")
        level_data.write(str(enemy.damage) + ",")
        level_data.write(str(enemy.speed) + ",")
        level_data.write(str(enemy.name) + ",")
        level_data.write(str(enemy.is_boss))
    level_data.close()
    # store player information
    player_data = open("player_data.txt", "w")
    player_data.write("MAP:\n")
    for i in player_map:
        for j in i:
            player_data.write(j + " ")
        player_data.write("\n")
    player_data.write("HP:\n" + str(player.hp) + "\n")
    player_data.write("WEIGHT:\n" + str(player.weight) + "\n")
    player_data.write("WEAPONS:\n")
    for key, value in player.weapons_dict.items():
        player_data.write(str(key) + ',' + value.print() + "\n")
    player_data.write("SPELLS:\n")
    for key, value in player.spells_dict.items():
        player_data.write(str(key) + ',' + value.print() + "\n")
    player_data.write("ITEMS:\n")
    for key, value in player.items_dict.items():
        player_data.write(str(key) + ',' + str(value) + "\n")
    player_data.close()


def load_game():
    level_file = open("level_data.txt", "r")
    level_data = level_file.readlines()
    level_file.close()
    level = []
    x, y = 0, 0
    last_room = "start"
    enemy = "none"
    for i in range(1, len(level_data)):
        level_data[i] = level_data[i].strip("\n")
        if "|" in level_data[i] or "-" in level_data[i]:
            temp = []
            level_data[i] = level_data[i].split()
            for j in level_data[i]:
                temp.append(j)
            level.append(temp)
        elif "CURRENT_POS" in level_data[i - 1]:
            x = int(level_data[i][0])
            y = int(level_data[i][2])
        elif "LAST_POS" in level_data[i - 1]:
            last_room = level_data[i]
        elif "ENEMY" in level_data[i - 1] and level_data[i] != "none":
            info = level_data[i].split(",")
            if info[4] == "True":
                info[4] = True
            else:
                info[4] = False
            enemy = e.Enemy(int(info[0]), int(info[1]), int(info[2]), info[3], bool(info[4]))
    player_file = open("player_data.txt", "r")
    player_data = player_file.readlines()
    player_file.close()
    player_map = []
    hp, weight = 25, 0
    weapons = {}
    spells = {}
    items = {}
    for i in range(1, len(player_data)):
        player_data[i] = player_data[i].strip("\n")
        if "|" in player_data[i] or "-" in player_data[i]:
            temp = []
            player_data[i] = player_data[i].split()
            for j in player_data[i]:
                temp.append(j.strip(" "))
            player_map.append(temp)
        elif "HP" in player_data[i - 1]:
            hp = int(player_data[i])
        elif "WEIGHT" in player_data[i - 1]:
            weight = int(player_data[i])
        elif "WEAPONS" in player_data[i - 1]:
            while "SPELLS" not in player_data[i]:
                info = player_data[i].split(",")
                weapons[info[0]] = weapon.Weapon(int(info[1]), int(info[2]), int(info[3]), info[4], int(info[5]), int(info[6]))
                i += 1
        elif "SPELLS" in player_data[i - 1]:
            while "ITEMS" not in player_data[i]:
                info = player_data[i].split(",")
                spells[info[0]] = spell.Spell(int(info[1]), int(info[2]), int(info[3]), info[4], int(info[5]))
                i += 1
        elif "ITEMS" in player_data[i - 1]:
            while i < len(player_data):
                info = player_data[i].split(",")
                items[info[0]] = int(info[1])
                i += 1
    player = p.Player(hp, weight, weapons, spells, items, {})
    play_game(x, y, level, player_map, player, last_room, enemy)


def play_game(x, y, level, player_map, player, last_room, enemy):
    if last_room == "left":
        player_map[y][x - 1] = "X"
    elif last_room == "right":
        player_map[y][x + 1] = "X"
    elif last_room == "up":
        player_map[y - 1][x] = "X"
    elif last_room == "down":
        player_map[y + 1][x] = "X"
    player_map[y][x + 1] = level[y][x + 1][0]
    player_map[y][x - 1] = level[y][x - 1][0]
    player_map[y - 1][x] = level[y - 1][x][0]
    if last_room != "start":
        player_map[y + 1][x] = level[y + 1][x][0]
    player_map[y][x] = "O"
    for i in player_map:
        for j in i:
            print(j, end=" ")
        print("\n")
    if enemy != "none":
        print("You are still in combat.")
        out = play.combat(player, enemy, True)
        if out[1] == "exit":
            save_game(level, player_map, player, x, y, last_room, out[2])
            menu()
        elif out[1] == "loss":
            print("Returning to main menu...\n")
            open("level_data.txt", "w").close()
            open("player_data.txt", "w").close()
            menu()
    elif level[y][x] == "s":
        input("You are in the starting room. Press enter to begin. ")
        level[y][x] = "-"
        player_map[y][x] = "-"
        play_game(x, y - 1, level, player_map, player, "down", "none")
    elif level[y][x] == "X":
        input("You are in an empty room.\n\nPress enter to continue.")
    elif level[y][x] == "!":
        print("You are in the boss room!")
        enemy = e.Enemy(random.randint(55, 65), random.randint(5, 7), 10, "boss", True)
        out = play.combat(player, enemy, False)
        if out[1] == "win":
            print("\nCongratulations! You brutally eviscerated the boss and escaped the dungeon! "
                  "I hope you feel good about yourself...\nReturning to main menu...\n\n")
            menu()
        elif out[1] == "exit":
            save_game(level, player_map, out[0], x, y, last_room, out[2])
        else:
            print("Returning to main menu...\n\n")
            menu()
    elif level[y][x] == "b":
        random.seed()
        val = random.random()
        if val < 0.75:
            print("You are in a basic room with an enemy.")
            names = ["goblin", "kobold", "slime", "gnome", "zombie", "skeleton"]
            enemy = e.Enemy(random.randint(14, 21), random.randint(2, 5),
                            random.randint(7, 14), names[random.randint(0, len(names) - 1)], False)
            out = play.combat(player, enemy, False)
            if out[1] == "exit":
                save_game(level, player_map, player, x, y, last_room, out[2])
                menu()
            elif out[1] == "loss":
                print("Returning to main menu...\n")
                open("level_data.txt", "w").close()
                open("player_data.txt", "w").close()
                menu()
        else:
            input("You are in an empty room.\n\nPress enter to continue.")
    elif level[y][x] in {"l-bt", "l-m", "l-c", "l"}:
        check_chest = input("You found a loot room! Will you check the chest? Y/N ")
        if check_chest.lower() == "y":
            if level[y][x] == "l-bt":
                print("The room was trapped!")
                player.deal_damage(random.randint(1, 6))
            elif level[y][x] == "l-m":
                print("The chest was a mimic!")
                enemy = e.Enemy(20, 3, 5, "mimic", False)
                out = play.combat(player, enemy, False)
                if out == "exit":
                    save_game(level, player_map, player, x, y, last_room, out[2])
                elif out == "loss":
                    print("Returning to main menu...\n")
                    open("level_data.txt", "w").close()
                    open("player_data.txt", "w").close()
                    menu()
            # elif level[y][x] == "l-c":
            #     print("You are presented with a choice!")
            #     # todo provide choice of items
            else:
                # todo add more items
                random.seed()
                num = random.randint(2, 3)
                if num != 1:
                    print("You found", str(num), "health potions.")
                else:
                    print("You found 1 health potion.")
                player.items_dict["Health Potion"] += num
                input("You now have " + str(player.items_dict["Health Potion"]) +
                      " health potions.\nPress enter to continue.")
    for i in player_map:
        for j in i:
            print(j, end=" ")
        print("\n")
    while True:
        next_room = input("Choose the next room to go to, or type options.\nType (u)p/(d)own/(l)eft/(r)ight: ")
        if next_room not in {"up", "down", "right", "left", "u", "d", "r", "l", "options"}:
            next_room = input("That is not a valid choice.\n"
                              "Choose the next room to go to, or type options.\n"
                              "Type (u)p/(d)own/(l)eft/(r)ight: ")
        if next_room == "options":
            if play.options() == "2":
                save_game(level, player_map, player, x, y, last_room, "none")
                menu()
        if level[y][x] != "s":
            level[y][x] = "X"
        if next_room == "up" or next_room == "u" and level[y - 1][x] not in {"-", "w", "s"}:
            y -= 1
            last_room = "down"
            break
        elif (next_room == "down" or next_room == "d") and level[y + 1][x] not in {"-", "w", "s"}:
            y += 1
            last_room = "up"
            break
        elif (next_room == "right" or next_room == "r") and level[y][x + 1] not in {"|", "w", "s"}:
            x += 1
            last_room = "left"
            break
        elif (next_room == "left" or next_room == "l") and level[y][x - 1] not in {"|", "w", "s"}:
            x -= 1
            last_room = "right"
            break
        else:
            print("You can't go through the wall!\n")
    play_game(x, y, level, player_map, player, last_room, "none")


def menu():
    choice = input("(1) New Game\n(2) Load Game\n(3) Exit\nEnter 1, 2 or 3: ")
    if choice == "1":
        new_game()
    elif choice == "2":
        # load game
        load_game()
    elif choice == "3":
        exit()
    else:
        print("Please choose a valid option: ")
        menu()


print("Welcome to Realmquest, a dynamically generated text based dungeon crawler project by Christian Griffiths")
menu()
