from ursina import *

class DialogueBox(Entity):
    def __init__(self, texts, **kwargs):
        super().__init__(
            model='quad',
            color=color.black,
            scale_y = 0.4,
            scale_x = 1.5,
            y = -0.2,
            x = 0,
            z = -2);

        self.name_text = Text(
            scale = 2,
            y = -0.1,
            x = -0.4,
            z = -5,
            )
        # self.name_text.world_parent = self
        self.t = Text(
            scale = 2,
            y = -0.2,
            x = -0.4,
            z = -5,
            )
        # self.t.world_parent = self

        self.image = Entity(
            model='quad',
            texture='portrait_Sabrina',
            parent=self,
            x = -0.35,
            scale_y = 0.5
            )

        self.image.world_scale_x = self.image.world_scale_y

        self.texts = texts
        self.current_text = 0

        for key, value in kwargs.items():
            setattr(self, key, value)


    @property
    def current_text(self):
      return self._current_text

    @current_text.setter
    def current_text(self, value):
        self._current_text = value
        if (value >= len(self.texts)):
            destroy(self.t)
            destroy(self.name_text)
            destroy(self)
        self.name_text.text = "<yellow>" + self.texts[value][0]
        self.image.texture = "textures/portrait_" + self.texts[value][0]
        self.t.text = self.texts[value][1]
        self.t.appear()





if __name__ == '__main__':
    app = Ursina()
    enemy = DialogueBox([
        ["Tooth criminal", "Omg"],
        ["Tooth criminal", "There are people here"],
        ["Tooth criminal", "I gotta..\nI gotta knock their <red>teeth <default>out!"]
        ],
        enabled=True)
    camera.orthographic
    camera.fov = 20
    def input(key):
        if key == 'tab':
            enemy.enabled = not enemy.enabled

    app.run()
