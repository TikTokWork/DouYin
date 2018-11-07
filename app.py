from flask import Flask, flash, redirect, url_for, render_template, request, jsonify
from flask_pymongo import PyMongo
import subprocess

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
        subprocess.call('scrapy crawl douyin -a douyinId={}'.format(user_id))
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
    id = ''
    nickname = ''
    author_desc = ''
    user_art = ''
    aweme_list = []
    for compose in compose_list:
        id = compose.get('id')
        nickname = compose.get('nickname')
        author_desc = compose.get('author_desc')
        description = compose.get('description')
        user_art = compose.get('user_art')
        url = compose.get('play_addr')
        small_data = {
            'description': description,
            'url': url
        }
        small_data_add = small_data.copy()
        aweme_list.append(dict(small_data_add))

    data = {
        'id': id,
        'douyin_id': douyin_id,
        'author_desc':author_desc,
        'nickname': nickname,
        'aweme_list': aweme_list,
        'user_art': user_art,
    }

    return dict(data)




