from ursina import *
from ursina.prefabs.health_bar import HealthBar


class Player(Entity):
    def __init__(self, **kwargs):
        super().__init__(
            scale=4,
            x = -15,
            z=-6,
            **kwargs
            )

        self.hp = 32 #number of teeth
        self.punch_power = 3
        self.kick_power = 7
        self.speed = 10

        self.time_of_last_attack = 0
        self.time_between_attacks = 0.5
        self.extra_kick_cooldown = 0.1 #this is added to time_between_attacks

        self.animator = Animator(
            animations = {
                'idle' : Animation('Tannlege idle', parent=self, scale=1.5, z=-.1, double_sided = True),
                'walk' : Animation('Tannlege run', parent=self, scale=1.5, double_sided = True),
                'punch' : Animation('Tannlege stillehit', parent=self, scale=1.5, double_sided = True),
                'kick' : Animation('Tannlege kick', parent=self, scale=1.5, double_sided = True)
            }
        )
        self.animator.state = 'idle'

        self.healthBar = HealthBar(
            position = (Vec3(-0.6, -0.3, 0)),
            scale_x = 0.8,
            scale_y = 0.2,
            max_value = self.hp,
            show_text = False,
            show_lines = False,
            roundness = 0.5,
            z = 0,
            )

        for key, value in kwargs.items():
            setattr(self, key, value)


    @property
    def hp(self):
      return self._hp

    @hp.setter
    def hp(self, value):
        if hasattr(self, '_hp') and value < self._hp:
            self.healthBar.value = value
            self.animator.animations[self.animator.state].blink(color.red)

        self._hp = value


    def on_enable(self):
        self.hp = 32
        self.x = -15
        self.y = 0
        self.healthBar.enabled = True


    def on_disable(self):
        self.healthBar.enabled = False

    def punch(self):
        if time.time() < self.time_of_last_attack + self.time_between_attacks:
            return 0
        else:
            self.time_of_last_attack = time.time()
            self.animator.state = 'punch'
            invoke(setattr, self.animator, "state", "idle", delay = self.time_between_attacks)
            return self.punch_power

    def kick(self):
        if time.time() < self.time_of_last_attack + self.time_between_attacks:
            return 0
        else:
            self.time_of_last_attack = time.time() + self.extra_kick_cooldown
            self.animator.state = 'kick'
            invoke(setattr, self.animator, "state", "idle", delay = 7/12)
            return self.kick_power

    def update(self):
        if self.animator.state == "punch" or self.animator.state == "kick":
            return
        if held_keys["w"] or held_keys["a"] or held_keys["s"] or held_keys["d"]:
            self.animator.state = "walk"
        else:
            self.animator.state = "idle"

    def input(self, key):
        if key == "a":
            self.scale_x = self.scale_y*-1
        if key == "d":
            self.scale_x = self.scale_y



if __name__ == '__main__':
  app = Ursina()
  enemy = Player(enabled=True)
  app.run()
