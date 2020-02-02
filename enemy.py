from ursina import *
from ursina.prefabs.health_bar import HealthBar

class Enemy(Entity):
    def __init__(self, boss=False, **kwargs):
        super().__init__(
                    model='quad',
                    texture='jonas_idle',
                    scale_y=2,
                    z=-5);
        self.speed = 1
        self.attack_power = 1
        self.max_hp = 10
        self.time_between_attacks = 3
        self.time_of_last_attack = 0

        self.current_walking_frame = 0
        self.time_between_walking_frames = 0.1

        self.angry = False #should be set to true when chasing the player

        if (boss):
            self.max_hp = 20
            attack_power = 3
            self.time_between_attacks = 2

        self.hp = self.max_hp
        if (boss):
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
    #     if value <= 0:
    #         self.die()
    #
    # def die(self):
    #     destroy(self)

    def attack(self):
        if time.time() < self.time_of_last_attack + self.time_between_attacks:
            return 0
        else:
            self.time_of_last_attack = time.time()
            return self.attack_power

    def next_walking_frame(self):
        if(not not self):
            self.texture = "jwalk_" + str(self.current_walking_frame)
            self.current_walking_frame = (self.current_walking_frame + 1) % 3
            invoke(self.next_walking_frame, delay=self.time_between_walking_frames)



if __name__ == '__main__':
  app = Ursina()
  enemy = Enemy()
  app.run()
