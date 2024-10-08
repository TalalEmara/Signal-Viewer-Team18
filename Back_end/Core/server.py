import asyncio
import websockets
import json
import requests

async def fetch_data(websocket, path):
    while True:
        response = requests.get("https://services.swpc.noaa.gov/json/planetary_k_index_1m.json")
        data = response.json()[-1]  # Get the latest data
        await websocket.send(json.dumps(data))
        await asyncio.sleep(60)  # Wait for a minute before fetching again

start_server = websockets.serve(fetch_data, "localhost", 5000)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

