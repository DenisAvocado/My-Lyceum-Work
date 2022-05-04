import json
import math
import os
import sys
from io import BytesIO
import requests
from PIL import Image
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPixmap


API_KEY = '40d1649f-0493-4b70-98ba-98533de7710b'

apt_name = ''
apt_hours = ''
apt_distance = ''
apt_address = ''


def lonlat_distance(a, b):
    degree_to_meters_factor = 111 * 1000
    a_lon, a_lat = a
    b_lon, b_lat = b

    radians_lattitude = math.radians((a_lat + b_lat) / 2.)
    lat_lon_factor = math.cos(radians_lattitude)

    dx = abs(a_lon - b_lon) * degree_to_meters_factor * lat_lon_factor
    dy = abs(a_lat - b_lat) * degree_to_meters_factor

    distance = math.sqrt(dx * dx + dy * dy)

    return distance


def geocode(address, number=0):
    geocoder_request =\
        f"http://geocode-maps.yandex.ru/1.x/?apikey={API_KEY}&geocode={address}&format=json"
    response = requests.get(geocoder_request)

    if response:
        json_response = response.json()
    else:
        print("Ошибка выполнения запроса:")
        print(geocoder_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")

    toponyms = json_response["response"]["GeoObjectCollection"]["featureMember"]
    return toponyms[number]["GeoObject"] if toponyms else None


def get_ll(address):
    toponym_to_find = address

    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": '40d1649f-0493-4b70-98ba-98533de7710b',
        "geocode": toponym_to_find,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)

    if not response:
        return False

    json_response = response.json()
    try:
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        toponym_coordinates = toponym["Point"]["pos"]
    except Exception:
        return False

    return toponym_coordinates


def get_delta(address1, address2):
    toponym1 = geocode(address1)
    toponym2 = geocode(address2)
    if not toponym1 or not toponym2:
        return None, None

    envelop1 = toponym1['boundedBy']['Envelope']
    envelop2 = toponym2['boundedBy']['Envelope']
    min_x1, min_y1 = envelop1['lowerCorner'].split()
    max_x1, max_y1 = envelop1['upperCorner'].split()
    min_x2, min_y2 = envelop2['lowerCorner'].split()
    max_x2, max_y2 = envelop2['upperCorner'].split()

    dx1 = float(max_x1) - float(min_x1)
    dy1 = float(max_y1) - float(min_y1)
    dx2 = float(max_x2) - float(min_x2)
    dy2 = float(max_y2) - float(min_y2)
    return f'{max(dx1, dx2) + 0.0025},{max(dy1, dy2) + 0.0025}'


def get_image(address):
    global apt_address, apt_name, apt_hours, apt_distance
    try:
        address_ll = ','.join(get_ll(address).split())
    except Exception:
        return False
    # delta = "0.025"

    search_params = {
        "apikey": "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3",
        "text": "аптека",
        "lang": "ru_RU",
        "ll": address_ll,
        "type": "biz"
    }

    response = requests.get("https://search-maps.yandex.ru/v1/", params=search_params)
    if not response:
        return False
    json_response = response.json()
    try:
        organization = json_response["features"][0]
        point = organization["geometry"]["coordinates"]
        org_point = "{0},{1}".format(point[0], point[1])

        apt_name = organization["properties"]["CompanyMetaData"]["name"]
        apt_address = organization["properties"]["CompanyMetaData"]["address"]
        apt_hours = organization["properties"]["CompanyMetaData"]["Hours"]["text"]
        apt_distance = lonlat_distance([float(ll) for ll in get_ll(address).split()],
                                       [float(ll) for ll in get_ll(apt_address).split()])

        pts = [f'{org_point},pm2gnm', f'{address_ll},pm2rdm']
    except Exception:
        return False

    # delta = str(max(abs(float(address_ll.split(',')[0]) - point[0]),
    #                 abs(float(address_ll.split(',')[1]) - point[1])) + 0.005)

    map_params = {
        "ll": address_ll,
        "spn": get_delta(address, apt_address),
        "l": "map",
        "pt": '~'.join(pts)
    }

    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=map_params)
    image = Image.open(BytesIO(response.content))
    image.save('chemistry_near.png')
    return image


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('search_aptek.ui', self)
        self.ok_but.clicked.connect(self.load)

    def load(self):
        if get_image(self.address_line.text()):
            get_image(self.address_line.text())

            self.ad_label.setText(apt_address)
            self.name_label.setText(apt_name)
            self.time_label.setText(apt_hours)
            self.dis_label.setText(f'{str(round(apt_distance))} м')

            pixmap = QPixmap('chemistry_near.png')
            self.apt_photo.setPixmap(pixmap)
            os.remove('chemistry_near.png')
            self.statusBar().showMessage('')
        else:
            self.statusBar().showMessage('Что-то пошло не так')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())


# get_image('Омск, ул. Макохи, 4')
# Омск, ул. Макохи, 4
# Омск, пр-т Космический, 14
# Омск, пр-т Маркса, 61
