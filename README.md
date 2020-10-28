# 疫情期间知乎话题问答分析

关键词：Streaming流式数据、分布式集群（Hadoop、Scala）、云服务器、可视化展示

## 数据爬取

关键词：BeautifulSoup、MongoDB、urllib

参考：

- 完整的知乎爬虫项目（py2）https://blog.csdn.net/maybeforever/article/details/97292261

- urllib介绍 https://blog.51cto.com/caochun/1746987、https://www.cnblogs.com/derek1184405959/p/8448875.html
- MongoDB官方文档 https://mongodb.net.cn/manual/

#### 代理池获取

由于单一IP爬取过于频繁会被封禁，所以我们需要维护一个代理池，思路

- 氪金（x）
- 从免费的IP网站爬取IP代理池
  - https://www.cnblogs.com/ruogu/p/9606599.html
  - py2 用的几个源都设置了反爬，复现暂时失败 https://github.com/ambition-hb/Pool_Proxy
  - 常用的免费IP网站 https://blog.csdn.net/weixin_44613063/article/details/102538757

#### 问题导向

爬取“疫情”标签下的问题和回答文本，分析相关问答中文本的情感以及关键词等

#### 时间导向

爬取2019.12-2020.05期间的问题及回答，分析其中与疫情有关的比例以及相关的内容

## 数据处理

- 采用筛选等方法，滤去与疫情无关的问题，针对疫情相关问题做进一步处理
- 文本处理，统一格式，存储于MongoDB中

## 数据分析

- 分析疫情期间疫情相关问题的比例和热度
  - 此处的热度可以选择自己定义的热度函数
- 疫情相关问答的文本
  - 文本情感分析
  - 关键词分析
- ……

## 结果展示

- 可视化，在线网站，演示视频，服务器远程接口

