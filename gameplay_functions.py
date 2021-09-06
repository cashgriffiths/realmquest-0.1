import random


def combat(player, enemy, save):
    if enemy.speed > 11 and not save:
        print("The enemy", enemy.name, "was faster than you!")
        player.deal_damage(enemy.damage)
        if player.hp <= 0:
            print("\nYou have been defeated...\n")
            return [player, "loss"]
    else:
        input("\nPress enter to continue")
    while True:
        cont = True
        print("\n\nIt is your turn."
              "\nYou have", player.hp, "hitpoints."
              "\nThe enemy", enemy.name, "has", enemy.hp, "hitpoints."
              "\n\nHere are your weapons:")
        for key, value in player.weapons_dict.items():
            if value.cooldown <= 0:
                ready = "Ready"
            elif value.cooldown == 1:
                ready = "1 turn"
            else:
                ready = str(value.cooldown) + " turns"
            print(key, ":", str(value.damage - 1) + "-" + str(value.damage + 1), "damage (" + ready + ")")
        print("\nHere are your spells:")
        for key, value in player.spells_dict.items():
            if value.cooldown <= 0:
                ready = "Ready"
            elif value.cooldown == 1:
                ready = "1 turn"
            else:
                ready = str(value.cooldown) + " turns"
            print(key, ":", str(value.damage - 2) + "-" + str(value.damage + 2), "damage (" + ready + ")")
        print("\nHere are your items:")
        for key, value in player.items_dict.items():
            print(key, ":", value)
        print()
        choice = input("Would you like to (1) attack, (2) cast a spell, (3) use an item, or (4) open options? ")
        if choice == "4":
            if options() == "2":
                return [player, "exit", enemy]
        # todo remove dev skip lol
        elif choice == "yeet":
            player.heal(20)
            return [player, "win"]
        # todo remove dev skip lol
        while choice not in {"1", "2", "3"}:
            choice = input("Please enter a valid choice.\n"
                           "Would you like to (1) attack, (2) use a spell, (3) use an item, or (4) open options? ")
            if choice == "4":
                if options() == "2":
                    return [player, "exit", enemy]
            # todo remove dev skip lol
            elif choice == "yeet":
                player.heal(20)
                return [player, "win"]
            # todo remove dev skip lol
        while True:
            random.seed()
            val = random.random()
            if choice == "1":
                for key, value in player.weapons_dict.items():
                    if value.cooldown <= 0:
                        ready = "Ready"
                    elif value.cooldown == 1:
                        ready = "1 turn"
                    else:
                        ready = str(value.cooldown) + " turns"
                    print(key, ":", str(value.damage - 1) + "-" + str(value.damage + 1), "damage (" + ready + ")")
                choice1 = input("Choose a weapon: ").title()
                print()
                try:
                    if player.weapons_dict[choice1].cooldown > 0:
                        print("You realize that your weapon is still on cooldown. The enemy", enemy.name,
                              "attacks during your fit of uncontrollable rage")
                        break
                    random.seed()
                    damage = random.randint(player.weapons_dict[choice1].damage - 1,
                                            player.weapons_dict[choice1].damage + 1)
                    if val <= 0.02:
                        print("You got lucky and dealt double damage!")
                        enemy.deal_damage(damage * 2)
                    else:
                        enemy.deal_damage(damage)
                    player.weapons_dict[choice1].set_cooldown()
                    break
                except KeyError:
                    print("That is not a valid weapon.")
            elif choice == "2":
                for key, value in player.spells_dict.items():
                    if value.cooldown <= 0:
                        ready = "Ready"
                    elif value.cooldown == 1:
                        ready = "1 turn"
                    else:
                        ready = str(value.cooldown) + " turns"
                    print(key, ":", str(value.damage - 2) + "-" + str(value.damage + 2), "damage (" + ready + ")")
                choice2 = input("Choose a spell: ").title()
                print()
                try:
                    if player.spells_dict[choice2].cooldown > 0:
                        print("You realize that your spell is still on cooldown. The enemy", enemy.name,
                              "attacks during your fit of uncontrollable rage")
                        break
                    random.seed()
                    damage = random.randint(player.spells_dict[choice2].damage - 2,
                                            player.spells_dict[choice2].damage + 2)
                    enemy.deal_damage(damage)
                    player.spells_dict[choice2].set_cooldown()
                    break
                except KeyError:
                    print("That is not a valid spell.")
            else:
                for key, value in player.items_dict.items():
                    print(key, ":", value)
                choice3 = input("Choose an item: ").title()
                print()
                if choice3 == "Health Potion":
                    if player.items_dict["Health Potion"] > 0:
                        player.heal(10)
                        player.items_dict["Health Potion"] -= 1
                        break
                    else:
                        print("You have no health potions left!")
                        cont = False
                        break
                else:
                    print("That is not a valid item.")
                    cont = False
        if cont:
            if enemy.hp <= 0:
                input("Enemy " + enemy.name + " has been defeated!\nPress enter to continue\n")
                for key in player.weapons_dict:
                    player.weapons_dict[key].update_cooldown()
                for key in player.spells_dict:
                    player.spells_dict[key].update_cooldown()
                return [player, "win"]
            # enemy turn
            random.seed()
            val = random.random()
            random.seed()
            if enemy.is_boss:
                print("boss")
                if val > 0.05:
                    player.deal_damage(random.randint(enemy.damage - 2, enemy.damage + 2))
                else:
                    print("The boss whiffed! Moron...\nPress enter to continue")
            else:
                damage = random.randint(enemy.damage - 1, enemy.damage + 1)
                if val < 0.02:
                    print("The enemy", enemy.name, "got lucky and dealt double damage!")
                    player.deal_damage(damage * 2)
                else:
                    player.deal_damage(damage)
            if player.hp <= 0 and not enemy.is_boss:
                print("\nYou have been defeated...\n")
                return [player, "loss"]
            elif player.hp <= 0:
                print("You died to the boss...")
                return [player, "loss"]
            # update cooldown
            for key in player.weapons_dict:
                player.weapons_dict[key].update_cooldown()
            for key in player.spells_dict:
                player.spells_dict[key].update_cooldown()


def options():
    choice = input("(1) Continue, (2) Save and exit: ")
    return choice
