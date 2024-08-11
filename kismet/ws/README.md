## OpenWrt
```
root@GL-E750:/# kismet --confdir /etc/kismet --datadir /tmp
```
## On local host
### kismet_event_listener
```
% python3 kismet_event_listener.py
```
**Result:**
```
Connected to Kismet WebSocket
Subscribed to all events
Received event of type: MESSAGE
Received event of type: DOT11_NEW_SSID_BASEDEV
Received event of type: NEW_DEVICE
Received event of type: PACKETCHAIN_STATS
Received event of type: TIMESTAMP
Received event of type: BATTERY
Received event of type: STATISTICS
Received event of type: DOT11_RESPONSE_SSID
Received event of type: GPS_LOCATION
```
### kismet_ws_client
```
% python3 kismet_ws_client.py -s -o output.txt
```
```
Timestamp: 1723408733, Type: Wi-Fi AP, MAC: AC:15:A2:XX:XX:XX, RSSI: -82, SSID: XXXXXXXX, Encryption: WPA2-PSK, Clients: ['B0:1C:0C:XX:XX:XX','76:80:2A:XX:XX:XX']
Timestamp: 1723408734, Type: Wi-Fi AP, MAC: D8:47:32:XX:XX:XX, RSSI: -86, SSID: YYYYYYYY, Encryption: WPA2-PSK, WPS Info: TP-Link AC1200 Wireless Dual Band Router Archer C50 4.0
Timestamp: 1723408735, Type: Wi-Fi Client, MAC: A0:9D:C1:XX:XX:XX, RSSI: -69
Timestamp: 1723408736, Type: Wi-Fi AP, MAC: 10:27:F5:XX:XX:XX, RSSI: -90, SSID: ZZZZZZZZ, Encryption: WPA2-PSK
Timestamp: 1723408737, Type: Wi-Fi Client, MAC: 4A:E8:8B:XX:XX:XX, RSSI: -79, SSID Probes: ["XXXXXXXX", "YYYYYYYY", "ZZZZZZZZ"]
Timestamp: 1723408738, Type: Wi-Fi Client, MAC: 76:80:2A:XX:XX:XX
```
