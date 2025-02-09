
# FigureChat
人人可用的数据查询大模型，只需要CPU即可使用。

<br>

<div>
	<p align="center">
  <img alt="Animation Demo" src="https://github.com/elenalulu/FigureChat/blob/main/docs/logo.png" width="660" />
  </p>
</div>

-----------------
## 本项目测试链接

https://s3.v100.vip:5502/


## Agent功能

- RAG部分：用elasticsearch做搜索为推理模型提供相关知识。
- LRM部分：用deepthink-7b的int4实现在CPU上的推理问答。
- 本地知识：可以添加个人pdf文档为推理模型提供本地知识。


<div>
	<p align="center">
  <img alt="Animation Demo" src="https://github.com/elenalulu/FigureChat/blob/main/docs/ui.png" width="660" />
  </p>
</div>

<br>

## 安装

1.下载gguf量化模型，放到主文件夹下: 

https://modelscope.cn/models/prithivMLmods/Deepthink-Reasoning-7B-GGUF/resolve/master/Deepthink-Reasoning-7B.Q4_K_M.gguf
也可以替换成deepseek相关模型，需要修改llamacpp设置。

<br>

2.解压llama_cpp.rar压缩包，放到主文件夹下；并启动量化模型:

```shell
cd llama_cpp

llama-server.exe -m ../Qwen2.5-7B-Instruct.Q4_K_M.gguf -c 2048
```
<br>

3.打开另一个终端，启动ui界面:

```shell
cd chat_ui

python main_finance.py
```

<br>

4.如有需要可以部署本地elasticsearch，也可以问作者索要远程es链接

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