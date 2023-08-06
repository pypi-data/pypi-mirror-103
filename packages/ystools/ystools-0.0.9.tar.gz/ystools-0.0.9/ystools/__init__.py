import requests
import hashlib
import time
import json
import os
from PIL import Image, ImageFont, ImageDraw, ExifTags
from qiniu import Auth, put_file, etag
import multiprocessing
from concurrent.futures import ProcessPoolExecutor
import cv2
import numpy as np

# import open3d as o3d
# import numpy as np
# import pylas


class Task:
    """接口获取数据
    STATUS_WAITING = 0; // 待处理
    STATUS_WORKING = 1; // 进行中
    STATUS_CHECK_WAIT = 2; // 待审核
    STATUS_INSPECTOR_WAIT = 3; // 待质检
    STATUS_PASS = 4; // 已通过
    STATUS_REFUSED = 5; // 已驳回
    STATUS_REFUSED = 6; // 客户通过
    """

    def __init__(self, token_ak, token_sk):
        self.__TOKEN_URL = 'http://label-export.testin.cn/develope/passport/get-token'
        self.__TASK_URL = 'http://label-export.testin.cn/develope/task/get-label-data'
        if not (token_ak and token_sk):
            raise ValueError('Invalid key')
        self.__TOKEN_AK = token_ak
        self.__TOKEN_SK = token_sk
        # self.__TOKEN_AK = 'ae1bdbc2d15e4fb4779558f75de21c95'
        # self.__TOKEN_SK = '29de907568f60c9a452f24ef1e0a03b0'

    def __getToken(self):
        data = {
            'access_key': self.__TOKEN_AK,
            'secret_key': self.__TOKEN_SK
        }
        response = requests.post(self.__TOKEN_URL, json=data)
        res = response.json()
        return res['data']['access_token']

    def __getTaskInfo(self, key, status, statuss, has_unable):
        page = 1
        taskList = []
        res = {}
        token = self.__getToken()
        while status in statuss:
            times = str(int(time.time()))
            data = {
                "task_key": key,
                "page": page,
                "page_num": 20,
                "has_unable": has_unable,
            }
            _sign = '&'.join([f'{k}={v}' for k, v in sorted(data.items(), key=lambda d: d[0])])
            s = token + _sign + times
            sign = hashlib.md5(s.encode('utf8')).hexdigest()
            data.update({"sign": sign, "access_token": token, "time": times, "status": status})
            page += 1
            r = requests.post(self.__TASK_URL, json=data, headers={'Content-Type': 'application/json'})
            res = r.json()
            if not res['data'] or not res['data']['taskList']:
                log_info = r.json()
                log_info['key'] = key
                log_info['status'] = status
                status += 1
                page = 1
                continue
            taskList += res['data']['taskList']
        if res: res['data']['taskList'] = taskList
        return res

    def getAllTaskInfo(self, keys, json_path, has_unable=0, status=2, statuss=[2, 3, 4]):
        task_all_info = {key: self.__getTaskInfo(key, status, statuss, has_unable) for key in keys if key}
        with open(json_path, 'w') as f:
            f.write(json.dumps(task_all_info))


class DrawPic:
    """画图"""

    def __init__(self, im):
        self._im = im
        self._draw = ImageDraw.Draw(self._im)

    def save_img(self, out_path, file_name):
        """保存图片"""
        if not os.path.exists(out_path):
            os.makedirs(out_path)
        self._im.save(os.path.join(out_path, file_name))

    def get_im(self):
        """获取内存中的图片"""
        return self._im

    def rotate(self):
        """旋转图片"""
        if self._im.mode == 'P':
            self._im = self._im.convert('RGB')
        try:
            for orientation in ExifTags.TAGS.keys():
                if ExifTags.TAGS[orientation] == 'Orientation': break
            exif = dict(self._im._getexif().items())
            if exif[orientation] == 3:
                self._im = self._im.rotate(180, expand=True)
            elif exif[orientation] == 6:
                self._im = self._im.rotate(270, expand=True)
            elif exif[orientation] == 8:
                self._im = self._im.rotate(90, expand=True)
        except:
            pass

    def img_cuboid(self, mark, color=None, width=None):
        """日形框标注框"""
        point1 = mark['finshPoints'][0]
        point2 = mark['finshPoints'][1]
        x1 = [point1['x'], point2['x']]
        y1 = [point1['y'], point2['y']]
        point3 = mark['finshPoints'][2]
        point4 = mark['finshPoints'][3]
        x2 = [point3['x'], point4['x']]
        y2 = [point3['y'], point4['y']]
        p1 = [min(x1), min(y1)]
        p2 = [min(x1), max(y1)]
        p3 = [max(x1), min(y1)]
        p4 = [max(x1), max(y1)]
        p5 = [min(x2), min(y2)]
        p6 = [min(x2), max(y2)]
        self._draw.rectangle(p1 + p4, outline=color, width=width)
        if min(x1) < min(x2):
            self._draw.line(p3 + p5, fill=color, width=width)
            self._draw.line(p5 + p6, fill=color, width=width)
            self._draw.line(p4 + p6, fill=color, width=width)
        else:
            self._draw.line(p1 + p5, fill=color, width=width)
            self._draw.line(p6 + p5, fill=color, width=width)
            self._draw.line(p6 + p2, fill=color, width=width)

    def img_rect(self, mark, color=None, outline=None, width=1):
        """矩形标注框"""
        self._draw.rectangle(
            [mark['point']['left'], mark['point']['top'], mark['point']['right'], mark['point']['bottom']],
            outline=outline, width=width, fill=color)

    def img_curve(self, mark, color=None, width=None):
        """曲线标注框"""
        for index, po in enumerate(mark['point']):
            p1 = [po['x'], po['y']]
            if index + 1 != len(mark['point']):
                p2 = [mark['point'][index + 1]['x'], mark['point'][index + 1]['y']]
                self._draw.line(p1 + p2, fill=color, width=width)

    def img_polygon(self, mark, fill_color=None, outline=None):
        """多边形标注框"""
        p = []
        for po in mark['point']:
            if po['x'] is None or po['y'] is None:
                continue
            p.append(po['x'])
            p.append(po['y'])
        self._draw.polygon(p, fill=fill_color, outline=outline)

    def img_point(self, mark, color=None, radius=None):
        """点标注"""
        self._draw.ellipse(
            (float(mark['point']['x']) - radius, float(mark['point']['y']) - radius, float(mark['point']['x']) + radius,
             float(mark['point']['y']) + radius), color)

    def img_ellipse(self, mark, color=None, outline_color=None):
        """圆形标注"""
        self._draw.ellipse(
            (mark['point']['left'], mark['point']['top'], mark['point']['right'], mark['point']['bottom']),
            fill=color, outline=outline_color)

    def do_mosaic(self, x, y, w, h, neighbor=5):
        """
        马赛克的实现原理是把图像上某个像素点一定范围邻域内的所有点用邻域内左上像素点的颜色代替，这样可以模糊细节，但是可以保留大体的轮廓。
        :param frame: opencv frame
        :param int x :  马赛克左顶点x值
        :param int y:  马赛克左顶点y值
        :param int w:  马赛克宽
        :param int h:  马赛克高
        :param int neighbor:  马赛克每一块的宽
        """
        frame = cv2.cvtColor(np.asarray(self._im), cv2.COLOR_RGB2BGR)
        neighbor = w // 10
        fh, fw = frame.shape[0], frame.shape[1]
        if (y + h > fh) or (x + w > fw):
            return
        for i in range(0, h - neighbor, neighbor):  # 关键点0 减去neightbour 防止溢出
            for j in range(0, w - neighbor, neighbor):
                rect = [j + x, i + y, neighbor, neighbor]
                color = frame[i + y][j + x].tolist()  # 关键点1 tolist
                left_up = (rect[0], rect[1])
                right_down = (rect[0] + neighbor - 1, rect[1] + neighbor - 1)  # 关键点2 减去一个像素
                cv2.rectangle(frame, left_up, right_down, color, -1)
        self._im = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))


