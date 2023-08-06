# Logitech X52/X52Pro module

Most of the information about how to configure the devices comes from a GUI program called gx52, created by Roberto Leinardi. His project can be found at https://github.com/leinardi/gx52 . Many thanks to him for his efforts, if you need a GUI app to set up your HOTAS, consider using his program.

If you want a command line tool, there is a utility called x52pro-linux, by nirenjan, available at https://github.com/nirenjan/x52pro-linux . It has a C library that you can use in your own software and a CLI tool to set you HOTAS. It's even available as packages in Debian and Arch.

-----------

## How to use it

- Initializing the module

```python
from x52 import x52

# locate all devices
joystick = x52()

# list devices
print(joystick.devices)
```

- Setting button colors

```python
# sets POV LED to green on device 0
joystick.set_led_color(joystick.devices[0], 'pov', 'green')

# Blinks I button and POV Hat 1
joystick.set_led_blink(joystick.devices[0], 'blink')

# stops blinking
joystick.set_led_blink(joystick.devices[0], 'solid')
```

Valid colors for POV Hat 2 and Throtlle are `on` and `off`. For all other buttons values are `amber`, `red`, `green` or `off`.

For blinking status, values are `blink` and `solid`.

- LED and MFD brightness

Brightness of LEDs and MFD can be set to values between 0 (which turns them off) and 127 (maximum).

You can set the brightness like this:

```python
# set brightness to 60
joystick.set_brightnes(joystick.devices[0],'mfd',60)
joystick.set_brightnes(joystick.devices[0],'led',60)

# turns the lighting off
joystick.set_brightnes(joystick.devices[0],'mfd',0)
joystick.set_brightnes(joystick.devices[0],'led',0)
```


- Sets the clock and date.

WARNING: The clock does NOT update itself. You need to call this method and update clock 1 everytime you want it to advance.

Setting the date is only possible when also setting the main clock (identified by 1) When setting clocks 2 and 3, is not possible to set the date, since those 2 only accept offsets from the main clock. The offsets are a number of minutes, between -1023 and 1023.

When setting the date, you can choose the format, valid options are 'DMY' (Day.Month.Year), 'MDY' (Mont.Day.Year) or 'YMD' (Year.Month.Day). The clocks can also be set to 24h or AM/PM modes.

Setting time and date:


```python
# set current date and time to clock 1, usind DMY and 24h formats
nowtime=datetime.now
joystick.set_clock(device=joystick.devices[0], clock=1, cur_time=nowtime , date_format = 'DMY', is24h = True)

# set clock 2 to 45min ahead
joystick.set_clock(device=joystick.devices[0], clock=2, cur_time=45 )
```

- Shift indicator

This indicator does nothing to the actual performance or functionality of the X52. It's just there so the official software can tell you when it's using different settings.

You can turn it on or off like this:

```python
#turn it on
joystick.set_shift(joystick.devices[0], 'on')

#turn it off
joystick.set_shift(joystick.devices[0], 'off')
```

- MFD Text

You can write on the 3 text lines of the MFD. Lines are limited to 16 characters, anything beyond that will be discarded. There are issues with non-US ASCII text, so try not to write anything fancy. Just call the method with the line number (1 to 3) and the text. A blank line ('') erases the line.

Examples:

```python
# write a text to line 1
joystick.write_mfd(joystick.devices[0], 1, 'A line of Text')
joystick.write_mfd(joystick.devices[0], 1, 'This text is too big and will be truncated')

# Erases line 1
joystick.write_mfd(joystick.devices[0], 1, '')
```
