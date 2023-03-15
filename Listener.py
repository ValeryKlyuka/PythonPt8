import sys
import pygame
import math

def listener(blocks, objects, hero, air, space, fireballs, interface, menu, frame):
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if menu.game_mode == 'game':
                    menu.game_mode = 'menu'
                elif menu.game_mode == 'menu':
                    menu.game_mode = 'game'
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if menu.new_game_rect.collidepoint(event.pos[0], event.pos[1]):
                    menu.game_mode = 'game'
                elif menu.load_game_rect.collidepoint(event.pos[0], event.pos[1]):
                    menu.game_mode = 'load'
                elif menu.exit_rect.collidepoint(event.pos[0], event.pos[1]):
                    sys.exit()

    def get_items(item):
        if item.type in ['монеты', 'ключ', 'здоровье', 'выход', 'воздух']:
            if item.type == 'монеты':
                interface.score += 3
                if interface.score > 20:
                    interface.score = 20
                objects.remove(item)
            elif item.type == 'здоровье':
                interface.health += 3
                if interface.health > 20:
                    interface.health = 20
                objects.remove(item)
            elif item.type == 'ключ':
                interface.key = True
                objects.remove(item)
            elif item.type == 'воздух' and frame in [10, 20 ,30, 40, 50, 60]:
                interface.health -= 1
            elif item.type == 'выход':
                if interface.score == 20 and interface.key:
                    interface.nextlevel = True

    def collision(dir):
        for item in objects:
            if dir == 'up':
                if item.y < hero.y and item.x > hero.x:
                    R = math.hypot(item.x - hero.x, item.y - hero.y)
                    if R != 0.0 and R <= 64:
                        get_items(item)
                        return True
            elif dir == 'down':
                if item.y > hero.y and item.x < hero.x:
                    R = math.hypot(item.x - hero.x, item.y - hero.y)
                    if R != 0.0 and R <= 64:
                        get_items(item)
                        return True
            if dir == 'left':
                if item.x < hero.x and item.y < hero.y:
                    R = math.hypot(item.x - hero.x, item.y - hero.y)
                    if R != 0.0 and R <= 55:
                        get_items(item)
                        return True
            elif dir == 'right':
                if item.x > hero.x and item.y > hero.y:
                    R = math.hypot(item.x - hero.x, item.y - hero.y)
                    if R != 0.0 and R <= 55:
                        get_items(item)
                        return True


    if keys[pygame.K_UP]:
        if not collision('up'):
            for item in blocks: item.y_in += 0.05
            for item in objects: item.y_in += 0.05
            for item in air: item.y_in += 0.05
            for item in space: item.y_in += 0.05
            for item in fireballs: item.y_in += 0.05
        hero.move('walk', 'up', frame // 8)
    elif keys[pygame.K_DOWN]:
        if not collision('down'):
            for item in blocks: item.y_in -= 0.05
            for item in objects: item.y_in -= 0.05
            for item in air: item.y_in -= 0.05
            for item in space: item.y_in -= 0.05
            for item in fireballs: item.y_in -= 0.05
        hero.move('walk', 'down', frame//8)
    if keys[pygame.K_LEFT]:
        if not collision('left'):
            for item in blocks: item.x_in += 0.05
            for item in objects: item.x_in += 0.05
            for item in air: item.x_in += 0.05
            for item in space: item.x_in += 0.05
            for item in fireballs: item.x_in += 0.05
        hero.move('walk', 'left', frame // 8)
    elif keys[pygame.K_RIGHT]:
        if not collision('right'):
            for item in blocks: item.x_in -= 0.05
            for item in objects: item.x_in -= 0.05
            for item in air: item.x_in -= 0.05
            for item in space: item.x_in -= 0.05
            for item in fireballs: item.x_in -= 0.05
        hero.move('walk', 'right', frame // 8)