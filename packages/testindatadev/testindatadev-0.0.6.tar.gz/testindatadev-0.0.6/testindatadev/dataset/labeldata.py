import json

class LabelData():
    def __init__(self):
        self.labels = []

    def AddLabels(self, label="", instance="", attrs={}, type="", data={}, index=""):
        label = {
            "label":label,
            "instance":instance,
            "type":type,
            "attrs":attrs,
            "data":data,
        }

        if index:
            label["index"] = index

        self.labels.append(label)

    def ToString(self):
        return json.dumps(self.labels)

