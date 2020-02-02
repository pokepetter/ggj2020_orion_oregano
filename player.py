from ursina import *
from ursina.prefabs.health_bar import HealthBar


class Player(Entity):
    def __init__(self, **kwargs):
        super().__init__(
            model='quad',
            color=color.yellow,
            scale_y=2,
            x = -15,
            z=-5,
            **kwargs
            )

        self.hp = 32 #number of teeth
        self.punch_power = 3
        self.kick_power = 5
        self.speed = 10

        self.time_of_last_attack = 0
        self.time_between_attacks = 0.5

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
        self._hp = value
        self.healthBar.value = value


    def on_enable(self):
        self.hp = 32
        self.x = -15
        self.y = 0
        self.healthBar.enabled = True


    def on_disable(self):
        self.healthBar.enabled = False

    def attack(self):
        if time.time() < self.time_of_last_attack + self.time_between_attacks:
            return 0
        else:
            self.time_of_last_attack = time.time()
            return self.punch_power



if __name__ == '__main__':
  app = Ursina()
  enemy = Player(enabled=False)
  enemy.enabled = False
  app.run()
