# coding: utf-8
from flask import Flask, render_template, request
import os, time, re, shutil
# import openai
from bs4 import BeautifulSoup
import requests
import pandas as pd
from collections import Counter
from elasticsearch import Elasticsearch
import ollama


# 连接到远程 Elasticsearch
es = Elasticsearch(
    hosts=["your path"]
)


# client = openai.OpenAI(
#     base_url="http://localhost:8080/v1", 
#     api_key = "no-key-required"
# )



app = Flask(__name__)


output = ''
article = ''
text = '<原文>'


def pdf_url(query): 
    global output
    global text
    first_pdf = 'none'

    #查询knowledge.csv的category是ashare
    company = 'none'

    csv_path = '../finance_knowledge.csv'
    df = pd.read_csv(csv_path)

    category = 'ashare'
    results = df[df['category'] == category]

    company_list = []
    if 'Empty DataFrame' not in str(results):
        for i in range(0, len(results)):
            oneline = results[i:(i+1)]
            knowledge = oneline['knowledge'].values
            knowledge = ''.join(knowledge)
            
            if knowledge in query:
                company = knowledge
                break


    #先精准查询company，再模糊查询query    
    result = es.search(
        index="company_abstract",
        body={
          "query": {
            "bool": {
              "must": [
                {
                  "term": {
                    "company.keyword": company
                  }
                }
              ],
              "should": [
                {
                  "match": {
                    "abstract": {
                      "query": query,
                      "fuzziness": "AUTO"
                    }
                  }
                }
              ],
              "minimum_should_match": 0
            }
          }
        }
    )

    if result['hits']['hits'] != []:
        output = result['hits']['hits'][0]["_source"]["abstract"]
        output = ''.join(output.split())

        dialoge = ''
        for i in range(0, min(1,len(result['hits']['hits']))): #控制显示原文数量
            biaoshi_i = result['hits']['hits'][i]["_source"]["biaoshi"]
            title_i = result['hits']['hits'][i]["_source"]["title"]
            pdf_i = 'https://data.eastmoney.com/report/info/' + biaoshi_i + '.html'
            dialoge += '<br>' + title_i + '：<a href="{}" target="_blank">{}</a>'.format(pdf_i, '点此链接查看原文')
        dialoge = '我查到相关研报->' + dialoge
        text_list = output.split('。')
        
        for i in range(0, min(4,len(text_list))):
            text += text_list[i] + '。'
      
    else:
        response = ollama.chat(model='deepseek-r1', messages=[
          {
            'role': 'user',
            'content': query,
          },
        ])

        answer = response['message']['content']
        answer = answer.split('</think>')
        dialoge = answer[1]
        output = 'none'


    return dialoge, output, text


def language_qa(query, output): 

    content = '根据以下内容，用写一段关于' + query + '的研究，以数据分析为主，不要出现根据谁的报告这种。内容如下：' + output
    print (content)

    response = ollama.chat(model='deepseek-r1', messages=[
      {
        'role': 'user',
        'content': content,
      },
    ])

    answer = response['message']['content']
    answer = answer.split('</think>')
    answer = answer[1]

    if answer != '':
        final_answer = answer.replace('\n','<br>')
        final_answer = 'AnalystWriting:' + final_answer

    return final_answer



def local_url(query):
    global article
    global text
    local_pdf = ''

    #查询es
    result = es.search(
    index="local_article",
    body={
        "query": {
            "match": {
                "article":  {
                        "query": query,
                      }
                }
            }
        }
    )

    if result['hits']['hits'] != []:
        article = result['hits']['hits'][0]["_source"]["article"]
        path = result['hits']['hits'][0]["_source"]["path"]
        page = result['hits']['hits'][0]["_source"]["page"]
        title = path.replace('./personal_pdf\\','').replace('.pdf','')

        dialoge = '我找到本地文档-> ' + '请参考第' + page + '页' + '<br>' + title 

    else:
        completion = client.chat.completions.create(
        model="",
        messages=[
            {"role": "user", "content": query}
        ]
        )
        output = completion.choices[0].message
        answer = output.content
        dialoge = str(answer)
        article = 'none'


    return dialoge, article, text


def local_qa(query, article):

    #用远程es查询结果做deepthink
    content = '根据以下内容，用写一段关于' + query + '的研究，回答得简洁。内容如下：' + article
    print (content)

    response = ollama.chat(model='deepseek-r1', messages=[
      {
        'role': 'user',
        'content': content,
      },
    ])

    answer = response['message']['content']
    answer = answer.split('</think>')
    answer = answer[1]

    if answer != '':
        final_answer =  answer.replace('\n','<br>')
    else:
        final_answer = '请等待我能力升级~'

    return final_answer



def internet_result(query):
    output = ''

    #baidu search
    url = 'https://www.baidu.com/s'
    param = {
        'wd':query 
    }
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
    }
    res = requests.get(url = url, params = param, headers = headers)
    res.encoding = 'utf-8'
    # print (res.text)

    beautisoup = BeautifulSoup(res.text,"lxml")
    results = beautisoup.find_all('div',class_="c-container")

    count = 0
    output = ''
    baidu_list = []
    title_list = []

    for result in results:

        if count<10:
            result = str(result).replace('\n','')
            description = re.findall(r'data-tools=(.+?)id=', result)
            description = ''.join(description)
            title = re.findall(r'title(.+?)url', str(description))
            title = ''.join(title)
            title = re.sub("<[^>]*?>","", title)
            title = title.replace(' ','').replace('":"','').replace('","','').replace("': &quot;","&quot;,'").replace("':&quot;","").replace("&quot;,'","")
            
            content = re.findall(r'"contentText":"(.+?)"', result)
            content = ''.join(content)
            content = re.sub("<[^>]*?>","", content)

            if '"url":"http' in str(description):
                url = re.findall(r'"url":"(.+?)"', str(description))
                url = ''.join(url)
            else:
                url = re.findall(r"url':(.+?)}", str(description))
                url = ''.join(url)
            url = url.replace(' ','').replace("&quot;","").replace(";","")

            if title != '' and title not in title_list:
                count += 1
                single_tuple = (title, content, url)
                baidu_list.append(single_tuple)
                title_list.append(title)

    count_baidu = 0
    for item in baidu_list:
        if count_baidu < 3:
            title = item[0]
            content = item[1]
            url = item[2]
            output = output + '<strong>' + title + '</strong>' + '<br><br>' 
            output = output + content + '<br><br>'
            output = output + '<a href="' + url + '" target="_blank">点此链接查看详情<a><br><br><br>'
            count_baidu += 1

    return output




@app.route("/")
def home():
    return render_template("index.html")


@app.route("/url")
def get_pdf_url():
    query = request.args.get('msg')

    #network chat
    if '&&&' not in query:
        dialoge, output, text = pdf_url(query)

    #personal chat
    else: 
        query = query.replace('&&&','')
        dialoge, output, text = local_url(query)

    return [dialoge]


@app.route("/text")
def get_pdf_text():
    time.sleep(2)

    return [text]


@app.route("/qa")
def get_doc_response():
    time.sleep(10)
    query = request.args.get('msg')

    web_reply = 'none'
    #network chat
    if '&&&' not in query:
        if output != 'none':
            web_reply = language_qa(query, output) 

    #personal chat        
    else:
        if article != 'none':
            query = query.replace('&&&','')
            web_reply = local_qa(query, article)

    return [web_reply]



        

if __name__ == "__main__":
    
    #show browser 
    os.system('"C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe" http://127.0.0.1:5501')

    #run 
    app.run(host="0.0.0.0", port=5501)