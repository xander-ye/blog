#!/usr/bin/env python
# -*- coding: utf-8 -*-
# scirpt.py in blog
# Created by yetongxue at 2019-07-19

import requests
import shutil
import oss2
import os
import sys


def download():
    path = '/Users/yetongxue/python/myblog/_posts/2016-12-31-collect-pic.md'
    with open(path, 'r') as f:
        i = 0
        for line in f.readlines():
            if line.startswith('![](http://upload-images.jianshu.io/upload_images/'):
                url = line[4: -2]
                r = requests.get(url, stream=True)
                if r.status_code == 200:
                    save_path = '/Users/yetongxue/Downloads/collect/20190719-收集散落的照片-{}.jpg'.format(i)
                    with open(save_path, 'wb') as f:
                        r.raw.decode_content = True
                        shutil.copyfileobj(r.raw, f)
                        i += 1


def upload():
    basedir = os.path.dirname(sys.argv[0])
    tmp = os.path.join(basedir, 'tmp')
    if not os.path.isdir(tmp):
        os.makedirs(tmp)

    # https://github.com/aliyun/aliyun-oss-python-sdk
    endpoint = 'oss-cn-chengdu.aliyuncs.com'
    auth = oss2.Auth(os.environ.get('ALIYUN_ACCESS_KEY_ID'), os.environ.get('ALIYUN_ACCESS_KEY_SECRET'))
    bucket = oss2.Bucket(auth, endpoint, 'my-blog-media')
    save_path = '/Users/yetongxue/Downloads/collect/20190719-收集散落的照片-{}.jpg'.format(2)
    result = bucket.put_object_from_file('20190719-收集散落的照片-0.jpg', save_path)
    if result.status == 200:
        pass




if __name__ == '__main__':
    # download()
    upload()
