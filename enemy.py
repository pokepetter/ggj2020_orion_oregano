from ursina import *



class Enemy(Entity):
    def __init__(self, **kwargs):
        self.hp = 10

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
