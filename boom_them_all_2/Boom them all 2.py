import os
import pygame
import random

pygame.init()
pygame.display.set_caption('Boom Them All 2')
size = width, height = 500, 500
screen = pygame.display.set_mode(size)


def load_image(name, color_key=None):
    full_name = os.path.join('data', name)
    try:
        image = pygame.image.load(full_name)
    except pygame.error as message:
        print(f'В папке отсутствует файл {name}')
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


class Bomb(pygame.sprite.Sprite):
    image = load_image("bomb.png")

    def __init__(self, pos):
        super().__init__(all_sprites)
        self.image = Bomb.image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.size_x = 50
        self.size_y = 51
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, pos):
        for key, val in bombs.items():
            if key[0] <= pos[0] <= key[0] + self.rect.width\
                    and (key[1]) <= pos[1] <= key[1] + self.rect.height:
                bombs[key].image = load_image('boom.png')


def intersection(bomba, x, y):
    x0_1 = bomba.rect.x
    y0_1 = bomba.rect.y
    x1_1, y1_1 = x0_1 + bomba.size_x, y0_1 + bomba.size_y
    x1_2, y1_2 = x + bomba.size_x, y + bomba.size_y
    x_inter = max(x0_1, x)
    y_inter = max(y0_1, y)
    x_inter_1 = min(x1_1, x1_2)
    y_inter_1 = min(y1_1, y1_2)
    if x_inter > x_inter_1 or y_inter > y_inter_1:
        return False
    else:
        return True


all_sprites = pygame.sprite.Group()
clock = pygame.time.Clock()

bombs = {}
bombs_list = []

count = 0
while count < 20:
    x = random.randint(0, width - 100)
    y = random.randint(0, height - 101)
    if bombs_list:
        inter = False
        for bomb in bombs_list:
            if intersection(bomb, x, y):
                inter = True
        if not inter:
            b = Bomb((x, y))
            bombs_list.append(b)
            bombs[(x, y)] = b
            count += 1
    else:
        b = Bomb((x, y))
        bombs_list.append(b)
        bombs[(x, y)] = b
        count += 1

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            all_sprites.update(event.pos)
    screen.fill('black')
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(50)
pygame.quit()