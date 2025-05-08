import pygame

from core.ai_difficult import get_ai_function
from core.scene import Scene

def testFunc():
    print("Select AI")

class AISelect2Scene(Scene):
    def __init__(self, screen, context, switch_scene):
        super().__init__(screen, context)
        self.switch_scene = switch_scene
        self.font = pygame.font.SysFont(None, 36)
        self.buttons_white = [
            (pygame.Rect(100, 150+i*70, 150, 50), label, diff)
            for i, (label, diff) in enumerate([("Easy", "easy"), ("Medium", "medium"), ("Hard", "hard"), ("Random", "random")])
        ]
        self.buttons_black = [
            (pygame.Rect(400, 150+i*70, 150, 50), label, diff)
            for i, (label, diff) in enumerate([("Easy", "easy"), ("Medium", "medium"), ("Hard", "hard"), ("Random", "random")])
        ]
        self.white_choice = None
        self.black_choice = None
        self.play_button = pygame.Rect(250, 450, 200, 50)
        self.back_button = pygame.Rect(10, 10, 100, 40)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for rect, _, diff in self.buttons_white:
                if rect.collidepoint(event.pos):
                    self.white_choice = diff
            for rect, _, diff in self.buttons_black:
                if rect.collidepoint(event.pos):
                    self.black_choice = diff
            if self.play_button.collidepoint(event.pos):
                if self.white_choice and self.black_choice:
                    w_func = get_ai_function(self.white_choice)
                    b_func = get_ai_function(self.black_choice)
                    self.context.set_ai_vs_ai(self.white_choice, w_func, self.black_choice, b_func)
                    self.switch_scene("gameplay_ai_ai")
            if self.back_button.collidepoint(event.pos):
                self.switch_scene("main_menu")

    def render(self):
        self.screen.fill((50, 50, 50))

  
        for rect, label, diff in self.buttons_white:
            color = (180, 220, 255) if self.white_choice == diff else (255, 255, 255)
            pygame.draw.rect(self.screen, color, rect)
            text_surf = self.font.render(label, True, (0, 0, 0))
            text_rect = text_surf.get_rect(center=rect.center)
            self.screen.blit(text_surf, text_rect)

        for rect, label, diff in self.buttons_black:
            color = (200, 200, 200) if self.black_choice == diff else (255, 255, 255)
            pygame.draw.rect(self.screen, color, rect)
            text_surf = self.font.render(label, True, (0, 0, 0))
            text_rect = text_surf.get_rect(center=rect.center)
            self.screen.blit(text_surf, text_rect)

        pygame.draw.rect(self.screen, (100, 255, 100), self.play_button)
        self.screen.blit(self.font.render("Play", True, (0, 0, 0)), (self.play_button.x+60, self.play_button.y+10))

        pygame.draw.rect(self.screen, (255, 100, 100), self.back_button)
        self.screen.blit(self.font.render("Back", True, (0, 0, 0)), (self.back_button.x+10, self.back_button.y+5))
