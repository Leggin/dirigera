import functools
import re
from typing import Dict, List, Union


def camelize_dict(data: Union[Dict, List]) -> Dict:
    camelize = functools.partial(re.sub, r"_([a-z])", lambda m: m.group(1).upper())

    if isinstance(data, list):
        return [camelize_dict(i) if isinstance(i, (dict, list)) else i for i in data]
    return {
        camelize(a): camelize_dict(b) if isinstance(b, (dict, list)) else b
        for a, b in data.items()
    }
