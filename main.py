import random

from Listener import listener
from objects import *
from build import *

pygame.init()
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
display = pygame.display.Info()
clock = pygame.time.Clock()
frame = 1

game_mode = 'menu'

col_x = 14
col_y = 14
max_level = 2
level = 1

def start_level(level):
    global ground, objects, air, space, col_x, col_y, map, interface, hero, elements, menu, fireballs
    # Создаём меню
    menu = Menu(screen)
    # Создание карты и объектов на ней
    ground = []
    objects = []
    air = []
    space = []
    fireballs = []

    map = Build(level, col_x, col_y)

    # Создаём меню
    interface = Interface(screen, level)

    # Создание объектов
    for q in range(4):
        for y in range(col_y):
            for x in range(col_x):
                if q == 0:
                    ground.append(Object(display, q, col_x, col_y, x, y, map.layer[q][y][x]))
                if q == 1:
                    if map.layer[0][y][x] == 'вода':
                        objects.append(Object(display, q, col_x, col_y, x, y, 'воздух'))
                    else:
                        objects.append(Object(display, q, col_x, col_y, x, y, map.layer[q][y][x]))
                        if objects[-1].type == 'воздух': objects.remove(objects[-1])
                if q == 2:
                    air.append(Object(display, q, col_x, col_y, x, y, map.layer[q][y][x]))
                if q == 3:
                    space.append(Object(display, q, col_x, col_y, x, y, map.layer[q][y][x]))

    hero = Hero(display, col_x, col_y, 7, 7)

    elements = objects
    elements.append(hero)

start_level(level)

def shot():
    for item in objects:
        if item.type in ['x-башня', 'y-башня'] and random.randint(0, 100) == 50:
            fireballs.append(Fireball(display, item.layer, item.col_x, item.col_y, item.x_in, item.y_in, item.type))

while True:
    listener(ground, objects, hero, air, space, fireballs, interface, menu, frame)
    screen.fill('Black')

    game_mode = menu.game_mode

    if game_mode == 'menu':
        menu.draw()
    elif game_mode == 'load':
        with open('save.txt', mode='r') as file:
            level = int(file.read())
            start_level(level)
            menu.game_mode = 'game'
    elif game_mode == 'game':
        # отрисовка земли
        for item in ground: item.draw(screen)
        # отрисовка объектов
        elements.sort(key=lambda x: x.y)
        for item in elements: item.draw(screen)
        # отрисовка файерболов
        shot()
        for item in fireballs:
            item.draw(screen)
            for obj in elements:
                if obj.type not in ['x-башня', 'y-башня', 'воздух'] and abs(item.x - obj.x) < 10 and abs(item.y - obj.y) < 10:
                    if obj.type == 'персонаж':
                        interface.health -= 3
                    fireballs.remove(item)
                    break

        # отрисовка воздуха
        for item in air: item.draw(screen)
        # отрисовка космоса
        for item in space: item.draw(screen)
        # отрисовка интерфейса
        interface.draw()
        # переход на следующий уровень
        if interface.nextlevel:
            if level < max_level:
                level += 1
                with open('save.txt', mode='r') as file:
                    save_level = int(file.read())
                if save_level < level:
                    with open('save.txt', mode='w') as file:
                        file.write(str(level))
                start_level(level)
                menu.game_mode = 'game'
            else:
                level = 1
                start_level(level)
                menu.game_mode = 'menu'
        if interface.health <= 0 or interface.time <= 0:
            level = 1
            start_level(level)
            menu.game_mode = 'menu'

        frame += 1
        if frame == 64:
            frame = 1
            interface.time -= 1

    pygame.display.update()
    clock.tick(64)