# redfisher
Tool for discovering new steem users who are acting in ways that benefit the community.

## Installation Instructions

- Have python installed
- Clone repo
- Open command line or kernel open in the file where setup.py is
- Run `python setup.py install`

## Useage

#### As of v1.1, you can run redfisher from the terminal by going to the file location and typing this:
~~~
python redfisher.py --min_sp=50 --posts_per_week=4
~~~

To start a streaming from a week ago, min sp of 60 and posts per week of 2:
~~~
import redfisher as rf

rf.redfisher()
~~~

Adding custom parameters:
~~~
import redfisher as rf

rf.redfisher(weeks=0.5, posts_per_week=1, min_sp=200)
~~~

To check an individual account:
~~~
import redfisher as rf

rf.check(user='sisygoboom', min_sp=10000, weeks=1, posts_per_week=1)
~~~
