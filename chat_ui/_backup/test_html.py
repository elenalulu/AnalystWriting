# coding: utf-8
from flask import Flask, render_template, request
import os, time, re, datetime, shutil
import openai
import pdfplumber
from bs4 import BeautifulSoup
import requests
import pandas as pd
from collections import Counter
import fitz 


client = openai.OpenAI(
	base_url="http://localhost:8080/v1", 
	api_key = "no-key-required"
)


query = '中科环保营业收入'


http_pdf = ''
company = ''
    
#which paper
content =  query + '根据上面文字输出问题词语，格式如下:公司&指标&其他'
completion = client.chat.completions.create(
model="",
messages=[
    {"role": "user", "content": content}
]
)
output = completion.choices[0].message
answer = re.findall(r"content='(.+?)'", str(output))
answer = '' .join(answer)
answer = str(answer)
answer = answer.lower()
print (answer)


keyword_csv = '../company_url.csv'
df = pd.read_csv(keyword_csv)

query_keyword_list = answer.split('&')
url_keyword_total = []
for query_keyword in query_keyword_list:

    results = df[df['company'] == query_keyword]
    if 'Empty DataFrame' not in str(results):
        for i in range(0, len(results)):
            oneline = results[i:(i+1)]
            company = oneline['company'].values 
            company = ''.join(company)
            url = oneline['url'].values 
            url = ''.join(url)
            # url = url.split('_')[1]

            url_keyword_dict = {'url': url, 'company': query_keyword}
            url_keyword_total.append(url_keyword_dict)
            

counts = Counter([item['url'] for item in url_keyword_total])

most_url = counts.most_common(1)
most_url = most_url[0]
most_url = str(most_url).split("',")
most_url = most_url[0]
most_url = most_url.replace("('",'')


http_pdf = 'https://pdf.dfcfw.com/pdf/H3_' + most_url + '_1.pdf'
print (http_pdf) 

dialoge = '请稍等，已找到原文→'


final_answer = ''
if company != '':
	now_company = company
response = requests.get(http_pdf)


page_contents = []
if response.status_code == 200:
    pdf_data = response.content
    pdf_document = fitz.open("pdf", pdf_data)
    
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text = page.get_text()  
        page_contents.append(text)


useful_articles = ''
for query_keyword in query_keyword_list:
	if query_keyword != now_company:
	    for article in page_contents:
	        if query_keyword in article and article not in useful_articles:
	            if len(useful_articles) < 1000: #control length
	                useful_articles += article


content = useful_articles + '。根据上文回答：' + query
print (content)
completion = client.chat.completions.create(
model="",
messages=[
    {"role": "user", "content": content}
]
)
output = completion.choices[0].message
answer = re.findall(r"content='(.+?)'", str(output))
answer = '' .join(answer)
answer = str(answer)
print (answer)

# if '否' not in answer:
#     final_answer =  answer.replace('\\n','<br>')

