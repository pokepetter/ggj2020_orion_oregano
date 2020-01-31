from ursina import *


window.set_z_order(window.Z_top)

app = Ursina()
window.color = color.light_gray
camera.orthographic = True
camera.fov = 20

player_speed = 10

player_top_constraint = 3
player_bottom_constraint = -5

enemies = []



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


def spawn_random_enemies(amount):
    for i in range(amount):
        enemies.append(Entity(
                    model='cube',
                    color=color.red,
                    scale_y=2,
                    x = random.randint(-10, 10),
                    y = random.randint(-3, 2),
                    z=-5))
spawn_random_enemies(3)


def go_to_next_street():
    global enemies
    player.x = 0
    player.y = 0
    for enemy in enemies:
        destroy(enemy)
    enemies = []
    spawn_random_enemies(3)


def update():
    player_controls()
    if player.x >= (camera.fov * camera.aspect_ratio / 2 - player.scale_x):
        go_to_next_street()

def player_controls():
    if player.x < (camera.fov * camera.aspect_ratio / 2 - player.scale_x):
        player.x += held_keys["d"] * time.dt * player_speed
    if player.x > -(camera.fov * camera.aspect_ratio / 2 - player.scale_x):
        player.x -= held_keys["a"] * time.dt * player_speed
    if player.y < player_top_constraint:
        player.y += held_keys["w"] * time.dt * player_speed
    if player.y > (player_bottom_constraint + player.scale_y/2):
        player.y -= held_keys["s"] * time.dt * player_speed









window.size = (window.fullscreen_size[0]//2, window.fullscreen_size[1]//2)
window.position = (int(window.size[0]), int(window.size[1]-(window.size[1]/2)))
window.borderless = False
window.fullscreen = False

input_handler.bind('right arrow', 'd')
input_handler.bind('left arrow', 'a')
input_handler.bind('up arrow', 'w')
input_handler.bind('down arrow', 's')

app.run()
