from ursina import *
from ursina.prefabs.health_bar import HealthBar
Texture.default_filtering = None

class Enemy(Entity):
    def __init__(self, boss=False, woman=False, **kwargs):
        super().__init__(
                    # model='quad',
                    # texture='jonas_idle',
                    scale=4,
                    z=-5);
        self.speed = 1
        self.attack_power = 2
        self.max_hp = 10
        self.time_between_attacks = 2
        self.time_of_last_attack = 0

        if not boss:
            self.name = "jonas_"
            if (woman):
                self.name = "Dame Lilla_"
            self.animator = Animator(
                animations = {
                    'idle' : Animation(self.name + 'idle', parent=self, scale=1.5, z=-.1),
                    'walk' : Animation(self.name + 'walk', parent=self, scale=1.5),
                    'attack' : Animation(self.name + 'punch', fps=1, parent=self, scale=1.5),
                }
            )
            self.animator.state = 'idle'

        if boss:
            self.max_hp = 20
            self.attack_power = 6
            self.time_between_attacks = 1
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
            position = (Vec3(-.2, 1, 0)),
            scale_x = .5,
            max_value = self.hp,
            show_text = False,
            show_lines = False,
            roundness = 0.25
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
        self.animator.animations['walk'].blink(color.red)


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
  t = time.time()
  enemy = Enemy()
  print('---', time.time() - t)
  camera.fov = 100
  def input(key):
      if key == '1':
          enemy.animator.state = 'idle'
      if key == '2':
          enemy.animator.state = 'walk'
      if key == '3':
          enemy.animator.state = 'attack'
  app.run()
