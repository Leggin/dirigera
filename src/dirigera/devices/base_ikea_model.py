from pydantic import BaseModel, ConfigDict, alias_generators


class BaseIkeaModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=alias_generators.to_camel, arbitrary_types_allowed=True
    )
