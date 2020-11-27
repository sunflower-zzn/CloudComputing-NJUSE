import json

import jieba
import pymongo
from collections import Counter

MONGODB_HOST = "127.0.0.1"
MONGODB_PORT = 27017
MONGODB_DBNAME = "zhihu"
MONGODB_A_SHEET_NAME = "answer"
MONGODB_S_SHEET_NAME = "separate"


# 计算string的分词
def cal(string):
    # 停用词集合
    stop_words = readFile('baidu_stopwords.txt')

    # 分词，同时剔除停用词
    word_list = []
    word_list = [word for word in jieba.cut(string, cut_all=False) if word not in stop_words]
    dic_words = dict(Counter(word_list))
    return dic_words


# 从mongoDB中读取数据
def readMongoDB():
    host = MONGODB_HOST
    port = MONGODB_PORT
    dbname = MONGODB_DBNAME
    client = pymongo.MongoClient(host=host, port=port)
    my_db = client[dbname]
    sheet = my_db[MONGODB_A_SHEET_NAME]
    result = []
    for item in sheet.find():
        result.append(item)
    return result


# 读取文件
def readFile(file_name):
    fp = open(file_name, "r", encoding="utf-8")
    content_lines = fp.readlines()
    fp.close()
    # 去除行末的换行符，否则会在停用词匹配的过程中产生干扰
    for i in range(len(content_lines)):
        content_lines[i] = content_lines[i].rstrip("\n")
    return content_lines


# 答案按月份分类
def separate_month(questionList):
    result = {}
    for question in questionList:
        created_time = question['created_time']
        data = created_time.split(" ")[0]
        m = data.split("-")[1]
        if m in result:
            temp = result[data.split("-")[1]]
            temp += question['content']
            result[m] = temp
        else:
            result[m] = question['content']
    return result


# 将分词结果存入mongodb
def storeMongoDB(data):
    host = MONGODB_HOST
    port = MONGODB_PORT
    dbname = MONGODB_DBNAME
    client = pymongo.MongoClient(host=host, port=port)
    my_db = client[dbname]
    sheet = my_db[MONGODB_S_SHEET_NAME]
    sheet.insert_one(data)


if __name__ == "__main__":

    dic = separate_month((readMongoDB()))

    words = {}

    # for key, val in dic.items():
    #     print(key)
    #     print("------------")
    #     sorted_words = sorted(cal(val).items(), key=lambda d: d[1], reverse=True)
    #     for word in sorted_words[:100]:
    #         print(word)
    total_data = {}

    for key in sorted(dic):
        print(key)
        print("-------")
        sorted_words = sorted(cal(dic[key]).items(), key=lambda d: d[1], reverse=True)
        data = {}
        db_data = {}
        tempList = []
        for word in sorted_words[:100]:
            data[word[0]] = word[1]
            print(word[0], ":", word[1])
            tempList.append(word[0] + ":" + str(word[1]))
        total_data[key] = data
        db_data[key] = ",".join(tempList)
        storeMongoDB(db_data)
        # print(word[1])
        j = json.dumps(data, ensure_ascii=False, indent=5)
        with open(key + 'month.json', "w", encoding='utf-8') as output_file:
            output_file.write(j)
            print("加载数据完成...")
    # print(total_data)

    j = json.dumps(total_data, ensure_ascii=False, indent=5)
    with open("separate.json", 'w',encoding="utf-8") as f:
        f.write(j)
