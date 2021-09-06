class Player:
    def __init__(self, hp, weight, weapons_dict, spells_dict, items_dict, armor_dict):
        self.hp = hp
        self.weight = weight
        self.weapons_dict = weapons_dict
        self.spells_dict = spells_dict
        self.items_dict = items_dict
        self.armor_dict = armor_dict

    def add_weight(self, weight):
        self.weight += weight
        print("You are now carrying " + self.weight + " pounds")

    def subtract_weight(self, weight):
        self.weight += weight
        print("You are now carrying " + self.weight + " pounds")

    def deal_damage(self, damage):
        self.hp -= damage
        input("You took " + str(damage) + " points of damage\n\nPress enter to continue")

    def heal(self, hp):
        temp = self.hp
        self.hp += hp
        if self.hp > 25:
            self.hp = 25
        print("You gained", self.hp - temp, "hitpoints")

    def list_items(self, list_name):
        if list_name == "weapons":
            for key, value in self.weapons_dict:
                print(key, end=", ")
        elif list_name == "spells":
            for i in self.spells_dict:
                print(i, end=", ")
        elif list_name == "items":
            for key, value in self.items_dict:
                print(key, end=", ")
