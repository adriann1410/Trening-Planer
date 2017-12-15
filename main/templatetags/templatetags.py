from django import template

register = template.Library()

@register.inclusion_tag("tags_templates/horizontal_form.html")
def horizontal_form(fields):
    return {'fields': fields}
