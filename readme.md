# Qute
Qute is a simple quote database - a bare bones clone of bash.org. The main goal is to make it dead simple to set up your own quote collection website.

## Configuration
In the spirit of [The Twelve Factor App](http://www.12factor.net/config), Qute pulls some django settings from environment variables:

	DEBUG=true
	STATIC_ROOT=/path/to/static_root
	STATIC_URL=/static/
	SECRET_KEY=f00bar
	ADMINS="Noah"<noah@example.com>,"Guy"<guy@example.com>

## Deployment
Try deploying me to heroku! I haven't figured out a good way to get django staticfiles and heroku to play nicely yet, so I'm currently hosting the static assets under a subdomain that is just running a simple webserver.

	# create and configure the app
	git clone https://github.com/noah256/qute.git
	heroku create --stack cedar
	heroku config:add DEBUG=false
	heroku config:add STATIC_ROOT=/tmp/unused_on_heroku
	heroku config:add STATIC_URL=//my.static.host/
	heroku config:add SECRET_KEY=`head -c 60 /dev/urandom | base64`
	heroku config:add ADMINS="Name"<name@example.com>

	# deploy
	git push heroku master

	# initial database setup
	heroku run python manage.py syncdb
	heroku run python manage.py migrate

	# deploy static assets
	foreman run manage.py collectstatic
	rsync  -pthrvz  --rsh='ssh  -p 22' path/to/local/static_root user@my.static.host:/path/to/static_root
	
	# open the app in your browser!
	heroku open

## TODO
- Implement a better ranking algorithm. ([How Not To Sort By Average Rating](http://evanmiller.org/how-not-to-sort-by-average-rating.html))
- Better access control for voting. Maybe take a page from [xkcdb](http://www.xkcdb.com/?about) and use sessions abd captcha?
- Figure out a better way to host staticfiles. There may be a way to get a heroku dyno to run collectstatic on startup, or maybe this is just a job for S3.
