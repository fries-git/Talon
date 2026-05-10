import asyncio
import websockets
import requests
from tinydb import TinyDB
import json
import logger
from dotenv import load_dotenv
load_dotenv()
import os
import logging
logging.getLogger("websockets.server").disabled = True

webhook_url = os.getenv("webhook", "")
port = os.getenv("port", 5613)
storageloc = os.getenv("store", "db.json")
bio = os.getenv("bio", "Welcome! Whoever is running this has not yet setup a bio (which can be done in the .env file by defining bio.)")
i = 1 # ignore this lmao
minbody = int(os.getenv("minimumlengthbody", 25))
mintitle = int(os.getenv("minimumlengthtitle", 5))

# This code is disgusting I need to fix this.

logger.Logger.cont("------------------------------->")
logger.Logger.search("Talon is a work in progress, expect bugs and downtime. If you find any, please report them to me.")
logger.Logger.like("Welcome to Talon, the Claw reimplementation!")
logger.Logger.cont("Please make any pull requests, and suggest ideas!")
logger.Logger.cont("You can reach out to me as fries on OChats or Barfpile (fries is the display name) on Discord.")
logger.Logger.cont("------------------------------->")

logger.Logger.info(f"Using port: {port}")
logger.Logger.info(f"Using storage location: {storageloc}")
if len(webhook_url) > 0:
    logger.Logger.info("webhook URL found.")
else:
    logger.Logger.warning("no webhook URL found.")

db = TinyDB(storageloc)

def getlatest():
    logger.Logger.get("getting the latest post:")
    posts = db.all()
    if posts:
        latest_post = posts[-1]
        logger.Logger.success("yeah we did it")
        return latest_post
    else:
        logger.Logger.error("no posts found")
        return {"error": "no posts found"}
    
def getbio():
        logger.Logger.get("Bio reuquested!")
        if len(bio) < 1:
            logger.Logger.warning("Something went wrong in the bio!")
            return {"error": "bio is not set up or something errored"}
        else:
            logger.Logger.success("successfully got the bio!")
            return {"success": bio}

def likepost(postnum, username):
    logger.Logger.info(f"liking post number {postnum}")
    posts = db.all()
    post = posts[postnum]
    usersliked = post.get("usersliked", [])
    if not (0 <= postnum < len(posts)):
        logger.Logger.error("post does not exist")
        return {"error": "post not found"}
    if username in usersliked:
        logger.Logger.warning(f"{username} already liked this post")
        return {"error": "already liked"}
    usersliked.append(username)
    db.update({
        "usersliked": usersliked,
        "likes": str(len(usersliked))
    }, doc_ids=[post.doc_id])
    logger.Logger.like(f"{username} liked post {postnum}")
    return {
        "success": True,
        "likes": len(usersliked)
    }

def deletepost(postnum, username):
    logger.Logger.info(f"deleting post number {postnum}")
    posts = db.all()
    if not (0 <= postnum < len(posts)):
        logger.Logger.error("post does not exist")
        return {"error": "post not found"}
    if username != posts[postnum].get("username"):
        logger.Logger.warning(f"{username} isnt the author of this post")
        return {"error": "you are not the author of this post"}
    db.remove(doc_ids=[posts[postnum].doc_id])
    logger.Logger.delete(f"{username} deleted post {postnum}")
    return {"success": "Message deleted successfully"}

def getcount(count):
    logger.Logger.get(f"getting the latest {count} posts")
    posts = db.all()
    if posts:
        latest_posts = posts[-count:]
        logger.Logger.success("successfully got the latest posts")
        return latest_posts
    else:
        logger.Logger.error("No posts found.")
        return {"error": "No posts found"}

def decodemsg(message):
    if isinstance(message, str):
        message = json.loads(message)
    username = message.get("username", "postname")
    body = message.get("body", "tempbody")
    title = message.get("title", "temptitle")
    
    if len(username) < 1 or len(body) < 25 or len(title) < 1:
        # uh how do i get the specific case of which one is missing without doing more elifs? so glad FUCKING COPILOT TRIED TO FINISH MY SENTENCE FOR ME.
        logger.Logger.error("Invalid post data. Missing username, title, or body.")
        return {"error": "missing key data"}

    db.insert({
        "likes": "0",
        "username": username,
        "body": body,
        "title": title,
        "usersliked": []
    })
    if len(webhook_url) > 0:
        try:
            requests.post(webhook_url, json={
                "username": f"{username} - Talon Post Notification",
                "embeds": [
                    {
                        "title": f"{title} - {username}",
                        "description": body,
                        "color": 1127128, # Decimal color (Red)
        }
    ]
            })
            logger.Logger.success("Successfully sent webhook notification.")
        except Exception as e:
            logger.Logger.error(f"Failed to send webhook notification: {e}")
    logger.Logger.success("Post saved to the DB.")
    return {"status": "saved"}

def testauth(token):
    requests.get(f"https://api.rotur.dev/me?auth={token}")

def returnsearch(query):
    logger.Logger.search(f"searching for {query}")
    posts = db.all()
    results = []
    for post in posts:
        if query.lower() in post.get("title", "").lower() or query.lower() in post.get("body", "").lower() or query.lower() in post.get("username", "").lower():
            results.append(post)
    if len(results) > 0:
        logger.Logger.success(f"found {len(results)} results for query: {query}")
    else:
        logger.Logger.warning(f"no results found for query: {query}")
    return results

async def handler(websocket):
    async for message in websocket:
        try:
            logger.Logger.info(f"received: {message}")
            if isinstance(message, str):
                gettype = json.loads(message)
            else:
                gettype = message
            msg_type = gettype.get("type")
            username = gettype.get("username")
            if msg_type == "post":
                response = decodemsg(gettype)
            elif msg_type == "get":
                response = getlatest()
            elif msg_type == "like":
                postnum = int(gettype.get("postnum", -1))
                response = likepost(postnum, username)
            elif msg_type == "deletepost":
                postnum = int(gettype.get("postnum", -1))
                response = deletepost(postnum, username)
            elif msg_type == "getcount":
                count = int(gettype.get("count", 1))
                response = getcount(count)
            elif msg_type == "getbio":
                response = getbio()
            elif msg_type == "search":
                query = str(gettype.get("query", ""))
                response = returnsearch(query)
            else:
                response = {"error": "Unknown type"}
            await websocket.send(json.dumps(response))
        
        except Exception as e:
            logger.Logger.error(f"Error occurred: {e}")
            await websocket.send(json.dumps({
                "error": str(e)
            }))

async def main():
    async with websockets.serve(handler, "localhost", int(port)):
        logger.Logger.info(f"WebSocket server running on ws://localhost:{port}")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())