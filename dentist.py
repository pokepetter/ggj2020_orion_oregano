from ursina import *
from copy import copy



class JawMinigame(Entity):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.started = False
        self.next_scene = None

        self.ui = Entity(parent=camera.ui)
        self.editor_camera = EditorCamera(parent=self, rotate_around_mouse_hit=False, y=1)
        self.editor_camera.rotation_x = 20
        camera.fov = 60
        self.bg = Sky(
            parent=self,
            texture='brick',
            color=color.lime.tint(-.35),
            # texture_scale=(64,32)
            )
        self.bg.texture.filtering = None
        self.animate_background_color()

        self.music = Audio('dentist', parent=self, repeat=True, autoplay=False)
        # self.music.volume = 1
        # self.floor = Entity(parent=self, model='plane', y=-8, scale=100, texture='white_cube', texture_scale=(64,64))
        # self.bg = Entity(model='quad', z=100, scale=1000, color=color.black)
        # self.bg.look_at(camera, 'back')

        self.tooth_slot_model = Entity(parent=self, model=Cylinder(height=.2), enabled=False)
        self.tooth_model = Entity(parent=self, model=Prismatoid(base_shape=Quad(), thicknesses=[(1,1), (.7,.7)]), enabled=False)
        self.jaw_model = Entity(parent=self, model='gum', enabled=False)

        self.jaw = self.generate_jaw()
        self.jaw.x = 20
        self.randomize_jaw(self.jaw)
        self.finished_jaw = self.generate_jaw()
        self.finished_jaw.x = -20
        self.finished_jaw.enabled = False

        mouse.visible = False
        self.cursor = Cursor(parent=self.ui, scale=.025)
        self.cursor.text_entity = Text(parent=self.cursor, text='tool_name', world_scale=25, y=1, z=-1)

        self.time = 30
        self.timer = Text(parent=self.ui, text='60.00', origin=(0,.5), y=.5, scale=2)
        self.out_of_time = False

        self.earnings = 0
        self.money_counter = Text(parent=self.ui, x=.82, y=.15, text='100.000', origin=(.5,0), scale=1.5, color=color.green)
        self.money_counter.dollar_text = Text(parent=self.money_counter, text='$', origin=(.5,0), x=-.135, color=color.green)

        self.tools_menu = Entity(parent=self.ui, position=(.75,-.0), scale=.15)
        self.tools = [
        'place_tooth',
        # 'syringe',
        'hammer'
        ]
        self.tool = 'place_tooth'

        for i, tool in enumerate(self.tools):
            b = Button(
            parent=self.tools_menu,
            text=tool,
            y=-i,
            scale=.9,
            color=color.light_gray,
            on_click=Func(setattr, self, 'tool', tool)
            )

    @property
    def tool(self):
        return self._tool

    @tool.setter
    def tool(self, value):
        self._tool = value
        if not value in self.tools:
            print(value, 'is not a tool!')

        # print('set tool:', value)
        self.cursor.texture = value
        self.cursor.text_entity.text = value

    @property
    def earnings(self):
        return self._earnings

    @earnings.setter
    def earnings(self, value):
        self._earnings = value
        self.money_counter.text = f'{value:,}'


    def generate_jaw(self):
        jaw = Entity(parent=self, rotation_x=-10)
        jaw_model = Entity(
            parent=jaw,
            model=copy(self.jaw_model.model),
            texture='Munn_1_lambert1_BaseColor',
            rotation_y=180,
            rotation_x=-10,
            scale=1.5,
            y=-2.7,
            z=-.2
            )
        jaw_model.texture.filtering = False
        jaw.teeth = list()

        tooth_positions = [
            (-4.6,-1.4), (-4.3,-2.5), (-3.6,-3.7), (-2.6,-4.4), (-1.3,-4.8),
            (-0.0,-4.7), (1.1,-4.3), (2.0,-3.7), (2.8,-2.7), (3.2,-1.4)
        ]
        # tooth_positions += [(-e[0]-1, e[1]) for e in reversed(tooth_positions)]
        for i in range(10):
            tooth_slot = Button(
                parent=jaw,
                model=copy(self.tooth_slot_model.model),
                origin_y=-.5,
                texture='white_cube',
                color=color.salmon,
                highlight_color=color.smoke,
                # x=(-5+i)*1.1,
                # z=curve.out_quad_boomerang(i/9) * -4
                )
            if i < len(tooth_positions):
                tooth_slot.x = tooth_positions[i][0]
                tooth_slot.z = tooth_positions[i][1]

            tooth_slot.look_at(Vec3(0,0,0))
            jaw.teeth.append(tooth_slot)

            tooth_slot.tooth = Entity(
                parent=tooth_slot,
                model=copy(self.tooth_model.model),
                origin_y=-.5,
                texture='white_cube',
                scale=1.1,
                enabled=True
                )

            tooth_slot.nail = Entity(
                parent=tooth_slot,
                model='cube',
                origin_y=-1,
                scale=(.1,1,.1),
                color=color.dark_gray,
                enabled=False,
                rotation_x=random.uniform(-1,1)*5,
                rotation_z=random.uniform(-1,1)*5,
                )

            tooth_slot.on_click = Func(self.click_on_tooth_slot, tooth_slot)

        return jaw


    def randomize_jaw(self, jaw):
        for tooth_slot in jaw.teeth:
            if random.random() < .1:
                tooth_slot.tooth.color = color.gold

            if random.random() < .5:
                tooth_slot.tooth.enabled = False
                tooth_slot.collision = True
                if random.random() < .25:
                    tooth_slot.nail.enabled = True


    def click_on_tooth_slot(self, tooth_slot):
        if self.out_of_time:
            return
        # print(self.tool, tooth_slot)
        if self.tool == 'hammer' and tooth_slot.nail.enabled:
            tooth_slot.nail.enabled = False

        if self.tool == 'place_tooth' and not tooth_slot.nail.enabled:
            tooth_slot.tooth.enabled = True
            tooth_slot.collision = False
            particle = Text(text='$100.00', origin=(0,0), color=color.lime, position=mouse.position, add_to_scene_entities=False)
            particle.scale *= 2
            particle.z -= 1
            particle.y += .1
            particle.animate_y(particle.y+1, duration=2, curve=curve.linear)
            particle.fade_out(delay=.2, duration=.2)
            Audio('placetooth', pitch=random.uniform(.8,1.1), volume=random.uniform(.8,1))
            self.earnings += 100
            self.check_for_win()


    def check_for_win(self):
        teeth_amount = len([e for e in self.jaw.teeth if e.tooth.enabled])
        if teeth_amount >= 10:
            t = time.time()

            win_text = Text(text='Good Job!', origin=(0,0))
            win_text.create_background(color=color.azure)
            win_text.scale *= 2
            destroy(win_text, delay=1)

            for i, e in enumerate(self.jaw.teeth):
                self.finished_jaw.teeth[i].tooth.color = e.tooth.color

            self.finished_jaw.enabled = True
            self.finished_jaw.x = 0
            self.finished_jaw.animate_x(-20, duration=1)
            invoke(setattr, self.finished_jaw, 'enabled', False, delay=1)
            self.jaw.x = 20
            self.randomize_jaw(self.jaw)
            self.jaw.animate_x(0, duration=1, delay=.5)

            self.time += 5
            self.timer.color = color.lime
            self.timer.animate_color(color.smoke, delay=.5)


    def input(self, key):
        if key == 'f':
            self.tool = 'hammer'
            for c in self.jaw.teeth:
                c.on_click()
            self.tool = 'place_tooth'
            for i, c in enumerate(self.jaw.teeth):
                invoke(c.on_click, delay=i*.05)

        if key == 'l':
            self.time = 1


    def update(self):
        if not self.started:
            return

        if self.time <= 0:
            if not self.out_of_time:
                self.stop()

            self.out_of_time = True
            return

        if self.time <= 10 and self.timer.color != color.orange:
            self.timer.scale = 3
            self.timer.color = color.orange

        if self.time <= 5 and self.timer.color != color.red:
            self.timer.scale = 5
            self.timer.color = color.red

        self.time -= time.dt
        self.time = max(0, self.time)
        self.timer.text = ("%1f" % self.time)[:5]


    def start(self):
        print('start')
        self.jaw.x = 20
        self.jaw.animate_x(0, duration=1)
        self.time = 30
        self.timer.scale = 2
        self.timer.color = color.smoke
        self.earnings = 0
        invoke(setattr, self.ui, 'enabled', True, delay=0)
        invoke(setattr, self.cursor, 'enabled', True, delay=1)
        invoke(self.music.play, delay=1)
        invoke(setattr, self, 'started', True, delay=1)


    def stop(self, go_to_next_scene=True):
        self.cursor.enabled = False
        self.ui.enabled=False

        if self.next_scene:
            camera.overlay.fade_in(delay=1, duration=1)
            invoke(setattr, self, 'enabled', False, delay=2)
            invoke(setattr, self.next_scene, 'enabled', True, delay=2)
            camera.overlay.fade_out(delay=2.1, duration=1)
            self.music.fade_out(duration=1, destroy_on_ended=False)



    def animate_background_color(self):
        # self.bg.color=color.random_color().tint(-.5)
        step = 1/150*128
        if self.started:
            self.bg.animate_color(color.random_color().tint(-.25), curve=curve.linear, duration=step)
            invoke(self.animate_background_color, delay=step)


if __name__ == '__main__':
    app = Ursina()

    window.color = color._32
    Text.default_resolution *= 4
    Text.default_font = 'monogram_extended.ttf'
    Text.size *= 2

    jaw_game = JawMinigame()
    # jaw_game.enabled = False
    jaw_game.stop()
    jaw_game.start()

    def input(key):
        if key == 'space':
            jaw_game.enabled = True

    app.run()
