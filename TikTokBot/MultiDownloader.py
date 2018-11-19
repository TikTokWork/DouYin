import os
import pymongo
from urllib.request import urlretrieve
import time
from threading import Thread
from queue import Queue

class MultiDownloader:
    def __init__(self, douyin_id):
        self.douyin_id = douyin_id
        self.client = pymongo.MongoClient(host='127.0.0.1', port=27017)
        self.db = self.client['TikTok']
        self.douyin = self.db['douyin']
        self.tiktok = self.db['tiktok']
        self.data_queue = Queue()

    def get_douyin_urls(self):
        douyin_object = self.douyin.find({'douyin_id': self.douyin_id})
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
            self.data_queue.put(dict(data_copy))

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
        infomation = data.get('infomation')
        print('%s文件开始下载' % infomation)
        urlretrieve(data.get('download_url'), file_name)
        print('%s下载结束' % infomation)

    def worker(self):
        while not self.data_queue.empty():
            data = self.data_queue.get()
            self.downloader(data)
            self.data_queue.task_done()


    def multi_douyin_video_download(self):
        # 抖音id为新建文件夹
        file_folder_name = 'E:\\Tik tok\\DouYin\\video\\{}'.format(self.douyin_id)
        folder = os.path.exists(file_folder_name)
        if not folder:
            os.makedirs(file_folder_name)
        os.chdir(file_folder_name)


        # 多线程进行下载
        for x in range(8):
            thread = Thread(target=self.worker,name=x)
            thread.start()
            print('%s线程启动' %x)
        self.data_queue.join()
        print('全部下载完成')

if __name__ == '__main__':
    douyin_id = input('请输入抖音ID：')
    start_time = time.time()
    multi_download = MultiDownloader(douyin_id)
    multi_download.get_douyin_urls()
    multi_download.multi_douyin_video_download()
    end_time = time.time()

    print('总用时为: %s 秒' % round(end_time-start_time))


