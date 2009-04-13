from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from twittersync.models import TwitterUser, Tweet

class TweetOptions(admin.ModelAdmin):
    list_display = ('title', 'posted')

    def title(self, instance):
        return "%s: %s" % (instance.twitter_user.username, instance.tweet)

class TwitterUserOptions(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        (_('These fields get automatically filled and updated on every update of your tweets.'), {
            'fields': ('twitter_id', 'location', 'name', 'image_url', 'homepage')
        }),
    )

admin.site.register(Tweet, TweetOptions)
admin.site.register(TwitterUser, TwitterUserOptions)