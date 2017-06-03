#!/usr/bin/env python3
# Python IR pulses sender
# Requires pigpio and pyslinger library
# Adrian Utama, Jun 2017 for QCamp

import pyslinger as pys
import time
from buttons_panasonic_proj import button_dict as bd


# Below contains information the user need to put forth to send IR signals
mod_freq = 38000
duty_cycle = 0.33

# ON-OFF sequences (in microseconds)
ir_header = [3572, 1688] # 3572 us ON, 1688 us OFF
ir_trail = [465, 1000] 
ir_one = [465, 1252]
ir_zero = [465, 384]

pre_data =  "\
0100\
0000\
0000\
0100\
0000\
0001\
0001\
0010\
0000\
0000\
"

button_press = bin(bd["KEY_POWER1"])[2:]

patt_tosend = pre_data + button_press

protocol = "QCamp"
gpio_pin = 15

protocol_config = dict(frequency = mod_freq,
			duty_cycle = duty_cycle,
			ir_header = ir_header,
                        ir_trail = ir_trail,
			ir_one = ir_one,
			ir_zero = ir_zero)
ir = pys.IR(gpio_pin, protocol, protocol_config)

for i in range(30):
    ir.send_code(patt_tosend)
    time.sleep(0.05)
ir.terminate_pigpio()