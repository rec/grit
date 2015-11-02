from __future__ import (
    absolute_import, division, print_function, unicode_literals)


def split_config(lines):
    def get_chunks():
        chunk = []
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if line.startswith('['):
                if chunk:
                    yield chunk
                chunk = []
            chunk.append(line)
        if chunk:
            yield chunk

    result = {}
    for chunk in get_chunks():
        name_parts = chunk[0][1:-1].split()
        dict_parts = {}
        for part in chunk[1:]:
            k, v = part.split('=')
            dict_parts[k.strip()] = v.strip()
        if len(name_parts) == 1:
            result[name_parts[0]] = dict_parts
        else:
            category, value = name_parts
            result.setdefault(category, {})[value[1:-1]] = dict_parts
    return result


def get_project(config):
    name, project = config['remote']['origin']['url'].split('/')[-2:]
    return name, project[:-4]
