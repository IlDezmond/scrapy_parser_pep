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
            pep_number = td_tags[1].css('::text').get()
            pep_name = td_tags[2].css('::text').get()
            pep_link = td_tags[1].css('a::attr(href)').get() + '/'
            yield response.follow(
                pep_link,
                callback=self.parse_pep,
                cb_kwargs={
                    'number': pep_number,
                    'name': pep_name,
                }
            )

    def parse_pep(self, response, **kwargs):
        pep_status = response.css(
            'dt:contains("Status:") + dd abbr::text'
        ).get()
        kwargs.update({'status': pep_status})

        yield PepParseItem(kwargs)
