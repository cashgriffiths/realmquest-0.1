class Weapon:
    def __init__(self, damage, speed, max_cooldown, debuff, weight, cooldown):
        self.damage = damage
        self.speed = speed
        self.cooldown = cooldown
        self.max_cooldown = max_cooldown
        self.debuff = debuff
        self.weight = weight

    def update_cooldown(self):
        self.cooldown -= 1
        if self.cooldown < 0:
            self.cooldown = 0

    def set_cooldown(self):
        self.cooldown = self.max_cooldown

    def print(self):
        return str(self.damage) + "," + str(self.speed) + "," + str(self.max_cooldown) + "," + self.debuff + "," + str(self.weight) + "," + str(self.cooldown)
