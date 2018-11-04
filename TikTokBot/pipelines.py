# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

from TikTokBot.items import DouYinBotItem,TiktokbotItem


class TiktokbotMongoDBPipeline(object):
    def __init__(self):
        # 连接数据库
        self.client = pymongo.MongoClient(host='127.0.0.1', port=27017)
        self.db = self.client['TikTok']
        self.douyin = self.db['douyin']
        self.tiktok = self.db['tiktok']

    def process_item(self, item, spider):
        dict_item = dict(item)
        flag = {'id': dict_item.get('id')}
        if isinstance(item, DouYinBotItem):
            self.douyin.update(flag, dict_item, upsert=True)
            return item
        elif isinstance(item, TiktokbotItem):
            self.tiktok.update(flag, dict_item, upsert=True)
            return item