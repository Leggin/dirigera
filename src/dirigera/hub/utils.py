import functools
import re
from typing import Dict, List, Union


def camelize_dict(d: Union[Dict, List]):
    camelize = functools.partial(re.sub, r"_([a-z])", lambda m: m.group(1).upper())

    if isinstance(d, list):
        return [camelize_dict(i) if isinstance(i, (dict, list)) else i for i in d]
    return {
        camelize(a): camelize_dict(b) if isinstance(b, (dict, list)) else b
        for a, b in d.items()
    }
