from DirectoryComparator import DirectoryComparator
import time
import os

#DIRECTORY = "./test"
DIRECTORY = "/home/propane/ProPane/"


listen_dir = DirectoryComparator(DIRECTORY)

while True:
    new_files = listen_dir.getNewFiles()

    for new_file in new_files:
        print "Examining file: %s" % new_file
        sub_dir = "%s/%s" % (DIRECTORY, new_file)
        if os.path.isdir(sub_dir):
            img_dir_comp = DirectoryComparator(sub_dir)
            print "Clearing memory"
            img_dir_comp.clearMemory()
            print "Waiting for transfer"
            img_dir_comp.waitForTransfer(10)
            print "Starting analysis system"
            command = "python analysis_system.py %s" % sub_dir
            os.system(command)	

    time.sleep(5)
