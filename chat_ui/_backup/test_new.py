
# coding: utf-8
from flask import Flask, render_template, request
import os, time, re, datetime
import openai
import pdfplumber
from bs4 import BeautifulSoup
import requests
import pandas as pd


client = openai.OpenAI(
    base_url="http://localhost:8080/v1", # "http://<Your api-server IP>:port"
    api_key = "no-key-required"
)


    
query = '博汇纸业营业收入是多少'
final_answer = ''
pdf_single = ''
    

content =  query + '。上面这个问题中所指的公司或者行业是哪个，输入格式如下：@公司@'
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

company_raw = answer.split('@')
company = company_raw[1]
print (company)


#查表确定filename
filename_csv = '../company_filename.csv'
df = pd.read_csv(filename_csv)

results = df[df['company'] == company]
if 'Empty DataFrame' not in str(results):
    for i in range(0, len(results)):
        oneline = results[i:(i+1)]
        filename = oneline['filename'].values 
        filename = ''.join(filename)
        print (filename)

        html_path = 'https://s10.z100.vip:32963/yanbao_html/' + filename + '.html'
        response = requests.get(html_path)
        response.encoding = 'utf-8'
        total_content = response.text
        

        def remove_html_tags(text):
            soup = BeautifulSoup(text, "html.parser")
            stripped_text = soup.get_text()
            return stripped_text

        article = remove_html_tags(total_content)
        article_split = article.split('数据来源')

        for duanluo in article_split:
            content =  duanluo + '。上文是否回答了：' + query + '。如果回答了，直接输出答案；如果没回答则输出否'
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
            
            if '否' not in answer:
                output = answer
                pdf_single = 'https://s10.z100.vip:32963/yanbao_pdf/' + filename + '.pdf'
                print (pdf_single)