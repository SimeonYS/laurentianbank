import re
import scrapy
from scrapy.loader import ItemLoader
from ..items import LlaurentianbankItem
from itemloaders.processors import TakeFirst

pattern = r'(\xa0)?'

class LlaurentianbankSpider(scrapy.Spider):
	name = 'laurentianbank'
	start_urls = ['https://www.laurentianbank.ca/en/about/my_news/index.sn']

	def parse(self, response):
		post_links = response.xpath('//div[@id="content2"]/a[@target="_self"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		date = response.xpath('//div[@id="content2"]/div/b/following-sibling::text()').get()
		date = re.findall(r'\d+\s\w+\s\d+', date)
		title = response.xpath('//div[@id="content2"]/div/b/text()').get()
		content = response.xpath('//div[@id="content2"]//text()[not (ancestor::div/b)]').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))

		item = ItemLoader(item=LlaurentianbankItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		yield item.load_item()
