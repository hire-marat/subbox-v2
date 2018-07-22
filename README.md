# subbox-v2
View your subcsriptions in chronological order.

# Deployment
I recommend deploying this as a local Google App Engine app, as for large
subscription feeds you will hit the datastore API limits very fast.

# FAQ
## It's slow
This is just a proof-of-concept.

While I personally don't mind waiting 10 minutes to retrieve a list of 20
thousand videos, this might be an issue for you.

The current method's read speed grows with the amount of videos.

Ways to improve read times:
* store each channel's videos in an array and sift through that for each
 subscribed channel, building a most-recent list, this would probably
 grow with how many subscriptions you have
* store each video by week and keep it in a sorted order, then filter out
 any videos from non-subscribed channels, this would probably grow with
 how many weeks there are since the inception of YouTube (around 700)