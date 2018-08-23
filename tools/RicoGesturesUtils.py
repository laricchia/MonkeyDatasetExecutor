import json
import numpy
from functools import reduce

class RicoGesture:
    TYPE_PRESS = 0
    TYPE_DRAG = 1

    def __init__(self, type, activity, start, end = [0, 0]):
        self.type = type
        self.activity = activity

        self.start_x = int(start[0])
        self.start_y = int(start[1])

        self.end_x = int(end[0])
        self.end_y = int(end[1])

    def __str__(self):
        return "<RicoGesture\tType: %d, Start: [%d,%d], End: [%d, %d]>" % (self.type, self.start_x, self.start_y, self.end_x, self.end_y)


class RicoGestureUtils:

    def __init__(self, size_x, size_y, base_path):
        self.size = [size_x, size_y]
        self.gestures = {}
        self.base_path = base_path

    def reduce_gestures_updating_size(self, acc, elem):
        acc[elem] = {"gestures": numpy.multiply(self.size, self.gestures[elem])}
        return acc

    def reduce_gestures_updating_activity(self, acc, elem):
        with open("%s/view_hierarchies/%s.json" % (self.base_path, elem), "r") as file:
            hier = json.load(file)
            try:
                acc[elem]["activity"] = (hier["activity_name"].split("/"))[1]
            except Exception as e:
                acc[elem]["activity"] = "null"
        #acc[elem]["activity"]
        return acc

    def parseGesturesFile(self):
        with open("%s/gestures.json" % self.base_path, "r") as g_file:
            self.gestures = json.load(g_file)
            self.gestures = {int(k): v for k,v in self.gestures.items()}
        self.gestures = reduce(lambda acc, elem: self.reduce_gestures_updating_size(acc, elem), self.gestures.keys(), {})
        self.gestures = reduce(lambda acc, elem: self.reduce_gestures_updating_activity(acc, elem), self.gestures.keys(), self.gestures)


    def getNextGesture(self):
        for gesture_key in sorted(self.gestures.keys()):
            gesture = self.gestures[gesture_key]["gestures"]
            #gesture = numpy.multiply(self.size, gesture)
            if len(gesture) > 0:
                if len(gesture) == 1:
                    yield RicoGesture(RicoGesture.TYPE_PRESS, self.gestures[gesture_key]["activity"], gesture[0])
                else:
                    yield RicoGesture(RicoGesture.TYPE_DRAG, self.gestures[gesture_key]["activity"], gesture[0], gesture[-1])
        raise StopIteration()
