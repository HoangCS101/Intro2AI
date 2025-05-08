import pygame
from core.scene import Scene
from core.ai_difficult import get_ai_function

class AISelect1Scene(Scene):
    def __init__(self, screen, context, switch_scene):
        super().__init__(screen, context)
        self.switch_scene = switch_scene
        self.font = pygame.font.SysFont(None, 40)
        self.buttons = [
            (pygame.Rect(300, 150, 200, 50), "Easy", "easy"),
            (pygame.Rect(300, 220, 200, 50), "Medium", "medium"),
            (pygame.Rect(300, 290, 200, 50), "Hard", "hard"),
            (pygame.Rect(300, 360, 200, 50), "Random", "random"),
        ]
        self.back_button = pygame.Rect(10, 10, 100, 40)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for rect, _, difficulty in self.buttons:
                if rect.collidepoint(event.pos):
                    func = get_ai_function(difficulty)
                    self.context.set_player_ai(difficulty, func)
                    self.switch_scene("gameplay_player_ai")
            if self.back_button.collidepoint(event.pos):
                self.switch_scene("main_menu")

    def render(self):
        self.screen.fill((30, 30, 30))
        for rect, text, _ in self.buttons:
            pygame.draw.rect(self.screen, (200, 200, 200), rect)
            self.screen.blit(self.font.render(text, True, (0, 0, 0)), (rect.x+10, rect.y+10))
        pygame.draw.rect(self.screen, (255, 100, 100), self.back_button)
        self.screen.blit(self.font.render("Back", True, (0, 0, 0)), (self.back_button.x+10, self.back_button.y+5))
