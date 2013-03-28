import Image
import os
import sys

class pImgMgr(object):

    def __getstate__(self):
        state = self.__dict__
        try:
            del state['color']
            del state['bw']
        except:
            pass
        return state

    def __init__(self, filename):
        self.filename = filename
   
    """ Returns the color data for the image """
    def getColor(self):
        try:
            return self.color
        except AttributeError:
            self.color = Image.open(self.filename)
            return self.color

    def save(self, filename):
        self.filename = filename
        try:
            self.getColor().save(filename)
        except IOError:
            os.mkdir(os.path.dirname(filename))
            self.getColor().save(filename)
        del self.color

    
    """ Returns the black and white data for the image """
    def getBW(self):
        try:
            return self.bw
        except AttributeError:
            self.bw = Image.open(self.filename).convert("L")
            return self.bw

    def free(self):
        try:
            del self.color
        except AttributeError:
            pass

        try:
            del self.bw
        except AttributeError:
            pass


