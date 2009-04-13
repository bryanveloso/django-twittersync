import twitter
import dateutils
from dateutil.tz import tzlocal
from django.core.management.base import BaseCommand
from twittersync.models import TwitterUser, Tweet

class Command(BaseCommand):
    help = "My shiny new management command."

    def handle(self, *args, **options):
        for user in TwitterUser.objects.all():
            api = twitter.Api(username=user.username, password=user.password)
            timeline = api.GetUserTimeline()

            # Update Twitter user data
            userdata = api.GetUser(user.username)

            user.twitter_id = userdata.id
            user.location = userdata.location
            user.name = userdata.name
            user.image_url = userdata.profile_image_url
            user.homepage = userdata.url
            user.description = userdata.description
            user.save()

            # Fetch tweets
            for tweet in timeline:
                data = tweet.AsDict()
                Tweet.objects.get_or_create(
                    twitter_user = user,
                    tweet = data['text'],
                    tweet_id = data['id'],
                    posted = dateutils.parse(data['created_at']).astimezone(tzlocal()).replace(tzinfo=None)
                )