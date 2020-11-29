import csv
from kafka import KafkaProducer
import time

def main():
    ##生产模块
    producer = KafkaProducer(bootstrap_servers=['121.196.222.214:9092'])
    with open('D:/QQfile/answer_results.csv','r',encoding='utf8')as fp:
        reader=csv.reader(fp)
        data_temp=[]
        for row in reader:
            data_temp.append(row)
        pre=[]
        date=[]
        pos=0
        for i in range(len(data_temp)-1):
            if data_temp[i][0]==data_temp[i+1][0]:
                date=data_temp[i][0]
                pre.append(data_temp[i][1])
            else:
                pos=i
                break
        print(pos)
        for i in range(len(pre)):
            string=pre[i]
            time.sleep(1)
            producer.send("txt", bytes(string.replace('\n','').encode('utf-8')))
            print(bytes(string.replace('\n','').encode('utf-8')))
if __name__ == '__main__':
    main()