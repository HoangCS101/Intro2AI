
import pygame
from core.context import Context

from scenes.ai_select_1 import AISelect1Scene
from scenes.ai_select_2 import AISelect2Scene
from scenes.gameplay_ai_ai import GameplayAIAIScene
from scenes.gameplay_player_ai import GameplayPlayerAIScene
from scenes.main_menu import MainMenuScene

board_width = board_height = 680 
move_log_panel_width = 210  # May want to adjust this if the board_width/board_height is changed.
move_log_panel_height = board_height

pygame.init()
screen = pygame.display.set_mode((board_width + move_log_panel_width, board_height))
context = Context()
clock = pygame.time.Clock()
scenes = {}
current_scene = None

def switch_scene(name):
    global current_scene
    if name not in scenes:
        if name == "main_menu":
            scenes[name] = MainMenuScene(screen, context, switch_scene)
        elif name == "ai_select_1":
            scenes[name] = AISelect1Scene(screen, context, switch_scene)
        elif name == "ai_select_2":
            scenes[name] = AISelect2Scene(screen, context, switch_scene)
        elif name == "gameplay_player_ai":
            scenes[name] = GameplayPlayerAIScene(screen, context, switch_scene)
        elif name == "gameplay_ai_ai":
            scenes[name] = GameplayAIAIScene(screen, context, switch_scene)
    current_scene = scenes[name]
    context.current_scene = name

switch_scene("main_menu")

running = True
while running:
    if callable(getattr(current_scene, 'pre_event', None)):
        current_scene.pre_event()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        else:
            current_scene.handle_event(event)

    current_scene.update()
    current_scene.render()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
