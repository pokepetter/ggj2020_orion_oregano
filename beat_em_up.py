from ursina import *
from enemy import Enemy
from player import Player
from dialogue_box import DialogueBox

class BeatEmUp(Entity):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        window.color = color.light_gray

        self.player_top_constraint = 3
        self.player_bottom_constraint = -5

        self.hitbox_size = 3 # how far away the enemies have to be for a hit

        self.current_street = 1
        self.last_street = 3

        self.enemies = []


        self.background = Entity(
        model = 'quad',
        texture = 'background1',
        position = (0, 11, 0),
        scale = (36, 17, 1),
        origin_y = .5,
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

        self.player = Player(parent=self)

        self.ui = Entity(parent=camera.ui)
        self.first_street_dialogue()
        self.dialogue.t.parent = self.ui
        self.dialogue.name_text.parent = self.ui

        self.spawn_random_enemies(3)


        for key, value in kwargs.items():
            setattr(self, key, value)


    def on_destroy(self):
        destroy(self.ui)


    def on_enable(self):
        self.ui.enabled = True
        self.player.healthBar.enabled = True


    def on_disable(self):
        self.ui.enabled = False
        self.player.healthBar.enabled = False


    def spawn_random_enemies(self, amount):
        for i in range(amount):
            self.enemies.append(Enemy(
                x = random.randint(-10, 10),
                y = random.randint(-3, 2),
                woman = (random.random() > 0.7),
                parent = self))


    def first_street_dialogue(self):
        self.dialogue = DialogueBox([
                    ["Sabrina", "Omg"],
                    ["Sabrina", "There are people here"],
                    ["Sabrina", "I gotta..\nI gotta knock their <red>teeth <default>out!"]
                ], parent=self.ui)

    def second_street_dialogue(self):
        self.dialogue = DialogueBox([
                    ["Sabrina", "So many teeth, so little time"],
                    ["Jonas", "you'll never get my teeth!"]
                ], parent=self.ui)

    def third_street_dialogue(self):
        self.dialogue = DialogueBox([
                    ["Margaret", "I'll crush you"],
                    ["Sabrina", "no u won't"],
                    ["Margaret", "Yes I will!!!"]
                ], parent=camera.ui)


    def go_to_next_street(self):
        self.current_street += 1
        self.player.x = -(camera.fov * camera.aspect_ratio / 2 - self.player.scale_x)
        for enemy in self.enemies:
            destroy(enemy)
        self.enemies = []
        if (self.current_street != 4):
            self.spawn_random_enemies(3)
        if(self.current_street == 2):
            self.background.texture = "background2"
            self.second_street_dialogue()
        if(self.current_street == 3):
            self.enemies.append(Enemy(
                x = random.randint(-10, 10),
                y = random.randint(-3, 2),
                boss=True,
                parent = self))
            self.third_street_dialogue()
        if(self.current_street == 4):
            self.background.color = color.black
            self.player.scale = 7
            self.player.x = 0
            self.player.y = 0
            self.dialogue = "something"
            self.player.animator.state = "reveal"
            invoke(self.end, delay=10)




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
                if distance2d(self.player.position, enemy.position) < self.hitbox_size:
                    enemy.hp = enemy.hp - self.player.punch()
                    enemy.animator.state = 'walk'
                    if enemy.hp <= 0:
                        self.enemies.remove(enemy)
                        destroy(enemy)

        if not self.dialogue and key == "k":
            for enemy in self.enemies:
                if distance2d(self.player.position, enemy.position) < self.hitbox_size:
                    enemy.hp = enemy.hp - self.player.kick()
                    enemy.animator.state = 'walk'
                    if enemy.hp <= 0:
                        self.enemies.remove(enemy)
                        destroy(enemy)

    def end(self):
        if self.parent:
            self.started = False
            self.parent.go_to_scene(self.parent.dentist_scene)


input_handler.bind('right arrow', 'd')
input_handler.bind('left arrow', 'a')
input_handler.bind('up arrow', 'w')
input_handler.bind('down arrow', 's')

if __name__ == "__main__":
    app = Ursina()
    camera.orthographic = True
    camera.fov = 20

    beat_em_up = BeatEmUp(enabled = True)
    def input(key):
        if key == 'f':
            print(camera.fov, beat_em_up.player.y, beat_em_up.player_top_constraint)


    app.run()
