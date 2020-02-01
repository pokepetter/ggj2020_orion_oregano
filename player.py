from ursina import *

class Player(Entity):
    def __init__(self, **kwargs):
        super().__init__(
            model='quad',
            color=color.yellow,
            scale_y=2,
            z=-5);
        self.hp = 32 #number of teeth
        self.punch_power = 3
        self.kick_power = 5

        for key, value in kwargs.items():
            setattr(self, key, value)

    @property
    def hp(self):
      return_self.hp

    @hp.setter
    def hp(self, value):
      if value <= 0:
        self.die()



if __name__ == '__main__':
  app = Ursina()
  enemy = Enemy()
  app.run()
