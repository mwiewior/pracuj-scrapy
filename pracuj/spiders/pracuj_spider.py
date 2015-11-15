import scrapy
import re
from pracuj.items import PracujItem

class PracujSpider(scrapy.Spider):
	name = "pracuj"
	allowed_domains = ["pracuj.pl"]
	#start_urls = ["http://www.pracuj.pl/praca?sal=15000"]
	start_urls = ['http://www.pracuj.pl/praca/call%20center;cc,5006']

	
	def parse(self, response):
	    for p in range(1,2):
		pageUrl=self.start_urls[0]+"/?pn="+str(p)
                yield scrapy.Request(pageUrl, self.parse_pages)
	
	def parse_pages(self, response):
	    for href in response.xpath('//*[@id="mainOfferList"]//li/h2/a/@href'):
		fullUrl="http://www.pracuj.pl/"+href.extract()
                yield scrapy.Request(fullUrl, callback=self.parse_jobs)	
	    	

	def parse_jobs(self, response):
            maybeJobTitle = response.selector.xpath('//*[@id="jobTitle"]').re(re.compile(ur'>[\w\s.,]+<', re.UNICODE))
            jobTitle = u''if len(maybeJobTitle)!=1 else maybeJobTitle[0].strip('<>')
            print jobTitle
            maybeJobLoc1 = response.selector.xpath('//*[@id="info"]').re(re.compile(ur': [\w\s.,]+', re.UNICODE))
            maybeJobLoc2 = response.selector.xpath("//span[@itemprop='addressRegion']").re(re.compile(ur'>[\w\s.,]+<', re.UNICODE))
	    jobLoc1 = u'' if len(maybeJobLoc1)!=1 else maybeJobLoc1[0].strip(': ')
            jobLoc2 = u'' if len(maybeJobLoc2)!=1 else maybeJobLoc2[0].strip('<>') 
            maybeJobDesc1 = response.selector.xpath('//*[@id="description"]//text()').extract()
	    maybeJobDesc2 = response.xpath("//div[@id='sOW1']//*").extract() if len(maybeJobDesc1)==0 else u''
            item = PracujItem()
            item['jobTitle'] = jobTitle
            item['jobDesc'] = maybeJobDesc1 if len(maybeJobDesc1)>0 else maybeJobDesc2
            item['jobLocation'] = jobLoc1 if (len(jobLoc1)>0 and not re.compile(ur'[0-9]+').match(jobLoc1))  else jobLoc2
            item['jobLink'] = response.url
            yield item


	def striphtml(data):
    	    p = re.compile(ur'<.*?>')
    	    return [p.sub('', d) for d in data] 		              
