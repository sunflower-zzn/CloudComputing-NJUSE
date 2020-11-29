# 进行格式的转换
# autho：zzn
# 2020/11/20
# coding=utf-8

import json
import csv


def json2csv(json_path, csv_path):
    # 读取json文件内容,返回字典格式
    with open(json_path, 'r', encoding='utf8')as fp:
        temp = ""
        for line in fp.readlines():
            temp += line.replace(" ", "")
        json_data = json.loads(temp)

    # 存放入csv文件中
    csv_file = open(csv_path, "w", newline="", encoding='utf-8')
    writer = csv.writer(csv_file, delimiter='\t')
    ansstrs = []
    for key, value in json_data.items():
        time = list(value.keys())[0][:10]
        content = list(value.values())[0]
        if time and content:
            ansstrs.append(time + " " + content)
    ansstrs = list(set(ansstrs))
    res = []
    for ansstr in ansstrs:
        data = str(ansstr).split(" ")
        if len(data) == 2:
            res.append(data)
    res.sort()  # 按时间排序
    for ls in res:
        writer.writerow(ls)


def tsv2csv(tsv_path, csv_path):
    tsv_file = open(tsv_path, 'r', encoding='utf8')
    csv_file = open(csv_path, "w", newline="", encoding='utf-8')
    writer = csv.writer(csv_file)
    for line in tsv_file.readlines():
        s = line[:-1].split("\t")
        writer.writerow([s[0], s[-2]])


def analydata(csv_path, res_path):
    csv_file = open(csv_path, "r", encoding='utf-8')
    res_file = open(res_path, "w", newline="", encoding='utf-8')
    writer = csv.writer(res_file)
    writer.writerow(["time", "neutral", "positive", "negative"])
    datas = []
    for line in csv_file.readlines():
        datas.append(line[:-1].split(","))
    times = []
    for data in datas:
        times.append(data[0])
    times = {}.fromkeys(times)
    for key in times.keys():
        times[key] = [0, 0, 0]
    for data in datas:
        times[data[0]][int(data[1])] += 1
    for res in times.items():
        # print(res)
        writer.writerow([res[0], res[1][0], res[1][1], res[1][2]])


if __name__ == '__main__':
    # json2csv("data/answer.json", "data/answer.csv")
    # tsv2csv("output/answer_result.tsv","output/answer_result.csv")
    analydata("output/answer_result.csv","output/final_results.csv")
