# filepath: d:\PROJECTS\Bike-spare-parts-Project\MomentumSpares\cart\templatetags\custom_filters.py
from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    """Adds a CSS class to a Django form field widget."""
    if hasattr(field, 'as_widget'):
        return field.as_widget(attrs={'class': css_class})
    return field  # Return the field as-is if it's not a form field