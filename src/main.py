import pygame
from constants import (
    BACKGROUNG_IMG,
    FILE_LEVEL,
    HERO_IMG,
    WINDOW_SIZE
)
from utils.functions import display_sentence
from utils.models import *


# Initialize pygame.
pygame.init()

# Create the window.
window = pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE)
# Background image.
background_menu = pygame.transform.scale(
    pygame.image.load(BACKGROUNG_IMG).convert_alpha(),
    WINDOW_SIZE
)

# Condition loop for the menu.
menu = True
# Condition loop for the game continue.
play = False
while menu:
    # Catch user events.
    for event in pygame.event.get():
        if (event.type == pygame.QUIT or
                event.type == pygame.KEYDOWN and
                event.key == pygame.K_ESCAPE):
            menu = False
        elif (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN):
            # Initialize the level.
            level = Level(FILE_LEVEL)
            level.generate_level()
            player_start_position = level.positions['player']
            end_position = level.positions['end']
            items_position = level.positions['items']
            walls_position = level.positions['walls']

            # Initialize the characters.
            player = Player(HERO_IMG, player_start_position,
                            end_position, items_position, walls_position)
            play, menu = True, False
        window.blit(background_menu, (0, 0))
        display_sentence(window, 'start')

    while play:
        # Catch user events.
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                menu, play = False, False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    play, menu = False, True
                elif (event.key == pygame.K_i):
                    if player.should_show_pocket:
                        player.should_show_pocket = False
                    else:
                        player.should_show_pocket = True
                elif (event.key == pygame.K_UP or
                      event.key == pygame.K_RIGHT or
                      event.key == pygame.K_DOWN or
                      event.key == pygame.K_LEFT):
                    # Change the position of the main character.
                    player.move_player(event.key)
                    # Check if we have some item to remove in the structure
                    if player.item_collected is not None:
                        item_position = player.item_collected
                        level.remove_item(item_position)
                        player.item_collected = None
        # Show the level.
        level.show_level(window)
        # Show the character.
        player.show_player(window)
        # Show all items collected
        player.show_pocket(window)
        # Check if the game is ended.
        player.check_status(window)
        # Re-initialize the display.
        pygame.time.Clock().tick(30)
        pygame.display.flip()

    pygame.time.Clock().tick(30)
    pygame.display.flip()


pygame.quit()
