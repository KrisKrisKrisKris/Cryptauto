import scrapy
import requests
import os
import re

from bs4 import BeautifulSoup
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from openai import OpenAI
from dotenv import load_dotenv
from scrapy import signals


class CoindeskSpider(CrawlSpider):
    #start region, declare spider name and allowed domains, as well as scripts to follow
    name = "coindesk"
    allowed_domains = ["coindesk.com"]
    start_urls = ["https://coindesk.com"]
    rules = (
        Rule(LinkExtractor(), callback = 'parse'),
    )
    #endregion

    #Start region
    #Actions to be performed on every crawled page
    def parse(self, response):
        #Record URL as a str
        url = response.url
        #Create tree of all elements within the html page
        soup = BeautifulSoup(response.text, 'html.parser')
        
        #Helper function to pull out the social media wrapper from articles
        def tag_filter(tag):
            return tag.name == 'div' and re.compile('^article-bodystyles__Social') in tag.get('class', [])

        try:
            #Finds the first <div> tag with class = 'article-body'
            article_body_tag = soup.find('div', {'data-module-name': re.compile(r'article-body')})

            #Should take elements caught by the filter and remove them from the soup tree
            #Does not prevent their text data from being added to the output and i dont know why
            unwanted = None
            unwanted_elements = article_body_tag.find_all(tag_filter)
            for unwanted_element in unwanted_elements:
                unwanted = unwanted_element.text
                unwanted_element.decompose()

            #Retrieves the text elements from the earlier specified <div> tag   
            article_body = article_body_tag.text if article_body_tag else None

        #Catches the error if there is no <div> with class = 'article-body'
        except AttributeError:
            article_body = "No article found"
            
        #Put all specified data from the page into a list   
        combined_data = {
            'url': url,
            'unwanted': unwanted,
            'data_from_beautifulsoup': article_body,
            }
        #return list
        yield combined_data

    #endregion
    
