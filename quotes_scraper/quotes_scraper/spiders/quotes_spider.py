import scrapy

class QuotesSpider(scrapy.Spider):
    name = "quotes_spider"
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
    ]

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }
            author_page = quote.css('small.author ~ a::attr(href)').get()
            if author_page is not None:
                yield response.follow(author_page, callback=self.parse_author)

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_author(self, response):
        yield {
            'name': response.css('h3.author-title::text').get().strip(),
            'birthdate': response.css('span.author-born-date::text').get(),
            'bio': response.css('div.author-description::text').get().strip(),
        }
