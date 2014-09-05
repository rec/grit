from __future__ import absolute_import, division, print_function, unicode_literals

def compose_on_keys(keys, dicts):
    """Compose dictionaries on a list of keys we understand."""
    settings = {}

    for key in keys:
        for d in dicts:
            value = d.get(key)
            if value:
                settings[key] = value
                break
    return settings
