#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License 2.X as published
#    by the Free Software Foundation.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

from datetime import datetime
from usb.core import Device
import usb.util

class Invalid_Setting(Exception):
    def __init__(self, message):
        self.message = message

class x52:
    """
    Configures various aspects of X52/X52 Pro HOTAS
    """
    __VENDOR_ID=0x06a3
    __SUPPORTED_DEVICES = (
        { 'product_id': 0x0762, 'device_type': 'X52 Pro', 'model': 'Saitek PLC Saitek X52 Pro Flight Control System'},
        { 'product_id': 0x0255, 'device_type': 'X52', 'model': 'Saitek PLC X52 Flight Controller'},
        { 'product_id': 0x075c, 'device_type': 'X52', 'model': 'Saitek PLC X52 Flight Controller'}
        )
    
    __LED_STATUS = {
        'off': 0,
        'on':  1,
        'blink': 0x51,
        'solid': 0x50
        }

    __LED_CODE = {
        'fire':      { 'red': None, 'green':  1 },
        'a':         { 'red':  2,   'green':  3 },
        'b':         { 'red':  4,   'green':  5 },
        'd':         { 'red':  6,   'green':  7 },
        'e':         { 'red':  8,   'green':  9 },
        't1':        { 'red': 10,   'green': 11 },
        't2':        { 'red': 12,   'green': 13 },
        't3':        { 'red': 14,   'green': 15 },
        'pov':       { 'red': 16,   'green': 17 },
        'i':         { 'red': 18,   'green': 19 },
        'throttle':  { 'red': None, 'green': 20 }
        }

    # Vendor request code for the device.ctrl_transfer function
    __VENDOR_REQUEST = 0x91
    # Joystick commands
    __VENDOR_COMMAND = { 'led': 0xb8, 'blink': 0xb4, 'mfd_brightness': 0xb1, 'led_brightness': 0xb2,
        'time': 0xc0, 'offset': {2: 0xc1, 3: 0xc2}, 'date': 0xc4, 'year': 0xc8, 'shift': 0xfd,
        'mfd_line': { 1: 0xd1, 2: 0xd2, 3: 0xd4 }
    }

    __BRIGHTNESS_MIN = 0x00
    __BRIGHTNESS_MAX = 0x7f
    __WRITE_TIMEOUT = 5000

    devices = []

    def __init__(self):
        for devs in self.__SUPPORTED_DEVICES:
            self.devices += list(usb.core.find(
                idVendor=self.__VENDOR_ID,
                idProduct=devs['product_id'],
                find_all=True))

    def __send_command__(self, device: Device, vendor_command: int, value: int):
        if type(device) is Device: 
            device.ctrl_transfer(64, self.__VENDOR_REQUEST, value, vendor_command, None, self.__WRITE_TIMEOUT)
        else:
            raise Invalid_Setting(f'Invalid device type')

    def set_led_color(self, device: Device = None, led: str = 'a', color: str = 'green'):
        """
        Sets the LED color for different buttons on the joystick.
        For the throtlle and Fire button, the valid values are 'on' or 'off'.
        For buttons A, B, D, E, I, T1, T2, T3 and POV Hat, the valid values
        are 'amber', 'red', 'green' and 'off'.
        """
        color_combos = {
            'amber': { 'red': self.__LED_STATUS['on'],  'green': self.__LED_STATUS['on'] },
            'green': { 'red': self.__LED_STATUS['off'], 'green': self.__LED_STATUS['on'] },
            'red':   { 'red': self.__LED_STATUS['on'],  'green': self.__LED_STATUS['off'] },
            'on':    { 'red': self.__LED_STATUS['off'], 'green': self.__LED_STATUS['on'] },
            'off':   { 'red': self.__LED_STATUS['off'],  'green': self.__LED_STATUS['off'] }
            }
        if color not in [ 'amber', 'red', 'green', 'on', 'off']:
            raise Invalid_Setting(f'Color "{color}" is invalid')
        if led in [ 'throttle', 'fire' ] and color not in [ 'on', 'off' ]:
            raise Invalid_Setting(f'Color "{color}" is invalid for "{led}"')
        for col,code in color_combos[color].items():
            if self.__LED_CODE[led][col]:
                self.__send_command__(device, self.__VENDOR_COMMAND['led'], ( self.__LED_CODE[led][col] << 8 ) + code )

    def set_led_blink(self, device: Device = None, state: str = 'solid'):
        """
        Sets blinking for the 'I' button and POV Hat 1.
        Valid values are 'blink' and 'solid'.
        """
        if state not in [ 'blink', 'solid' ]:
            raise Invalid_Setting(f'Invalid  setting {state}')
        self.__send_command__(device, self.__VENDOR_COMMAND['blink'], self.__LED_STATUS[state] )

    def set_brightnes(self, device: Device = None, part: str = 'led', level: int = 64):
        """
        Sets brightness for the MFD and LEDs.
        Parameters are 'mfd' or 'led' for which component will be set and
        an integer between 0 and 127 for the intensity.
        """
        if part not in [ 'mfd', 'led' ]:
            raise Invalid_Setting(f'Invalid component {part}')
        if level < self.__BRIGHTNESS_MIN: level = self.__BRIGHTNESS_MIN
        if level > self.__BRIGHTNESS_MAX: level = self.__BRIGHTNESS_MAX
        self.__send_command__(device, self.__VENDOR_COMMAND[part+'_brightness'], level)

    def set_clock(self, device: Device = None, clock: int = 1, cur_time = datetime.now(), date_format: str = 'DMY', is24h: int = 1):
        """
        Sets the clock and date.

        WARNING: The clock does NOT update itself. You need to call this method and update clock
        1 everytime you want it to advance.

        Setting the date is only possible when also setting the main clock (identified by 1)
        When setting clocks 2 and 3, is not possible to set the date, since those 2 only
        accept offsets from the main clock. The offsets are a number of minutes, between
        -1023 and 1023.

        The parameters are:
        - device: a usb.core device object
        - clock: which of the clock to set (1, 2 or 3)
        - cur_time: A datetime value for clock 1 or an offset for 2 and 3
        - date_format: can be 'DMY', 'MDY' or 'YMD', depending on the order
        - is24h: can be 0 or 1. 0 = AM/PM clock, 1 means a 24h clock
        """
        if is24h!=0: is24h = 1
        if clock<1 or clock>3:
            raise Invalid_Setting(f'Invalid clock: {clock}')
        if clock==1 and type(cur_time) is not datetime:
            raise Invalid_Setting(f'Invalid value for clock {clock}')
        elif clock>1 and type(cur_time) is not int:
            raise Invalid_Setting(f'Invalid value for clock {clock}')
        if clock==1:
            year = cur_time.year 
            month = cur_time.month
            day = cur_time.day
            date_values = { 'DMY': {1: (month << 8) + day,    2: year % 100 },
                            'MDY': {1: (day   << 8) + month,  2: year % 100 },
                            'YMD': {1: (month << 8) + (year % 100),   2: day }
            }
            self.__send_command__(device, self.__VENDOR_COMMAND['date'], date_values[date_format][1])
            self.__send_command__(device, self.__VENDOR_COMMAND['year'], date_values[date_format][2])
            clock_val = (is24h << 15) + (cur_time.hour << 8) + cur_time.minute
            self.__send_command__(device, self.__VENDOR_COMMAND['time'], clock_val)
        else:
            if cur_time > 1024 or cur_time < -1024:
                raise Invalid_Setting(f'Invalid value for offset in clock {clock}')
            offset = is24h << 15
            # this is was hard to understand. 1 << 10 tells the device that the
            # offset is negative. Then we turn a the negative value received in
            # cur_time into a positive and add it to the offset
            if cur_time < 0:
                offset += (1 << 10) + (cur_time * -1)
            else:
                offset += cur_time
            self.__send_command__(device, self.__VENDOR_COMMAND['offset'][clock], offset)

    def set_shift(self, device: Device = None, shift: str = 'off'):
        """
        Set the Shift state indicator. options are 'on' or 'off'
        """
        status = { 'on': 0x51, 'off': 0x50 }
        if shift not in status:
            raise Invalid_Setting(f'Invalid status for shift')
        self.__send_command__(device, self.__VENDOR_COMMAND['shift'], status[shift] )

    def write_mfd(self, device: Device = None, line: int = 1, text: str = r'' ):
        """
        Write to a line of the MFD. Strings are limited to 16 characters, anything
        beyond that will be discarded.

        Write an empty string to clear the line.

        Parameters are the line number (1, 2 or 3) and the text
        """
        if line<1 or line>3:
            raise Invalid_Setting(f'Invalid line number')
        if len(text):
            # we only want 16 characters
            if len(text)>16: text = text[0:15]
            #erase the line before writing
            self.__send_command__(device, self.__VENDOR_COMMAND['mfd_line'][line] | 8, 0 )
            if len(text) % 2: text += ' ' # make sure we have even number of letters
            for c in range(0, len(text), 2):
                # take an even char, bitshifts it and adds the previous odd char
                value = int.from_bytes(text[c + 1].encode("ascii"), "big") << 8 \
                    | int.from_bytes(text[c].encode("ascii"), "big")
                self.__send_command__(device, self.__VENDOR_COMMAND['mfd_line'][line], value )
        else:
            # line | 8 = bitwise OR to indicate to the device that we want to
            # erase the line
            self.__send_command__(device, self.__VENDOR_COMMAND['mfd_line'][line] | 8, 0 )
