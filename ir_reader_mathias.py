import time
from buttons_panasonic_proj import button_dict as bd


file_location = "/home/pi/out.dat"
def rounder(tup):
    off_time = tup[0]
    on_time = tup[1]
    
    if off_time > 3000:
        if off_time < 3650:
	    return "h"
        else:
            print('not recognized pulse length')
            return None
   
    if off_time < 400:
	print('pulse not recognized')
	return None

    if on_time > 1400:
        return "t"
    elif on_time > 700:
        return "1"
    else:
        return "0"


def follow(thefile):
    thefile.seek(0, 2)
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.01)
            continue
        yield line

def main():
    logfile = open(file_location, "r")
    loglines = follow(logfile)
    for line in loglines:
	split_line = line.split(' ')
	amplitude = split_line[0] 
	pulse = int(split_line[1])
	print(amplitude, pulse)	


if __name__ == '__main__':
    main()

    