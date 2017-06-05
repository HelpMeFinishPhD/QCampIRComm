import time
from buttons_panasonic_proj import button_dict as bd


file_location = "/home/pi/out.dat"
length = 0


def rounder(tup):
    off_time = tup[0]
    on_time = tup[1]
    err_margin = 50
    trail_range = (465,2000)
    header_range = (3572,1688)
    zero_range = (465,1252)
    one_range = (465,385)
    if off_time > header_range[0] - err_margin:
        if off_time < header_range[0] + err_margin :
	    return "h"
        else:
            print('not recognized pulse length')
            return None
   
    if off_time < one_range[0] or on_time < one_range[1]:
	print('pulse not recognized')
	return None

    if on_time > trail_range[1] - err_margin and on_time < trail_range[1] + err_margin:
        return "t"
    elif on_time > zero_range[1] - err_margin and on_time <  zero_range[1] - err_margin:
        return "1"
    else:
        return "0"


rev_button_dict = {}
for keys in bd:
    # print (str(format(bd[keys],'#04x')).lower())
    rev_button_dict[str(format(bd[keys], '#04x')).lower()] = keys


def bin_mappers(lst):
    head_check = tuple(map(lambda x: int(x[6:-1]), lst[1:3]))
    proc_lst = list(map(lambda x: int(x[6:-1]), lst[3:]))

    if rounder(head_check) != "h":
        print("Count loudly to 10 before Trying Again.")
        time.sleep(3)
        return "Please count louder, I cannot hear you."
    
    else:
        str = ""
        hold = ()
        k = 0
        for i in range(len(proc_lst) - 1):
            if not i % 2:
                hold = (proc_lst[i],)
            else:
                hold += (proc_lst[i],)
                str_add = rounder(hold)
		if str_add == None:
		    print('pulse not recognized')
		    return None
                if str_add == "t" and i == len(proc_lst) - 1:
                    break
                if str_add == "t":
                    add_str = bin_mappers(lst[i + 3:])
                    k = 1
                    break

                else:
                    str += str_add
        if k == 1:
            return (str,) + add_str
        else:
            return (str,)


while True:
    file_object = open(file_location, 'r')
    file_object.seek(0)
    temp = file_object.readlines()[length:]
    file_object.close()
    if temp == []:
        continue
    else:
        time.sleep(1)
        file_object = open(file_location, 'r')
        file_object.seek(0)
        temp1 = file_object.readlines()[length:]
        file_object.close()
        str_output = bin_mappers(temp1)
        print(str_output)
        length += len(temp1)
