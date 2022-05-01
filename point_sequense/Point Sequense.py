import requests
import pygame
import os
import distance

with open('points.txt', 'rt', encoding='utf-8') as f:
    text = f.readlines()

points = []
for line in text:
    for p in line.split(';'):
        la, lo = p.strip().split(',')
        points.append(','.join([lo, la]))

meters = 0
for i in range(1, len(points)):
    la, lo = [float(loa) for loa in points[i - 1].split(',')], [float(loa) for loa in points[i].split(',')]
    meters += distance.lonlat_distance(la, lo)
print(f'Длина пути равна {round(meters / 1000, 2)} км')

med_la = sum([float(la.split(',')[0]) for la in points]) / len(points)
med_lo = sum([float(lo.split(',')[1]) for lo in points]) / len(points)

pygame.display.set_caption('Первый поход до ЖД Вокзала')
request = f'https://static-maps.yandex.ru/1.x/?l=map&pl={",".join(points)}&pt={med_la},{med_lo},pm2dgl'
response = requests.get(request)
map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(response.content)

pygame.init()
screen = pygame.display.set_mode((600, 450))

screen.blit(pygame.image.load(map_file), (0, 0))

pygame.display.flip()
while pygame.event.wait().type != pygame.QUIT:
    pass
pygame.quit()

os.remove(map_file)