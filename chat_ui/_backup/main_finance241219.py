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



def data_qa(query):

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
                    break

    return output, pdf_single 



def internet_result(query):
    output = ''

    #baidu搜索
    url = 'https://www.baidu.com/s'
    param = {
        'wd':query #搜索词
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
    for result in results:
        #6天前这种剔除了，可以考虑加进来
        if count<10 and '股票行情' not in str(result) and '<div class="c-container"' in str(result) and '<div class="result c-container' not in str(result):
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

            if '"newTimeFactorStr":""' in str(result) or '天前' in str(result):
                timestamp = 0 
            else:
                date = re.findall(r'"newTimeFactorStr":"(.+?)日', str(result))
                date = ''.join(date)
                date = '头' + date + '日'

                year = re.findall(r'头(.+?)年', str(date))
                year = ''.join(year)
                year = int(year)
                month = re.findall(r'年(.+?)月', str(date))
                month = ''.join(month)
                month = int(month)
                day = re.findall(r'月(.+?)日', str(date))
                day = ''.join(day)
                day = int(day)
                date_change = datetime.datetime(year, month, day)
                timestamp = date_change.timestamp()
            

            count += 1
            single_tuple = (timestamp, title, content, url)
            baidu_list.append(single_tuple)

    #按日期排序
    baidu_list.sort(key=lambda x:x[0], reverse=True)

    count_baidu = 0
    for item in baidu_list:
        if count_baidu < 3:
            title = item[1]
            content = item[2]
            url = item[3]
            output = output + '<strong>' + title + '</strong>' + '<br><br>' 
            output = output + content + '<br><br>'
            output = output + '<a href="' + url + '" target="_blank">点此链接查看详情<a><br><br><br>'
            count_baidu += 1

    return output



app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/qa")
def get_doc_response():
    query = request.args.get('msg')

    # #数据查询
    # if '多少' in query or '量' in query or '数据' in query or '数字' in query or '营收' in query or '收入' in query or '利润' in query: 
    #     output, pdf_single = data_qa(query)
    # #文字理解
    # else:
    #     output, pdf_single = language_qa(query)

    output, pdf_single = data_qa(query)

    #互联网查询
    internet = ''
    if pdf_single == 'none':
        internet = internet_result(query)

    return [output, pdf_single, internet]


        

if __name__ == "__main__":
    
    #show browser 
    os.system('"C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe" http://127.0.0.1:5501')

    #run 
    app.run(host="0.0.0.0", port=5501)