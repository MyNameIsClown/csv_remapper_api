from pydantic import BaseModel

class RenameKeyModel(BaseModel):
    file_uuid: str
    key_names: list[str]