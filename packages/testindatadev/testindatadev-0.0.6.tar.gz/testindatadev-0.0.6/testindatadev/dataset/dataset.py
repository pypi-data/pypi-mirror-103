import sys
import os

sys.path.append(os.path.dirname(__file__) + os.sep + '../')

from s3.minio.minio import YcMinio
from s3.qiniu.qiniu import Qiniu
from dataset.request import Request

# 本类用来屏蔽各种存储对象(oss, minio, 七牛)之间的差异，通过type构造不同的客户端解决问题，类似工厂类
# 各个OSS均需要实现本类中的所有方法
class Dataset():
    def __init__(self, T_key, datasetName, ip):
        self.OSS_TYPE_DEFAULT = 0
        self.OSS_TYPE_MINIO = 0
        self.OSS_TYPE_ALI = 1
        self.OSS_TYPE_AWS = 2
        self.OSS_TYPE_QINIU = 3

        self.DATASET_TYPE_IMAGE = 0
        self.DATASET_TYPE_VIDEO = 1
        self.DATASET_TYPE_AUDIO = 2
        self.DATASET_TYPE_POINT_CLOUD = 3
        self.DATASET_TYPE_FUSION_POINT_CLOUD = 4
        self.DATASET_TYPE_POINT_CLOUD_SEMANTIC_SEGMENTATION = 5
        self.DATASET_TYPE_TEXT = 6

        self.req = Request(T_key, datasetName, ip)
        info = self.req.GetAccess()
        self.access_key = info['access_key']
        self.secret_key = info['secret_key']
        self.upload_token = info['upload_token']
        self.endpoint = info['endpoint']
        self.bucket = info['bucket']
        self.file_path = info["file_path"]
        self.oss_type = info['oss_type']
        self.datasetName = datasetName
        self.datasetType = info["dataset_type"]
        self.ip = ip
        if self.oss_type == self.OSS_TYPE_MINIO or \
            self.oss_type == self.OSS_TYPE_DEFAULT or \
            self.oss_type == self.OSS_TYPE_AWS:
            self.client = YcMinio(self.access_key, self.secret_key, self.endpoint)
            if self.bucket not in self.client.ListAllBucket():
                raise Exception(f"bucket:{self.bucket} is not exist!")
        elif self.oss_type == self.OSS_TYPE_QINIU:
            self.client = Qiniu(self.upload_token)
        else:
            raise Exception("尚未支持其他类型的云存储")

    
    def PutFileToDataset(self, objectName, filePath):
        self.client.PutObject(self.bucket, self.file_path + "/" + self.datasetName + "/" + objectName, filePath)

    def SyncDataToWeb(self, data):
        info = self.req.Upload(data)
        return info

    def GetData(self, offset, limit, metaKey="", metaValue="", label="", sensor=""):
        if metaKey == "" or metaValue == "":
            metaKey=""
            metaValue=""

        info = self.req.GetData(offset, limit, metaKey, metaValue, label, sensor)
        for item in info["files"]:
            if self.oss_type == self.OSS_TYPE_MINIO:
                item['url'] = "http://" + self.ip + item["url"]

        return info

    def GetFileAndLabelByFid(self, fid):
        info = self.req.GetFileAndLabelByFid(fid)
        return info

    def GetFileAndLabelByReferid(self, referId):
        info = self.req.GetFileAndLabelByReferid(referId)
        return info

