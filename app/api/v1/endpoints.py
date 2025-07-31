import os
import uuid
from fastapi import UploadFile, APIRouter, HTTPException, status
from csv_remapper_lib import CSVFile, ConnectorType

from app.api.v1.schemas import (
    RenameKeyModel,
    RenameKeysModel,
    RemoveKeyModel,
    RemoveKeysModel,
    NormalizeValueModel,
    MergeKeysModel
)
from .utils import file_exists

router = APIRouter(prefix="/csv-file")

# Ensure the files directory exists for storing CSVs
os.makedirs("files", exist_ok=True)

@router.post("/")
async def create_file(file: UploadFile):
    contents = await file.read()
    # TODO: Analyze file toprevent security risks
    # Save file
    file_id = str(uuid.uuid4())
    csv_route = "files/%s.csv" % (file_id)
    os.makedirs(os.path.dirname(csv_route), exist_ok=True)
    with open(csv_route, "x") as f:
        f.write(contents.decode().replace("\r\n", "\n"))
    # TODO: Start counter for remove file
    # Return File id
    return {"file_id": file_id}

@router.put("/{file_id}/rename-key/")
def rename_key(file_id: str, rename_key_model: RenameKeyModel):
    # Found file
    csv_route = "files/%s.csv" % (file_id)
    if not file_exists(csv_route):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"Error": "File not exists or has been deleted"})
    csv = CSVFile(csv_route)
    try:
        csv.rename_key(rename_key_model.key_names[0], rename_key_model.key_names[1])
        csv.save()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return "Success"

@router.put("/{file_id}/rename-keys/")
def rename_keys(file_id: str, rename_keys_model: RenameKeysModel):
    # Found file
    csv_route = "files/%s.csv" % (file_id)
    if not file_exists(csv_route):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"Error": "File not exists or has been deleted"})
    csv = CSVFile(csv_route)
    try:
        csv.rename_keys(rename_keys_model.key_dict)
        csv.save()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return "Success"

@router.put("/{file_id}/remove-key")
def remove_key(file_id: str, remove_key_model: RemoveKeyModel):
    # Found file
    csv_route = "files/%s.csv" % (file_id)
    if not file_exists(csv_route):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"Error": "File not exists or has been deleted"})
    csv = CSVFile(csv_route)
    try:
        csv.remove_key(remove_key_model.key_name)
        csv.save()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"Error": str(e)})
    return "Success"

@router.put("/{file_id}/remove-keys")
def remove_keys(file_id: str, remove_keys_model: RemoveKeysModel):
    # Found file
    csv_route = "files/%s.csv" % (file_id)
    if not file_exists(csv_route):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"Error": "File not exists or has been deleted"})
    csv = CSVFile(csv_route)
    try:
        csv.remove_keys(remove_keys_model.key_names)
        csv.save()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"Error": str(e)})
    return "Success"

@router.put("/{file_id}/normalize-values")
def normalize_values(file_id: str, normalize_model: NormalizeValueModel):
    # Found file
    csv_route = "files/%s.csv" % (file_id)
    if not file_exists(csv_route):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"Error": "File not exists or has been deleted"})
    csv = CSVFile(csv_route)
    try:
        if normalize_model.mode == "to_positive":
            csv.to_positive_number(normalize_model.key)
        elif normalize_model.mode == "to_negative":
            csv.to_negative_number(normalize_model.key)
        elif normalize_model.mode == "to_date":
            csv.to_date(normalize_model.key)
        csv.save()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"Error": str(e)})
    return "Success"

@router.put("/{file_id}/merge-keys")
def merge_keys(file_id: str, merge_keys_model: MergeKeysModel):
    # Found file
    csv_route = "files/%s.csv" % (file_id)
    if not file_exists(csv_route):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"Error": "File not exists or has been deleted"})
    csv = CSVFile(csv_route)
    try:
        connector = ConnectorType(
            type=merge_keys_model.connector.type,
            operator= merge_keys_model.connector.operator,
            delimiter=merge_keys_model.connector.delimiter,
            time_format=merge_keys_model.connector.time_format
        )
        csv.merge_keys(
            ordered_key_list=merge_keys_model.ordered_keys,
            connector=connector,
            new_key_name=merge_keys_model.new_key_name
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"Error": str(e)})
    csv.save()
    return "Merge complete"