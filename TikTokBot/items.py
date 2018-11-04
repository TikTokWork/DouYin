# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TiktokbotItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field() #用户uid
    user_art = scrapy.Field() # 用户所有作品
    description = scrapy.Field() #用户简介
    play_addr = scrapy.Field() #用户纯链接
    down_addr = scrapy.Field() #用户生成的下载链接

class DouYinBotItem(scrapy.Item):
    id = scrapy.Field() #用户uid
    nickname = scrapy.Field() #用户昵称
    user_art = scrapy.Field() # 用户所有作品
    description = scrapy.Field() #用户简介
    play_addr = scrapy.Field() #用户纯链接
    download_addr = scrapy.Field() #用户生成的下载链接


