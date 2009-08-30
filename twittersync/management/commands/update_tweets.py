import twitter
import dateutil

from dateutil.tz import tzlocal
from django.core.management.base import BaseCommand
from twitter import Twitter
from twittersync.models import TwitterUser, Tweet

class Command(BaseCommand):
    help = 'Sync up with Twitter. For great justice.'

    def handle(self, *args, **options):
        for user in TwitterUser.objects.all():
            api = Twitter(user.username, user.password)
            timeline = api.statuses.user_timeline()

            # Update Twitter user data
            userdata = api.users.show(screen_name=user.username)

            user.twitter_id = userdata['id']
            user.location = userdata['location']
            user.name = userdata['name']
            user.image_url = userdata['profile_image_url']
            user.homepage = userdata['url']
            user.description = userdata['description']
            user.save()

            # Fetch tweets
            for tweet in timeline:
                Tweet.objects.get_or_create(
                    twitter_user = user,
                    tweet = tweet['text'],
                    tweet_id = tweet['id'],
                    posted = dateutil.parser(tweet['created_at']).astimezone(tzlocal()).replace(tzinfo=None)
                )