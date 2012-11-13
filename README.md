# SandysList by B1naryth1ef & Friends
Sandyslist was a site I threw together in about 12 hours after the devastation hurricane Sandy brought to the east coast. The original idea was to help people who need stuff connect to people who could supply stuff. After further discussion (the original idea having come out of #HurricaneHackers) we decided to discontinue the push for this app in favor of others.


## Technical Specs
SandysList is built in Flask, using MongoDB (MongoEngine as the hook), and bootstrap. It was built to run on Heroku, with a pretty simple setup. Some of the routes are a bit messy, and the auth system is complete, err, shit.

## Forking/Using
Your welcome to use as you see fit, I decided not to waste my time licensing it, so steal it if you really want. For a version that implements auth and cleans up some of the ideas here, see [Sandys Redux](https://github.com/b1naryth1ef/sandysredux). The redux'd version fixes a few problems we had here and adds users/etc in.