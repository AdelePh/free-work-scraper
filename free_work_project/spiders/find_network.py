# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 12:26:56 2022

@author: minhp
"""


#import time
#from selenium.webdriver.common.action_chains import ActionChains
#
##☺driver = webdriver.PhantomJS(r"C:\Users\minhp\laveille_ia-main\phantomjs-2.1.1-windows\bin\phantomjs.exe")
#

#
#driver.find_element_by_xpath('//div[@class="flex items-center gap-2 lg:ml-auto"]')
#element = driver.find_element_by_xpath('//button/*[name()="svg"]').click()
#ActionChains(driver).move_to_element(element).click().perform()
##[@class="pointer-events-none icon-custom fill-current flex-none inline-flex"]/*[name()="path"]
##time.sleep(15)
#
##driver.find_element_by_xpath('//*[@id="email-or-phone"]')
#
#print(driver.current_url)                                 
                                    

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
import pandas as pd

from selenium.webdriver.chrome.options import Options


all_urls =  list(pd.read_csv('result_v1.csv')['links'])
chrome_options = Options()



linkedin = []
twitter = []
facebook = []
others = []
result_df = pd.DataFrame(columns = ['Linkedin', 'Twitter', 'Facebook','Others'])
#try: 
for url in all_urls: 
    
    print(url)
    
    
    driver = webdriver.Chrome(r"C:\Users\minhp\Per_projects\leboncoin\chromedriver.exe")

    driver.get(url)
    
    xpath = '//div[@class="flex items-center gap-2 lg:ml-auto"]/button/*[name()="svg"]'
    
    elements = driver.find_elements(By.XPATH, xpath)
    count = 1
    link_linkedin = ""
    link_twitter = ""
    link_facebook = ""
    link_others = ""
    
    for element in elements: 
        ActionChains(driver).move_to_element(element).click().perform()
        driver.switch_to.window(driver.window_handles[count])
        
        if 'linkedin' in driver.current_url:
            link_linkedin = driver.current_url
            linkedin.append(link_linkedin)

        elif 'twitter' in driver.current_url:
            link_twitter = driver.current_url
            twitter.append(link_twitter)

        elif 'facebook' in driver.current_url:
            link_facebook = driver.current_url
            facebook.append(link_facebook)
        else: 
            
            link_others = link_others + ', ' + driver.current_url
            others.append(driver.current_url)
            
        count = count + 1
        driver.switch_to.window(driver.window_handles[0])
        
    result_df = result_df.append({'Url':url,'Linkedin': link_linkedin, 'Twitter': link_twitter, 'Facebook': link_facebook, 'Others': link_others},  ignore_index = True)
    
    driver.quit()
    
    result_df.to_excel('network_social.xlsx')
#except:
#    url =""
#    link_linkedin = ""
#    link_twitter = ""
#    link_facebook = ""
#    link_others = ""
#    result_df = result_df.append({'Url':url,'Linkedin': link_linkedin, 'Twitter': link_twitter, 'Facebook': link_facebook, 'Others': link_others},  ignore_index = True)
#    pass
