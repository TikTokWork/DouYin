# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from TikTokBot.items import DouYinBotItem,TiktokbotItem
import urllib.request
import pymongo
import os


class DouYinbotMongoDBPipeline(object):
    def __init__(self):
        # 连接数据库
        self.client = pymongo.MongoClient(host='127.0.0.1', port=27017)
        self.db = self.client['TikTok']
        self.douyin = self.db['douyin']
        self.tiktok = self.db['tiktok']


    def process_item(self, item, spider):
        dict_item = dict(item)
        if isinstance(item, DouYinBotItem):
            self.douyin.insert_one(dict_item)
            return item
        elif isinstance(item, TiktokbotItem):
            self.tiktok.insert_one(dict_item)
            return item

class DouYinBotVideoPipeline(object):
    def __init__(self):
        self.count = 1
        self.tag = 1

    def process_item(self, item, spider):
        video_url = item['play_addr']
        aweme_id = item['aweme_id']
        data = {
            'file_name': aweme_id,
            'download_url': video_url
        }
        file_folder_name = 'D:\\program\\Scrapy\\DouYin\\video\\{}'.format(item['douyin_id'])
        folder = os.path.exists(file_folder_name)
        if not folder:
            os.makedirs(file_folder_name)
        os.chdir(file_folder_name)
        file_name = data.get('file_name') + '.mp4'
        url = data.get('download_url')
        headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
        request = urllib.request.Request(url, headers=headers)
        u = urllib.request.urlopen(request)
        f = open(file_name, 'wb')
        meta = u.info()
        file_size = round(int(meta.get('Content-Length')) / (1024*1024))
        print("正在下载: %s 大小: %s MB 第%s个文件" % (file_name, file_size, self.count))
        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break
            f.write(buffer)
        f.close()
        print('第%s个文件下载成功' % self.count)
        self.count += 1
        return item



