import cv2
from typing import Any, Union, Sequence


class Face:
    def __init__(self, faceId, croppedFace, faceRecNo=None, emotionClass=None, emotionScore=None, coordinates=None, name=None):
        self.faceId = faceId
        self.croppedFace = croppedFace
        self.faceRecNo = faceRecNo
        self.emotionClass = emotionClass
        self.emotionScore = emotionScore
        self.coordinates = coordinates
        self.name = name

class Coordinate:
    def __init__(self, id, coordinates):
        self.imageId = id
        self.coordinates = coordinates


class RoI:
    def __init__(self, RoI, id):
        self.RoI = RoI
        self.id = id


def drawBoundary(img, coordinates, text, color):

    if(len(coordinates) == 4):
        x, y, w, h = coordinates
        cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
        # cv2.putText(img, text, (x, y - 4), cv2.FONT_HERSHEY_SIMPLEX,
        #             0.8, color, 1, cv2.LINE_AA)
        return img


def detect(img: Any, frameId: int,  classifier: Any, label: str, scaleFactor: float = 1.1, minNeighbors: int = 10, color=(255, 0, 0), drawBox=True) -> Sequence[Face]:

    grayscaleImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    features = classifier.detectMultiScale(
        grayscaleImage, scaleFactor, minNeighbors)
    faces = []
    faceIndex = 0

    for(x, y, w, h) in features:
        newFaceId = str(frameId)+"_" + str(faceIndex)
        roi = getRoI(img, (x, y, w, h))
        faces.append(Face(newFaceId, roi, coordinates=(x, y, w, h)))
        if(drawBox):
            drawBoundary(img, (x, y, w, h), label, color)
    return faces


def getRoIs(img, coordinatesList: Sequence[Coordinate]) -> Sequence[RoI]:
    RoIs = []
    for element in coordinatesList:
        RoIs.append(RoI(img[element.coordinates[1]:element.coordinates[1] + element.coordinates[3],
                            element.coordinates[0]:element.coordinates[0] + element.coordinates[2]], element.id))
    return RoIs


def getRoI(img, coordinates) -> Any:

    return img[coordinates[1]:coordinates[1] + coordinates[3], coordinates[0]:coordinates[0] + coordinates[2]]
