## OpenWrt
```
root@GL-E750:/# kismet --confdir /etc/kismet --datadir /tmp
```
## On remote host
### kismet_event_listener
```
python3 kismet_event_listener.py
```
**Result:**
```
Connected to Kismet WebSocket
Subscribed to all events
Received event of type: MESSAGE
Received event of type: MESSAGE
Received event of type: DOT11_NEW_SSID_BASEDEV
Received event of type: NEW_DEVICE
Received event of type: GPS_LOCATION
Received event of type: PACKETCHAIN_STATS
Received event of type: TIMESTAMP
Received event of type: BATTERY
Received event of type: STATISTICS
Received event of type: MESSAGE
Received event of type: DOT11_RESPONSE_SSID
Received event of type: MESSAGE
Received event of type: NEW_DEVICE
Received event of type: MESSAGE
...
Received event of type: GPS_LOCATION
```
### kismet_new_devices
