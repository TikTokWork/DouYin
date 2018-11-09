from flask import Flask, flash, redirect, url_for, render_template, request, jsonify, send_from_directory, make_response
from flask_pymongo import PyMongo
import subprocess
import os, zipfile

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/TikTok'
mongo = PyMongo(app)

# 前端首页显示
@app.route('/', methods=["GET", "POST"])
def index():
    return render_template('index.html')

# 前后端通信API接口
@app.route('/api/douyin', methods=["GET"])
def start_douyin_spider():
    user_id = request.args.get('id')
    author_info = mongo.db.douyin.find({'douyin_id': user_id})
    if(author_info.count() != 0):
        return jsonify({
            'status_code': 200,
            'user_info': generate_douyin_response(user_id)
        })
    else:
        scrapy_process = subprocess.Popen('scrapy crawl douyin -a douyinId={}'.format(user_id))
        if(scrapy_process.wait() == 0):
            file_path = os.path.join('D:\\program\\Scrapy\\DouYin\\video', user_id)
            make_zipfile(file_path)
            return jsonify({
                'status_code': 200,
                'user_info': generate_douyin_response(user_id)
            })

# 前端抖音界面显示
@app.route('/douyin')
def douyin():
    return render_template('DouYin.html')

# 前端TikTok界面显示
@app.route('/tiktok')
def tiktok():
    return render_template('TikTok.html')

# 下载view
@app.route('/download/<path:user_id>/<path:file_name>')
def downloader(user_id, file_name):
    dirpath = os.path.join('D:\\program\\Scrapy\\DouYin\\video', user_id)
    response = make_response(send_from_directory(dirpath, file_name, as_attachment=True))
    response.headers["Content-Disposition"] = "attachment; filename={}".format(file_name.encode().decode('latin-1'))
    return response

# 联系我们
@app.route('/contact')
def contact():
    return render_template('contact.html')

# 关于我们
@app.route('/about')
def about():
    return render_template('about.html')


# 从数据库生成JSON格式响应包
def generate_douyin_response(user_id):
    compose_list = mongo.db.douyin.find({'douyin_id': user_id})
    douyin_id = user_id
    nickname = ''
    author_desc = ''
    user_art = ''
    aweme_list = []
    for compose in compose_list:
        aweme_id = compose.get('aweme_id')
        nickname = compose.get('nickname')
        author_desc = compose.get('author_desc')
        description = compose.get('description')
        user_art = compose.get('user_art')

        data = {
            'aweme_id': aweme_id,
            'description': description
        }

        data_copy = data.copy()
        aweme_list.append(dict(data_copy))

    data = {
        'douyin_id': douyin_id,
        'author_desc':author_desc,
        'nickname': nickname,
        'aweme_list': aweme_list,
        'user_art': user_art,
    }

    return dict(data)

# 将生成的视频文件夹打包
def make_zipfile(source_dir):
    zip_file_name = source_dir + '.zip'
    z = zipfile.ZipFile(zip_file_name, 'w', zipfile.ZIP_DEFLATED)
    for dirpath, dirnames, filenames in os.walk(source_dir):
        fpath = dirpath.replace(source_dir, '')
        fpath = fpath and fpath + os.sep or ''
        for filename in filenames:
            z.write(os.path.join(dirpath, filename), fpath + filename)
            print(filename + '已压缩入：' + zip_file_name)
    print(source_dir + '压缩成功')
    z.close()


