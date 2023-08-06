import os
import sys
import json
import re

sys.path.append(os.path.dirname(__file__) + os.sep + './')

from dataset.dataset import Dataset
from dataset.file import File
from utils import util
from dataset.localdb import LocalDb

#sdk入口
class TDA():
    def __init__(self, T_key, debug=False):
        self.T_key = T_key
        self.commitFlag = False
        self.commitId = ""
        self.datasetName = ""
        self.fileList = []
        self.debug = debug

    def Debug(self):
        """
        set sdk to debug mod
        """
        self.debug = True

    def SetDataset(self, datasetName, ip):
        """
        Set the dataset to be processed
        datasetName: the name of the dataset
        ip: the ip address to the testin-dataset service, default is pubulic network service.
        """
        result = re.findall(r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b",ip)
        if result:
            self.ip = result[0]
        else:
            raise Exception("ip is invalid")

        self.datasetName = datasetName
        self.dataset = Dataset(self.T_key, datasetName, self.ip)
        self.filePrefix = self.datasetName
        if self.dataset.file_path != "":
            self.filePrefix = self.dataset.file_path.strip("/") + "/" + self.datasetName.strip("/")

    def RiseException(self):
        raise Exception("You have not set the dataset name yet!")

    def UploadFilesToDataset(self, rootPath, ext=""):
        """
        Upload files to dataset service directly
        rootPath: local file root path
        ext: if set, files endswith this extension will be uploaded
        """
        if self.debug:
            print(f"[UPLOAD_FILES] upload file to dataset without metedata and annotations!")

        if not self.datasetName:
            self.RiseException()

        total = 0
        for root, dir, files in os.walk(rootPath):
            for fileName in files:
                if fileName.endswith(ext):
                    total += 1

        if self.debug:
            print(f"[UPLOAD_FILES] file total: {total}")

        syncData = []
        j = 0
        i = 0
        retInfo = {'succ': 0, 'fail': 0}
        dirname = os.path.dirname(rootPath.rstrip("/"))
        
        for root, dir, files in os.walk(rootPath):
            for fileName in files:
                if fileName.endswith(ext):
                    filePath = os.path.join(root, fileName)
                    objectName = filePath.replace(dirname, "").lstrip("/")
                    self.__UploadFileToDataset(filePath, objectName)
                    tmp = {
                        "ref_id": "",
                        "name": fileName,
                        "path": self.filePrefix + "/" + objectName,
                        "size": int(util.getFileSize(filePath)),
                        "md5": util.getFileMd5(filePath),
                        "frame_id":"",
                        "sensor":"",
                        "meta": {},
                        "anotations": {},
                    }
                    syncData.append(tmp)
                    i += 1
                    if self.debug:
                        per = (i * 100) // total
                        showText = filePath + " =====> " + objectName
                        process = "\r[UPLOAD_FILES][%3s%%]: %s" % (per, showText)
                        print(process)


                    j += 1
                    if j >= 1000:
                        j = 0
                        info = self.dataset.SyncDataToWeb(syncData)
                        if self.debug:
                            print(f"[UPLOAD_FILES] sync data to server, success:{info['succ']}, fail:{info['fail']}")

                        retInfo["succ"] += info["succ"]
                        retInfo["fail"] += info["fail"]
                        syncData = []

        if len(syncData) >= 0:#最后几个没同步的数据
            info = self.dataset.SyncDataToWeb(syncData)
            if self.debug:
                print(f"[UPLOAD_FILES] sync data to server, success:{info['succ']}, fail:{info['fail']}")
            retInfo["succ"] += info["succ"]
            retInfo["fail"] += info["fail"]

        return retInfo

    def UploadFileToDataset(self, filePath):
        """
        Upload one file to dataset service directly
        filePath: local file path
        """
        pathInfo = os.path.split(filePath)
        parentDir = os.path.abspath(os.path.join(pathInfo[0], ".."))
        objectName = pathInfo[0].replace(parentDir, "").strip("/").strip("\\") + "/" + pathInfo[1]
        self.__UploadFileToDataset(filePath, objectName)

        if self.debug:
            print(f"[UPLOAD_ONE_FILE][{filePath}  =====> {objectName}]")

        syncData = {
            "ref_id": "",
            "name": os.path.basename(filePath),
            "path": self.filePrefix+ "/" + objectName,
            "size": int(util.getFileSize(filePath)),
            "md5": util.getFileMd5(filePath),
            "frame_id":"",
            "sensor":"",
            "meta": {},
            "anotations": {},
        }

        info = self.dataset.SyncDataToWeb([syncData])
        if self.debug:
            print(f"[UPLOAD_ONE_FILE] sync data to server, success:{info['succ']}, fail:{info['fail']}")

        return info
        
    def __UploadFileToDataset(self, filePath, objectName):
        """
        Upload one file to OSS
        filePath: local file path
        objectName: OSS object name
        """
        if not self.datasetName:
            self.RiseException()
        return self.dataset.PutFileToDataset(objectName, filePath)

    def AddFile(self, filepath, objectName="") -> File:
        """
        Create a File object which is used for visualize data
        filePath: local file path
        objectName: OSS object name
        """
        if not self.datasetName:
            self.RiseException()

        file = File(filepath, objectName.lstrip("/"), self.filePrefix, self.dataset.endpoint, self.dataset.datasetType)
        self.fileList.append(file)
        if self.debug:
            print(f"[ADD FILE] filepath:{filepath}, objectName:{file.objectPath}")

        return file

    def Commit(self, commitId = ""):
        """
        commit a dataset data
        commitId: if set, this commit will add to the committed data before
        """
        if not self.datasetName:
            self.RiseException()

        db = LocalDb(commitId)
        if self.debug:
            if commitId:
                print(f"[COMMIT FILE] with commitId:{commitId}")
            else:
                print(f"[COMMIT FILE] without commitId!")

            print(f"[COMMIT FILE] begin insert data to local db")

        if len(self.fileList) <= 0:
            raise Exception("one file must be added at least")

        db.insertVal(self.fileList)

        if self.debug:
            print(f"[COMMIT FILE] end insert data to local db")

        db.close()

        self.commitFlag = True
        self.commitId = db.commitId
        return db.commitId

    def Upload(self, commitId = ""):
        """
        upload a committed dataset data and sync annotations to the testin-dataser server
        commitId: if set, this commit will be upload and snync
        """
        if not self.datasetName:
            self.RiseException()

        if commitId != "":
            if self.debug:
                print(f"[UPLOAD_VISUALIZE_FILE] upload visualize files to dataset with committed data: {self.commitId}")
            self.commitFlag = True
            self.commitId = commitId

        if not self.commitFlag:
            self.commitId = self.Commit(commitId)
            if self.debug:
                print(f"[UPLOAD_VISUALIZE_FILE] upload visualize files to dataset without commit, auto commit:{self.commitId}")

        if not self.commitId:
            self.commitId = self.Commit(commitId)
            if self.debug:
                print(f"[UPLOAD_VISUALIZE_FILE] upload visualize files to dataset without commit, auto commit:{self.commitId}")

        db = LocalDb(self.commitId)
        allData = db.fetchAll()
        total = len(allData)
        if total <= 0:
            raise Exception("one file must be added at least")

        syncData = []
        i = 0
        j = 0
        retInfo = {'succ': 0, 'fail': 0}
        for data in allData:
            self.__UploadFileToDataset(data["filepath"], data["objectPath"])
            tmp = {
                "ref_id":data["referid"],
                "name":data["filename"],
                "path":data["osspath"],
                "size":data["filesize"],
                "md5":data["md5"],
                "frame_id":data["frame_id"],
                "sensor":data["sensor"],
                "meta":json.loads(data["metadata"]),
                "anotations":json.loads(data["labeldata"]),
            }
            syncData.append(tmp)
            i += 1
            j += 1

            if self.debug:
                per = (j * 100) // total
                showText = data['filepath'] + " =====> " + data['objectPath']
                process = f"\r[UPLOAD_FILES][{self.commitId}][%3s%%]: %s" % (per, showText)
                print(process)

            if i >= 100:
                i = 0
                info = self.dataset.SyncDataToWeb(syncData)
                if self.debug:
                    print(f"[UPLOAD_FILES] sync data to server, success:{info['succ']}, fail:{info['fail']}")
                retInfo["succ"] += info["succ"]
                retInfo["fail"] += info["fail"]
                syncData = []


        if len(syncData) >= 0:#最后几个没同步的数据
            info = self.dataset.SyncDataToWeb(syncData)
            if self.debug:
                print(f"[UPLOAD_FILES] sync data to server, success:{info['succ']}, fail:{info['fail']}")
            retInfo["succ"] += info["succ"]
            retInfo["fail"] += info["fail"]

        return retInfo

    def GetData(self, offset=0, limit=100, metaKey="", metaValue="", label="", sensor=""):
        """
        search data from testin-dataset service by criteria
        offset: offset of the search result
        limit: numbers of the search result
        metaKey: which metadata key you would like to use to search 
        metaValue: set metadata value to your search  metadata key, if metaKey is not set, metaValue will be ignore
        label: search by label
        sensor: search by sensor
        all above criteria will be juxtaposition
        """
        if limit > 1000:
            raise Exception("limit must less than 1000")

        if metaKey == "" or metaValue == "":
            metaKey=""
            metaValue=""

        return self.dataset.GetData(offset, limit, metaKey="", metaValue="", label="", sensor="")

    def GetFileAndLabel(self, fid="", ref_id=""):
        """
        search data from testin-dataset service by fid or ref_id
        fid: fid
        ref_id: referid you set when you upload data to testin-dataset service
        """
        if fid == "" and ref_id == "":
            raise Exception("fid or ref_id must be set")

        if fid:
            return self.dataset.GetFileAndLabelByFid(fid)

        return self.dataset.GetFileAndLabelByReferid(ref_id)





