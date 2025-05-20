from django import template

register = template.Library()

@register.filter
def get_item(dictionnaire, cle):
    return dictionnaire.get(cle)
