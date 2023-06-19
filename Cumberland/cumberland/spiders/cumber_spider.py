import scrapy
from scrapy.http import HtmlResponse
from selenium import webdriver
import time


class CumberSpider(scrapy.Spider):
    name = 'cumber'
    start_urls = ['https://cumberland-eplanning.t1cloud.com/Pages/XC.Track/SearchApplication.aspx?d=thismonth&k=DeterminationDate&']
    
    # def __init__(self):
    #     self.driver = webdriver.Chrome()
    #     options = webdriver.ChromeOptions()
    #     options.add_argument('--disable-aia-fetching')
    #     self.driver = webdriver.Chrome(options=options)


    def parse(self, response):
        # self.driver.get(response.url)
        # body = self.driver.page_source
        # sel_response = HtmlResponse(url=response.url, body=body, encoding='utf-8')
        
        # Extracting data using Scrapy selectors
        results = response.css('div.result')

        for result in results:

            inner_page_url =  result.css("a.search::attr(href)").get()

            # time.sleep(3)
            yield  response.follow(inner_page_url, callback=self.parse_inner_page)
            
        # next_page = sel_response.css('a.action.next').attrib['href']

        # if next_page:
        #     yield sel_response.follow(next_page, callback= self.parse)

    def parse_inner_page(self, response):

        main_data = {
            "Applicant": [i.replace("Applicant - ","") for i in response.css("#ppl div.applicationInfoDetail::text").getall()[:-1]],
            "Application Address": response.css("#addr div.applicationInfoDetail a::text").getall()
        }
    
        details = response.css("div.inlineColumns")

        more_details = { 
            key[:-1] : value
            for (key,value) in
            zip(details.css("div.inlineColumn1::text").getall(),details.css("div.inlineColumn2::text").getall()) 
        }

        main_data.update(more_details)
        yield main_data
