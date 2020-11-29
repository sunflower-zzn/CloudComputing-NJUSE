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
    word_list = [word for word in jieba.cut(string, cut_all=False) if word not in stop_words]
    dic_words = dict(Counter(word_list))
    return dic_words


def cal_separate(string):
    # 停用词集合
    stop_words = readFile('baidu_stopwords.txt')

    # 分词，同时剔除停用词
    word_list = []
    word_list = [word for word in jieba.cut(string, cut_all=False) if word not in stop_words]
    # print(word_list)
    return word_list


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


# 答案按天分类
def separate_day(questionList):
    result = {}
    for question in questionList:
        created_time = question['created_time'].split(" ")[0]
        if created_time in result:
            temp = result[created_time]
            temp += question['content']
            result[created_time] = temp
        else:
            result[created_time] = question['content']
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


def deal_separate(type):
    if type == "month":
        dic = separate_month(readMongoDB())
    else:
        dic = separate_day(readMongoDB())
    total_data = {}
    for key in sorted(dic):
        print(key)
        print("-------")
        word_list = cal_separate((dic[key]))
        print(word_list)
        total_data[key] = "|".join(word_list)
    print(total_data)
    j = json.dumps(total_data, ensure_ascii=False, indent=5)
    with open("separateWord_" + type + ".json", 'w', encoding="utf-8") as f:
        f.write(j)
    return total_data


def deal_count(type):
    if type == "month":
        dic = separate_month(readMongoDB())
    else:
        dic = separate_day(readMongoDB())

    total_data = {}
    for key in sorted(dic):
        sorted_words = sorted(cal(dic[key]).items(), key=lambda d: d[1], reverse=True)
        data = {}
        db_data = {}
        for word in sorted_words[:100]:
            data[word[0]] = word[1]
            print(word[0], ":", word[1])
        total_data[key] = data
        storeMongoDB(db_data)
    print(total_data)
    j = json.dumps(total_data, ensure_ascii=False, indent=5)
    with open("countWord" + type + '.json', "w", encoding='utf-8') as output_file:
        output_file.write(j)
        print("加载数据完成...")


if __name__ == "__main__":
    deal_separate("day")
