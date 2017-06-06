import time

def check_pulses(values, pulse_lengths, margin):
    for value, pulse_length in zip(values, pulse_lengths):
        if value <= pulse_length - margin or value >= pulse_length + margin:
            return False
    return True


def rounder(tup, dictionary):
    off_time = tup[0]
    on_time = tup[1]
    margin = dictionary['margin']
    trailer = dictionary['trailer']
    header = dictionary['header']
    zero = dictionary['zero']
    one= dictionary['one']

    if check_pulses(tup, header, margin):
        return 'h'
    if check_pulses(tup, trailer, margin):
        return 't'
    if check_pulses(tup, zero, margin):
        return '1'
    if check_pulses(tup, one, margin):
        return '0'
    return ''


def follow_file(thefile):
    thefile.seek(0, 2)
    print('exec seek')
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.01)
            continue
        yield line

def read_ir_receiver(protocol_dict, file_name):
    logfile = open(file_location, "r")
    loglines = follow_file(logfile)

    pulse_1 = -1
    pulse_2 = -1
    counter = 1
    word = ""
    start_word_flag = False
    word_length = protocol_dict['word_length']
    
    for line in loglines:
        split_line = line.split(' ')
        amplitude = split_line[0] 
        pulse_time = int(split_line[1])
        #print(amplitude, pulse_time)

        if counter == 1 and amplitude == 'pulse':
            pulse_1 = pulse_time
            counter+=1
        elif counter ==2 and amplitude == 'space':
            pulse_2 = pulse_time
            letter = rounder((pulse_1, pulse_2), protocol_dict)
            counter = 1
            if letter == 'h':
                start_word_flag = True
                word=''
            elif (letter == 't') or (len(word) == word_length):
                start_word_flag = False
                yield word
                word='' # clean up word again
            elif start_word_flag == True:
                word += letter


        else:
            counter=1

def word_completed(word, protocol_dict):
    try:
        a = word[-16:]
        print(protocol_dict[a])
    except KeyError:
        print('Code not found in dictionary')

from buttons_panasonic_proj import button_dict as bd
file_location = "/home/pi/out.dat"
rev_button_dict = {'{}'.format(bin(bd[key]))[2:]:key for key in bd if type(bd[key]) is not tuple}
for word in read_ir_receiver(bd, file_location):
    word_completed(word, rev_button_dict)

