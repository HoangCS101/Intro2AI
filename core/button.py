import pygame as p

class Button:
    def __init__(self, rect, text, callback, font, color=(180,180,180), hover_color=(220,220,220)):
        self.rect = p.Rect(rect)
        self.text = text
        self.callback = callback
        self.font = font
        self.color = color
        self.hover_color = hover_color

    def draw(self, screen):
        mouse_over = self.rect.collidepoint(p.mouse.get_pos())
        p.draw.rect(screen, self.hover_color if mouse_over else self.color, self.rect)
        text_surf = self.font.render(self.text, True, (0,0,0))
        screen.blit(text_surf, text_surf.get_rect(center=self.rect.center))

    def handle_event(self, event):
        if event.type == p.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.callback()