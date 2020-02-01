from ursina import *
from dentist import JawMinigame
from beat_em_up import BeatEmUp


class DirtyDentist(Entity):
    def __init__(self):
        super().__init__(self, eternal=True)
        self.scene_0 = BeatEmUp(parent=self, enabled=False)
        self.scene_1 = JawMinigame(parent=self, enabled=False)


    def go_to_scene(self, value):
        print('go to scene:', value)
        camera.overlay.fade_in(duration=1)
        self.scene = value
        invoke(setattr, self.scene, 'enabled', True, delay=1)
        camera.overlay.fade_out(duration=1, delay=1.1)



    def input(self, key):
        if key == '1':
            self.go_to_scene(self.scene_0)
        if key == '2':
            self.go_to_scene(self.scene_1)




if __name__ == '__main__':
    app = Ursina()
    window.color = color._32
    window.fps_counter.enabled = False
    window.exit_button.visible = False
    Text.default_resolution *= 4
    Text.default_font = 'monogram_extended.ttf'
    Text.size *= 2

    DirtyDentist()
    app.run()
