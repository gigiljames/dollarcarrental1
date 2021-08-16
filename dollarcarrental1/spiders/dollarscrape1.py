import scrapy
from ..items import Dollarcarrental1Item
from datetime import datetime

class Dollarscrape1Spider(scrapy.Spider):
    name = 'dollarscrape1'
    #allowed_domains = ['dollar.com']
    start_urls = ['http://dollar.com/']

    def start_requests(self):
        urls = [r'https://www.dollar.com/loc/modules/multilocation/?near_location=10010&services__in=&language_code=en-us&published=1&within_business=true',r'https://www.dollar.com/loc/modules/multilocation/?near_location=10018&services__in=&language_code=en-us&published=1&within_business=true']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_page)

    def parse_page(self, response):
        items = Dollarcarrental1Item()
        json_response = response.json()
        for i in json_response.get('objects', []):
            phone = []
            for j in i.get('phones', []):
                phone.append(j.get('number', ''))
            weektimes = ['Monday : ','Tuesday : ','Wednesday : ','Thursday : ','Friday : ','Saturday : ','Sunday : ']
            times = i.get('hours_by_type', {}).get('primary',{}).get('hours',[])
            for m in range(7):
                for n in range(2):
                    t = times[m][0][n]
                    t += ' '
                    t = t.replace(":00 ",'')
                    # print(t)
                    d = datetime.strptime(t, "%H:%M")
                    times[m][0][n] = d.strftime("%I:%M%p")
                time_per_day = ' - '.join(times[m][0])
                weektimes[m] += time_per_day
            # print(weektimes)
            items = {
                'StoreID':i.get('id', ''), 
                'StoreName':i.get('location_name', ''), 
                'Street':i.get('street', ''), 
                'City':i.get('city', ''), 
                'State':i.get('state', ''), 
                'StoreTiminings':' | '.join(weektimes),
                'Phone':', '.join(phone),
                'Latitude':i.get('lat', ''),
                'Longitude':i.get('lon', ''),
                }
            yield items
        
