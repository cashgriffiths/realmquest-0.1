class Enemy:
    def __init__(self, hp, damage, speed, name, is_boss):
        self.hp = hp
        self.damage = damage
        self.speed = speed
        self.name = name
        self.is_boss = is_boss

    def deal_damage(self, damage):
        self.hp -= damage
        print("The enemy", self.name, "took", damage, "points of damage.")
