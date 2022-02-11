import os
import pygame
import random

pygame.init()
pygame.display.set_caption('Boom Them All')
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

    def update(self, pos):
        for key, val in bombs.items():
            if key[0] <= pos[0] <= key[0] + self.rect.width\
                    and (key[1]) <= pos[1] <= key[1] + self.rect.height:
                bombs[key].image = load_image('boom.png')


all_sprites = pygame.sprite.Group()
clock = pygame.time.Clock()

bombs = {}
for i in range(20):
    x = random.randint(0, width - 50)
    y = random.randint(0, height - 51)
    bombs[(x, y)] = Bomb((x, y))

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