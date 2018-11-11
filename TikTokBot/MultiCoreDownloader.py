import os
import pymongo
from urllib.request import urlretrieve
import time
from multiprocessing import Pool

class MultiCoreDownloader:
    def __init__(self, douyin_id):
        self.douyin_id = douyin_id
        self.client = pymongo.MongoClient(host='127.0.0.1', port=27017)
        self.db = self.client['TikTok']
        self.douyin = self.db['douyin']
        self.tiktok = self.db['tiktok']

    def get_douyin_urls(self):
        douyin_object = self.douyin.find({'douyin_id': self.douyin_id})
        data_list = []
        for douyin_item in douyin_object:
            file_name = douyin_item.get('aweme_id')
            download_url = douyin_item.get('play_addr')
            description = douyin_item.get('description')

            data = {
                'file_name': file_name,
                'download_url': download_url,
                'infomation': description
            }
            data_copy = data.copy()
            data_list.append(dict(data_copy))

        return data_list

    def downloader(self, data):
        file_name = data.get('file_name') + '.mp4'
        infomation = data.get('infomation')
        print('%s文件开始下载' % infomation)
        urlretrieve(data.get('download_url'), file_name)
        print('%s下载结束' % infomation)

    def multi_douyin_video_download(self, data_list):
        # 抖音id为新建文件夹
        file_folder_name = 'D:\\program\\Scrapy\\DouYin\\video\\{}'.format(self.douyin_id)
        folder = os.path.exists(file_folder_name)
        if not folder:
            os.makedirs(file_folder_name)
        os.chdir(file_folder_name)

        # 多进程进行下载
        pool = Pool()
        pool.map(self.downloader, data_list)
        print('全部下载结束')

if __name__ == '__main__':
    douyin_id = input('请输入抖音ID：')
    start_time = time.time()
    multi_download = MultiCoreDownloader(douyin_id)
    data_list = multi_download.get_douyin_urls()
    multi_download.multi_douyin_video_download(data_list)
    end_time = time.time()

    print('总用时为: %s 秒' % round(end_time - start_time))


