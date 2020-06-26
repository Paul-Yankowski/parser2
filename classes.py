import json

import requests


class Query_Manager:
    cars = []
    phones = []
    def __init__(self) :
        self.get_data()

    def get_data(self):

        headers = {
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
            'accept': '*/*'}

        URL = 'https://ab.onliner.by/sdapi/ab.api/search/vehicles?page=' + str(1) + '&extended=true&limit=50'
        cars_resp = requests.get(URL, headers=headers)
        data = cars_resp.json()
        for car in range(0, 50):
            self.cars.append(data['adverts'][car])
            phone = 'https://ab.onliner.by/sdapi/ab.api/vehicles/' + str(data['adverts'][car].get('id')) + '/phones'
            phones_resp = requests.get(phone, headers=headers)
            self.phones.append(phones_resp.json())

class Parser:
    parsed_data =[]
    # def __init__(self):
    #     self.parse_data()
    #     print(self.parsed_data)
    def parse_data(self, query):
        count = 0
        for car in query.cars:
            parsedCar = {
                'car': car.get('title'),
                'year': car.get('specs').get('year'),
                'engine': str(car.get('specs').get('engine').get('capacity')) + ' ' +
                          str(car.get('specs').get('engine').get('type')),
                'transmission': car.get('specs').get('transmission'),
                'odometer': str(car.get('specs').get('odometer').get('value')) + ' km',
                'price': str(car.get('price').get('amount')) + ' USD',
                'seller': car.get('seller').get('name'),
                'phones': query.phones[count]
            }
            count += 1
            self.parsed_data.append(parsedCar)

class Processor:
    parsing = Parser()
    parsing.parse_data(query=Query_Manager())
    with open('onliner_cars_classes.json', 'w') as f:
        for car in parsing.parsed_data:
            json.dump(car, f,ensure_ascii=False)
