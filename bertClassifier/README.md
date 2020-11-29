# BERT_Chinese_Classification
本项目用于云计算大作业中的中文文本情感分析部分，使用bert进行文本分类任务

# 参考

- [奇点机智的文章](https://www.jianshu.com/p/aa2eff7ec5c1)
- [renxingkai](https://github.com/renxingkai)/[BERT_Chinese_Classification](https://github.com/renxingkai/BERT_Chinese_Classification)
- [pengming617/bert_classification: 利用bert预训练的中文模型进行文本分类](https://github.com/pengming617/bert_classification)

# 代码结构

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

# 具体实现

本项目基于BERT的开源代码，借助google提供的预训练模型，使用标定好的情感分类数据集进行fine tune，具体实现步骤如下：

## 预训练模型

本实验，是用BERT进行中文情感分类，以下介绍具体操作步骤。

对于中文而言，google公布了一个参数较小的BERT预训练模型。具体参数数值如下所示：

```
Chinese Simplified and Traditional, 12-layer, 768-hidden, 12-heads, 110M parameter
```

下载链接：https://storage.googleapis.com/bert_models/2018_11_03/chinese_L-12_H-768_A-12.zip

## fine tune

BERT的代码同论文里描述的一致，主要分为两个部分。一个是**训练语言模型（language model）的预训练（pretrain）部分**。另一个是**训练具体任务(task)的fine-tune部分**。在开源的代码中：

- 预训练入口：run_pretraining.py
- fine-tune入口：针对不同的任务分别在run_classifier.py和run_squad.py。
  - run_classifier.py：分类任务。例如CoLA、MRPC、MultiNLI。
  - run_squad.py：阅读理解(MRC)任务，如squad2.0和squad1.1。

因此如果要在自己的数据集上fine-tune跑分类任务代码，需要编写类似run_classifier.py的具体任务文件。

## 代码部分

代码部分的实现，主要涉及以下部分：

- run_classifier.py：class MyProcessor
  - get_train_examples：读取训练语料，返回list[InputExample]，进行训练任务
  - get_dev_examples：读取评估语料，返回list[InputExample]，进行评估任务
  - get_test_examples：读取预测数据，返回list[InputExample]，进行预测任务
  - get_labels：设置标签，根据语料分类的不同设置不同的标签
  - 对于一个需要执行训练、交叉验证和测试完整过程的模型而言，自定义的processor里需要继承DataProcessor，并重载获取label的get_labels和获取单个输入的get_train_examples,get_dev_examples和get_test_examples函数。其分别会在main函数的FLAGS.do_train、FLAGS.do_eval和FLAGS.do_predict阶段被调用。
- run_classifier.py：main
  - processors：添加自己的MyProcessor
  - 设置训练、评估、预测任务的输入输出格式及文件夹即可
- single_predict.py&intent.py
  - 类似于run_classifier.py的main方法，实现了predicts方法以实现语句级别的预测
  - intent.py为一个执行demo

###MyProcessor

```python
class MyProcessor(DataProcessor):

    # read txt
    # 返回InputExample类组成的list
    # text_a是一串字符串，text_b则是另一串字符串。在进行后续输入处理后(BERT代码中已包含，不需要自己完成)
    # text_a和text_b将组合成[CLS] text_a [SEP] text_b [SEP]的形式传入模型
    def get_train_examples(self, data_dir):
        file_path = os.path.join(data_dir, 'train_sentiment.txt')
        f = open(file_path, 'r', encoding='utf-8')
        train_data = []
        index = 0
        for line in f.readlines():
            guid = 'train-%d' % index  # 参数guid是用来区分每个example的
            line = line.replace("\n", "").split("\t")
            text_a = tokenization.convert_to_unicode(str(line[1]))  # 要分类的文本
            label = str(line[2])  # 文本对应的情感类别
            train_data.append(InputExample(guid=guid, text_a=text_a, text_b=None, label=label))  
            # 加入到InputExample列表中
            index += 1
        return train_data

    # read txt
    # 返回InputExample类组成的list
    # text_a是一串字符串，text_b则是另一串字符串。在进行后续输入处理后(BERT代码中已包含，不需要自己完成)
    # text_a和text_b将组合成[CLS] text_a [SEP] text_b [SEP]的形式传入模型
    def get_dev_examples(self, data_dir):
        file_path = os.path.join(data_dir, 'test_sentiment.txt')
        f = open(file_path, 'r', encoding='utf-8')
        dev_data = []
        index = 0
        for line in f.readlines():
            guid = 'dev-%d' % index # 参数guid是用来区分每个example的
            line = line.replace("\n", "").split("\t")
            text_a = tokenization.convert_to_unicode(str(line[1])) # 要评估的文本
            label = str(line[2]) # 文本对应的情感类别
            dev_data.append(InputExample(guid=guid, text_a=text_a, text_b=None, label=label))
            # 加入到InputExample列表中
            index += 1
        return dev_data

    # csv
    # 读取zhihu回答的csv文件进行相关
    def get_test_examples(self, data_dir):
        file_path = os.path.join(data_dir, 'answer.csv')
        test_df = pd.read_csv(file_path, encoding='utf-8', header=None, sep='\n')
        test_data = []
        for index, test in enumerate(test_df.values):
            guid = 'test-%d' % index
            text_a = tokenization.convert_to_unicode(str(test[0]).split("\t")[1])
            # 传入一个随意的label数值，因为在模型的预测（prediction）中label将不会参与计算！！
            test_data.append(InputExample(guid=guid, text_a=text_a, text_b=None, label=str(0)))
        return test_data

    def get_labels(self):
        # 分别对应三类情感标签
        return ['0', '1', '2']
```

修改完成MyProcessor后，需要在在原本main函数的processor字典里，加入修改后的processor类，即可在运行参数里指定调用该processor。

```python
    processors = {
        # "cola": ColaProcessor,
        # "mnli": MnliProcessor,
        # "mrpc": MrpcProcessor,
        # "xnli": XnliProcessor,
        "my": MyProcessor,
    }
```

###single_predict.py

```python
def predicts(text_data):
    ...
    
    # predict_examples = processor.get_test_examples(FLAGS.data_dir) 
    # 不使用get_test_examples批量处理，而是直接读取list
    test_data = []
    for index in range(len(text_data)):
        guid = 'test-%d' % index
        text_a = tokenization.convert_to_unicode(str(text_data[index]))
        # text_b = tokenization.convert_to_unicode(str(test[1]))
        # label = str(test[2])
        test_data.append(InputExample(guid=guid, text_a=text_a, text_b=None, label=None))
        
	...
```

# 训练&测试

使用train.sh进行fine tune训练，并进行评估：

```shell
#!/usr/bin/env bash

python run_classifier.py \
  --data_dir=data \
  --task_name=my \
  --vocab_file=chinese_L-12_H-768_A-12/vocab.txt \
  --bert_config_file=chinese_L-12_H-768_A-12/bert_config.json \
  --output_dir=my_model \
  --do_train=true \
  --do_eval=true \
  --init_checkpoint=chinese_L-12_H-768_A-12/bert_model.ckpt \
  --max_seq_length=70 \
  --train_batch_size=32 \
  --learning_rate=5e-5 \
  --num_train_epochs=3.0
```

训练结果：

```reStructuredText
eval_accuracy = 0.90064484
eval_loss = 0.30996767
global_step = 1605
loss = 0.30984673
```

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





