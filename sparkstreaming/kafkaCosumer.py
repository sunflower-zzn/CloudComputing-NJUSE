import findspark
findspark.init('/root/Downloads/spark-2.4.7-bin-hadoop2.7')
from pyspark import SparkContext
from pyspark import SparkConf
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils, TopicAndPartition


def start():
    sconf = SparkConf()
    sconf.set('spark.cores.max', 3).set('spark.io.compression.codec','snappy')
    sc = SparkContext(appName='txt', conf=sconf)
    ssc = StreamingContext(sc, 10)
    brokers = "121.196.222.214:9092"
    topic = 'txt'
    user_data = KafkaUtils.createDirectStream(ssc, [topic], kafkaParams={"metadata.broker.list": brokers})
    gender_users = user_data.flatMap(lambda x:x[1].split('|')).map(lambda gender: (gender, 1)).reduceByKey(lambda a, b: a + b)
    gender_users.pprint()
    gender_users.saveAsTextFiles("/usr/wordcount/w")
    ssc.start()
    ssc.awaitTermination()


if __name__ == '__main__':
    start()
