from django import template

register = template.Library()


@register.simple_tag
def relative_url(value, field_name, urlencode=None):
    url = '?{}={}'.format(field_name, value)
    if urlencode:
        querystring = urlencode.split('&')
        filtered_querystring = filter(lambda p: p.split('=')[0] != field_name,
                                      querystring)
        encoded_querystring = '&'.join(filtered_querystring)
        url = '{}&{}'.format(url, encoded_querystring)
    return url


@register.filter
def is_list(value):
    return isinstance(value, list)


@register.filter
def replace_underscores(value):
    return value.replace('_', ' ')


@register.filter
def is_url(value):
    try:
        return value.startswith('www') or value.startswith('http')
    except AttributeError:
        return False


@register.filter
def proper_label(value):
    if value == 'types':
        return 'Genre (Type)'
    if value == 'instruments':
        return 'Instrument or Voice'
    if value == 'composers':
        return 'Composer'
    if value == 'styles':
        return 'Genre (Style)'
    if value == 'sacred_or_secular':
        return 'Sacred/Secular'
    if value == 'certainty':
        return 'Attribution'
    else:
        return value


@register.filter
def get_model_name(value):
    return value._meta.db_table


@register.filter
def get_number_of_messages(value):
    return len(value._loaded_messages)
