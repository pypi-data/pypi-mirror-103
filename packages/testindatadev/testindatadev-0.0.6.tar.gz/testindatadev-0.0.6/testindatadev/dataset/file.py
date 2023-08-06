import os, sys
import hashlib

sys.path.append(os.path.dirname(__file__) + os.sep + './')

from metadata import MetaData
from labeldata import LabelData
from utils import util

class File():
    def __init__(self, filepath, basePath, filePrefix, endpoint, fileType):
        self.TYPE_IMAGE = 0
        self.TYPE_VIDEO = 1
        self.TYPE_AUDIO = 2
        self.TYPE_POINT_CLOUD = 3
        self.TYPE_FUSION_POINT_CLOUD = 4
        self.TYPE_POINT_CLOUD_SEMANTIC_SEGMENTATION = 5
        self.TYPE_TEXT = 6

        self.metadata = {}
        self.labeldata = LabelData()
        self.filePrefix = filePrefix
        self.fileType = fileType
        self.freamId = ""
        self.sensor = ""
        if basePath == "":
            self.objectPath = os.path.basename(filepath)
            self.osspath = self.filePrefix + "/" + os.path.basename(filepath)
        else:
            basePath = basePath.rstrip("/")
            if filepath.find(basePath) < 0:
                raise Exception(f"basePath must be part of filepath!")
            self.osspath = self.filePrefix + "/" + filepath.split(basePath + "/")[1]
            self.objectPath = filepath.split(basePath + "/")[1]

        self.osspath = endpoint.rstrip("/") + "/" + self.osspath

        self.referId = ""
        self.filepath = filepath
        self.filename = os.path.basename(filepath)
        self.md5 = util.getFileMd5(self.filepath)
        self.filesize = int(util.getFileSize(self.filepath))
        self.type = util.getFiletype(self.filepath)

        with open(self.filepath, "rb") as bf:
            file_md5 = hashlib.md5(bf.read())
            self.md5 = file_md5.hexdigest()

    #数据自查
    def SelfCheck(self):
        if not self.referId:
            raise Exception(f"referid must be set!")

        if self.fileType == self.TYPE_FUSION_POINT_CLOUD:
            if not self.freamId:
                raise Exception(f"3D fusion data must set freamId")

            if not self.sensor:
                raise Exception(f"3D fusion data must set sensor")


    def AddmetaData(self, madedata):
        self.metadata = MetaData(madedata)

    def AddReferId(self, ref_id):
        if ref_id == "":
            raise Exception(f"referId can not be empty string!")
        self.referId = ref_id

    def SetFreamId(self, frame_id = ""):
        self.freamId = frame_id

    def SetSensor(self, sensor = ""):
        self.sensor = sensor

    #添加box
    def AddBox2D(self, box2d, label="", instance="", attrs={}):
        # 数据格式检查
        if not type(box2d) is dict:
            raise Exception(f"box must be a dict, {type(box2d)} gavin")

        keys = list(set(box2d.keys()))
        keys.sort()
        if keys != ['height', 'width', 'x', 'y']:
            raise Exception(f"box keys must be ['height', 'width', 'x', 'y'], {keys} gavin")

        self.labeldata.AddLabels(label=label, instance=instance, attrs=attrs, type="box2d", data=box2d)

    #添加椭圆
    def AddEllipse(self, ellipse, label="", instance="", attrs={}):
        if not type(ellipse) is dict:
            raise Exception(f"ellipse must be a dict, {type(ellipse)} gavin")

        keys = list(set(ellipse.keys()))
        keys.sort()
        if keys != ['height', 'width', 'x', 'y']:
            raise Exception(f"ellipse keys must be ['height', 'width', 'x', 'y'], {keys} gavin")

        self.labeldata.AddLabels(label=label, instance=instance, attrs=attrs, type="ellipse", data=ellipse)


    def AddPolygon(self, polygon, label="", instance="", attrs={}, index = 0):
        if not type(polygon) is list:
            raise Exception(f"polygon must be a list, {type(polygon)} gavin")

        for poly in polygon:
            keys = list(set(poly.keys()))
            if keys != ["x", "y"] and keys != ["y", "x"]:
                raise Exception(f"poly point keys must be ['x', 'y'], {list(set(poly.keys()))} gavin")


        self.labeldata.AddLabels(label=label, instance=instance, attrs=attrs, type="polygon", data=polygon, index=index)

    def AddLine(self, line, label="", instance="", attrs={}):
        if not type(line) is list:
            raise Exception(f"line must be a list, {type(line)} gavin")

        for point in line:
            keys = list(set(point.keys()))
            if keys != ["x", "y"] and keys != ["y", "x"]:
                raise Exception(f"line point keys must be ['x', 'y'], {keys} gavin")


        self.labeldata.AddLabels(label=label, instance=instance, attrs=attrs, type="line", data=line)


    def AddCurve(self, curve, label="", instance="", attrs={}):
        if not type(curve) is list:
            raise Exception(f"curve must be a list, {type(curve)} gavin")

        for point in curve:
            keys = list(set(point.keys()))
            if keys != ["x", "y"] and keys != ["y", "x"]:
                raise Exception(f"curve point keys must be ['x', 'y'], {keys} gavin")


        self.labeldata.AddLabels(label=label, instance=instance, attrs=attrs, type="curve", data=curve)


    def AddPoint(self, point, label="", instance="", attrs={}):
        if not type(point) is dict:
            raise Exception(f"curve must be a list, {type(point)} gavin")

        keys = list(set(point.keys()))
        if keys != ["x", "y"] and keys != ["y", "x"]:
            raise Exception(f"curve point keys must be ['x', 'y'], {keys} gavin")


        self.labeldata.AddLabels(label=label, instance=instance, attrs=attrs, type="point", data=point)


    def AddParallel(self, parallel, label="", instance="", attrs={}):
        if not type(parallel) is list:
            raise Exception(f"parallel must be a list, {type(parallel)} gavin")

        if len(parallel) != 4:
            raise Exception(f"parallel points numbers must be 4, {len(parallel)} gavin")

        for point in parallel:
            keys = list(set(point.keys()))
            if keys != ["x", "y"] and keys != ["y", "x"]:
                raise Exception(f"parallel point keys must be ['x', 'y'], {keys} gavin")


        self.labeldata.AddLabels(label=label, instance=instance, attrs=attrs, type="parallel", data=parallel)


    def AddBox3D(self, box3d, label="", instance="", attrs={}):
        # 数据格式检查
        if not type(box3d) is dict:
            raise Exception(f"box3D must be a dict, {type(box3d)} gavin")

        keys = list(set(box3d.keys()))
        keys.sort()
        if keys != ['position', 'rotation', 'scale']:
            raise Exception(f"box3D keys must be ['position', 'rotation', 'scale'], {keys} gavin")

        self.labeldata.AddLabels(label=label, instance=instance, attrs=attrs, type="box3d", data=box3d)


    def AddCuboid(self, cuboid, label="", instance="", attrs={}):
        # 数据格式检查
        if not type(cuboid) is dict:
            raise Exception(f"cuboid must be a dict, {type(cuboid)} gavin")

        keys = list(set(cuboid.keys()))
        keys.sort()
        if keys != ['back', 'front']:
            raise Exception(f"cuboid keys must be ['back', 'front'], {keys} gavin")

        if len(cuboid["back"]) != 4:
            raise Exception(f"cuboid back length must be 4, {len(cuboid['back'])} gavin")

        for point in cuboid["back"]:
            keys = list(set(point.keys()))
            if keys != ["x", "y"] and keys != ["y", "x"]:
                raise Exception(f"cuboid point keys must be ['x', 'y'], {keys} gavin")

        if len(cuboid["front"]) != 4:
            raise Exception(f"cuboid front length must be 4, {len(cuboid['front'])} gavin")

        for point in cuboid["front"]:
            keys = list(set(point.keys()))
            if keys != ["x", "y"] and keys != ["y", "x"]:
                raise Exception(f"cuboid point keys must be ['x', 'y'], {keys} gavin")


        self.labeldata.AddLabels(label=label, instance=instance, attrs=attrs, type="cuboid", data=cuboid)

    
    def AddSideCuboid(self, sideCuboid, label="", instance="", attrs={}):
        # 数据格式检查
        if not type(sideCuboid) is dict:
            raise Exception(f"box3D must be a dict, {type(sideCuboid)} gavin")

        keys = list(set(sideCuboid.keys()))
        keys.sort()
        if keys != ['back', 'front']:
            raise Exception(f"box3D keys must be ['back', 'front'], {keys} gavin")

        if len(sideCuboid["back"]) != 2:
            raise Exception(f"cuboid back length must be 4, {len(sideCuboid['back'])} gavin")

        for point in sideCuboid["front"]:
            keys = list(set(point.keys()))
            if keys != ["x", "y"] and keys != ["y", "x"]:
                raise Exception(f"cuboid point keys must be ['x', 'y'], {keys} gavin")

        if len(sideCuboid["front"]) != 4:
            raise Exception(f"cuboid front length must be 4, {len(sideCuboid['front'])} gavin")

        for point in sideCuboid["front"]:
            keys = list(set(point.keys()))
            if keys != ["x", "y"] and keys != ["y", "x"]:
                raise Exception(f"cuboid point keys must be ['x', 'y'], {keys} gavin")

        self.labeldata.AddLabels(label=label, instance=instance, attrs=attrs, type="side_cuboid", data=sideCuboid)

