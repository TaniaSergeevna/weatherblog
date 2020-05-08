import scrapy

global weather_today

weather_today = []


class WeatherSpider(scrapy.Spider):
    name = "weather"
    start_urls = [
        'http://www.gismeteo.ua/city/daily/5093/',
    ]

    def parse(self, response):
        time = [str(time) + '.00'
                for time in
                response.xpath('//div[@class="widget__wrap"]/div[@class="widget js_widget"]/div[@class="widget__body"]'
                               '/div[@class="widget__container"]/div[@class="widget__row widget__row_time"]/'
                               'div[@class="widget__item"]/div[@class="w_time"]/span/text()').extract()
                ]

        weather = [weather
                   for weather in response.css('span').xpath('@data-text').extract()
                   ]

        degree = [degree
                  for degree in response.xpath('//div[@class="chart chart__temperature"]/div[@class="values"]'
                                               '/div[@class="value"]'
                                               '/span[@class="unit unit_temperature_c"]/text()').extract()
                  ]

        wind = [str(wind).replace('\n', '').replace(' ', '')
                for wind in response.xpath('//div[@class="widget__row widget__row_table widget__row_wind-or-gust"]'
                                           '/div[@class="widget__item"]/div[@class="w_wind"]'
                                           '/div[@class="w_wind__warning w_wind__warning_ "]'
                                           '/span[@class="unit unit_wind_m_s"]/text()').extract()
                ]
        time.insert(0, 'Time')
        weather.insert(0, 'Weather')
        degree.insert(0, 'Degree')
        wind.insert(0, 'Wind')
        weather_today.append(time)
        weather_today.append(weather)
        weather_today.append(degree)
        weather_today.append(wind)
