import scrapy


class UdacitySpider(scrapy.Spider):
    name = 'udacity'
    start_urls = ['https://www.udacity.com/courses/all/']

    def parse_detail(self, response):
        title = response.xpath('//h1/text()').extract_first()
        headline = response.xpath('//div[contains(@class, "legible")]/text()').extract_first()
        image = response.xpath('//div/div/section/div/div[2]/section[1]/div[1]').extract_first()

        instructors = []
        for div in response.xpath('//div[contains(@class, "card instructor")]'):
            instructors.append(
                {
                    'name': div.xpath('.//h5/text()').extract_first(),
                    'image': div.xpath('.//img/@src').extract_first()
                }
            )
        yield {
            'title': title,
            'headline': headline,
            'image': image,
            'instructors': instructors
        }

    def parse(self, response):
        divs = response.xpath('//*[@id="__next"]/div/div/div[2]/div[2]/div/div[2]/main/div[2]/ul/li/article')
        for div in divs:
            link = div.xpath('.//a')
            href = link.xpath('./@href').extract_first()
            yield scrapy.Request(
                url=f'https://www.udacity.com{href}',
                callback=self.parse_detail
            )
            # title = link.xpath('./@aria-label').extract_first()
            # img = link.xpath('.//div[1]/div/div[2]').extract_first()
            # description = link.xpath('.//div[3]/section/p/text()').extract_first()
            # yield {
            #     'title': title,
            #     'url': href,
            #     'img': img,
            #     'description': description
            # }
