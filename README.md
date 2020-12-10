# SmartDogCollar
Network Embedded System Project

## How to run:
requirements: python3, ```pip3 install rssi```

for more info on connecting ad-hoc networks on a pi, [read the docs](https://www.raspberrypi.org/documentation/configuration/wireless/access-point-routed.md)
### Server
1. (optional) modify your node to broadcast a wifi SSID
1. use ifconfig to get the gateway node IP
1. change the TCP_IP in demo_server.py to the IP found
1. copy demo_server.py to the location of your choice on your node that broadcasts wifi
1. run using ```python3  <PATH_TO_FILE>/demo_server.py```
### Client

1. change 'pi-mobile' in demo_client.py to the ssid set above, or of your home network
1. change TCP_IP in demo_client.py to the IP found above
1. copy demo_client.py to the perimeter nodes
1. connect to the same network as the server
1. run using ```python3 <PATH_TO_FILE>/demo_client.py```
