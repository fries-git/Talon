# Changelog

The github commit messages are getting too long so here's where I will start including more detailed changelogs. This will only get updated for major stuff.\
It now works with Rotur Authentication! This is a massive change so please let me know if docs seem to be unupdated.
> Instead of a username, users now pass their Rotur token. Is this a security vulnerability? Who knows!!! Sure feels like it, but I've been assured this is fine.\

Fixed some bugs relating to the issue of varying return information.
> It should normally return either `{"success": (otherinformation)}` but a bunch of functions just used random bs? Like: `{"status": "saved"}` when a message got saved.

Now while docs should be up to date, please check me on this. I'm going to make a client now, then ill work on more updates.
