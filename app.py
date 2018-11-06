from flask import Flask, flash, redirect, url_for, render_template,request
import subprocess

app = Flask(__name__)

# 前端首页显示
@app.route('/', methods=["GET", "POST"])
def index():
    return render_template('index.html')

# 前后端通信API接口
@app.route('/api/douyin', methods=["GET"])
def start_douyin_spider():
    user_id = request.args.get('id')
    scrapy_process = subprocess.Popen('scrapy crawl douyin -a douyinId={}'.format(user_id))
    if(scrapy_process.poll()):
        # TODO:打印JSON格式文件数据并且显示在界面上
        pass
    else:
        # TODO://返回错误信息
        pass
    return redirect('/douyin')

# 前端抖音界面显示
@app.route('/douyin')
def douyin():
    return render_template('DouYin.html')

# 前端TikTok界面显示
@app.route('/tiktok')
def tiktok():
    return render_template('TikTok.html')

# 联系我们
@app.route('/contact')
def contact():
    return render_template('contact.html')

# 关于我们
@app.route('/about')
def about():
    return render_template('about.html')







