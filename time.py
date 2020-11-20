import json as js
from os import listdir
import matplotlib
import matplotlib.pyplot as plt
import pylab
from matplotlib import ticker


# 输入json文件夹路径，进行数据筛选
def getData(path):
    label = '/'
    fileList = listdir(path)
    res = {}

    for filename in fileList:
        file = path + label + filename
        with open(file, 'r', encoding='UTF-8')as f:
            pop = js.load(f)
            question = pop["0"]["question"]
            times = dict()

            for item in pop.values():
                time = item["releaseTime"][4:9]
                if time in times.keys():
                    times[time] += 1
                else:
                    times[time] = 1

            info = dict()
            info["length"] = len(times.keys())
            info["from"] = min(times.keys())
            info["to"] = max(times.keys())
            info["dates"] = sorted(times.items(), key=lambda times: times[0], reverse=False)
            res[question] = info
            f.close()
    # print(res)
    return res


# 问题讨论持续时长分布图
def func1(res):
    pylab.mpl.rcParams['font.sans-serif'] = ['SimHei']

    res1 = dict()  # 持续时长：问题数
    for info in res.values():
        length = info["length"]
        if length in res1.keys():
            res1[length] += 1
        else:
            res1[length] = 1
    list1 = sorted(res1.items(), key=lambda res1: res1[0], reverse=False)
    # print(list1)

    x1 = []
    y1 = []
    for item in list1:
        x1.append(item[0])
        y1.append(item[1])
    # print(x1)
    # print(y1)
    title = "问题讨论持续时长分布图 "
    plt.title(title, fontsize=10)
    plt.bar(range(len(y1)), y1, color='lightsteelblue')
    plt.plot(range(len(y1)), y1, marker='o', color='orange')
    plt.xticks(range(len(x1)), x1)
    plt.xlabel('持续时长/天')
    plt.ylabel("问题数/个")
    plt.legend()
    plt.show()


# 每日回答数分布图
def func3(res):
    pylab.mpl.rcParams['font.sans-serif'] = ['SimHei']

    res3 = dict()  # 日期：回答数
    for info in res.values():
        dates = info["dates"]
        for date in dates:
            if date[0] in res3.keys():
                res3[date[0]] += date[1]
            else:
                res3[date[0]] = date[1]
    list3 = sorted(res3.items(), key=lambda res3: res3[0], reverse=False)
    # print(list3)

    x3 = []
    y3 = []
    for item in list3:
        x3.append(item[0])
        y3.append(item[1])
    # print(x3)
    # print(y3)

    fig, ax = plt.subplots(1, 1)
    title = "每日回答数分布图 "
    plt.title(title, fontsize=10)
    plt.legend()
    font = {'size': 8}
    matplotlib.rc('font', **font)
    ax.plot(x3, y3, color='lightseagreen', lw=2)
    tick_spacing = 4
    ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    plt.xlabel('日期', fontsize=10)
    plt.ylabel('回答数/个', fontsize=10)
    plt.xticks(rotation=90, fontsize=8)
    plt.yticks(fontsize=10)
    plt.subplots_adjust(top=0.9, bottom=0.2, left=0.15, right=0.95)
    fig.set_size_inches(28, 20)
    plt.show()


# path = 'C://Users/94285/Desktop/answer'
# res = getData(path)
# func1(res)
# func3(res)
