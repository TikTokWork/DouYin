# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urlencode
import json

from TikTokBot.items import TiktokbotItem,DouYinBotItem


class DouyinSpider(scrapy.Spider):
    name = 'douyin'
    allowed_domains = ['aweme.snssdk.com']
    count = 0
    total_count = 0
    pure_douyin_id = ''

    def __init__(self, douyinId=None, *args, **kwargs):
        super(DouyinSpider, self).__init__(douyinId, **kwargs)
        para = {
            'keyword': douyinId, 'offset': '0',
            'count': '10', 'is_pull_refresh': '0',
            'hot_search': '0', 'latitude': '0.0',
            'longitude': '0.0', 'ts': '1541132020',
            'js_sdk_version': '1.2.2', 'app_type': 'normal',
            'manifest_version_code': '310', '_rticket': '1541132020223',
            'ac': 'wifi', 'device_id': '53910643127',
            'iid': '48828704455', 'os_version': '9',
            'channel': 'douyin_tengxun_wzl', 'version_code': '310',
            'device_type': 'ONEPLUS%20A6000', 'language': 'zh',
            'uuid': '869897033037051', 'resolution': '1080*2200',
            'openudid': '0061ee21378e2667', 'update_version_code': '3102',
            'app_name': 'aweme', 'version_name': '3.1.0',
            'os_api': '28', 'device_brand': 'OnePlus', 'ssmix': 'a',
            'device_platform': 'android', 'dpi': '420', 'aid': '1128',
            'as': 'a1655c4d14bffb4edb6899', 'cp': 'c4f2ba5f44b8d2e4e1aiOm',
            'mas': '01ba655c793ea7e1590398abacaa88d2d99c9c1c6c4626a62c4666'
        }
        data = urlencode(para)
        base_url = 'https://aweme.snssdk.com/aweme/v1/general/search/single/'
        url = base_url + '?' + data
        self.start_urls = [url]
        self.pure_douyin_id = douyinId

    def parse(self, response):
        json_object = json.loads(response.body.decode('utf-8'))
        # print(json_object)
        datas = json_object.get('data')
        uid = ''
        for data in datas:
            if('user_list' in data):
                user_list = data.get('user_list')
                user = user_list[0]
                uid = user.get('user_info').get('uid')
                self.total_count = user.get('user_info').get('aweme_count')
                print(self.total_count)

        para = {
            'max_cursor': '0', 'user_id': uid,
            'count': '20', 'retry_type': 'no_retry',
            'ts': '1541132020', 'js_sdk_version': '1.2.2', 'app_type': 'normal',
            'manifest_version_code': '310', '_rticket': '1541132020223',
            'ac': 'wifi', 'device_id': '53910643127',
            'iid': '48828704455', 'os_version': '9',
            'channel': 'douyin_tengxun_wzl', 'version_code': '310',
            'device_type': 'ONEPLUS%20A6000', 'language': 'zh',
            'uuid': '869897033037051', 'resolution': '1080*2200',
            'openudid': '0061ee21378e2667', 'update_version_code': '3102',
            'app_name': 'aweme', 'version_name': '3.1.0',
            'os_api': '28', 'device_brand': 'OnePlus', 'ssmix': 'a',
            'device_platform': 'android', 'dpi': '420', 'aid': '1128',
            'as': 'a1655c4d14bffb4edb6899', 'cp': 'c4f2ba5f44b8d2e4e1aiOm',
            'mas': '01ba655c793ea7e1590398abacaa88d2d99c9c1c6c4626a62c4666'
        }
        para_url = urlencode(para)
        base_url = 'https://aweme.snssdk.com/aweme/v1/aweme/post/'
        next_url = base_url + '?' + para_url
        yield scrapy.Request(url=next_url, callback=self.parse_user)

    def parse_user(self, response):
        douyin_item = DouYinBotItem()
        json_object = json.loads(response.body.decode('utf-8'))
        # print(json_object)
        aweme_list = json_object.get('aweme_list')
        max_cursor = json_object.get('max_cursor')
        object_list = []
        id = ''
        for aweme_item in aweme_list:
            id = aweme_item.get('author_user_id')
            aweme_id = aweme_item.get('aweme_id')
            douyin_id = self.pure_douyin_id
            author_desc = aweme_item.get('author').get('signature')
            desc = aweme_item.get('desc')
            nickname = aweme_item.get('author').get('nickname')
            play_addr = aweme_item.get('video').get('play_addr').get('url_list')[0]

            douyin_item['id'] = id
            douyin_item['aweme_id'] = aweme_id
            douyin_item['douyin_id'] = douyin_id
            douyin_item['author_desc'] = author_desc
            douyin_item['description'] = desc
            douyin_item['nickname'] = nickname
            douyin_item['play_addr'] = play_addr
            douyin_item['user_art'] = self.total_count

            yield douyin_item

            # data = {
            #     '用户Id': id,
            #     '用户昵称': nickname,
            #     '视频简介': desc,
            #     '下载链接': download_addr,
            #     '无水印链接': play_addr
            # }

            self.count = self.count+1


            # data_add = data.copy()
            # object_list.append(dict(data_add))

        para = {
            'max_cursor': max_cursor, 'user_id': id ,
            'count': '20', 'retry_type': 'no_retry',
            'ts': '1541132020', 'js_sdk_version': '1.2.2', 'app_type': 'normal',
            'manifest_version_code': '310', '_rticket': '1541132020223',
            'ac': 'wifi', 'device_id': '53910643127',
            'iid': '48828704455', 'os_version': '9',
            'channel': 'douyin_tengxun_wzl', 'version_code': '310',
            'device_type': 'ONEPLUS%20A6000', 'language': 'zh',
            'uuid': '869897033037051', 'resolution': '1080*2200',
            'openudid': '0061ee21378e2667', 'update_version_code': '3102',
            'app_name': 'aweme', 'version_name': '3.1.0',
            'os_api': '28', 'device_brand': 'OnePlus', 'ssmix': 'a',
            'device_platform': 'android', 'dpi': '420', 'aid': '1128',
            'as': 'a1655c4d14bffb4edb6899', 'cp': 'c4f2ba5f44b8d2e4e1aiOm',
            'mas': '01ba655c793ea7e1590398abacaa88d2d99c9c1c6c4626a62c4666'
        }
        para_url = urlencode(para)
        base_url = 'https://aweme.snssdk.com/aweme/v1/aweme/post/'
        next_url = base_url + '?' + para_url
        if(self.count < self.total_count):
            yield scrapy.Request(url=next_url, callback=self.parse_user)












