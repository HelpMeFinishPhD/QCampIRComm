import pigpio
import time
import numpy as np

pi = pigpio.pi()
in_pin = 18

pi.set_mode(in_pin,pigpio.INPUT)
pi.set_pull_up_down(in_pin,pigpio.PUD_DOWN)


def timer(in_pin):
    curr = pi.read(in_pin)
    now = curr
    start = time.time()
    while curr == now:
	now = pi.read(in_pin)
    end = time.time()
    return end - start

def one_read_out(in_pin):
    start = time.time()
    out = pi.read(in_pin)
    end = time.time()
    return end - start


if __name__ == "__main__":
    print(one_read_out(in_pin))
#    time_list = [one_read_out(in_pin)[0] for _ in range(10)]
#    print(np.mean(time_list))

	
	
