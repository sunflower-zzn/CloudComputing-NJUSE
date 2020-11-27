import time


def timeTransfer(string):
    timeStamp = int(string)
    timeArray = time.localtime(timeStamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    print(otherStyleTime)
    return otherStyleTime


def getCurrentTime():
    a = time.strftime("%a %b %d %H:%M:%S %Y", time.localtime())
    strings = a.split(" ")
    strings[3] = '00:00:00'

    # print(" ".join(strings))
    # print(time.mktime(time.strptime(a, "%a %b %d %H:%M:%S %Y")))
    return time.mktime(time.strptime(" ".join(strings), "%a %b %d %H:%M:%S %Y"))


getCurrentTime()
