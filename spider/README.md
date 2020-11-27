## spider

> 爬虫部分

### 简介

> 使用scrapy+ajax方式爬取知乎新冠肺炎话题中精华部分的所有问题的所有答案

一共有三个爬虫

- zhihu  爬取问题id及问题标题
- answer 爬取问题下的答案内容及发布时间
- update_answer 爬取当天新增的答案

爬取结果分别存入数据库中的question表、answer表。

### mongodb设置

在settings.py中可以设置自己的mongodb的地址、端口、数据库名称、保存问题的表、保存答案的表

### 使用方法

在外层spider所在目录中输入

~~~
scrapy crawl [爬虫名称]
~~~

eg:

~~~
scrapy crawl zhihu
~~~

## dealString

> 对每个月的文本 分词 统计词频

直接在deal_string中run就可以