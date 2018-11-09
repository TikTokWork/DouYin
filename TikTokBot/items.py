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
    douyin_id = scrapy.Field() # 用户id
    author_desc = scrapy.Field() # 用户简介
    user_art = scrapy.Field() # 用户所有作品
    description = scrapy.Field() #用户简介
    play_addr = scrapy.Field() #用户纯链接

class DouYinBotItem(scrapy.Item):
    aweme_id = scrapy.Field() #作品id
    nickname = scrapy.Field() #用户昵称
    douyin_id = scrapy.Field()  # 用户id
    author_desc = scrapy.Field()  # 用户简介
    user_art = scrapy.Field() # 用户所有作品
    description = scrapy.Field() #作品简介
    play_addr = scrapy.Field() #所有作品纯链接


