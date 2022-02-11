import random
import pygame
import os


def load_image(name, color_key=None):
    full_name = os.path.join('data', name)
    try:
        image = pygame.image.load(full_name)
    except pygame.error as message:
        print(f'В папке отсутствует файл {name}')
        raise SystemExit(message)

    if color_key == -1:
        color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


class Creature(pygame.sprite.Sprite):
    image = load_image('creature.png')

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Creature.image
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(width)
        self.rect.y = random.randrange(height)

    def update(self, *args):
        if args[0] == 1:
            self.rect = self.rect.move(-10, 0)
        elif args[0] == 2:
            self.rect = self.rect.move(10, 0)
        elif args[0] == 3:
            self.rect = self.rect.move(0, -10)
        elif args[0] == 4:
            self.rect = self.rect.move(0, 10)


if __name__ == '__main__':
    pygame.init()

    size = width, height = (500, 500)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Герой двигается!')
    all_sprites = pygame.sprite.Group()

    Creature(all_sprites)

    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    num = 1
                if event.key == pygame.K_RIGHT:
                    num = 2
                if event.key == pygame.K_UP:
                    num = 3
                if event.key == pygame.K_DOWN:
                    num = 4
                for cr in all_sprites:
                    all_sprites.update(num)

        screen.fill('white')
        all_sprites.draw(screen)
        pygame.display.flip()

    pygame.quit()