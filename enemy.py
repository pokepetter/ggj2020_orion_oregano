from ursina import *
from ursina.prefabs.health_bar import HealthBar
Texture.default_filtering = None

class Enemy(Entity):
    def __init__(self, boss=False, **kwargs):
        super().__init__(
                    # model='quad',
                    # texture='jonas_idle',
                    scale_y=2,
                    z=-5);
        self.speed = 1
        self.attack_power = 1
        self.max_hp = 10
        self.time_between_attacks = 3
        self.time_of_last_attack = 0
        if not boss:
            self.animator = Animator(
                animations = {
                    'idle' : Animation('jonas_idle', parent=self, scale=1.5, z=-.1),
                    'walk' : Animation('jonas_walk', parent=self, scale=1.5),
                    'attack' : Animation('jonas_punch', fps=1, parent=self, scale=1.5),
                }
            )
            self.animator.state = 'idle'

        if boss:
            self.max_hp = 20
            attack_power = 3
            self.time_between_attacks = 2
            self.animator = Animator(
                animations = {
                    'walk' : Animation('GDB walk', parent=self, scale=1.5),
                    'attack' : Animation('GDBoss hit', fps=1, parent=self, scale=1.5),
                }
            )

        self.hp = self.max_hp
        if boss:
            self.hp -= 1


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


    def attack(self):
        if time.time() < self.time_of_last_attack + self.time_between_attacks:
            return 0
        else:
            self.time_of_last_attack = time.time()
            self.animator.state = 'attack'
            invoke(setattr, self.animator, 'state', 'walk', delay=.1)
            return self.attack_power



if __name__ == '__main__':
  app = Ursina()
  enemy = Enemy()

  def input(key):
      if key == '1':
          enemy.animator.state = 'idle'
      if key == '2':
          enemy.animator.state = 'walk'
      if key == '3':
          enemy.animator.state = 'attack'
  app.run()
