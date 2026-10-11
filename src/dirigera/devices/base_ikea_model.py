from pydantic import BaseModel


def to_camel(string: str) -> str:
    string_split = string.split("_")
    return string_split[0] + "".join(word.capitalize() for word in string_split[1:])


class BaseIkeaModel(BaseModel, arbitrary_types_allowed=True, alias_generator=to_camel):
    def _copy_from(self, other: "BaseIkeaModel") -> None:
        """Overwrite all fields of this instance with the values of another one."""
        for name in type(self).model_fields:
            setattr(self, name, getattr(other, name))
