from selenium import webdriver
from selenium.common.exceptions import TimeoutException
import pymongo
from time import sleep
import os

class CrawlVideo():
    def __init__(self, douyin_id):
        self.client = pymongo.MongoClient(host='127.0.0.1', port=27017)
        self.db = self.client['TikTok']
        self.douyin = self.db['douyin']
        self.tiktok = self.db['tiktok']
        self.douyin_id = douyin_id

    def get_video_url(self):
        object_list = self.douyin.find({'douyin_id': self.douyin_id})
        video_list = []
        description = ''
        for object in object_list:
            video_url = object.get('play_addr')
            if(description == ''):
                description = object.get('description')
            video_list.append(video_url)
        video_data = {
            'file_name': description,
            'download_urls': video_list
        }
        return video_data

    def download_video(self, data):
        file_folder_name = 'D:\\program\\Scrapy\\DouYin\\video\\{}'.format(self.douyin_id)
        folder = os.path.exists(file_folder_name)
        if not folder:
            os.makedirs(file_folder_name)
        else:
            os.chdir(file_folder_name)
        # Firefox 下载

        # profile = webdriver.FirefoxProfile()
        # profile.set_preference('browser.download.dir', file_folder_name)
        # # 设置下载到自定义路径（2为自定义）
        # profile.set_preference('browser.download.folderList', 2)
        # # 不显示下载管理器
        # profile.set_preference('browser.download.manager.showWhenStarting', False)
        # # 设置下载文件类型
        # profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'video/mp4')
        # driver = webdriver.Firefox(profile)

        # Chrome下载
        options = webdriver.ChromeOptions()
        profiles = {'profile.default_content_settings.popups': 0, 'download.default_directory': file_folder_name}
        options.add_experimental_option('prefs', profiles)

        driver = webdriver.Chrome(options=options)

        video_list = data.get('download_urls')
        for video_item in video_list:
            driver.get(video_item + '.mp4')
            sleep(3)

        driver.quit()

if __name__ == '__main__':
    id = input('请输入数据库存在的抖音id：')
    crawl_video = CrawlVideo(str(id))
    data = crawl_video.get_video_url()
    crawl_video.download_video(data)




