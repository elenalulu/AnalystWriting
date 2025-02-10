
# FigureChat
人人可用的数据查询大模型，只需要CPU即可使用。 ⭐本项目测试链接：https://s3.v100.vip:5502/
<br>
👀运行本代码需要部署elasticsearch，运行前请先在/chat_ui/main_finance.py中填入es路径
<div>
	<p align="center">
  <img alt="Animation Demo" src="https://github.com/elenalulu/FigureChat/blob/main/docs/logo.png" width="660" />
  </p>
</div>

-----------------


## Agent功能

- RAG部分：用elasticsearch做搜索为推理模型提供相关知识。
- LRM部分：用deepseek-r1的7b量化模型实现CPU级推理问答。
- 本地知识：可以添加个人pdf文档为推理模型提供本地知识。
<br>

<div>
	<p align="center">
  <img alt="Animation Demo" src="https://github.com/elenalulu/FigureChat/blob/main/docs/ui.png" width="660" />
  </p>
</div>

<br>

## 安装

1.安装ollama：https://github.com/ollama/ollama 
<br>

2.安装完成后拉取deepseek-r1模型：
```shell
ollama run deepseek-r1
```
<br>

3.安装python中的ollama：
```shell
pip install ollama
```
<br>

4.启动ui界面:

```shell
cd chat_ui

python main_finance.py
```
<br>

5.如有需要可以部署本地elasticsearch，也可以问作者远程es链接

先做本地文档处理：
```shell
python deal_local_document.py
```

并且在main_finance.py内填入合适的es路径
```shell
es = Elasticsearch(
    hosts=["your own path"]
)
```
<br>

## 个人文档使用
1.向personal_pdf文件夹放入个人pdf。 <br>
2.在ui界面，"点此添加本地文档"，即可进行本地文档查询。 <br>



## Contact

<img src="docs/wechat.jpg" width="200" />


## License

The product is licensed under The Apache License 2.0, which allows for free commercial use. Please include the link to FigureChat and the licensing terms in your product description.


## Contribute

The project code is still quite raw. If anyone makes improvements to the code, we welcome contributions back to this project.