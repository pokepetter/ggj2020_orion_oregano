from ursina import *
from dentist import JawMinigame


app = Ursina()

window.color = color._32
window.fps_counter.enabled = False
window.exit_button.visible = False
Text.default_resolution *= 4
Text.default_font = 'monogram_extended.ttf'
Text.size *= 2


dentist_minigame = JawMinigame()
dentist_minigame.stop(False)
dentist_minigame.enabled = False

next_scene = Entity(model='cube', color=color.red, enabled=False)
dentist_minigame.next_scene = next_scene



def input(key):
    global dentist_minigame
    if key == 'j':
        camera.overlay.fade_in(duration=1)
        camera.overlay.fade_out(duration=1, delay=1.1)
        print('lol')
        invoke(setattr, dentist_minigame, 'enabled', True, delay=1)
        invoke(dentist_minigame.start, delay=1)


app.run()
