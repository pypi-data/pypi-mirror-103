from aiohttp import ClientSession
from bunch import Bunch
from qiniu import PersistentFop, put_file, put_data, BucketManager, Auth


class ClientConf(Bunch):
    access: str
    secret: str


class QBox:
    """七牛上传"""
    def __init__(self, qbox_config: dict = None):
        self.config = qbox_config
        self.qiniu_auth = Auth(qbox_config.get('access_key'), qbox_config.get('secret_key'))
        self.bucket = BucketManager(self.qiniu_auth)
        self.return_body = """
                {
                    "key": $(key),
                    "size": $(fsize),
                    "type": $(mimeType),
                    "hash": $(etag),
                    "width": $(imageInfo.width),
                    "height": $(imageInfo.height),
                    "orientation": $(imageInfo.Orientation.val),
                    "color": $(exif.ColorSpace.val),
                    "videoDuration": $(avinfo.video.duration),
                    "videoWidth": $(avinfo.video.width),
                    "videoHeight": $(avinfo.video.height),
                    "videoRotate": $(avinfo.video.tags.rotate)
                }
                """

    def qiniu_sign(self, name, return_url=None, return_body=None, save_key='$(etag)', prefix='', expires=3600, host='',
                   is_video=False):
        """
        获取令牌
        :param name:
        :param return_url:
        :param return_body:
        :param save_key:
        :param prefix:
        :param expires:
        :param host:
        :param is_video:
        :return:
        """
        bucket_name = name
        if return_url and return_url.startswith("//"):
            return_url = "http:%s" % return_url

        url = ''
        original_url = ''
        if host:
            url = f'{host}/$(key)?vframe/jpg/offset/1/w/660/h/660' if is_video else f'{host}/$(key)~500x.webp' # f'{host}/$(key)?imageView2/1/w/660/h/660'
            original_url = f'{host}/$(key)'

        if not return_body:
            return_body = '{"key": $(key), "size": $(fsize), "type": $(mimeType), "hash": $(etag), "width": $(imageInfo.width), "height": $(imageInfo.height), "orientation": $(imageInfo.Orientation.val), "color": $(exif.ColorSpace.val), "videoDuration": $(avinfo.video.duration), "videoWidth": $(avinfo.video.width), "videoHeight": $(avinfo.video.height), "videoRotate": $(avinfo.video.tags.rotate), "url": "'+url+'", "originalUrl": "'+original_url+'"}'

        if prefix:
            save_key = '%s%s' % (prefix, save_key)

        up_token = self.qiniu_auth.upload_token(bucket_name, policy={'returnBody': return_body, 'returnUrl': return_url,
                                                                     'saveKey': save_key}, expires=expires)
        return bucket_name, up_token

    def qiniu_upload(self, bucket_name, key, file_data, return_all=False):
        """
        文件上传
        :param bucket_name:
        :param key:
        :param file_data:
        :return:
        """
        up_token = self.qiniu_auth.upload_token(bucket_name, key, policy={'returnBody': self.return_body})
        ret, info = put_data(up_token, key, file_data)
        if return_all:
            return ret, info
        return ret

    def qiniu_delete(self, bucket_name, key):
        """
        删除文件
        :param bucket_name:
        :param key:
        :return:
        """
        ret, info = self.bucket.delete(bucket_name, key)
        return ret

    def qiniu_fetch(self, url, bucket_name, key):
        """
        获取文件
        :param url:
        :param bucket_name:
        :param key:
        :return:
        """
        ret, info = self.bucket.fetch(url, bucket_name, key)
        return ret

    def qiniu_stat(self, bucket_name, key):
        """
        获取文件
        :param bucket_name:
        :param key:
        :return:
        """
        ret, info = self.bucket.stat(bucket_name, key)
        return ret

    def qiniu_copy(self, res_bucket, key, bucket_to, key_to):
        """
        复制文件
        :param res_bucket:
        :param key:
        :param bucket_to:
        :param key_to:
        :return:
        """
        return self.bucket.copy(res_bucket, key, bucket_to, key_to)

    def qiniu_rename(self, bucket, key, key_to, force='false'):
        """
        重命名文件
        :param bucket:
        :param key:
        :param key_to:
        :param force:
        :return:
        """
        return self.bucket.rename(bucket, key, key_to, force=force)

    def qiniu_pfop(self, key, bucket, persistentOps, pipeline=''):
        """"""
        pfop = PersistentFop(self.qiniu_auth, bucket, pipeline=pipeline)
        return pfop.execute(key, persistentOps, 1)

    def qiniu_upload_file(self, token, key, file_path):
        """"""
        return put_file(token, key, file_path)

    @classmethod
    async def qiniu_image_info(cls, url):
        """
        获取图片信息
        """
        need_url = f"{url}?imageInfo"
        try:
            async with ClientSession() as session:
                async with session.get(need_url) as response:
                    data = await response.json()
        except Exception as e:
            data = {}
        return data
