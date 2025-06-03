from django import template
from datetime import datetime, timezone

register = template.Library()

@register.filter
def custom_natural_time(value):
    if not value:
        return ''

    now = datetime.now(timezone.utc)
    deltatime = now - value

    if deltatime.days == 0 and deltatime.seconds < 60:
        return 'just now'
    elif deltatime.days == 0 and deltatime.seconds < 3600:
        return f'{deltatime.seconds // 60} minutes ago'
    elif deltatime.days == 0:
        return f'{deltatime.seconds // 3600} hours ago'
    elif deltatime.days == 1:
        return 'yesterday'
    elif deltatime.days < 7:
        return f'{deltatime.days} days ago'
    else:
        return value.strftime("%d %B %Y")
