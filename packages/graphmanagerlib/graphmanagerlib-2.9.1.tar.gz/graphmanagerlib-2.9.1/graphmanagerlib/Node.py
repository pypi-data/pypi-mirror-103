class Node:
    def __init__(self, XMin, YMin, XMax,YMax,Object,Tag):
        self.XMin = XMin
        self.YMin = YMin
        self.XMax = XMax
        self.YMax = YMax
        self.Object = Object
        self.Tag = Tag


    def getInfo(self):
        return [self.XMin, self.YMin, self.XMax, self.YMax, self.Objects, self.Tag]

    def to_string(self):
        return [self.XMin]
        return ','.join([str(self.XMin), str(self.YMin), str(self.XMax), str(self.YMax),self.Object, self.Tag])


