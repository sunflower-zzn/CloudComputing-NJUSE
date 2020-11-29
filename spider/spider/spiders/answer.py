import json
import re
import scrapy
import pymongo
from spider.settings import MONGODB_PORT
from spider.settings import MONGODB_HOST
from spider.settings import MONGODB_DBNAME
from spider.settings import MONGODB_A_SHEET_NAME
from spider.settings import MONGODB_Q_SHEET_NAME
from spider.tools.time_transfer import timeTransfer
from spider.items import AnswerItem
from lxml import etree
from scrapy.http import Request, FormRequest


class AnswerSpider(scrapy.Spider):
    name = 'answer'
    allowed_domains = ['www.zhihu.com']
    start_urls = []
    base_url = "https://www.zhihu.com/api/v4/questions/{}/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cattachment%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%2Cis_recognized%2Cpaid_info%2Cpaid_info_content%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics%3Bsettings.table_of_content.enabled%3B&limit=5&offset=0&platform=desktop&sort_by=default"

    def __init__(self,*args, **kwargs):
        self.host = MONGODB_HOST
        self.port = MONGODB_PORT
        self.database = MONGODB_DBNAME
        self.sheet = MONGODB_Q_SHEET_NAME

        client = pymongo.MongoClient(host=self.host, port=self.port)
        db = client[self.database]
        collection = db[self.sheet]

        for item in collection.find():
            print(item['id'])
            print(item['title'])
            self.start_urls.append(self.base_url.format(item['id']))

    def parse(self, response):
        # 保存为AnswerItem交给piplines处理
        Item = AnswerItem()
        data = json.loads(response.body)
        dataList = data['data']
        nextUrl = data['paging']
        if not nextUrl['is_end']:
            self.start_urls.append(nextUrl['next'])
        for d in dataList:
            content = d['content']
            # 收集到的content带有前端标签，利用lxml的etree去除标签
            response = etree.HTML(text=content)
            content = response.xpath('string(.)')

            Item['content'] = content
            Item['title'] = d['question']['title']
            Item['created_time'] = timeTransfer(d['created_time'])
            yield Item
            print(d['question']['title'])
            print("-------------------------")
            print(content)
            print(timeTransfer(d['created_time']))
        pass