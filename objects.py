import random

import pygame

class Object:
    def __init__(self, display, layer, col_x, col_y, x, y, type, animate = False):
        self.W = display.current_w
        self.H = display.current_h
        self.col_x = col_x
        self.col_y = col_y
        self.layer = layer
        self.x_in = x
        self.y_in = y
        self.frame = 1
        self.anim_dir = 1
        self.y_anim = 0
        self.x = (self.W / 2) + 56 * (self.x_in - self.y_in)
        self.y = (self.H / 2) - (self.layer*64) + 32 * (self.y_in + self.x_in - self.col_y)
        self.type = type

        if self.type in ['ключ', 'здоровье', 'монеты']:
            self.animate = True
        else:
            self.animate = False

        self.tiles = {'воздух' : 'images/tiles/voxelTile_00.png',
                      'трава': 'images/tiles/voxelTile_03.png',
                      'вода': 'images/tiles/voxelTile_06.png',
                      'земля': 'images/tiles/voxelTile_11.png',
                      'песок': 'images/tiles/voxelTile_12.png',
                      'сосна': 'images/tiles/voxelTile_14.png',
                      'береза': 'images/tiles/voxelTile_15.png',
                      'печь': 'images/tiles/voxelTile_17.png',
                      'инструменты': 'images/tiles/voxelTile_18.png',
                      'кирпич' : 'images/tiles/voxelTile_19.png',
                      'руда' : 'images/tiles/voxelTile_31.png',
                      'монеты' : 'images/environment/coin.png',
                      'здоровье' : 'images/environment/heart.png',
                      'ключ' : 'images/environment/keycard.png',
                      'голубая сосна' : 'images/environment/pine_blue.png',
                      'зеленая сосна' : 'images/environment/pine_green.png',
                      'коричневое дерево' : 'images/environment/tree_brown.png',
                      'зеленое дерево' : 'images/environment/tree_green.png',
                      'выход': 'images/environment/escape.png',
                      'x-башня' : 'images/environment/tower_x.png',
                      'y-башня': 'images/environment/tower_y.png'
                      }
        self.image = pygame.image.load(self.tiles[type]).convert_alpha()
    def draw(self, screen):
        self.x = (self.W / 2) + 56 * (self.x_in - self.y_in)

        # анимация статического объекта
        if self.animate:
            if self.frame == 0 or self.frame == 32:
                self.anim_dir *= -1
            self.y_anim -= 1 * self.anim_dir
            self.frame += 1 * self.anim_dir

        self.y = (self.H / 2) + self.y_anim - (self.layer*64) + 32 * (self.y_in + self.x_in - self.col_y)
        self.rect = self.image.get_rect(center=(self.x, self.y))
        screen.blit(self.image, self.rect)

class Fireball:
    def __init__(self, display, layer, col_x, col_y, x, y, type):
        self.dir = random.choice([1,-1])
        self.W = display.current_w
        self.H = display.current_h
        self.layer = layer
        self.col_x = col_x
        self.col_y = col_y
        self.x_in = x
        self.y_in = y
        self.x = (self.W / 2) + 56 * (self.x_in - self.y_in)
        self.y = (self.H / 2) - (self.layer * 64) + 32 * (self.y_in + self.x_in - self.col_y)
        self.type = type
        self.image = pygame.image.load('images/environment/fireball.png')
    def draw(self, screen):
        self.screen = screen
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.screen.blit(self.image, self.rect)
        if self.type == 'x-башня':
            self.x_in += self.dir * 0.05
        elif self.type == 'y-башня':
            self.y_in += self.dir * 0.05
        self.x = (self.W / 2) + 56 * (self.x_in - self.y_in)
        self.y = (self.H / 2) - (self.layer * 64) + 32 * (self.y_in + self.x_in - self.col_y)

class Hero:
    def __init__(self, display, col_x, col_y, x, y, hero = 'girl'):
        self.type = 'персонаж'
        self.W = display.current_w
        self.H = display.current_h
        self.col_x = col_x
        self.col_y = col_y
        self.x_in = x
        self.y_in = y
        self.x = self.W / 2 + 56 * (self.x_in - self.y_in)
        self.y = self.H / 2 + 32 * (self.y_in + self.x_in - self.col_y)
        self.anim = 'walk'
        self.dir = 'down'
        self.frame = 1

        self.image = {'walk' : {'down' : 0, 'up': 0, 'left' : 0, 'right' : 0}}
        item = []
        for dir in range(4):
            move = {0 : 'down', 1 : 'up', 2 : 'right', 3 : 'left'}
            for i in range(1, 9):
                item.append(pygame.image.load(f'images/hero/{hero}/walk_{move[dir]}_{i}.png'))
            self.image['walk'][move[dir]] = item
            item = []
        print(self.image)
    def draw(self, screen):
        self.rect = self.image[self.anim][self.dir][self.frame].get_rect(center=(self.x, self.y))
        screen.blit(self.image[self.anim][self.dir][self.frame], self.rect)
    def move(self, anim, dir, frame):
        self.anim = anim
        self.dir = dir
        self.frame = frame

