from ursina import *
from dentist import JawMinigame
from beat_em_up import BeatEmUp


class DirtyDentist(Entity):
    def __init__(self):
        super().__init__(self)
        self.scene = None
        t = time.time()
        self.beat_em_up_scene = None
        print('beat_em_up_scene load time:', time.time()-t)
        self.dentist_scene = JawMinigame(parent=self, enabled=False)
        t = time.time()
        self.go_to_scene(self.beat_em_up_scene)
        print('dentist_scene load time:', time.time()-t)


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
            invoke(setattr, self.dentist_scene, 'enabled', False, delay=1)
        else:
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
