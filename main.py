import asyncio
import websockets
from tinydb import TinyDB
import json
from dotenv import load_dotenv
load_dotenv()
import os
port = os.getenv("port", 5613)
storageloc = os.getenv("store", "db.json")

print(f"Using port: {port}")
print(f"Using storage location: {storageloc}")

db = TinyDB(storageloc)

def getlatest():
    print("getting the latest post:")
    posts = db.all()
    if posts:
        latest_post = posts[-1]
        print("yeah we did it")
        return latest_post
    else:
        print("no posts found")
        return {"error": "no posts found"}

def likepost(postnum, username):

    print(f"liking post number {postnum}")
    posts = db.all()
    if 0 <= postnum < len(posts):
        getusernames = posts[postnum].get("usersliked", [])
        if username in getusernames:
            print(f"{username} has already liked this post")
            return {"error": "you have already liked this post"}
        
        post = posts[postnum]
        post["usersliked"].append(username)
        db.update(post, doc_ids=[postnum + 1])
        print("post liked successfully")
        return {"success": "liked"}
    
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
    
    if len(username) < 1 or len(body) < 25 or len(title) < 1:
        # uh how do i get the specific case of which one is missing? so glad FUCKING COPILOT TRIED TO FINISH MY SENTENCE FOR ME.
        print("Invalid post data. Missing username, title, or body.")
        return {"error": "missing key data"}

    db.insert({
        "likes": "0",
        "username": username,
        "body": body,
        "title": title,
        "usersliked": []
    })
    print("Post saved to the DB.")
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
            elif msg_type == "like":
                postnum = int(gettype.get("postnum", -1))
                response = likepost(postnum)
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
    async with websockets.serve(handler, "localhost", int(port)):
        print(f"WebSocket server running on ws://localhost:{port}")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())