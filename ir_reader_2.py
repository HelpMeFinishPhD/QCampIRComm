import time
from buttons_panasonic_proj import button_dict as bd


file_location = "/home/pi/out.dat"
length = 0


def check_pulses(values, pulse_lengths, margin):
    for value, pulse_length in (values, pulse_lengths):
        if value <= pulse_length - margin or value >= pulse_length + margin:
            return False
    return True


def rounder(tup, bd):
    off_time = tup[0]
    on_time = tup[1]
    err_margin = 50
    trailer = bd['trailer']
    header = bd['header']
    zero = bd['zero']
    one= bd['one']

    if check_pulses(tup, header, margin):
        return 'h'

    if check_pulses(tup, trailer, margin):
        return 't'

    if check_pulses(tup, zero, margin):
        return '1'

    if check_pulses(tup, one, margin):
        return '0'

    print('pulse not recognized')
    return ''



def follow(thefile):
    thefile.seek(0, 2)
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.01)
            continue
        yield line

# rev_button_dict = {}
# for keys in bd:
#     # print (str(format(bd[keys],'#04x')).lower())
#     rev_button_dict[str(format(bd[keys], '#04x')).lower()] = keys


# def bin_mappers(lst):
#     head_check = tuple(map(lambda x: int(x[6:-1]), lst[1:3]))
#     proc_lst = list(map(lambda x: int(x[6:-1]), lst[3:]))

#     if rounder(head_check) != "h":
#         print("Count loudly to 10 before Trying Again.")
#         time.sleep(3)
#         return "Please count louder, I cannot hear you."

#     else:
#         str = ""
#         hold = ()
#         k = 0
#         for i in range(len(proc_lst) - 1):
#             if not i % 2:
#                 hold = (proc_lst[i],)
#             else:
#                 hold += (proc_lst[i],)
#                 str_add = rounder(hold)
#                 if str_add == None:
#                     print('pulse not recognized')
#                     return None
#                 if str_add == "t" and i == len(proc_lst) - 1:
#                     break
#                 if str_add == "t":
#                     add_str = bin_mappers(lst[i + 3:])
#                     k = 1
#                     break

#                 else:
#                     str += str_add
#         if k == 1:
#             return (str,) + add_str
#         else:
#             return (str,)


def do_it():
    logfile = open(file_location, "r")
    loglines = follow(logfile)
    temp = False
    pulse_high = -1

    pulse_1 = -1
    pulse_2 = -1
    counter = 1
    word = []
    start_word_flag = False
    for line in loglines:
        split_line = line.split(' ')
        amplitude = split_line[0] 
        pulse_time = int(split_line[1])

        if counter == 1 and amplitude == 'Pulse':
            pulse1 = pulse_time
            counter+=1
        elif counter ==2 and amplitude == 'Space':
            pulse_2 = pulse_time
            letter = rounder(pulse_1, pulse_2)
            counter = 1
            if letter == 'h':
                start_word_flag = True
            if start_word_flag == True:
                word.append(letter)
            if (letter == 't') or (len(word) >= word_length):
                word_completed(word)
                print(word) # Here everything can happen
                start_word_flag = False
                word=[] # clean up word again

        elif:
            counter=1

def word_completed(word):
    print('here do stuff')
    print('word')





# while True:
#     file_object = open(file_location, 'r')
#     file_object.seek(0)
#     temp = file_object.readlines()[length:]
#     file_object.close()
#     if temp == []:
#         continue
#     else:
#         time.sleep(1)
#         file_object = open(file_location, 'r')
#         file_object.seek(0)
#         temp1 = file_object.readlines()[length:]
#         file_object.close()
#         str_output = bin_mappers(temp1)
#         print(str_output)
#         length += len(temp1)
