from ursina import *
from ursina.prefabs.health_bar import HealthBar

class Enemy(Entity):
    def __init__(self, **kwargs):
        super().__init__(
                    model='quad',
                    color=color.red.tint(random.random() / 2),
                    scale_y=2,
                    z=-5);
        self.max_hp = 10
        self.hp = self.max_hp
        self.speed = 1

        self.healthBar = HealthBar(
        world_parent = self,
        position = (Vec3(-1, 1, 0)),
        scale_x = 2,
        max_value = self.hp,
        show_text = False,
        show_lines = False,
        roundness = 0.5
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
    #     if value <= 0:
    #         self.die()
    #
    # def die(self):
    #     destroy(self)


if __name__ == '__main__':
  app = Ursina()
  enemy = Enemy()
  app.run()
