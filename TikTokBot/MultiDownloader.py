import os
import pymongo
from urllib.request import urlretrieve
import time
from queue import Queue
from concurrent.futures import wait, ThreadPoolExecutor, ALL_COMPLETED

class MultiDownloader:
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

            data = {
                'file_name': file_name,
                'download_url': download_url
            }
            data_copy = data.copy()
            data_list.append(dict(data_copy))

        return data_list

    # 显示下载速度
    def Schedule(self, a, b, c):
        #  a:已经下载的数据块
        #  b:数据块的大小
        #  c:远程文件的大小
        per = 100.0 * a * b / c
        if per > 100:
            per = 100
        print('%.2f%%' % per)


    def downloader(self, data):
        file_name = data.get('file_name') + '.mp4'
        print('开始下载')
        urlretrieve(data.get('download_url'), file_name, self.Schedule)
        print('下载结束')


    def multi_douyin_video_download(self, data_list):
        # 抖音id为新建文件夹
        file_folder_name = 'D:\\program\\Scrapy\\DouYin\\video\\{}'.format(self.douyin_id)
        folder = os.path.exists(file_folder_name)
        if not folder:
            os.makedirs(file_folder_name)
        os.chdir(file_folder_name)
        headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}

        # 多线程进行下载
        executor = ThreadPoolExecutor(len(data_list))
        future_tasks = [executor.submit(self.downloader, data) for data in data_list]
        wait(future_tasks, return_when=ALL_COMPLETED)

if __name__ == '__main__':
    douyin_id = input('请输入抖音ID：')
    start_time = time.time()
    multi_download = MultiDownloader(douyin_id)
    data_list = multi_download.get_douyin_urls()
    multi_download.multi_douyin_video_download(data_list)
    end_time = time.time()

    print('总用时为: %s' % (end_time-start_time))


