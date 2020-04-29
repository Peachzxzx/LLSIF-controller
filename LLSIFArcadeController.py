"""
    LLSIF Arcade Controller
    Copyright (C) 2020  Peerawich Pruthametvisut
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 2 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import usb
import pyautogui
RQ_SWITCH_MODE  = 0
RQ_GET_SWITCH_A = 1
RQ_GET_SWITCH_B = 2
RQ_GET_SWITCH_C = 3
RQ_GET_SWITCH_D = 4
RQ_GET_SWITCH_E = 5
RQ_GET_SWITCH_F = 6
RQ_GET_SWITCH_G = 7
RQ_GET_SWITCH_H = 8
RQ_GET_SWITCH_I = 9
RQ_GET_SWITCH   = 10


####################################
def find_mcu_boards():
    '''
    Find all Practicum MCU boards attached to the machine, then return a list
    of USB device handles for all the boards

    >>> devices = find_mcu_boards()
    >>> first_board = McuBoard(devices[0])
    '''
    boards = [dev for bus in usb.busses()
                  for dev in bus.devices
                  if (dev.idVendor,dev.idProduct) == (0x16c0,0x05dc)]
    return boards

####################################
class McuBoard:
    '''
    Generic class for accessing Practicum MCU board via USB connection.
    '''
    ################################
    def __init__(self, dev):
        self.device = dev
        self.handle = dev.open()

    ################################
    def usb_write(self, request, data=[], index=0, value=0):
        '''
        Send data output to the USB device (i.e., MCU board)
           request: request number to appear as bRequest field on the USB device
           index: 16-bit value to appear as wIndex field on the USB device
           value: 16-bit value to appear as wValue field on the USB device
        '''
        reqType = usb.TYPE_VENDOR | usb.RECIP_DEVICE | usb.ENDPOINT_OUT
        self.handle.controlMsg(
                reqType, request, data, value=value, index=index)

    ################################
    def usb_read(self, request, length=1, index=0, value=0):
        '''
        Request data input from the USB device (i.e., MCU board)
           request: request number to appear as bRequest field on the USB device
           length: number of bytes to read from the USB device
           index: 16-bit value to appear as wIndex field on the USB device
           value: 16-bit value to appear as wValue field on the USB device

        If successful, the method returns a tuple of length specified
        containing data returned from the MCU board.
        '''
        reqType = usb.TYPE_VENDOR | usb.RECIP_DEVICE | usb.ENDPOINT_IN
        buf = self.handle.controlMsg(
                reqType, request, length, value=value, index=index)
        return buf


""" Button formation diagram for 1920*1080 screen
  "     
  "    A               I   |
  "      B           H     |
  "        C       G       | Right
  "          D   F         |
  "            E           |
  " {y,x} = {285,275} {335,535} {485,750} {700,900} {960,950} {1220,900} {1435,750} {1585,535} {1635,275}
"""
press = pyautogui.mouseDown
release = pyautogui.mouseUp
def buttonA():
    press(x=1635,y=275)
    #osExe('adb shell "sendevent /dev/input/event5 3 58 255 && sendevent /dev/input/event5 3 53 275 && sendevent /dev/input/event5 3 54 285 && sendevent /dev/input/event5 0 2 0"')
def buttonB():
    press(x=1585,y=535)
    #osExe('adb shell "sendevent /dev/input/event5 3 58 255 && sendevent /dev/input/event5 3 53 535 && sendevent /dev/input/event5 3 54 335 && sendevent /dev/input/event5 0 2 0"')
def buttonC():
    press(x=1435,y=750)
    #osExe('adb shell "sendevent /dev/input/event5 3 58 255 && sendevent /dev/input/event5 3 53 750 && sendevent /dev/input/event5 3 54 485 && sendevent /dev/input/event5 0 2 0"')
def buttonD():
    press(x=1220,y=900)
    #osExe('adb shell "sendevent /dev/input/event5 3 58 255 && sendevent /dev/input/event5 3 53 900 && sendevent /dev/input/event5 3 54 700 && sendevent /dev/input/event5 0 2 0"')
def buttonE():
    press(x=960,y=950)
    #osExe('adb shell "sendevent /dev/input/event5 3 58 255 && sendevent /dev/input/event5 3 53 950 && sendevent /dev/input/event5 3 54 960 && sendevent /dev/input/event5 0 2 0"')
def buttonF():
    press(x=700,y=900)
    #osExe('adb shell "sendevent /dev/input/event5 3 58 255 && sendevent /dev/input/event5 3 53 900 && sendevent /dev/input/event5 3 54 1220 && sendevent /dev/input/event5 0 2 0"')
def buttonG():
    press(x=485,y=750)
    #osExe('adb shell "sendevent /dev/input/event5 3 58 255 && sendevent /dev/input/event5 3 53 750 && sendevent /dev/input/event5 3 54 1435 && sendevent /dev/input/event5 0 2 0"')
def buttonH():
    press(x=335,y=535)
    #osExe('adb shell "sendevent /dev/input/event5 3 58 255 && sendevent /dev/input/event5 3 53 535 && sendevent /dev/input/event5 3 54 1585 && sendevent /dev/input/event5 0 2 0"')
def buttonI():
    press(x=285,y=275)
    #osExe('adb shell "sendevent /dev/input/event5 3 58 255 && sendevent /dev/input/event5 3 53 275 && sendevent /dev/input/event5 3 54 1635 && sendevent /dev/input/event5 0 2 0"')
####################################
class PeriBoard:

    ################################
    def __init__(self, mcu):
        self.mcu = mcu

    ################################
    def get_switch(self):
        states = self.mcu.usb_read(request=RQ_GET_SWITCH,length=10)
        if states[9]:
            release()
            #osExe('adb shell "sendevent /dev/input/event5 1 330 0 && sendevent /dev/input/event5 0 0 0"')
            return
        elif states[0]:
            #buttonA()
            press(x=1175,y=495)
        elif states[1]:
            #buttonB()
            press(x=1160,y=580)
        elif states[2]:
            #buttonC()
            press(x=1115,y=650)
        elif states[3]:
            #buttonD()
            press(x=1045,y=695)
        elif states[4]:
            #buttonE()
            press(x=965,y=710)
        elif states[5]:
            #buttonF()
            press(x=885,y=695)
        elif states[6]:
            #buttonG()
            press(x=815,y=650)
        elif states[7]:
            #buttonH()
            press(x=770,y=580)
        elif states[8]:
            #buttonI()
            press(x=755,y=500)
        #osExe('adb shell "sendevent /dev/input/event5 1 330 1 && sendevent /dev/input/event5 0 0 0"')
        #print(states)
        return
#osExe("adb start-server")
a = PeriBoard(McuBoard(find_mcu_boards()[0]))
while True:
    a.get_switch()