from ursina import *

class Enemy(Entity):
    def __init__(self, **kwargs):
        super().__init__(
                    model='quad',
                    color=color.red.tint(random.random() / 2),
                    scale_y=2,
                    z=-5);
        self.hp = 10

        for key, value in kwargs.items():
            setattr(self, key, value)

    @property
    def hp(self):
      return self._hp

    @hp.setter
    def hp(self, value):
        self._hp = value
    #     if value <= 0:
    #         self.die()
    #
    # def die(self):
    #     destroy(self)


if __name__ == '__main__':
  app = Ursina()
  enemy = Enemy()
  app.run()
