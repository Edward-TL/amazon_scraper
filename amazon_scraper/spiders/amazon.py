import scrapy


class AmazonSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = [
        'https://www.amazon.com.mx/gp/bestsellers/digital-text/ref=zg_bs_digital-text_home_all?pf_rd_p=01d2df49-74bd-42d3-a898-95a4f3beb031&pf_rd_s=center-4&pf_rd_t=2101&pf_rd_i=home&pf_rd_m=AVDBXBAVVSXLQ&pf_rd_r=6APAMAKKFSPVHG8MWSXT&pf_rd_r=6APAMAKKFSPVHG8MWSXT&pf_rd_p=01d2df49-74bd-42d3-a898-95a4f3beb031'
    ]

    def parse(self, response):
        print('*' * 10)
        print('\n\n')

        ranking = response.xpath('//span[@class=“zg-badge-text”]/text()').getall()
        image_urls = response.xpath('//div[@id="zg-center-div"]//div[@class="a-section a-spacing-small"]/img[@src]').getall()
        products = response.xpath('//div[@id="zg-center-div"]//div[contains(@class, "p13n-sc-truncated")]/text()').getall()
        star_ratings = response.xpath('//div[@id="zg-center-div"]//span[@class="a-icon-alt"]/text()').getall()
        q_reviews = response.xpath('//div[@id="zg-center-div"]//a[@class="a-size-small a-link-normal"]/text()').getall()
        min_price = response.xpath('//div[@id="zg-center-div"]//span[@class="p13n-sc-price"][1]/text()').getall()
        max_price = response.xpath('//div[@id="zg-center-div"]//span[@class="p13n-sc-price"][2]/text()').getall()
        autor = response.xpath('//div[@id="zg-center-div"]//span[@class="a-size-small a-color-base"]/text()').getall()
        edition = response.xpath('//div[@id="zg-center-div"]//span[@class="a-size-small a-color-secondary"]/text()').getall()

        try:
            for book in range(len(ranking)):
                info = f'''Position: #{ranking[book]}
                image_src: {image_urls[book]}
                book name: {products[book]}
                stars: {star_ratings[book]}
                number of reviews: {q_reviews[book]}
                price: {min_price[book]}
                autor: {autor[book]}
                edition: {edition[book]}
                
                --------------------------------------

                '''
                print()
        except:
            pass
        
        # print(response.status, response.headers)
        print('\n\n')
        print('*' * 10)