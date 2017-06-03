import time
from buttons_panasonic_proj import button_dict as bd


file_location = "/home/pi/out.dat"
length = 0


import time
def follow(thefile):
    thefile.seek(0,2)
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line

if __name__ == '__main__':
    logfile = open(file_location, "r")
    loglines = follow(logfile)
    for line in loglines:
        print line