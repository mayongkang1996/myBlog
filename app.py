from flask import Flask
from flask import render_template
from flask import redirect
from flask import request
from peewee import *
# 有用，别删了
import psycopg2

from flask_wtf import FlaskForm
# from flask_bootstrap import Bootstrap


app = Flask(__name__)

# 连接数据库
pg_db = PostgresqlDatabase('postgres',#数据库
                           user='postgres', #用户
                           password=123456, # 密码
                           host='127.0.0.1', # 主机地址
                           port=5432) #端口号


class BaseModel(Model):
    class Meta:
        database = pg_db


class Artical(BaseModel):
    id = IntegerField()
    title = CharField()
    content = CharField()
    tags = CharField()
    date = DateTimeField()


@app.route('/')
def index():
    return render_template("home/index.html")


@app.route('/list')
def hello_world():
    return render_template('home/list.html')


@app.route('/admin')
def select():
    data = Artical.select()
    return render_template('admin/index.html', data=data)


@app.route('/admin/add')
def add():
        return render_template('admin/add.html')


@app.route('/admin/save', methods=['POST'])
def save():
    title = request.form.get('title')
    content = request.form.get('content')
    tags = request.form.get("tags")
    date = request.form.get('date')
    status = Artical.insert(title=title, content=content, tags=tags)
    if status:
        return redirect("admin")
    else:
        return redirect("admin/index")


# 删除
@app.route('/del/<id>')
def dels(id):
    res = Artical.select().where(Artical.id ==id).get().delete_instance()
    if res:
        return redirect('/admin')
    else:
        return redirect('/admin')


# # 自定义错误页面
# @app.errorhandler(404)
# def page_not_found(e):
#     return render_template('error/404.html')
#
# # 500错误
# @app.errorhandler(500)
# def internal_server_error(e):
#     return render_template('error/500.html')


if __name__ == '__main__':
    app.run()
