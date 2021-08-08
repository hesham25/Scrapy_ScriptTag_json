import scrapy
import json
from requests_html import HTML

class FiSpider(scrapy.Spider):
    name = 'finder'
    start_urls = ['https://www.davidclulow.com/store-finder/']

    def parse(self, response):    
        script = response.xpath('//script[contains(text(),"var maplistScriptParamsKo")]/text()').extract_first()
        script_text = script.split('var maplistScriptParamsKo = ')[1].split('};\n')[0] + '}'
        data_dict = json.loads(script_text)
        data = data_dict['KOObject'][0]['locations']
        for item in data:
            row = {}
            address = item.get('address')
            if address:
                row['title'] = item.get('title')
                description_tag = item.get('description')
                #soup = bf(description_tag, 'html.parser')
                html = HTML(html=description_tag)
                row['storemanager'] = html.xpath('//div[@class="additionalDetail"]//div[@class="storemanager"]/text()',first=True)
                row['optometrist'] = html.xpath('//div[@class="additionalDetail"]//div[@class="optometrist"]/text()',first=True)
                row['servicesavailable'] = html.xpath('//div[@class="additionalDetail"]//div[@class="servicesavailable"]/text()',first=True)
                row['Phone'] = html.xpath('//div[@class="additionalDetail"]//div[@class="telephone"]/a/text()',first=True)
                row['E mail'] = html.xpath('//div[@class="additionalDetail"]//div[@class="email"]//a[contains(@href,"mailto")]/text()',first=True)
                img_tag = html.xpath('//div[@class="additionalDetail"]//img/@src',first=True)
                image = 'https://www.davidclulow.com' + img_tag if img_tag else ''
                row['img'] = image
                row['link'] = html.xpath('//div[@class="additionalDetail"]//a[@class="read-more-button"]/@href',first=True)
                row['address'] = html.find('div.additionalDetail div.address',first=True).full_text
                op_hrs = html.find('div.additionalDetail table',first=True)
                if op_hrs : op_hrs = op_hrs.full_text.strip()
                row['Opening hours'] = op_hrs
                row['latitude'] = item.get('latitude','')
                row['longitude'] = item.get('longitude','')
                yield row
                print()
