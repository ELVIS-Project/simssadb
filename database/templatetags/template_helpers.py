from django import template

register = template.Library()


@register.simple_tag
def relative_url(value, field_name, urlencode=None):
    url = "?{}={}".format(field_name, value)
    if urlencode:
        querystring = urlencode.split("&")
        filtered_querystring = filter(
            lambda p: p.split("=")[0] != field_name, querystring
        )
        encoded_querystring = "&".join(filtered_querystring)
        url = "{}&{}".format(url, encoded_querystring)
    return url


@register.filter
def is_list(value):
    return isinstance(value, list)


@register.filter
def replace_underscores(value):
    return value.replace("_", " ")


@register.filter
def is_url(value):
    try:
        return value.startswith("www") or value.startswith("http")
    except AttributeError:
        return False


@register.filter
def proper_label(value):
    if value == "types":
        return "Genre (Type)"
    if value == "instruments":
        return "Instrument or Voice"
    if value == "composers":
        return "Composer"
    if value == "styles":
        return "Genre (Style)"
    if value == "sacred_or_secular":
        return "Sacred/Secular"
    if value == "certainty":
        return "Attribution"
    else:
        return value


@register.filter
def get_model_name(value):
    return value._meta.db_table


@register.filter
def get_number_of_messages(value):
    return len(value._loaded_messages)


@register.filter
def group_order(val, key): # Return a GroupedResult using collections.OrderedDict?
    order_map = {
        'Pitch Statistics Feature': 0,
        'Melodic Interval Features': 1,
        'Chords and Vertical Interval Features': 2,
        'Musical Texture Features': 3,
        'Rhythm Features': 4,
        'Rhythm and Tempo Features': 5,
        'Instrumentation Features': 6,
        'Dynamics Features': 7,
    }
    return sorted(val, key=lambda x: order_map.get(x.grouper))

@register.filter
def proper_group(value):
    if value == "P" or value == "Pitch Statistics Features":
        return "Overall Pitch Statistic Features"
    if value == "M" or value == "Melodic Interval Features":
        return "Melodic Interval Features"
    if value == "C" or value == "Chords and Vertical Interval Features":
        return "Chord and Vertical Interval Features"
    if value == "T" or value == "Musical Texture Features":
        return "Texture Features"
    if value == "R" or value == "Rhythm Features":
        return "Rhythm Features (Excluding Tempo)"
    if value == "RT" or value == "Rhythm and Tempo Features":
        return "Rhythm Features (Incorporating Tempo)"
    if value == "I" or value == "Instrumentation Features":
        return "Instrumentation Features"
    if value == "D" or value == "Dynamics Features":
        return "Dynamics Features"
    else:
        return value