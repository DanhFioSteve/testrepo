import scrapy

class GoodreadsSpider(scrapy.Spider):
    name = "goodreads"
    start_urls = ['https://www.goodreads.com/list/show/1.Best_Books_Ever']

    def parse(self, response):
        for book in response.css('tr'):
            yield {
                'title': book.css('a.bookTitle span::text').get(),
                'author': book.css('a.authorName span::text').get(),
                'rating': book.css('span.minirating::text').get(),
                'details': book.css('a.bookTitle::attr(href)').get(),
                'description': book.css('span.readable span::text').get(),
                'num_reviews': book.css('a.gr-hyperlink::text').re_first(r'\d+'),
                'num_ratings': book.css('span.votes.value-title::text').re_first(r'\d+'),
                'published_year': book.css('span.greyText.smallText.uitext::text').re_first(r'\d{4}'),
                'genres': book.css('a.actionLinkLite.bookPageGenreLink::text').getall(),
                'isbn': book.css('div.infoBoxRowItem span::text').re_first(r'\d+'),
            }

        next_page = response.css('a.next_page::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)