class Interface:
    def __init__(self, screen, level):
        self.screen = screen
        self.key = False
        self.nextlevel = False
        self.health = 20
        self.score = 0
        self.time = 5
        self.help = ['1.  Найди ключ', '2. Собери монеты', '3. Найди выход']
        self.inventory_image = pygame.image.load('images/Menu/Inventory.png')
        self.inventory_rect = self.inventory_image.get_rect(topleft=(10,10))
        self.time_scale_image = pygame.image.load('images/Menu/Time_scale.png')
        self.time_scale_rect = self.time_scale_image.get_rect(topleft=(400,30))
        self.score_scale_image = pygame.image.load('images/Menu/Score_scale.png')
        self.score_scale_rect = self.score_scale_image.get_rect(topleft=(400, 80))
        self.health_scale_image = pygame.image.load('images/Menu/Health_scale.png')
        self.health_scale_rect = self.health_scale_image.get_rect(topleft=(460, 160))
        self.level_info_image = pygame.image.load('images/Menu/Level_info.png')
        self.level_info_rect = self.level_info_image.get_rect(topleft=(1640, 30))
        self.info_image = pygame.image.load('images/Menu/Info.png')
        self.info_rect = self.info_image.get_rect(topleft=(10, 320))
        # Шкала здоровья и очков
        self.health_point_image = pygame.image.load('images/Menu/Health_point.png')
        self.score_point_image = pygame.image.load('images/Menu/Score_point.png')
        self.time_point_image = pygame.image.load('images/Menu/Score_point.png')
        # Создание шрифта
        self.font1 = pygame.font.Font('fonts/Old-Soviet.otf', 32)
        self.level_text = self.font1.render(f'Уровень {level}', True, 'White')
        self.font2 = pygame.font.Font('fonts/Old-Soviet.otf', 22)
        self.coins = pygame.image.load('images/environment/coin.png')
        self.coins_rect = self.coins.get_rect(center=(120, 150))
        self.keycard = pygame.image.load('images/environment/keycard.png')
        self.keycard_rect = self.keycard.get_rect(center=(260, 160))
    def draw(self):
        self.screen.blit(self.inventory_image, self.inventory_rect)
        self.screen.blit(self.time_scale_image, self.time_scale_rect)
        self.screen.blit(self.score_scale_image, self.score_scale_rect)
        self.screen.blit(self.health_scale_image, self.health_scale_rect)
        self.screen.blit(self.level_info_image, self.level_info_rect)
        self.screen.blit(self.info_image, self.info_rect)

        if self.score == 20:
            self.screen.blit(self.coins, self.coins_rect)
        if self.key:
            self.screen.blit(self.keycard, self.keycard_rect)

        for i in range(self.health):
            self.health_point_rect = self.health_point_image.get_rect(topleft=(533 + i*13, 184))
            self.screen.blit(self.health_point_image, self.health_point_rect)
        for i in range(self.score):
            self.score_point_rect = self.score_point_image.get_rect(topleft=(483 + i*13, 117))
            self.screen.blit(self.score_point_image, self.score_point_rect)
        for i in range(self.time):
            self.time_point_rect = self.time_point_image.get_rect(topleft=(411 + i*13, 43))
            self.screen.blit(self.time_point_image, self.time_point_rect)

        self.screen.blit(self.level_text, (1690, 55))

        line = 0
        for text in self.help:
            if text == self.help[0] and self.key == False:
                self.info_text = self.font2.render(text, True, 'Black')
                self.screen.blit(self.info_text, (36, 416 + line*30))
            elif text == self.help[1] and self.score < 20:
                self.info_text = self.font2.render(text, True, 'Black')
                self.screen.blit(self.info_text, (36, 416 + line*30))
            elif text == self.help[2]:
                self.info_text = self.font2.render(text, True, 'Black')
                self.screen.blit(self.info_text, (36, 416 + line*30))
            line += 1

class Menu:
    def __init__(self, screen):
        self.x = 960
        self.y = 540
        self.game_mode = 'menu'
        self.screen = screen
        self.image = pygame.image.load('images/Menu/Menu.png')
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.font = pygame.font.Font('fonts/Old-Soviet.otf', 16)
        self.new_game = self.font.render('Новая Игра', True, 'White')
        self.new_game_rect = self.new_game.get_rect(center=(960, 472))

        self.load_game = self.font.render('Загрузить', True, 'White')
        self.load_game_rect = self.load_game.get_rect(center=(960, 530))
        self.options = self.font.render('Настройки', True, 'White')
        self.options_rect = self.options.get_rect(center=(960, 588))
        self.exit = self.font.render('Выход', True, 'White')
        self.exit_rect = self.exit.get_rect(center=(960, 646))
    def draw(self):
        self.screen.blit(self.image, self.rect)
        self.screen.blit(self.new_game, self.new_game_rect)
        self.screen.blit(self.load_game, self.load_game_rect)
        self.screen.blit(self.options, self.options_rect)
        self.screen.blit(self.exit, self.exit_rect)
