# coding: utf-8
import pdfplumber
import glob
import os
import pandas as pd


root_dir = './personal_pdf/'
pattern = f'{root_dir}/*.pdf'
pdf_list = glob.glob(pattern)


#打印已有path
local_csv = './local_article.csv'
df = pd.read_csv(local_csv)
df_path = df['path']

total_path_list = []
for path in df_path:
	total_path_list.append(path)



#提取article
for pdf_path in pdf_list:
	
	if pdf_path not in total_path_list:
		print (pdf_path)

		with pdfplumber.open(pdf_path) as pdf:

			for page in pdf.pages:
				page_number = page.page_number
				wholepage = page.extract_text()
				wholepage = ''.join(wholepage.split())
				wholepage = wholepage.replace(',','，')

			
				if not os.path.exists(local_csv):
					with open(local_csv, 'w') as file:
						head = 'path,page,article,tag' + '\n\n'
						file.write(head)

				#写入csv
				tag = 'local'
				single = '"' + pdf_path + '","' + str(page_number) + '","' + wholepage + '","' + tag + '"' + '\n\n'
				with open (local_csv,'a+',encoding='utf-8')as fl:
					fl.write(single)



#import remote es
import csv
import sys
import os
import logging
import datetime 
from elasticsearch import Elasticsearch
from elasticsearch import helpers
import json

logging.basicConfig()
es = Elasticsearch(hosts=["your own path"])

def importCSV(indexName,typeName,fileName):
    if not os.path.exists(fileName):
        print ("file not found")
        return
    actions=[]
    if not es.indices.exists(index=indexName,allow_no_indices=True):
        #print "not found index"
        es.indices.create(index=indexName,body={},ignore=400)
    for item in csv.DictReader(open(fileName, "r", encoding="utf-8")):  
        actions.append({"_index":indexName,"_type":typeName,"_source":item})
    res = helpers.bulk(es,actions,chunk_size=100)
    es.indices.flush(index=[indexName])
    return len(actions)

def encoding(item):
    for i in item:
        item[i]=str(item[i]).encode('utf-8')
    return item    

if __name__=="__main__":

    json_name = 'local_article'
    es.indices.delete(index=json_name, ignore=[400, 404])  #delete index all!!

    body = {
            "mappings": {
                "info": {
                    "properties": {
                        "tag": {
                            "type": "text"
                        }
                  }
                }
              }
            }
    es.indices.create(index=json_name, body=body)

    csv_file = './' + json_name + '.csv'
    result=importCSV(json_name, "info", csv_file) 
    print (csv_file, 'import finished!')