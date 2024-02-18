# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 10:08:00 2023

@author: Alvaro
"""
import math
import numpy as np
import matplotlib.pyplot as plt
# %matplotlib inline
import requests
from matplotlib.animation import FuncAnimation
import re
# from requests_html import HTMLSession
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# response = requests.get(district22)
# html_content = response.text
# response21 = requests.get(district21)
# html_content21 = response21.text


district22 = 'https://tx.milesplit.com/meets/501276-uil-6a-district-24-2022/results/851669'
district21 = 'https://tx.milesplit.com/meets/447797-uil-6a-district-24-2021/results/774565/raw'
regex = r'([^0-9][0-8]\s*(\s*|Houston)\s*Clear Lake\s*[0-9]*)'



def getdata(url):
    response = requests.get(url)
    code = response.text
    return code

def getSoup(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup

def getPlacement_JS(url):
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options )
    driver.get(url)
    driver.implicitly_wait(1)
    rendered_html = driver.page_source
    driver.quit()

    actual_row=''
    soup = BeautifulSoup(rendered_html, 'lxml')
    table_rows = soup.find_all('tr')
    for row in table_rows:
        cells = row.find_all('td')
        
        for cell in cells: 
            if("Clear Lake High School" in cell.get_text() and "</a" not in str(cell)):
                #print("--Break--")
                actual_row = row
    #print(actual_row)        
    reg = r'([1-9])'        
    placement= 0
    cells = actual_row.find_all('td')
    #print(cells)
    for cell in cells:
        #print(re.findall(reg, str(cell)))
        if(re.findall(reg, str(cell))!=0):
            lists = re.findall(reg, str(cell)) 
            placement  = lists[0] if lists else None
            #print(lists)
            break
            
    return placement


soup = getSoup(district22)
links = soup.find_all('a')
lists =[]

for link in links:
    if 'href' in link.attrs:
        href = link['href']
        # print(href.find("https")!=-1)
        # print("https://tx.milesplit.com/meets/" in href)
        #print(href)
        if(href.find("https")!=-1 and 'https://tx.milesplit.com/meets/' in href):
            lists.append(href)
    
    
title = ""
filtered = []
for i in range (len(lists)):
    title = getSoup(lists[i]).title.string
    # print(title)
    if "compare" not in title.lower():
        filtered.append(lists[i])
        
def getInfo(year):
    districtYearLink =""
    yearString = "uil-6a-district-24-" + str(year)
    #print(yearString)
    for i in range (len(filtered)):
        if year!=2022 and yearString in filtered[i]:
            districtYearLink= filtered[i]
            
    if("results" not in districtYearLink):       
            districtYearLink+= "/results"
    district_requests = getdata(districtYearLink)
    #print(len(re.findall(r'"Completed" Results', district_requests))>0)
    districtSoup = getSoup(districtYearLink)
    all_links= districtSoup.find_all('a')
    print(len(re.findall(r'SCORERS', district_requests))>0)
    if(len(re.findall(r'Varsity Boys', district_requests))>0):
        for x in all_links:
            if('Varsity Boys' in x.text):
                districtYearLink = x['href'] 
    
    if(len(re.findall(r'"Completed" Results', district_requests))>0 and (year>2020)):
       for j in all_links:
           if('"Completed" Results' in j.text):
               districtYearLink = j['href']
               #print(j['href'])
       
    print(districtYearLink)
    district_requests = getdata(districtYearLink)
    instances = re.findall(regex, district_requests)
    
    if('raw' not in districtYearLink):
        instances = getPlacement_JS(districtYearLink)
    
    return instances
            
for i in range(2014,2022):
    if(i != 2017):
        print("Year: " + str(i))
        print(getInfo(i))
          
    



 