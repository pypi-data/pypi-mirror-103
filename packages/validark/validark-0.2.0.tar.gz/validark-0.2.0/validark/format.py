import re


def camel_to_snake(value: str) -> str:
    value = re.sub(r"[\-\.\s]", '_', str(value))
    return (value[0].lower() +
            re.sub(r"[A-Z]", lambda matched: '_' +
                   matched.group(0).lower(), value[1:]))


def snake_to_camel(value: str) -> str:
    value = re.sub(r"^[\-_\.]", '', str(value))
    return (value[0].lower() +
            re.sub(r"[\-_\.\s]([A-Za-z])",
                   lambda matched: matched.group(1).upper(), value[1:]))


def normalize(data, format='camel'):
    if isinstance(data, (str, int, float, bool, type(None))):
        return data

    if isinstance(data, (list, tuple)):
        return [normalize(item, format) for item in data]

    format_function = snake_to_camel if format == 'camel' else camel_to_snake

    normalized_data = {}
    for key, value in data.items():
        if not isinstance(value, (str, int, float, bool)):
            value = normalize(value, format)
        normalized_data[format_function(key)] = value

    return normalized_data
