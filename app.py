#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import tornado.ioloop
import tornado.web
import os
import uuid
import time
import sqlite3

import time
import datetime


conn = sqlite3.connect('data.db')


def date_format(time):
    return datetime.datetime.fromtimestamp(time).strftime("%Y-%m-%d %H:%M:%S")


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')


class SearchFileHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('''
<!DOCTYPE html>
<html lang="zh-CN">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- 上述3个meta标签*必须*放在最前面，任何其他内容都*必须*跟随其后！ -->
    <title>Bootstrap</title>

    <link href="/static/bootstrap/css/bootstrap.min.css" rel="stylesheet">

  </head>
  <body>
        <ol class="breadcrumb">
        <li><a href="/">Home</a></li>
        <li class="active">search</li>
        </ol>
        <form action='search' method='post'>
        <div class="row">
            <div class="col-sm-4"></div>
            <div class="col-sm-4">
                <div class="input-group">
                <input type="text" name="search_text" class="form-control" placeholder="Search for...">
                <span class="input-group-btn">
                <button class="btn btn-primary" type="submit">搜索</button>
                </span>
                </div><!-- /input-group -->
            </div>
            <div class="col-sm-4"></div>
        </div>
         </form>
          <script src="//cdn.bootcss.com/jquery/1.11.3/jquery.min.js"></script>
    <script src="/static/bootstrap/js/bootstrap.min.js"></script>
  </body>
</html>
        ''')

    def post(self):
        self.write('''
<!DOCTYPE html>
<html lang="zh-CN">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- 上述3个meta标签*必须*放在最前面，任何其他内容都*必须*跟随其后！ -->
    <title>Bootstrap</title>

    <link href="/static/bootstrap/css/bootstrap.min.css" rel="stylesheet">

  </head>
  <body>
  <ol class="breadcrumb">
        <li><a href="/">Home</a></li>
        <li class="active">result</li>
        </ol>''')
        search_text = self.get_argument("search_text")
        sql = "select timestamp,text,filename from data where text like '%%%s%%'" % (search_text)
        cursor = conn.execute(sql)
        self.write("""<table class="table table-hover">""")
        self.write("""<tr>""")
        for row in cursor:
            self.write("timestamp:%s" % (date_format(row[0])))
            self.write("<br>")
            self.write("info:%s" % (row[1]))
            self.write("<br>")
            self.write('<img src="/static/%s" class="img-responsive img-rounded">' % (row[2]))
            self.write("<br>")
        self.write("""</tr>""")
        self.write("""</table>""")
        self.write('''
        <script src="//cdn.bootcss.com/jquery/1.11.3/jquery.min.js"></script>
    <script src="/static/bootstrap/js/bootstrap.min.js"></script>
  </body>
</html>
        ''')


class UploadFileHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('''
        <!DOCTYPE html>
<html lang="zh-CN">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- 上述3个meta标签*必须*放在最前面，任何其他内容都*必须*跟随其后！ -->
    <title>Bootstrap</title>

    <link href="/static/bootstrap/css/bootstrap.min.css" rel="stylesheet">

  </head>
  <body>
  <ol class="breadcrumb">
        <li><a href="/">Home</a></li>
        <li class="active">upload</li>
        </ol>
        <div class="row">
        <div class="col-sm-4"></div>
        <div class="col-sm-4">
            <form action='upload' enctype="multipart/form-data" method='post'>
            <input type='file' name='file'/><br/>
            <textarea rows="4" cols="50" name="comment" placeholder="请在此处输入文本..."></textarea>
            <br>
            <button type='submit' class='btn btn-primary'>上传</button>
            </form>
        </div>
        <div class="col-sm-4"></div>
        </div>
          <script src="//cdn.bootcss.com/jquery/1.11.3/jquery.min.js"></script>
    <script src="/static/bootstrap/js/bootstrap.min.js"></script>
  </body>
</html>
        ''')

    def post(self):
        # 文件的暂存路径
        upload_path = os.path.join(os.path.dirname(__file__), 'data')
        file_count = 0
        file_list = []
        if 'file' not in self.request.files:
            self.write('{"status":400, "message":"未上传任何图片"}')
            return
        # 提取表单中‘name’为‘file’的文件元数据
        file_metas = self.request.files['file']
        comment = self.get_argument("comment")
        for meta in file_metas:
            file_count = file_count + 1
            filename = str(uuid.uuid4()) + "_" + meta['filename']
            file_list.append(filename)
            filepath = os.path.join(upload_path, filename)
            # 有些文件需要已二进制的形式存储，实际中可以更改
            with open(filepath, 'wb') as up:
                up.write(meta['body'])
            sql = ("INSERT INTO data (timestamp,text,filename) VALUES (%s, '%s', '%s')"
                % (int(time.time()), comment, filename))
            print sql
            conn.execute(sql)
            conn.commit()
        self.write('{"status":200, "message":"ok", "result":%s}' % (file_list))
        self.redirect('/', permanent=True)


app = tornado.web.Application([
    (r'/', IndexHandler),
    (r'/upload', UploadFileHandler),
    (r'/search', SearchFileHandler),
], static_path=os.path.join(os.path.dirname(__file__), "data"))


if __name__ == '__main__':
    app.listen(3000)
    tornado.ioloop.IOLoop.instance().start()
    conn.close()
