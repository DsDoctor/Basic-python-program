# made by Sheng Du
from pykeyboard import PyKeyboard
from pymouse import PyMouse
import time


def switch_sub_program():
    k.press_key('control')
    k.tap_key('tab')
    k.release_key('control')
    time.sleep(0.14)


def send_message(mes):
    if len(mes) != 1:
        k.type_string(mes)
    else:
        k.tap_key(mes)
    k.tap_key('return')
    time.sleep(0.05)


def refresh():
    for program in range(2):
        m.click(83, 68, 1)
        switch_sub_program()
    time.sleep(2)
    for program in range(2):
        m.click(379, 266, 1)
        switch_sub_program()
        time.sleep(1)
    for program in range(2):
        m.click(614, 798)
        switch_sub_program()
    time.sleep(2)


if __name__ == '__main__':
    k = PyKeyboard()
    m = PyMouse()
    for epoch in range(16):
        for message in range(501):
            send_message('1')
            switch_sub_program()
        time.sleep(3)
        refresh()
