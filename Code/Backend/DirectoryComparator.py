import os
import glob
import time

class DirectoryComparator(object):

    def __init__(self, directory):
        self.directory = directory
        self.current_files = set(os.listdir(self.directory))

    def getNewFiles(self):
        new_file_set = set(os.listdir(self.directory))
        diff_file_set = new_file_set - self.current_files
        self.current_files = new_file_set
        return list(diff_file_set)

    def waitForTransfer(self, timeout):
        while True:
            current_files = self.current_files[:]
            new_files = self.getNewFiles()
            print "New files: %s\nCurrent files: %s" % (new_files, current_files)
            if len(new_files) == 0 and not dir_empty:
                break
            time.sleep(timeout)

    def clearMemory(self):
        self.current_files = set([])
        print "Current files: %s" % self.current_files

