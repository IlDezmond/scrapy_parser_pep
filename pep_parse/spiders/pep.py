import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response, **kwargs):
        tr_tags = response.css('section[id=numerical-index] tbody tr')
        for tr_tag in tr_tags:
            td_tags = tr_tag.css('td')
            pep_link = td_tags[1].css('a::attr(href)').get() + '/'
            yield response.follow(
                pep_link,
                callback=self.parse_pep
            )

    def parse_pep(self, response):
        pep_status = response.css(
            'dt:contains("Status:") + dd abbr::text'
        ).get()
        title = response.css('h1.page-title::text').get().split(' – ')
        number = title[0].replace('PEP', '')
        pep_name = title[1]
        data = {
            'number': number,
            'name': pep_name,
            'status': pep_status,
        }
        yield PepParseItem(data)
