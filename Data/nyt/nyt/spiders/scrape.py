import scrapy


class CrossWord(scrapy.Spider):
    #  this class scraps all the cross words for NYTimes
    name = "crossword"
    start_date = '1/27/2020'
    start_urls = [
        f'https://www.xwordinfo.com/Crossword?date={start_date}',
    ]

    def parse(self, response):

        hxs = scrapy.Selector(response)
        count = 0
        count_till_skip = 0
        across_dict = {}
        for row in response.xpath('//*[@id="ACluesPan"]/div[2]//text()').getall():
            across_dict['direction'] = 'Across'

            # every odd row is a question and every even row is an answer
            if count % 2 == 0:
                across_dict['answers'] = row
            else:
                across_dict['question'] = row

            count += 1
            count_till_skip += 1
            # every third data pulled from scrapy is not needed so we skip it with this code
            if count_till_skip == 3:
                yield across_dict
                count = 0
                count_till_skip = 0

        count = 0
        count_till_skip = 0
        down_dict = {}
        for row in response.xpath('//*[@id="DCluesPan"]/div[2]//text()').getall():

            down_dict['direction'] = 'Down'
            if count % 2 == 0:
                down_dict['answers'] = row
            else:
                down_dict['question'] = row

            count += 1
            count_till_skip += 1
            # every third data pulled from scrapy is not needed so we skip it with this code
            if count_till_skip == 3:
                yield down_dict
                count = 0
                count_till_skip = 0

        next_page = response.xpath('//*[@id="CPHContent_BotLinks"]/a[2]/@href').get()
        if next_page is not None:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko)'
                              ' Chrome/51.0.2704.84 Safari/537.36'
            }

            yield response.follow(next_page, callback=self.parse, headers=headers, meta={'dont_merge_cookies': True})
