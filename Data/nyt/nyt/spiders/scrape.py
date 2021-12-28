import scrapy


class CrossWord(scrapy.Spider):
    name = "crossword"
    start_urls = [
        'https://www.xwordinfo.com/Crossword?date=1/27/2020',
    ]

    def parse(self, response):

        hxs = scrapy.Selector(response)
        count = 0
        count2 = 0
        d = {}
        for row in response.xpath('//*[@id="ACluesPan"]/div[2]//text()').getall():
            d['direction'] = 'Across'

            if count % 2 == 0:
                d['answers'] = row
            else:
                d['question'] = row

            count+=1
            count2 += 1
            if count2 == 3:
                yield (d)
                count=0
                count2 = 0

        count = 0
        count2 = 0
        d = {}
        for row in response.xpath('//*[@id="DCluesPan"]/div[2]//text()').getall():

            d['direction'] = 'Down'
            if count % 2 == 0:
                d['answers'] = row
            else:
                d['question'] = row

            count += 1
            count2 += 1
            if count2 == 3:
                yield (d)
                count=0
                count2 = 0


        next_page = response.xpath('//*[@id="CPHContent_BotLinks"]/a[2]/@href').get()
        if next_page is not None:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36'
            }

            yield response.follow(next_page, callback=self.parse, headers=headers, meta={'dont_merge_cookies': True})

