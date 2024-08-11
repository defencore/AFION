import asyncio
import websockets
import json
import argparse

# Global variable to store the last event
last_logged_event = None

async def process_event(event, event_type, output_file=None, show_info=False, display_event_type=True):
    global last_logged_event

    timestamp = event.get("kismet.device.base.last_time", None)
    device_type = event.get("kismet.device.base.type", None)
    mac = event.get("kismet.device.base.macaddr", None)
    
    # Search for RSSI from several possible fields
    rssi = event.get("kismet.device.base.signal", {}).get("kismet.common.signal.last_signal", None)
    if not rssi:
        rssi = event.get("kismet.device.base.signal", {}).get("kismet.common.signal.min_signal", None)
    if not rssi:
        rssi = event.get("kismet.device.base.signal", {}).get("kismet.common.signal.max_signal", None)

    bssid = event.get("dot11.device.last_bssid", None)
    if bssid == "00:00:00:00:00:00":
        bssid = None

    # Search for SSID for different device types
    ssid = event.get("kismet.device.base.name", None)
    if not ssid or ssid == mac:
        ssid = event.get("kismet.device.base.commonname", None)
    if not ssid or ssid == mac:
        ssid = event.get("dot11.device", {}).get("dot11.advertisedssid", {}).get("ssid", None)
    
    # Check for Wi-Fi AP + ST
    if device_type == "Wi-Fi Device" and not ssid:
        ssid = event.get("dot11.device", {}).get("dot11.probedssid", {}).get("ssid", None)
    
    # If SSID is still not found, use Unknown_SSID_<MAC>
    if not ssid or ssid == mac:
        ssid = f"Unknown_SSID_{mac}"

    # Search for SSID Probes
    ssid_probes = []
    if "dot11.device" in event and "dot11.device.probed_ssid_map" in event["dot11.device"]:
        ssid_probes = [probe.get("dot11.probedssid.ssid", "").strip() for probe in event["dot11.device"]["dot11.device.probed_ssid_map"]]
    
    # Remove empty SSID Probes
    ssid_probes = [probe for probe in ssid_probes if probe]

    # Format SSID Probes with quotes, only if there are values
    ssid_probes_str = f'SSID Probes: [{", ".join([f"\"{probe}\"" for probe in ssid_probes])}]' if ssid_probes else None

    encryption = event.get("kismet.device.base.crypt", None)

    # Processing additional fields for DOT11_NEW_SSID_BASEDEV
    wps_info = None
    if event_type == "DOT11_NEW_SSID_BASEDEV":
        responded_ssid = event.get("dot11.device", {}).get("dot11.device.responded_ssid_map", [])
        if responded_ssid:
            wps_vendor = responded_ssid[0].get("dot11.advertisedssid.wps_manuf", None)
            wps_device = responded_ssid[0].get("dot11.advertisedssid.wps_device_name", None)
            wps_model_name = responded_ssid[0].get("dot11.advertisedssid.wps_model_name", None)
            wps_model_number = responded_ssid[0].get("dot11.advertisedssid.wps_model_number", None)

            # Combine all WPS info into one string, excluding redundant values
            wps_info_parts = []
            if wps_vendor:
                wps_info_parts.append(wps_vendor)
            if wps_device and wps_device not in wps_vendor:
                wps_info_parts.append(wps_device)
            if wps_model_name and wps_model_name not in wps_device and wps_model_name not in wps_vendor:
                wps_info_parts.append(wps_model_name)
            if wps_model_number and wps_model_number not in wps_device and wps_model_number not in wps_model_name:
                wps_info_parts.append(wps_model_number)

            if wps_info_parts:
                wps_info = f"WPS Info: {' '.join(wps_info_parts)}"

    # Search for clients
    clients = []
    if "dot11.device" in event and "dot11.device.associated_client_map" in event["dot11.device"]:
        clients = list(event["dot11.device"]["dot11.device.associated_client_map"].keys())
    
    clients_str = f'Clients: {clients}' if clients else None

    # Create a list for output
    output_parts = []

    if display_event_type:
        output_parts.append(f"Event Type: {event_type}")
    if timestamp:
        output_parts.append(f"Timestamp: {timestamp}")
    if device_type:
        output_parts.append(f"Type: {device_type}")
    if mac:
        output_parts.append(f"MAC: {mac}")
    if bssid:
        output_parts.append(f"BSSID: {bssid}")
    if rssi is not None:
        output_parts.append(f"RSSI: {rssi}")
    if ssid and ssid != f"Unknown_SSID_{mac}":
        output_parts.append(f"SSID: {ssid}")
    if ssid_probes_str:
        output_parts.append(ssid_probes_str)
    if encryption:
        output_parts.append(f"Encryption: {encryption}")
    if wps_info:
        output_parts.append(wps_info)
    if clients_str:
        output_parts.append(clients_str)

    # Output only if there is data
    if output_parts:
        output_str = ", ".join(output_parts)
        
        # Duplicate check
        if output_str != last_logged_event:
            last_logged_event = output_str
            if show_info:
                print(output_str)
            if output_file:
                with open(output_file, 'a') as f:
                    f.write(output_str + '\n')


async def connect_and_subscribe(output_file=None, show_info=False, display_event_type=True):
    ip = "192.168.8.1"
    user = "admin"
    password = "admin"
    uri = f"ws://{ip}:2501/eventbus/events.ws?user={user}&password={password}"

    while True:
        try:
            async with websockets.connect(uri) as websocket:
                print("Connected to Kismet WebSocket")

                # Subscribe to all events
                subscribe_request = {
                    "SUBSCRIBE": "*"
                }
                await websocket.send(json.dumps(subscribe_request))
                
                print("Subscribed to all events")

                # Process received events
                while True:
                    try:
                        message = await websocket.recv()
                        data = json.loads(message)
                        event_type = list(data.keys())[0]
                        
                        if event_type in ["DOT11_RESPONSE_SSID", "NEW_DEVICE", "DOT11_NEW_SSID_BASEDEV"]:
                            event_data = data[event_type]
                            await process_event(event_data, event_type, output_file, show_info, display_event_type)
                    except websockets.exceptions.ConnectionClosed:
                        print("WebSocket connection closed. Reconnecting...")
                        break
        except (websockets.exceptions.ConnectionClosedError, OSError) as e:
            print(f"Connection error: {e}. Retrying in 5 seconds...")
            await asyncio.sleep(5)
        else:
            print("Successfully reconnected to WebSocket.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Kismet WebSocket Client")
    parser.add_argument("-o", "--output", type=str, help="Output file to write information")
    parser.add_argument("-s", "--show", action="store_true", help="Show information on screen")
    parser.add_argument("-d", "--display_event_type", action="store_true", help="Display Event Type in output")
    args = parser.parse_args()

    asyncio.run(connect_and_subscribe(args.output, args.show, args.display_event_type))
