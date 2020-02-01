from ursina import *
from enemy import Enemy
from player import Player
from dialogue_box import DialogueBox

class BeatEmUp(Entity):

    def __init__(self, **kwargs):
        super().__init__()
        window.color = color.light_gray
        camera.orthographic = True
        camera.fov = 20

        self.player_top_constraint = 3
        self.player_bottom_constraint = -5

        self.current_street = 1
        self.last_street = 3

        self.enemies = []


        self.asphalt = Entity(
            model = 'quad',
            color = color.light_gray.tint(-.4),
            z = 0,
            y = 3,
            origin_y = .5,
            scale = (1000, 8, 10),
            collider = 'box',
            ignore = True,
            parent = self
            )

        self.below_ground = Entity(
            model = 'quad',
            color = color.olive.tint(-.4),
            z = 0,
            y = -5,
            origin_y = .5,
            scale = (1000, 8, 10),
            collider = 'box',
            ignore = True,
            parent = self
            )

        self.player = Player(parent = self)

        self.dialogue = DialogueBox([
                    ["Tooth criminal", "Omg"],
                    ["Tooth criminal", "There are people here"],
                    ["Tooth criminal", "I gotta..\nI gotta knock their <red>teeth <default>out!"]
                ], parent=camera.ui)

        self.spawn_random_enemies(3)



    def spawn_random_enemies(self, amount):
        for i in range(amount):
            self.enemies.append(Enemy(
                x = random.randint(-10, 10),
                y = random.randint(-3, 2),
                parent = self))




    def go_to_next_street(self):
        self.current_street += 1
        self.player.x = -(camera.fov * camera.aspect_ratio / 2 - self.player.scale_x)
        for enemy in self.enemies:
            destroy(enemy)
        self.enemies = []
        self.spawn_random_enemies(3)
        if(self.current_street == 3):
            self.boss = Enemy(
                x = random.randint(-10, 10),
                y = random.randint(-3, 2),
                hp = 20,
                parent = self)




    def update(self):
        if not self.dialogue:
            self.player_controls()
            self.enemies_chase_player()
        if self.player.x >= (camera.fov * camera.aspect_ratio / 2 - self.player.scale_x) and self.enemies==[]:
            self.go_to_next_street()

    def player_controls(self):
        if self.player.x < (camera.fov * camera.aspect_ratio / 2 - self.player.scale_x):
            self.player.x += held_keys["d"] * time.dt * self.player.speed
        if self.player.x > -(camera.fov * camera.aspect_ratio / 2 - self.player.scale_x):
            self.player.x -= held_keys["a"] * time.dt * self.player.speed
        if self.player.y < self.player_top_constraint:
            self.player.y += held_keys["w"] * time.dt * self.player.speed
        if self.player.y > (self.player_bottom_constraint + self.player.scale_y/2):
            self.player.y -= held_keys["s"] * time.dt * self.player.speed

    def enemies_chase_player(self):
        for enemy in self.enemies:
            if enemy.hp < enemy.max_hp:
                enemy.position = lerp(enemy.position, self.player.position, enemy.speed * time.dt)
                if distance2d(self.player.position, enemy.position) < 1:
                    self.player.hp -= enemy.attack()


    def input(self, key):
        if self.dialogue and key == "space":
            self.dialogue.current_text += 1

        if not self.dialogue and key == "space":
            for enemy in self.enemies:
                if distance2d(self.player.position, enemy.position) < 1:
                    enemy.hp = enemy.hp - self.player.punch_power
                    if(enemy.hp <= 0):
                        self.enemies.remove(enemy)
                        destroy(enemy)


input_handler.bind('right arrow', 'd')
input_handler.bind('left arrow', 'a')
input_handler.bind('up arrow', 'w')
input_handler.bind('down arrow', 's')

if __name__ == "__main__":
    app = Ursina()
    beat_em_up = BeatEmUp()
    app.run()
