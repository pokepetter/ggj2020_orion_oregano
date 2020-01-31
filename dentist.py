from ursina import *
from copy import copy





class JawMinigame(Entity):

    def __init__(self):
        super().__init__()
        self.tooth_base_model = Entity(model=Cylinder(height=.1), enabled=False)
        self.tooth_model = Entity(model=Prismatoid(base_shape=Quad(), thicknesses=[(1,1), (.7,.7)]), enabled=False)
        self.jaw = self.generate_jaw()



    def generate_jaw(self):
        jaw = Entity()
        for i in range(10):
            tooth_base = Button(
                parent=jaw,
                model=copy(self.tooth_base_model.model),
                origin_y=-.5,
                texture='white_cube',
                color=color.salmon,
                highlight_color=color.smoke,
                x=(-5+i)*1.1,
                z=curve.out_quad_boomerang(i/9) * -4
                )
            tooth_base.look_at(Vec3(0,0,2))

            tooth = Entity(
                parent=tooth_base,
                model=copy(self.tooth_model.model),
                origin_y=-.5,
                texture='white_cube',
                scale=1.1,
                enabled=False
                )
            tooth_base.tooth = tooth

            if random.random() < .1:
                tooth.color = color.gold

            tooth_base.on_click = Sequence(
                Func(setattr, tooth_base.children[0], 'enabled', True),
                Func(self.check_for_win),
                )


            tooth.enabled = random.random() < .5

        return jaw



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
            for c in self.jaw.children:
                c.on_click()


if __name__ == '__main__':
    app = Ursina()

    JawMinigame()
    window.color = color._32
    editor_camera = EditorCamera()
    editor_camera.rotation_x = 20
    app.run()
