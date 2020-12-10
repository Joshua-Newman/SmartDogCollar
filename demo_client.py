import rssi
from time import sleep, time


# Python TCP Client A
import socket

host = socket.gethostname()
port = 5005
BUFFER_SIZE = 2000

tcpClientA = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


interface = 'wlan0'
rssi_scanner = rssi.RSSI_Scan(interface)

ssids = ['pi-mobile']

# sudo argument automatixally gets set for 'false', if the 'true' is not set manually.
# python file will have to be run with sudo privileges.

import rssi
from time import sleep, time


# Python TCP Client A
import socket

host = socket.gethostname()
port = 5005
BUFFER_SIZE = 2000

tcpClientA = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


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

now = time()
rollingaverage = []
while True:
    MESSAGE = ""
    # get RSSI data
    ap_info = rssi_scanner.getAPinfo(networks=ssids, sudo=True)
    if(ap_info != False):
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
    if(time()-now > 5):  # collect data for 5 seconds, then send
        tcpClientA = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcpClientA.connect(("192.168.16.1", port))
        tcpClientA.sendall(MESSAGE.encode('utf-8'))
        # data = tcpClientA.recv(BUFFER_SIZE)
        print("sent data:")
        print(MESSAGE)
        tcpClientA.close()
        now = time()