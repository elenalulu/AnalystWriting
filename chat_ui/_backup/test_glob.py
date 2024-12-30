

import glob
 
# 定义模糊匹配的模式
pattern = "*.txt"  # 匹配当前目录下所有扩展名为.txt的文件
 
# 获取匹配的文件列表
matched_files = glob.glob(pattern)
 
# 打印匹配到的文件
for filename in matched_files:
    print(filename)