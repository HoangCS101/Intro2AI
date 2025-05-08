import pygame
from core.scene import Scene

class MainMenuScene(Scene):
    def __init__(self, screen, context, switch_scene):
        super().__init__(screen, context)
        self.switch_scene = switch_scene
        self.font = pygame.font.SysFont(None, 40)
        self.buttons = [
            (pygame.Rect(300, 200, 200, 50), "Player vs AI", lambda: switch_scene("ai_select_1")),
            (pygame.Rect(300, 300, 200, 50), "AI vs AI", lambda: switch_scene("ai_select_2"))
        ]

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for rect, _, callback in self.buttons:
                if rect.collidepoint(event.pos):
                    callback()

    def render(self):
        self.screen.fill((0, 0, 0))
        for rect, text, _ in self.buttons:
            pygame.draw.rect(self.screen, (255, 255, 255), rect)
            label = self.font.render(text, True, (0, 0, 0))
            text_rect = label.get_rect(center=rect.center)
            self.screen.blit(label, text_rect)
