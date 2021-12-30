# Scrapy爬虫使用

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

## 基于Bert的文本情感分析使用说明

### 代码结构

- **预训练脚本**：train.sh
- **预测脚本**：predict.sh
- **单条语句预测**：intent.py
- **预训练模型**：[chinese_L-12_H-768_A-12](https://storage.googleapis.com/bert_models/2018_11_03/chinese_L-12_H-768_A-12.zip)
  - bert_model.ckpt：负责模型变量载入的
  - vocab.txt：训练时中文文本采用的字典
  - bert_config.json：BERT在训练时，可选调整的一些参数
- **语料**：
  - 携程酒店评论语料-三分类：data/threeClassifier
  - 中文情感分析语料chnsenticorp-二分类：data/chnsenticor
  - 知乎语料-未标定：data/zhihu

### 使用流程

使用train.sh进行fine tune训练，并进行评估:
（建议使用GPU进行训练）

```shell
sh train.sh
```

训练结果：my_model/eval_results.txt

```reStructuredText
eval_accuracy = 0.90064484
eval_loss = 0.30996767
global_step = 1605
loss = 0.30984673
```

fine-tune训练模型下载：https://zzn-normal.oss-cn-beijing.aliyuncs.com/%E5%AD%A6%E4%B9%A0/my_model.zip

使用predict.sh执行批量预测任务：

```shell
#!/usr/bin/env bash
python run_classifier.py \
  --task_name=my \
  --do_predict=true \
  --data_dir=data \
  --vocab_file=chinese_L-12_H-768_A-12/vocab.txt \
  --bert_config_file=chinese_L-12_H-768_A-12/bert_config.json \
  --init_checkpoint=my_model \
  --max_seq_length=70 \
  --output_dir=output
```

单句调试部分：intent.py

```
from single_predict import predicts


sentences = ['testsentence0',
             'testsentence1']
dic = predicts(sentences)
for item in dic.items():
    print(item)
```

# 关于流计算以及对应连接工具代码的使用

### 环境配置

使用kafka16.0以及spark2.4.7以及对应的spark-kafka-assembly.jar以及mongodb等工具。

### 使用代码过程

1. 首先，在装有kafka16.0的服务器(linux)上运行代码

   ```shell
   cd 对应kafka包解压位置
   输入 
   ./bin/zookeeper-server-start.sh config/zookeeper.properties
   启动zookeeper
   进入另外一个控制台
   输入
   ./bin/kafka-server-start.sh config/server.properties
   启动kafka
   ```

2. 在装有spark2.4.7以及对应jars文件夹下含有对应assembly包的服务器上

   ```shell
   编辑kafkaCusomer.py将kafka地址设置为服务器ip
   输入
   python3 kafkaCusomer.py或者kafkaCusomer_mode.py代码
   运行sparkstreaming监视
   新开一个控制台
   然后本地或者服务器运行readMongo.py连接mongodb获取数据
   然后本地或者服务器运行kafkaProducer将数据传入kafka
   这时在sparkstreaming界面可以看到对应结果，并且对应结果已经存入服务器本地文件夹中
   运行json_convert.py将结果转化为json格式
   最后使用linkWithMongo.py将json上传到mongodb中
   ```

3. 代码具体解释详见说明文档。
