#!/usr/bin/env python
# -*- coding: utf-8 -*-
# scirpt.py in blog
# Created by yetongxue at 2019-07-19

import requests
import shutil
import oss2
import os
import sys
import time


class Script(object):
    def __init__(self):
        self.basedir, self.filedir = self.init_dir()

    def init_dir(self):
        basedir = os.path.dirname(sys.argv[0])
        tmpdir = os.path.join(basedir, 'tmp')
        if not os.path.isdir(tmpdir):
            os.makedirs(tmpdir)
        filedir = os.path.join(tmpdir, 'filedir')
        if not os.path.isdir(filedir):
            os.makedirs(filedir)
        return tmpdir, filedir

    def download(self):
        path = '/Users/yetongxue/python/myblog/_posts/2016-12-31-collect-pic.md'
        with open(path, 'r') as f:
            i = 0
            for line in f.readlines():
                if line.startswith('![](http://upload-images.jianshu.io/upload_images/'):
                    url = line[4: -2]
                    r = requests.get(url, stream=True)
                    if r.status_code == 200:
                        filename = 'photo-collecting-{}.jpg'.format(i)
                        save_path = os.path.join(self.filedir, filename)
                        with open(save_path, 'wb') as f:
                            r.raw.decode_content = True
                            shutil.copyfileobj(r.raw, f)
                            i += 1

    def get_files(self):
        files = [(x[0], x[2]) for x in os.walk(self.filedir)]
        return files[0][1]

    def upload(self):
        endpoint = 'oss-cn-chengdu.aliyuncs.com'
        bucket_name = 'my-blog-media'
        auth = oss2.Auth(os.environ.get('ALIYUN_ACCESS_KEY_ID'), os.environ.get('ALIYUN_ACCESS_KEY_SECRET'))
        bucket = oss2.Bucket(auth, endpoint, bucket_name)
        uploads = []
        for i in range(87):
            filename = 'photo-collecting-{}.jpg'.format(i)
            filepath = os.path.join(self.filedir, filename)
            oss_filename = '{}-{}'.format(time.time(), filename)
            result = bucket.put_object_from_file(oss_filename, filepath)
            if result.status == 200:
                url = 'https://{}.{}/{}'.format(bucket_name, endpoint, oss_filename)
                markdown_url = '![]({})'.format(url)
                uploads.append(markdown_url)

        upload_file = os.path.join(self.basedir, 'filename.txt')
        if not os.path.exists(upload_file):
            os.system('touch {}'.format(upload_file))
        with open(upload_file, 'w') as f:
            f.write('\n'.join(uploads))


if __name__ == '__main__':
    script = Script()
    # script.download()
    script.upload()
