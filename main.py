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

        # self.go_to_scene(self.beat_em_up_scene)
        # invoke(self.go_to_scene, self.beat_em_up_scene)
        self.start_screen = Entity(parent=camera.ui, model='quad', texture='main_menu_bg', scale_x=camera.aspect_ratio)
        Text(world_parent=self.start_screen, text='[press start]', origin=(0,0), y=-.45, color=color.black)


    def go_to_scene(self, value):
        print('go to scene:', value)
        camera.overlay.color = color.black
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
        # camera.overlay.fade_out(duration=1, delay=1.2)
        # camera.overlay.color = color.clear
        invoke(setattr, camera.overlay, 'color', color.clear, delay=1)


    def input(self, key):

        if key == 'space':
            self.start_screen.enabled = False
            self.ignore = True
            self.go_to_scene(self.beat_em_up_scene)



if __name__ == '__main__':
    app = Ursina()
    # texture_importer.textureless = True
    window.fullscreen = True
    window.show_ursina_splash = True
    window.exit_button.visible = False
    window.fps_counter.enabled = False
    Text.default_resolution *= 4
    Text.default_font = 'monogram_extended.ttf'
    Text.size *= 2
    t = time.time()
    game = DirtyDentist()
    print('---', time.time()-t)
    window.color = color.black

    def input(key):
        if key == '1':
            game.go_to_scene(game.beat_em_up_scene)
        if key == '2':
            game.go_to_scene(game.dentist_scene)
        if key == 'f7':
            game.scene.end()
    app.run()
