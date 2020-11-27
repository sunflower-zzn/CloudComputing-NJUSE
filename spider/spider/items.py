# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class QuestionItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    """回答属性

        Attributes:
            id 问题id
            title 问题标题
            """
    id = Field()
    title = Field()


class AnswerItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    """回答属性

        Attributes:
            content 回答内容
            title 问题标题
            created_time 回答时间
            """
    content = Field()
    title = Field()
    created_time = Field()
