import requests

from distance import lonlat_distance


API_KEY = '40d1649f-0493-4b70-98ba-98533de7710b'


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


def get_coordinates(address):
    toponym = geocode(address)
    if not toponym:
        return None, None
    else:
        longitude, latitude = toponym["Point"]["pos"].split()
        return float(longitude), float(latitude)


def main():
    try:
        home_address = input('Адрес дома: ')
        school_address = input('Адрес школы: ')
        print(f'{round(lonlat_distance(get_coordinates(home_address), get_coordinates(school_address)))} м')
    except Exception:
        print('Неверный адрес')


if __name__ == '__main__':
    main()

# Для теста
# Омск, ул.Волгоградская, 26
# Омск, Лесной проезд, 5

