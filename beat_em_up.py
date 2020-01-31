from ursina import *


window.set_z_order(window.Z_top)

app = Ursina()
window.color = color.light_gray
camera.orthographic = True
camera.fov = 20

player_speed = 10

player_top_constraint = 3
player_bottom_constraint = -5



asphalt = Entity(
    model = 'cube',
    color = color.light_gray.tint(-.4),
    z = -.1,
    y = 3,
    origin_y = .5,
    scale = (1000, 8, 10),
    collider = 'box',
    ignore = True,
    )

below_ground = Entity(
    model = 'cube',
    color = color.olive.tint(-.4),
    z = -.1,
    y = -5,
    origin_y = .5,
    scale = (1000, 100, 10),
    collider = 'box',
    ignore = True,
    )

player = Entity(
        model='cube',
        color=color.orange,
        scale_y=2,
        z=-5)

window.size = (window.fullscreen_size[0]//2, window.fullscreen_size[1]//2)
window.position = (int(window.size[0]), int(window.size[1]-(window.size[1]/2)))
window.borderless = False
window.fullscreen = False

def update():
    player_controls()

def player_controls():
    if player.x < (camera.fov * camera.aspect_ratio / 2 - player.scale_x):
        player.x += held_keys["d"] * time.dt * player_speed
    if player.x > -(camera.fov * camera.aspect_ratio / 2 - player.scale_x):
        player.x -= held_keys["a"] * time.dt * player_speed
    if player.y < player_top_constraint:
        player.y += held_keys["w"] * time.dt * player_speed
    if player.y > (player_bottom_constraint + player.scale_y/2):
        player.y -= held_keys["s"] * time.dt * player_speed


input_handler.bind('right arrow', 'd')
input_handler.bind('left arrow', 'a')
input_handler.bind('up arrow', 'w')

app.run()
