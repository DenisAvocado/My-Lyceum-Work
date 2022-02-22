import pygame


size = width, height = 501, 501
CENTER = (width // 2, height // 2)

with open('points.txt') as f:
    points = []
    data = f.readlines()
    for elem in data:
        elem = elem.strip()
        for line in elem.split(', '):
            line = line[1:-1]
            dot = []
            for point in line.split(';'):
                if point[-1] == ')':
                    point = point[:-1]
                if ',' in point:
                    point = point[:point.index(',')] + '.' + point[point.index(',') + 1:]
                if dot:
                    dot.append(height - (float(point) * 20 + CENTER[1]))
                else:
                    dot.append(float(point) * 20 + CENTER[0])
            points.append(dot)
    max_x, min_x = max([p[0] for p in points]), min([p[0] for p in points])
    max_y, min_y = max([p[1] for p in points]), min([p[1] for p in points])
    center_x = (max_x + min_x) // 2
    center_y = (max_y + min_y) // 2
    print(max_x, min_x)
    print(max_x, min_y)
    print(center_x, center_y)


print(points)


class Figure:
    def __init__(self):
        self.zoom = 1

    def draw(self):
        pygame.draw.polygon(screen, 'white', points, 1)

    def count(self):
        if self.zoom <= 0:
            self.zoom = 0.1
        for i in range(len(points)):
            points[i][0] = points[i][0] * self.zoom + (center_x - (center_x * self.zoom))
            points[i][1] = points[i][1] * self.zoom + (center_y - (center_y * self.zoom))


figure = Figure()

pygame.init()
pygame.display.set_caption('Zoom')
screen = pygame.display.set_mode(size)
running = True
figure.draw()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
            if figure.zoom < 1:
                figure.zoom = 1
            figure.zoom += 0.01
            figure.count()
            pygame.display.flip()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
            if figure.zoom > 1:
                figure.zoom = 1
            figure.zoom -= 0.01
            figure.count()
            pygame.display.flip()
        screen.fill('black')
        figure.draw()
        pygame.display.flip()
pygame.quit()