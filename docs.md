# Docs

## Returns
Message Get: `{"username": (str), "title": (str), "body": (str)}`\
Is returned when user requests a message. For many like the latest 10 messages, it slaps them in an array, in order, still in this format.

## Posts

Create Post: `{"type": "post", "username": (str), "title": (str), "body": (str)}`\
Creates a post with the title and body specified. Username should always be the username of the logged in user regardless of if this uses Rotur or other.\
Get Latest Post: `{"type": "get"}`\
Gets the latest post and returns it as the json specified in **Returns**.\
Get Posts Count: `{"type": "getcount", "count": (int)}`\
Gets the **n** latest posts where **n** is a positive integer.
