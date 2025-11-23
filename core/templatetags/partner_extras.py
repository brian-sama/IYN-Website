from django import template
from core.models import Partner

register = template.Library()

@register.simple_tag
def get_partner_by_name(name):
    try:
        return Partner.objects.get(name=name)
    except Partner.DoesNotExist:
        return None
