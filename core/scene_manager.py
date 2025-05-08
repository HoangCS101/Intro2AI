class SceneManager:
    def __init__(self, ctx):
        self.ctx = ctx
        self.scene = None

    def go_to(self, scene_class):
        self.scene = scene_class(self)

    def handle_event(self, event):
        if self.scene:
            self.scene.handle_event(event)

    def update(self):
        if self.scene:
            self.scene.update()

    def draw(self, screen):
        if self.scene:
            self.scene.draw(screen)