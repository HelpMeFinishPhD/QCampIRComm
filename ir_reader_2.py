import time
from buttons_panasonic_proj import button_dict as bd


file_location = "/home/pi/out.dat"
length = 0


def rounder(tup):
    if tup[0] > 3000 and tup[0] < 3650:
        return "h"
    else:
        ot = tup[1]
        if ot > 1400:
            return "t"
        elif ot > 700:
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
        str_output = bin_mappers(temp1)[1:]
        for elem in str_output:
            # print(hex(int(str_output,2)))
            print(rev_button_dict[hex(int(elem[-16:], 2))])
        length += len(temp1)
