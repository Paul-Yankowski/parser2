import requests
import json
cars = []
phones=[]
headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
'accept':'*/*' }
def get_data():
    for i in range(1,4):
        URL = 'https://ab.onliner.by/sdapi/ab.api/search/vehicles?page='+str(i)+'&extended=true&limit=50'
        cars_resp=requests.get(URL,headers=headers)
        data = cars_resp.json()
        for car in range(0,50):
            cars.append(data['adverts'][car])
            phone = 'https://ab.onliner.by/sdapi/ab.api/vehicles/' + str(data['adverts'][car].get('id')) + '/phones'
            phones_resp=requests.get(phone,headers=headers)
            phones.append(phones_resp.json())
def parse_data():
    get_data()
    parsedCars = []
    count = 0
    for car in cars:
        parsedCar={
        'car': car.get('title'),
        'year': car.get('specs').get('year'),
        'engine': str(car.get('specs').get('engine').get('capacity'))+' '+
                   str(car.get('specs').get('engine').get('type')),
        'transmission': car.get('specs').get('transmission'),
        'odometer': str(car.get('specs').get('odometer').get('value'))+' km',
        'price': str(car.get('price').get('amount'))+' USD',
        'seller': car.get('seller').get('name'),
        'phones': phones[count]
                }
        count += 1
        parsedCars.append(parsedCar)
    return parsedCars

def start():
    with open('onliner_cars.json', 'w') as f:
        for car in parse_data():
            json.dump(car, f,ensure_ascii=False)
start()


