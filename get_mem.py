#!/usr/bin/env python3
import json

MEMINFO = '/proc/meminfo'


def meminfo_to_dict(text_info):
    lines = [line for line in text_info.split('\n') if line != '']
    res = {}
    for line in lines:
        l, r = line.split(':')
        r = r.strip().split(' ')

        if len(r) == 2:
            value, unit = r
            res[l] = {
                'value': int(value),
                'unit': unit
            }
        else:
            value = int(r[0])
            res[l] = {
                'value': int(value),
                'unit': ''
            }
    return res


if __name__ == '__main__':
    with open(MEMINFO, 'r') as fp:
        meminfo = fp.read()
    meminfo = meminfo_to_dict(meminfo)

    total = meminfo['MemTotal']['value']
    free = meminfo['MemFree']['value']
    unit = meminfo['MemFree']['unit']
    print(json.dumps({
        'total': total,
        'free': free,
        'usage': total - free,
        'rate': round((total - free) * 100 / total, 2),
        'unit': unit
    }))
