import pytest
import uuid
from fastapi import HTTPException, status
from app.api.v1.endpoints import (
    rename_key, rename_keys, remove_key, remove_keys,
    normalize_values, merge_keys
)
from app.api.v1.schemas import (
    RenameKeyModel, RenameKeysModel, RemoveKeyModel, RemoveKeysModel,
    NormalizeValueModel, MergeKeysModel, MergeConnectorModel
)
from csv_remapper_lib import MergeType


class DummyCSV:
    def __init__(self, path):
        self.path = path
        self.saved = False

    def rename_key(self, old, new):
        if old == "fail":
            raise Exception("rename error")

    def rename_keys(self, mapping):
        if "fail" in mapping:
            raise Exception("rename keys error")

    def remove_key(self, key):
        if key == "fail":
            raise Exception("remove error")

    def remove_keys(self, keys):
        if "fail" in keys:
            raise Exception("remove keys error")

    def to_positive_number(self, key):
        if key == "fail":
            raise Exception("normalize error")

    def to_negative_number(self, key):
        pass

    def to_date(self, key):
        pass

    def merge_keys(self, ordered_key_list, connector, new_key_name):
        if new_key_name == "fail":
            raise Exception("merge error")

    def save(self):
        self.saved = True


@pytest.fixture(autouse=True)
def patch_file_exists_and_csv(monkeypatch):
    # Always simulate that the file exists and CSVFile is DummyCSV
    monkeypatch.setattr(
        "app.api.v1.endpoints.file_exists", lambda path: True
    )
    monkeypatch.setattr(
        "app.api.v1.endpoints.CSVFile", DummyCSV
    )


def test_rename_key_success():
    model = RenameKeyModel(key_names=["a", "b"])
    result = rename_key(str(uuid.uuid4()), model)
    assert result == "Success"


def test_rename_key_missing_file(monkeypatch):
    # Simulate missing file
    monkeypatch.setattr(
        "app.api.v1.endpoints.file_exists", lambda path: False
    )
    with pytest.raises(HTTPException) as exc:
        rename_key("1234", RenameKeyModel(key_names=["a", "b"]))
    assert exc.value.status_code == status.HTTP_400_BAD_REQUEST


def test_rename_key_exception():
    with pytest.raises(HTTPException) as exc:
        rename_key("1234", RenameKeyModel(key_names=["fail", "b"]))
    assert exc.value.status_code == status.HTTP_400_BAD_REQUEST


def test_rename_keys_success():
    mapping = {"x": "y"}
    model = RenameKeysModel(key_dict=mapping)
    assert rename_keys(str(uuid.uuid4()), model) == "Success"


def test_rename_keys_exception():
    with pytest.raises(HTTPException):
        rename_keys("1234", RenameKeysModel(key_dict={"fail": "y"}))


def test_remove_key_success():
    model = RemoveKeyModel(key_name="a")
    assert remove_key(str(uuid.uuid4()), model) == "Success"


def test_remove_key_exception():
    with pytest.raises(HTTPException):
        remove_key("1234", RemoveKeyModel(key_name="fail"))


def test_remove_keys_success():
    model = RemoveKeysModel(key_names=["a", "b"])
    assert remove_keys(str(uuid.uuid4()), model) == "Success"


def test_remove_keys_exception():
    with pytest.raises(HTTPException):
        remove_keys("1234", RemoveKeysModel(key_names=["fail"]))


def test_normalize_values_positive():
    model = NormalizeValueModel(key="a", mode="to_positive")
    assert normalize_values(str(uuid.uuid4()), model) == "Success"


def test_normalize_values_negative():
    model = NormalizeValueModel(key="a", mode="to_negative")
    assert normalize_values(str(uuid.uuid4()), model) == "Success"


def test_normalize_values_date():
    model = NormalizeValueModel(key="a", mode="to_date")
    assert normalize_values(str(uuid.uuid4()), model) == "Success"


def test_normalize_values_exception():
    with pytest.raises(HTTPException):
        normalize_values("1234", NormalizeValueModel(key="fail", mode="to_positive"))


def test_merge_keys_success():
    connector = MergeConnectorModel(type=MergeType.TEXT, operator="", delimiter="-", time_format="")
    model = MergeKeysModel(
        ordered_keys=["a", "b"],
        connector=connector,
        new_key_name="merged"
    )
    assert merge_keys(str(uuid.uuid4()), model) == "Merge complete"


def test_merge_keys_exception():
    connector = MergeConnectorModel(type=MergeType.TEXT, operator="", delimiter="-", time_format="")
    model = MergeKeysModel(
        ordered_keys=["a"],
        connector=connector,
        new_key_name="fail"
    )
    with pytest.raises(HTTPException):
        merge_keys("1234", model)