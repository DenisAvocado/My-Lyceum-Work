import os
import pygame

pygame.init()
pygame.display.set_caption('Машинка')
size = width, height = 600, 95
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


class Car(pygame.sprite.Sprite):
    image = load_image("car2.png")

    def __init__(self, pos):
        super().__init__(all_sprites)
        self.image = Car.image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.move_one = 1

    def update(self):
        self.rect = self.rect.move(self.move_one, 0)
        if self.rect.x + self.rect.width == width:
            self.image = pygame.transform.flip(self.image, True, False)
            self.move_one = -1
        if self.rect.x == 0 and self.move_one == -1:
            self.image = pygame.transform.flip(self.image, True, False)
            self.move_one = 1


all_sprites = pygame.sprite.Group()
clock = pygame.time.Clock()

car = Car((0, 5))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill('white')
    all_sprites.draw(screen)
    all_sprites.update()
    pygame.display.flip()
    clock.tick(50)
pygame.quit()