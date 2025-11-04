# ORM - Object Relation Mapping - відображення даних на об'єкти та 
# зв'язки між ними
import requests


class NbuRate :
    def __init__(self, j:dict):
        '''Очікуються дані у dict, який відображає JSON
        {'r030': 12, 'txt': 'Алжирський динар', 'rate': 0.32011, 'cc': 'DZD', 'exchangedate': '22.10.2025'}'''
        self.r030 = j["r030"]
        self.name = j["txt"]
        self.rate = j["rate"]
        self.abbr = j["cc"]

    def __str__(self):
        return "%s (%s) %f" % (self.abbr, self.name, self.rate)
    


class RatesData :
    def __init__(self):
        self.exchange_date = None
        self.rates = []



class NbuRatesData(RatesData) :   # спадкування іншого класу
    url = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json"

    def __init__(self):
        request = requests.get(NbuRatesData.url)
        response = request.json()
        '''Курси валют за даними НБУ'''
        self.exchange_date = response[0]["exchangedate"]
        self.rates = [NbuRate(r) for r in response]




def main() :
    rates_data:RatesData = NbuRatesData()
    # print(rates_data.exchange_date, *rates_data.rates, sep='\n')
    abbr = input("Введіть код валюти: ")
    # for rate in rates_data.rates :
    #     if rate.abbr == abbr :
    #         print(rate)
    #         break
    # else:
    #     print("Не знайдено") 

    print(
        next((rate for rate in rates_data.rates if rate.abbr == abbr), 
             "Не знайдено"))
    # 2 - знайти за частковим збігом AU:  AUD, XAU
    # 3 - знайти за частковим збігом у назві
        

if __name__ == '__main__':
    main()

'''
Д.З. Реалізувати вибірку курсів валют на задану дату, що вводиться користувачем
документація АРІ:
https://bank.gov.ua/ua/open-data/api-dev
Забезпечити перевірку валідності дати, а також те, що це дата з минулого
Вивести всі курси за абеткою по абревіатурі
'''