from ursina import *
from dentist import JawMinigame
from beat_em_up import BeatEmUp


class DirtyDentist(Entity):
    def __init__(self):
        super().__init__(self)
        self.scene = None
        self.beat_em_up_scene = None
        self.dentist_scene = JawMinigame(parent=self, enabled=False)

        self.street_music = Audio('street', loop=True, autoplay=False)
        self.dentist_music = Audio('dentist', loop=True, autoplay=False)

        self.go_to_scene(self.beat_em_up_scene)


    def go_to_scene(self, value):
        print('go to scene:', value)
        camera.overlay.fade_in(duration=1)
        if value == self.beat_em_up_scene:
            destroy(self.beat_em_up_scene, delay=1)
            camera.fov = 20
            camera.orthographic = True
            camera.position = (0,0,-20)
            camera.rotation = (0,0,0)
            self.beat_em_up_scene = BeatEmUp(parent=self, enabled=False)
            self.scene = self.beat_em_up_scene
            self.dentist_music.fade_out()
            self.street_music.play()
            self.street_music.fade_in()

            invoke(setattr, self.dentist_scene, 'enabled', False, delay=1)
        else:
            self.street_music.fade_out(duration=1)
            self.dentist_music.play()
            self.dentist_music.fade_in(duration=1, delay=1)
            invoke(setattr, self.beat_em_up_scene, 'enabled', False, delay=1)
            self.scene = self.dentist_scene

        invoke(setattr, self.scene, 'enabled', True, delay=1.1)
        camera.overlay.fade_out(duration=1, delay=1.2)



    def input(self, key):
        if key == '1':
            self.go_to_scene(self.beat_em_up_scene)
        if key == '2':
            self.go_to_scene(self.dentist_scene)
        if key == 'f7':
            self.scene.end()



if __name__ == '__main__':
    app = Ursina()
    # texture_importer.textureless = True
    # window.show_ursina_splash = True
    Text.default_resolution *= 4
    Text.default_font = 'monogram_extended.ttf'
    Text.size *= 2
    t = time.time()
    DirtyDentist()
    print('---', time.time()-t)
    window.color = color.black

    app.run()
