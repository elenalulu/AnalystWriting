
# FigureChat
人人可用的数据查询大模型，只需要CPU即可使用。

<br>

<div>
	<p align="center">
  <img alt="Animation Demo" src="https://github.com/elenalulu/FigureChat/blob/main/docs/logo.png" width="660" />
  </p>
</div>

-----------------

## 用途

- 用量化模型实现在CPU上进行数据查询。
- 使用关键词查询来搜索所有研究报告。
- 可以添加个人pdf文档来定制化数据查询。


<div>
	<p align="center">
  <img alt="Animation Demo" src="https://github.com/elenalulu/FigureChat/blob/main/docs/ui.png" width="660" />
  </p>
</div>

<br>

## 安装

1.下载gguf量化模型，放到主文件夹下: 

https://modelscope.cn/models/QuantFactory/Qwen2.5-7B-Instruct-GGUF/resolve/master/Qwen2.5-7B-Instruct.Q4_K_M.gguf

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


## 个人文档使用
1.向personal_pdf文件夹放入个人pdf。 <br>
2.把文件名写完整，例如：邮储银行_深度报告：聚焦稳健发展_经营韧性不断增强.pdf。 <br>
3.在ui界面，点击个人文档页，即可进行本地文档查询。 <br>



## Contact

<img src="docs/wechat.jpg" width="200" />


## License

The product is licensed under The Apache License 2.0, which allows for free commercial use. Please include the link to FigureChat and the licensing terms in your product description.


## Contribute

The project code is still quite raw. If anyone makes improvements to the code, we welcome contributions back to this project.