import scrapy
import requests
import os
import re
import logging

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
        unwanted = None
        #Record URL as a str
        url = response.url
        #Create tree of all elements within the html page
        soup = BeautifulSoup(response.text, 'html.parser')
        
        #Helper function to pull out the social media wrapper from articles
        def tag_filter(article):
            unwanted = article.find('div', {'class': re.compile('^article-bodystyles__Social')})
            return unwanted

        try:
            #Finds the headline, subheadline, and articlebody <div> tags
            article = soup.find('article')
            article_headline = article.find('div', {'class': re.compile(r'at-headline')})
            article_subheadline = article.find('div', {'class': re.compile(r'at-subheadline')})
            article_body_tag = article.find('div', {'data-module-name': re.compile(r'article-body')})
            
            #takes elements caught by the filter and remove them from the soup tree
            unwanted = tag_filter(article)
            if unwanted != None:
                unwanted.decompose()

            #Retrieves the text elements from the earlier specified <div> tags  
            article_body = article_body_tag.text if article_body_tag else None
            article_title = article_headline.text if article_headline else None
            article_subtitle = article_subheadline.text if article_subheadline else None

            
        #Catches the error if there is no <div> with class = 'article-body'
        except AttributeError:
            return "No article found"
            
        #Put all specified data from the page into a list   
        combined_data = {
            'url': url,
            'article title': article_title,
            'article subtitle': article_subtitle,
            'article body': article_body,
            }
        
        #return list
        yield combined_data

    #endregion
    
