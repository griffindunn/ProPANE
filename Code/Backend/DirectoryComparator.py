import os
import glob
import time

class DirectoryComparator(object):

    def __init__(self, directory):
        self.directory = directory
        self.current_files = set(os.listdir(self.directory))

    def addIgnoreFile(self, filename):
        self.current_files.add(filename)

    def getNewFiles(self):
        new_file_set = set(os.listdir(self.directory))
        diff_file_set = new_file_set - self.current_files
        self.current_files = new_file_set
        return list(diff_file_set)

    def waitForTransfer(self, timeout):
        while True:
            if len(self.getNewFiles()) == 0:
                break
            print "Sleeping"
            time.sleep(timeout)
