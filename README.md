# redfisher
Tool for discovering new steem users who are acting in ways that benefit the community.

## Installation Instructions
- Have python 3 installeed
- Unzip .tar.gz
- Open command line or kernel and go to the unpacked folder
- Run `python setup.py install`

## Useage
To start a streaming from a week ago, min sp of 60 and posts per week of 2:
~~~
import redfisher

redfisher()
~~~

Adding custom parameters:
~~~
import redfisher

redfisher(weeks=0.5, posts_per_week=1, min_sp=200)
~~~

To check an individual account:
~~~
import redfisher

check(user='sisygoboom', min_sp=10000, weeks=1, posts_per_week=1)
~~~
