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
    def __init__(self, mkdir=True):
        self.tmp_dir, self.images_dir = self.init_dir(mkdir)

    def init_dir(self, mkdir):
        base_dir = os.path.dirname(sys.argv[0])
        tmp_dir = os.path.join(base_dir, 'tmp')
        images_dir = os.path.join(tmp_dir, 'images')
        if mkdir:
            if os.path.isdir(images_dir):
                shutil.rmtree(tmp_dir)
            os.makedirs(images_dir)
        return tmp_dir, images_dir

    def download(self, urls):
        for i in range(len(urls)):
            r = requests.get(urls[i], stream=True)
            if r.status_code == 200:
                filename = '{}.jpg'.format(i)
                save_path = os.path.join(self.images_dir, filename)
                with open(save_path, 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)

    def get_files_path(self):
        files = [(x[0], x[2]) for x in os.walk(self.images_dir)]
        paths = filter(lambda filename: filename not in ['.DS_Store'], files[0][1])
        paths = list(paths)
        paths.sort(key=lambda filename: int(filename.split('.')[0]))
        return paths

    def upload(self, ):
        endpoint = 'oss-cn-chengdu.aliyuncs.com'
        bucket_name = 'my-blog-media'
        auth = oss2.Auth(os.environ.get('ALIYUN_ACCESS_KEY_ID'), os.environ.get('ALIYUN_ACCESS_KEY_SECRET'))
        bucket = oss2.Bucket(auth, endpoint, bucket_name)
        uploads = []
        for filename in self.get_files_path():
            filepath = os.path.join(self.images_dir, filename)
            oss_filename = '{}-{}.jpg'.format('hello-kubernetes-20190404', time.time())
            result = bucket.put_object_from_file(oss_filename, filepath)
            if result.status == 200:
                url = 'https://{}.{}/{}'.format(bucket_name, endpoint, oss_filename)
                markdown_url = '![]({})'.format(url)
                uploads.append(markdown_url)

        images_url_file_path = os.path.join(self.tmp_dir, 'images_url.txt')
        if not os.path.exists(images_url_file_path):
            os.system('touch {}'.format(images_url_file_path))
        with open(images_url_file_path, 'w') as f:
            f.write('\n\n'.join(uploads))


if __name__ == '__main__':
    script = Script(mkdir=False)
    path = '/Users/yetongxue/python/myblog/_posts/2017-08-19-hello-docker.md'
    download_urls = []
    with open(path, 'r') as f:
        for line in f.readlines():
            if line.startswith('![](http://upload-images.jianshu.io/upload_images'):
                download_urls.append(line[4: -2])
    # script.download(download_urls)
    script.upload()

