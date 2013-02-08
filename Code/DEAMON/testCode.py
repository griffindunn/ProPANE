## Open the file with read only permit
f = open('results.txt')
## Read the first line 
line = f.readline()
## If the file is not empty keep reading line one at a time
## till the file is empty
f1=open("writeback.txt", "w")
while line:
    f1.write(line)  
    print line
    line = f.readline()
f1.close()
f.close()