class Executor:
    """多进程"""

    def __init__(self, thread_nums=multiprocessing.cpu_count() * 2):
        self._executor = ProcessPoolExecutor(max_workers=thread_nums)

    def execute(self, func, *arg):
        return self._executor.submit(func, *arg[0])


class QniuApi:
    """七牛API"""

    def __init__(self, conf):
        self.__conf = conf

    def download(self, key, dist, bucket=None):
        '''下载文件'''
        if bucket is None:
            bucket = self.__conf
        url = self.from_qiniu_get_url(bucket['AK'], bucket['SK'], bucket['BUCKET_DOMAIN'], key)
        if bucket['INTRANET']:
            url = url.replace(bucket['BUCKET_DOMAIN'], bucket['INTRANET_DOMAIN'])
        headers = {"Host": bucket['BUCKET_DOMAIN']}
        response_data_file = requests.get(url, stream=True, headers=headers)
        assert response_data_file.status_code == 200
        with open(dist, 'wb') as f:
            for chunk in response_data_file.iter_content(chunk_size=1024 * 4):
                if chunk:
                    f.write(chunk)
        return dist

    def from_qiniu_get_url(self, ak, sk, domain, key):
        '''生成私有下载链接'''
        q = Auth(ak, sk)
        base_url = 'http://%s/%s' % (domain, key)
        return q.private_download_url(base_url, expires=3600)

    def upload_file(self, local_file, save_name, conf=None):
        '''上传七牛云'''
        if conf is None:
            conf = self.__conf
        q = Auth(conf['AK'], conf['SK'])
        token = q.upload_token(conf['BUCKET_NAME'], save_name, 3600)
        ret, info = put_file(token, save_name, local_file)
        assert ret['key'] == save_name
        assert ret['hash'] == etag(local_file)
        return save_name


class Tools:
    """工具"""

    def getAttr(self, propArr, tmp, pcode):
        for pro in propArr:
            if pro['prevcode'] == pcode:
                tmp.append({'pname': pro['pname'], 'ptitle': pro['ptitle']})
                if pro['pcode'] != pro['prevcode']:
                    self.getAttr(propArr, tmp, pro['pcode'])

    def getExtraValue(self, propArr, pcode):
        data = {}
        for pro in propArr:
            if pro['prevcode'] == pcode or not pro['prevcode']:
                data[pro['pname']] = pro['pcode']
        for k, v in data.items():
            tmp = []
            self.getAttr(propArr, tmp, v)
            data[k] = tmp
        return data


# class PointCloud:
#     """点云处理"""
#
#     def format_change(self, file, out_path, target_ext):
#         """格式转换"""
#
#         if file.endswith('bin'):
#             data = np.fromfile(file, dtype=np.float32)
#             # format:
#             point_cloud_with_normal = np.reshape(data, (data.shape[0] // 4, 4))
#             pcd = o3d.geometry.PointCloud()
#             pcd.points = o3d.utility.Vector3dVector(point_cloud_with_normal[:, 0:3])
#         elif file.endswith(('pcd', 'ply')):
#             pcd = o3d.io.read_point_cloud(file)
#         elif file.endswith('txt'):
#             pcd = np.loadtxt(file, dtype=np.float32, delimiter=',')
#         elif file.endswith('las'):
#             pcd = pylas.read('filename.las')
#             print(1)
