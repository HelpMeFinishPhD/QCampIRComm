#!/usr/bin/env python3
# Python IR pulses sender
# Requires pigpio and pyslinger library
# Adrian Utama, Jun 2017 for QCamp

import pyslinger as pys
import time
from buttons_panasonic_proj import button_dict as bd


def dict_to_bin(cmd):
    return bin(bd[cmd])[2:]


class ir_receiver:
    def __init__(self):
        pass


class ir_sender:
    def __init__(self, mod_freq=38000, duty_cycle=0.33,
                 header=(3572, 1688),  # 3572 us ON, 1688 us OFF
                 trail=(465, 1000),
                 one=(465, 1252),  # Pulse width of a logical one
                 zero=(465, 384),  # Pulse width of a logical zero
                 protocol="QCamp",
                 cmd_dict=bd):
        self.protocol = protocol
        self.cmd_dict = bd
        self.pre_data = dict_to_bin("PRE_DATA")
        self.protocol_config = dict(frequency=mod_freq,
                                    duty_cycle=duty_cycle,
                                    header=header,
                                    trail=trail,
                                    one=one,
                                    zero=zero)

    def ir_send(self, code=None, gpio_pin_out=15):
        ir = pys.IR(gpio_pin_out, self.protocol, self.protocol_config)
        code = self.pre_data + code
        print(code)
        ir.send_code(code)
        time.sleep(0.05)
        ir.terminate_pigpio()


if __name__ == '__main__':
    dev = ir_sender()
    power_on = bin(bd['KEY_POWER1'])[2:]
    print(power_on)
    dev.ir_send(power_on, 15)
