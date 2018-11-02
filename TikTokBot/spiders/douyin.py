# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urlencode
import json
import time

from TikTokBot.items import TiktokbotItem


class DouyinSpider(scrapy.Spider):
    name = 'douyin'
    allowed_domains = ['aweme.snssdk.com']
    douyinId = input('请输入抖音号')
    time_stamp = int(time.time())
    rticket = int(round(time.time()) * 1000)
    para = {
        'keyword': douyinId, 'offset': '0',
        'count':'10', 'is_pull_refresh': '0',
        'hot_search': '0', 'latitude':'0.0',
        'longitude':'0.0', 'ts': '1541132020',
        'js_sdk_version':'1.2.2', 'app_type':'normal',
        'manifest_version_code':'310', '_rticket': '1541132020223',
        'ac': 'wifi', 'device_id': '53910643127',
        'iid': '48828704455', 'os_version': '9',
        'channel': 'douyin_tengxun_wzl', 'version_code': '310',
        'device_type': 'ONEPLUS%20A6000', 'language': 'zh',
        'uuid': '869897033037051', 'resolution': '1080*2200',
        'openudid': '0061ee21378e2667', 'update_version_code': '3102',
        'app_name': 'aweme', 'version_name': '3.1.0',
        'os_api': '28', 'device_brand':'OnePlus', 'ssmix': 'a',
        'device_platform': 'android', 'dpi': '420','aid': '1128',
        'as': 'a1655c4d14bffb4edb6899', 'cp': 'c4f2ba5f44b8d2e4e1aiOm', 'mas': '01ba655c793ea7e1590398abacaa88d2d99c9c1c6c4626a62c4666'
    }
    data = urlencode(para)

    base_url = 'https://aweme.snssdk.com/aweme/v1/general/search/single/'
    url = base_url + '?' + data
    start_urls = [url]


    def parse(self, response):
        item = TiktokbotItem()
        json_object = json.loads(response.body.decode('utf-8'))
        # print(json_object)
        datas = json_object.get('data')
        object_list = []
        for data in datas:
            if('user_list' in data):
                user_list = data.get('user_list')
                user=user_list[0]
                uid=user.get('user_info').get('uid')
        # print(uid)
        #         for user in user_list:
        #             user_info = user.get('user_info')
        #             nickname = user_info.get('nickname')
        #             birthday = user_info.get('birthday')
        #             signature = user_info.get('signature')
        #             id = user_info.get('unique_id')
        #             uid=user_info.get('uid')
        #     else:
        #         aweme_info = data.get('aweme_info')
        #         aweme_id = aweme_info.get('aweme_id')
        #         desc = aweme_info.get('desc')
        #         play_addr = aweme_info.get('video').get('play_addr').get('url_list')
        #         down_addr = aweme_info.get('video').get('download_addr').get('url_list')
        #         play_data = {
        #             'Id': aweme_id,
        #             '简介': desc,
        #             '纯链接': play_addr,
        #             '下载链接': down_addr,
        #         }
        #         play_data_list = play_data.copy()
        #         object_list.append(dict(play_data_list))
        # print(object_list)







