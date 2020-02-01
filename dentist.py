from ursina import *
from copy import copy



Text.default_resolution *= 2

class JawMinigame(Entity):

    def __init__(self):
        super().__init__()
        self.tooth_slot_model = Entity(model=Cylinder(height=.1), enabled=False)
        self.tooth_model = Entity(model=Prismatoid(base_shape=Quad(), thicknesses=[(1,1), (.7,.7)]), enabled=False)
        self.jaw = self.generate_jaw()

        mouse.visible = False
        self.cursor = Cursor(scale=.025)
        self.cursor.text_entity = Text(parent=self.cursor, text='tool_name', world_scale=50, y=1, z=-1)

        self.tools = ['place_tooth', 'syringe', 'hammer']
        self.tool = 'place_tooth'

        self.time = 30
        self.timer = Text('60.00', origin=(0,.5), y=.45, scale=2)
        self.out_of_time = False
        # Entity(parent=self.cursor, model='quad', scale=3, texture='brick')

        self.ui = Entity(parent=camera.ui, position=(.75,-.0), scale=.15)
        for i, tool in enumerate(self.tools):
            b = Button(
                parent=self.ui,
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


    def generate_jaw(self):
        jaw = Entity()
        for i in range(10):
            tooth_slot = Button(
                parent=jaw,
                model=copy(self.tooth_slot_model.model),
                origin_y=-.5,
                texture='white_cube',
                color=color.salmon,
                highlight_color=color.smoke,
                x=(-5+i)*1.1,
                z=curve.out_quad_boomerang(i/9) * -4
                )
            tooth_slot.look_at(Vec3(0,0,2))

            tooth_slot.tooth = Entity(
                parent=tooth_slot,
                model=copy(self.tooth_model.model),
                origin_y=-.5,
                texture='white_cube',
                scale=1.1,
                enabled=False
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

            if random.random() < .1:
                tooth_slot.tooth.color = color.gold

            tooth_slot.on_click = Func(self.click_on_tooth_slot, tooth_slot)

            if random.random() < .5:
                tooth_slot.tooth.enabled = True
            elif random.random() < .25:
                tooth_slot.nail.enabled = True

        return jaw


    def click_on_tooth_slot(self, tooth_slot):
        if self.out_of_time:
            return
        # print(self.tool, tooth_slot)
        if self.tool == 'hammer' and tooth_slot.nail.enabled:
            tooth_slot.nail.enabled = False

        if self.tool == 'place_tooth' and not tooth_slot.nail.enabled:
            tooth_slot.tooth.enabled = True
            # particle = Text(parent=scene, text='$100.00', color=color.lime, position=tooth_slot.tooth.position, scale=10)
            # particle.z -= 1
            # particle.y += 1
            particle = Text(text='$100.00', origin=(0,0), color=color.lime, position=mouse.position)
            particle.scale *= 2
            particle.z -= 1
            particle.y += .1
            particle.animate_y(particle.y+1, duration=2, curve=curve.linear)
            particle.fade_out(delay=.2, duration=.2)
            self.check_for_win()


    def check_for_win(self):
        teeth_amount = len([e for e in self.jaw.children if e.tooth.enabled])
        print(teeth_amount, 10)
        if teeth_amount >= 10:
            win_text = Button(text='Good Job!', color=color.azure)
            win_text.fit()
            win_text.scale *= 3
            destroy(win_text, delay=1)

            self.jaw.animate_x(-16, duration=1)
            destroy(self.jaw, delay=1)
            self.jaw = self.generate_jaw()
            self.jaw.x = 13.5
            self.jaw.animate_x(0, duration=1, delay=.5)



    def input(self, key):
        if key == 'f':
            self.tool = 'hammer'
            for c in self.jaw.children:
                c.on_click()
            self.tool = 'place_tooth'
            for c in self.jaw.children:
                c.on_click()

        if key == 'l':
            self.time = 1


    def update(self):
        if self.time <= 0:
            if not self.out_of_time:
                destroy(self.cursor)
                camera.overlay.fade_in(delay=.5, duration=1)
                self.ui.animate_x((.5*camera.aspect_ratio)+.05, duration=.25, curve=curve.in_out_expo)
                destroy(self.ui, delay=1.5)
                destroy(self)

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



if __name__ == '__main__':
    app = Ursina()

    jaw_game = JawMinigame()
    jaw_game.time = 15
    window.color = color._32
    editor_camera = EditorCamera()
    editor_camera.rotation_x = 20
    app.run()
