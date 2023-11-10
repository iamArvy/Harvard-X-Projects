from django import template
import markdown as md

register = template.Library()

@register.filter(name='markdown')
def markdown_filter(text):
    return md.markdown(text, extensions=['markdown.extensions.extra'])
