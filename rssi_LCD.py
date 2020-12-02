# rssi_lcd.py
# setup instructions on https://www.circuitbasics.com/raspberry-pi-lcd-set-up-and-programming-in-python/
# rssi stuff found at https://pypi.org/project/rssi/
# run 'sudo pip install rssi'
# run 'sudo apt install python-smbus'
# run 'sudo pip install smbus2'
# to use run 'sudo python rssi_lcd.py'

import I2C_LCD_driver
import rssi
import time

interface = 'wlan0'
rssi_scanner = rssi.RSSI_Scan(interface)

ssids = ['pi-mobile']

# sudo argument automatixally gets set for 'false', if the 'true' is not set manually.
# python file will have to be run with sudo privileges.

mylcd = I2C_LCD_driver.lcd()
while True:

    ap_info = rssi_scanner.getAPinfo(networks=ssids, sudo=True)
    name=ap_info[0]["ssid"]
    signal=ap_info[0]["signal"]
    
    mylcd.lcd_clear()
    mylcd.lcd_display_string(u"SSID: {}".format(name),1)
    mylcd.lcd_display_string(u"RSSI: {} dBm".format(signal),2)
    time.sleep(.1)
