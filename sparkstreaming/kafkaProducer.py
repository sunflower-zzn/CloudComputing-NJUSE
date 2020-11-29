import json
from kafka import KafkaProducer
from kafka import KafkaConsumer
from kafka.errors import KafkaError
import time


def main():
    ##生产模块
    producer = KafkaProducer(bootstrap_servers=['121.196.222.214:9092'])
    with open('D:\QQfile\separateWord_day.json','r',encoding='utf8')as fp:
        json_data = json.load(fp)
        items = json_data.items()
        keys = []
        for key, value in items:
            keys.append(str(key))
        for i in range(len(keys)):
            string=str(json_data[keys[1]])[:5000]
            time.sleep(1)
            producer.send("txt", bytes(string.replace('\n','').encode('utf-8')))
            print(bytes(string.replace('\n','').encode('utf-8')))
            # producer.flush()
if __name__ == '__main__':
    main()