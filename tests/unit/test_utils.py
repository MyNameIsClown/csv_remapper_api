import pytest
from app.api.v1.utils import file_exists

def test_file_exists_true(tmp_path):
    # Create a temporary file and ensure file_exists returns True
    temp_file = tmp_path / "temp.txt"
    temp_file.write_text("hello world")
    assert file_exists(str(temp_file)) is True


def test_file_exists_false(tmp_path):
    # Check a nonexistent file returns False
    fake_file = tmp_path / "does_not_exist.txt"
    assert file_exists(str(fake_file)) is False