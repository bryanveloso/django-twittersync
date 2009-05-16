import twitter
import dateutils
from dateutil.tz import tzlocal
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel

class TwitterUser(TimeStampedModel):
    username = models.CharField(_('twitter username'), max_length=255)
    password = models.CharField(_('twitter password'), max_length=255)

    # Automatically
    twitter_id = models.IntegerField(_('twitter userid'), blank=True, null=True)
    location = models.CharField(_('twitter location'), max_length=255, blank=True)
    name = models.CharField(_('twitter screen name'), max_length=255, blank=True)
    image_url = models.URLField(_('twitter location'), blank=True)
    homepage = models.URLField(_('twitter homepage'), blank=True)

    def __unicode__(self):
        return self.username

class Tweet(TimeStampedModel):
    twitter_user = models.ForeignKey(TwitterUser, related_name='tweets')
    tweet = models.TextField(_('tweet'))
    tweet_id = models.IntegerField(_('tweet id'), blank=True, null=True)
    posted = models.DateTimeField(_('posted'), blank=True, null=True)

    class Meta:
        ordering = ['-posted']

    def __unicode__(self):
        return "%s: %s" % (self.twitter_user.username, self.tweet)

    def get_absolute_url(self):
        return 'http://twitter.com/%s/status/%s' % (self.twitter_user.username, self.tweet_id)

    def save(self, *args, **kwargs):
        if not self.tweet_id and self.tweet:
            api = twitter.Api(username=self.twitter_user.username,
                              password=self.twitter_user.password)
            tweet = api.PostUpdate(self.tweet)
            self.tweet_id = tweet.id
            self.posted = dateutils.parse(tweet.created_at).astimezone(tzlocal()).replace(tzinfo=None)
        super(Tweet, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        api = twitter.Api(username=self.twitter_user.username,
                          password=self.twitter_user.password)
        api.DestroyStatus(self.tweet_id)
        super(Tweet, self).delete(*args, **kwargs)