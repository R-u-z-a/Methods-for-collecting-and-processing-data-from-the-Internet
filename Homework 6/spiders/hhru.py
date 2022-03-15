import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = [
        'https://hh.ru/search/vacancy?area=1&search_field=name&search_field=company_name&search_field=description&text=%D0%BC%D0%B5%D0%BD%D0%B5%D0%B4%D0%B6%D0%B5%D1%80+%D0%BF%D0%BE+%D0%B7%D0%B0%D0%BA%D1%83%D0%BF%D0%BA%D0%B0%D0%BC&order_by=relevance&search_period=0&items_on_page=20&no_magic=true&L_save_area=true',
        'https://hh.ru/search/vacancy?area=2&excluded_text=&search_field=name&search_field=company_name&search_field=description&text=%D0%BC%D0%B5%D0%BD%D0%B5%D0%B4%D0%B6%D0%B5%D1%80+%D0%BF%D0%BE+%D0%B7%D0%B0%D0%BA%D1%83%D0%BF%D0%BA%D0%B0%D0%BC&order_by=relevance&search_period=0&items_on_page=20&no_magic=true&L_save_area=true']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@data-qa='pager-next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath("//a[@data-qa='vacancy-serp__vacancy-title']/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        name = response.xpath("//h1//text()").get()
        salary = response.xpath("//div[@data-qa='vacancy-salary']/span/text()").getall()
        url = response.url
        yield JobparserItem(name=name, salary=salary, url=url)
