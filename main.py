from ursina import *
from dentist import JawMinigame


app = Ursina()

window.color = color._32
Text.default_resolution *= 4
Text.default_font = 'monogram_extended.ttf'
Text.size *= 2


dentist_minigame = JawMinigame()
dentist_minigame.enabled = False





def input(key):
    if key == 'j':
        print('lol')
        dentist_minigame.enabled = True


app.run()
