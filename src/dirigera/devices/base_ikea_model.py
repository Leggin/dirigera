from pydantic import BaseModel


def to_camel(string: str) -> str:
    string_split = string.split("_")
    return string_split[0] + "".join(word.capitalize() for word in string_split[1:])


class BaseIkeaModel(BaseModel, arbitrary_types_allowed=True, alias_generator=to_camel):
    pass
