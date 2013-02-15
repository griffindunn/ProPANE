from DirectoryComparator import DirectoryComparator

DIRECTORY = "./test"

listen_dir = DirectoryComparator(DIRECTORY)

while True:
    new_files = listen_dir.getNewFiles()

    for new_file in new_files:
        print "Examining file: %s" % new_file
        sub_dir = "%s/%s" % (DIRECTORY, new_file)
        if os.path.isdir(sub_dir):
            img_dir = DirectoryComparator(sub_dir)
            print "Waiting for transfer"
            img_dir.waitForTransfer(10)
            print "Starting analysis system"

    time.sleep(5)
