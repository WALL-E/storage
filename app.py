#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import tornado.ioloop
import tornado.web
import os
import uuid


class UploadFileHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('''
        <html>
          <head><title>Upload File</title></head>
          <body>
            <form action='upload' enctype="multipart/form-data" method='post'>
            <input type='file' name='file'/><br/>
            <input type='file' name='file'/><br/>
            <input type='file' name='file'/><br/>
            <input type='submit' value='上传'/>
            </form>
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
        for meta in file_metas:
            file_count = file_count + 1
            filename = str(uuid.uuid4()) + "_" + meta['filename']
            file_list.append(filename)
            filepath = os.path.join(upload_path, filename)
            # 有些文件需要已二进制的形式存储，实际中可以更改
            with open(filepath, 'wb') as up:
                up.write(meta['body'])
        self.write('{"status":200, "message":"ok", "result":%s}' % (file_list))


app = tornado.web.Application([
    (r'/upload', UploadFileHandler),
])


if __name__ == '__main__':
    app.listen(3000)
    tornado.ioloop.IOLoop.instance().start()
