

## 简介

> 使用scrapy+ajax方式爬取知乎新冠肺炎话题中精华部分的所有问题的所有答案

一共有三个爬虫

- zhihu  爬取问题id及问题标题
- answer 爬取问题下的答案内容及发布时间
- update_answer 爬取当天新增的答案

爬取结果分别存入数据库中的question表、answer表。

### mongodb安装

 [菜鸟教程](https://www.runoob.com/mongodb/mongodb-tutorial.html)

### scrapy安装

[scrapy安装指南](https://scrapy-chs.readthedocs.io/zh_CN/0.24/intro/install.html)

## 使用流程

### 配置mongodb

在settings.py中可以设置自己的mongodb

- 地址（本机为127.0.0.1）
- 端口（一般都是27017）
- 数据库名称 **MONGODB_DBNAME**（自定义）
- 保存问题的表  **MONGODB_Q_SHEET_NAME** （自定义）
- 保存答案的表   **MONGODB_A_SHEET_NAME**（自定义）

### 启动爬虫

在外层spider所在目录命令行中输入

~~~shell
scrapy crawl [爬虫名称]
#eg
scrapy crawl question
~~~

- 首先启动question爬虫，爬取问题并存入数据库
- 之后启动answer爬虫，先读取数据库中的问题id爬取所有答案并存入数据库
- 之后可以启动update_answer，可以爬取当天的新问题到数据库

## dealString

> 对每个月/每一天的文本 分词 统计词频

deal_separate与deal_count分别可以切词和统计词频。

可以传入"month"或者"day"来确定切词的精度。