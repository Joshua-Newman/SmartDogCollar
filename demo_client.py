import I2C_LCD_driver
import rssi
from time import sleep
import board
import busio
import adafruit_lsm9ds1

# Python TCP Client A
import socket

host = socket.gethostname()
port = 5005
BUFFER_SIZE = 2000

tcpClientA = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpClientA.connect((host, port))


tcpClientA.close()

# I2C connection:
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)

interface = 'wlan0'
rssi_scanner = rssi.RSSI_Scan(interface)

ssids = ['pi-mobile']

# sudo argument automatixally gets set for 'false', if the 'true' is not set manually.
# python file will have to be run with sudo privileges.

# Variables from power regression of RSSI data
# distance=A*(r/t)^B+C
# where r is the RSSI value and t is the RSSI at 1m
A = 0.812080813887844
B = 3.63550212364731
C = 0.1879191861
t = -37

mylcd = I2C_LCD_driver.lcd()
rollingaverage = []
while True:
    global name
    global signal
    MESSAGE = ""
    # get RSSI data
    ap_info = rssi_scanner.getAPinfo(networks=ssids, sudo=True)
    if(ap_info != False):
        for i in range(10):
            name = ap_info[0]["ssid"]
            signal = ap_info[0]["signal"]
            rollingaverage.append(signal)
        if len(rollingaverage) == 60:
            rollingaverage.pop(0)
        rssi_average = sum(rollingaverage)/len(rollingaverage)
        distance = A*(rssi_average/t)**B + C

        MESSAGE += "SSID: {}\n".format(name)
        MESSAGE += "RSSI: {} dBm\n".format(signal)
        MESSAGE += "RSSI (avg): {} dBm\n ".format(rssi_average)
        MESSAGE += "Distance: {} m\n".format(distance)

    else:
        MESSAGE += "OUT OF RANGE\n"

    tcpClientA.send(MESSAGE)
    data = tcpClientA.recv(BUFFER_SIZE)
    print("sent data:")
    print(MESSAGE)
    sleep(5)
