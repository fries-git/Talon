import asyncio
import websockets
from tinydb import TinyDB
import json
db = TinyDB("db.json")
from dotenv import load_dotenv
load_dotenv()
import os
port = os.getenv("port", 5613)


def getlatest():
    print("Getting the latest post.")
    posts = db.all()
    if posts:
        latest_post = posts[-1]
        print(f"latest post is: {latest_post}")
        return latest_post
    else:
        print("no posts found")
        return {"error": "No posts found"}
    
def getcount(count):
    print(f"getting the latest {count} posts")
    posts = db.all()
    if posts:
        latest_posts = posts[-count:]
        print("successfully got the latest posts")
        return latest_posts
    else:
        print("No posts found.")
        return {"error": "No posts found"}

def decodemsg(message):
    if isinstance(message, str):
        message = json.loads(message)
    username = message.get("username", "postname")
    body = message.get("body", "tempbody")
    title = message.get("title", "temptitle")

    db.insert({
        "username": username,
        "body": body,
        "title": title
    })
    print("Post saved.")
    return {"status": "saved"}

async def handler(websocket):
    async for message in websocket:
        try:
            print(f"received: {message}")
            if isinstance(message, str):
                gettype = json.loads(message)
            else:
                gettype = message
            msg_type = gettype.get("type")
            if msg_type == "post":
                response = decodemsg(gettype)
            elif msg_type == "get":
                response = getlatest()
            elif msg_type == "getcount":
                count = int(gettype.get("count", 1))
                response = getcount(count)
            else:
                response = {"error": "Unknown type"}
            await websocket.send(json.dumps(response))
        except Exception as e:
            print(f"Error occurred: {e}")
            await websocket.send(json.dumps({
                "error": str(e)
            }))

async def main():
    async with websockets.serve(handler, "localhost", port):
        print(f"WebSocket server running on ws://localhost:{port}")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())