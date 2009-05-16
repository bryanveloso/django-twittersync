from django.template import Library
from django.utils.safestring import mark_safe
import re

register = Library()

@register.filter(name='at_reply')
def twitter_at_reply(tweet):
    # http://www.djangosnippets.org/snippets/848/
    pattern = re.compile(r"(\A|\W)@(?P<user>\w+)(\Z|\W)")
    repl = (r'\1@<a href="http://twitter.com/\g<user>"'
            r' title="\g<user> on Twitter">\g<user></a>\3')

    return mark_safe(pattern.sub(repl, tweet))