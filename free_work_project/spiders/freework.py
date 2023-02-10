import scrapy
import time
import pandas as pd
import re
from bs4 import BeautifulSoup
#from bs4 import BeautifulSoup
#from urllib.request import urlopen
#import re
#list_links =[]
#for i in range(1,67):
#    url = 'https://www.free-work.com/fr/companies?page='+str(i)
#    html = urlopen(url)
#    bs = BeautifulSoup(html,'html.parser')
#    links = bs.find_all('a', href = re.compile('^(/fr/companies/)'))
#    for link in links:
#        list_links.append('https://www.free-work.com'+link.attrs['href'])
#        
#df = pd.DataFrame({'links':list_links})
#df.to_excel('links.xlsx')
#        

class FreeworkSpider(scrapy.Spider):
    name = 'freework'
    allowed_domains = ['free-work.com']
    start_urls = list(pd.read_excel('links.xlsx')['links'])

#    def parse(self, response):
#        num_page = response.css('#content > div > div > div > div > div:nth-child(3) > button:nth-child(12)').attrib['data-page'].strip()
#        num_page = int(num_page)
#        for page_number in range(num_page-1):
#            next_page_url = 'https://www.free-work.com/fr/companies?page=' + str(page_number)
#            yield scrapy.Request(next_page_url, callback=self.parse_page)
#            
#        
#    def parse_page(self, response):
#        search_results = response.css('#content > div > div > div > div > div.space-y-4')
#        for link in search_results.xpath('//a[contains(@href,"/fr/companies/")]/@href').extract():
#            absolute_link = 'https://www.free-work.com' + link
#            time.sleep(1)
#            yield {'link': absolute_link}
#            yield scrapy.Request(absolute_link, callback= self.get_info_each_company)
        
    def parse(self,response):
        #name = response.xpath('//*[@id="content"]/div/div/div/div/div[1]/header/div/div/div/div[1]/div/div/h1/text()').extract()
        link = response.request.url
        name = response.xpath('//div[@class="text-2xl font-bold"]/h1/text()').extract()
        #year_founded = response.xpath('//*[@id="content"]/div/div/div/div/div[1]/div[1]/div[1]/div/span[2]/span/text()').extract()  
        year_founded = response.xpath('//*[@id="content"]/div/div/div/div/div[1]/div[1]/div[1]/div/span[2]/span/text()').extract()
        chifre = response.xpath('//*[@id="content"]/div/div/div/div/div[1]/div[1]/div[2]/div/span[2]/span/text()').extract()
        collaborateur =  response.xpath('//*[@id="content"]/div/div/div/div/div[1]/div[1]/div[3]/div/span[2]/span/text()').extract()
        siege = response.xpath('//*[@id="content"]/div/div/div/div/div[1]/div[1]/div[4]/div/span[2]/span/text()').extract()
        activity = response.xpath('//*[@id="content"]/div/div/div/div/div[1]/div[1]/a/div/span[2]/span/text()').extract()
        #presentation = response.xpath('//*[@id="content"]/div/div/div/div/div[1]/div[2]/div[2]/text()').extract()
        site_web = ''
        presentation_search = response.xpath('//div[@class="space-y-8 p-4 shadow bg-white rounded-lg"]').extract()
        if len(presentation_search) != 0: 
            try: 
                soup = BeautifulSoup(presentation_search[0],'html.parser')
            except:
                soup = '' 
            if soup != '':
                original_text = soup.text
                head_paragraph = soup.find('div',class_='lg:flex justify-between').text
                tail_paragraph = soup.find('div',class_='inline-flex items-center')
                
                site_web = tail_paragraph.find_all('a',href='True')
                if len(site_web) != 0:
                    site_web = site_web[0]
                else: 
                    site_web = response.xpath('//*[@id="content"]/div/div/div/div/div[1]/div[2]/div[3]/div/a/@href').extract()
    
                tail_paragraph = tail_paragraph.text
                text = original_text.replace(head_paragraph,'')
                text = text.replace(tail_paragraph,'')
                try: 
                    skill_header = soup.find('div',class_='font-semibold text-xl mb-4').text
                    skills_text = soup.find('div',class_='flex flex-wrap gap-1').text
                    text = text.replace(skill_header,'')
                    text = text.replace(skills_text,'') 
                    text = re.sub(' +',' ',text)
                except:
                    text = re.sub(' +',' ',text)
        else:
            text = ""
 
        tag_contain_skills = response.xpath('//div[@class="flex flex-wrap gap-1"]')
        skills = []
        if len(tag_contain_skills)!=0:
            tag = tag_contain_skills[0]
            all_skills = tag.xpath('.//div[@class="truncate"]/text()').extract()
            if len(all_skills) != 0:
                for skill in all_skills:
                    skill = skill.strip()
                    skills.append(re.sub(' +',' ',skill))
        
     
        try: 
            if len(name) != 0:
                name = name[0].strip()
                name = re.sub(' +',' ',name)
            
            if len(year_founded) != 0:
                year_founded = year_founded[0].encode('utf8').strip()
                year_founded = re.sub(' +',' ',year_founded) 
            
            if len(chifre) != 0:
                chifre = chifre[0].encode('utf8').strip()
                chifre = re.sub(' +',' ',chifre)
            
            if len(collaborateur) != 0:
                collaborateur = collaborateur[0].encode('utf8').strip()
                collaborateur = re.sub(' +',' ',collaborateur)
            
            if len(siege) != 0:
                siege = siege[0].encode('utf8').strip()
                siege = re.sub(' +',' ',siege)
            
            if len(activity) != 0:
                activity = activity[0].encode('utf8').strip()
                activity = re.sub(' +',' ',activity)
                
#            if len(text) != 0:
#                text = text[0].encode('utf8').strip()
#                text = re.sub(' +',' ',text)
        except:
            pass

#        except:    
#            print("error",name)
#            print("eror",year_founded)
        dictionary  =  {'links':link,'name':name,'Anné de crétion': year_founded,'Chiffre affaires':chifre,'Collaborateurs':collaborateur,'Siege':siege,'Activité':activity,'Presentation':text,'Website':site_web,'Skills':skills}
        
        yield dictionary


            
                     