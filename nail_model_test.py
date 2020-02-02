from ursina import *




app = Ursina()

nail_model = Entity(
    model=Prismatoid(
        base_shape=Circle(10),
        path=(Vec3(0,0,0), Vec3(0,.9+.5,0), Vec3(0,.91+.5,0), Vec3(0,1+.5,0)),
        thicknesses=(.2,.2,1,1),
        ))

EditorCamera()
app.run()
