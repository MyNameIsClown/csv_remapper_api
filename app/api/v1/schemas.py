from pydantic import BaseModel
from csv_remapper_lib import MergeType

class RenameKeyModel(BaseModel):
    key_names: list[str]

class RenameKeysModel(BaseModel):
    key_dict: dict

class RemoveKeyModel(BaseModel):
    key_name: str

class RemoveKeysModel(BaseModel):
    key_names: list[str]

class NormalizeValueModel(BaseModel):
    mode: str
    key: str

class MergeConnectorModel(BaseModel):
    type: MergeType
    operator: str = "+"
    delimiter: str = ""
    time_format: str = ""


class MergeKeysModel(BaseModel):
    ordered_keys: list[str]
    connector: MergeConnectorModel
    new_key_name: str
