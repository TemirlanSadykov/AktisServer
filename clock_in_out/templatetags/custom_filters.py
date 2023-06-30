from django import template
import datetime

register = template.Library()

@register.filter
def duration_format(seconds):
    duration = datetime.timedelta(seconds=seconds)
    hours = duration.seconds // 3600
    minutes = (duration.seconds % 3600) // 60
    seconds = duration.seconds % 60

    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"