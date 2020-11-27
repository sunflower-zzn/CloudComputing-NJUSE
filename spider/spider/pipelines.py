# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo
from spider.settings import MONGODB_PORT
from spider.settings import MONGODB_HOST
from spider.settings import MONGODB_DBNAME
from spider.settings import MONGODB_Q_SHEET_NAME
from spider.settings import MONGODB_A_SHEET_NAME
from spider.items import QuestionItem
from spider.items import AnswerItem


class QuestionPipeline(object):

    def __init__(self):
        host = MONGODB_HOST
        port = MONGODB_PORT
        dbname = MONGODB_DBNAME
        client = pymongo.MongoClient(host=host, port=port)
        self.my_db = client[dbname]

    def process_question(self, item):
        sheet_name = MONGODB_Q_SHEET_NAME
        self.sheet = self.my_db[sheet_name]
        data = dict(item)
        self.sheet.insert(data)
        return item

    def process_answer(self, item):
        sheet_name = MONGODB_A_SHEET_NAME
        self.sheet = self.my_db[sheet_name]
        data = dict(item)
        self.sheet.insert(data)
        return item

    def process_item(self, item, spider):
        if isinstance(item, QuestionItem):
            self.process_question(item)
        else:
            self.process_answer(item)
