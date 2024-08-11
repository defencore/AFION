import asyncio
import websockets
import json

async def list_all_events(ip, user, password):
    uri = f"ws://{ip}:2501/eventbus/events.ws?user={user}&password={password}"
    
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
            message = await websocket.recv()
            data = json.loads(message)
            event_type = list(data.keys())[0]  # Extract event type
            print(f"Received event of type: {event_type}")

# Define variables
ip = "192.168.8.1"
user = "admin"
password = "admin"

# Run the request
asyncio.run(list_all_events(ip, user, password))
