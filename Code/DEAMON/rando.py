import os
import sys
import shutil

line2 = "test.txt"
src = "./SubmitPics/" + line2
dst = "./ProcessPics/" + line2

os.rename(src, dst)

#shutil.move(src, dst)
