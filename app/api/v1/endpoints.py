import os
import re
import ast
import uuid
from datetime import datetime
from fastapi import UploadFile, APIRouter, HTTPException, status, Body
from fastapi.responses import FileResponse, JSONResponse
from csv_remapper_lib import CSVFile, ConnectorType
from cryptography.fernet import Fernet

from app.api.v1.schemas import (
    RenameKeyModel,
    RenameKeysModel,
    RemoveKeyModel,
    RemoveKeysModel,
    NormalizeValueModel,
    MergeKeysModel,
    TransformModel
)
from app.api.v1.utils import (
    check_file_id_exists,
    convert_python_types_to_string
)

router = APIRouter(prefix="/csv-file")

# Ensure the files directory exists for storing CSVs
os.makedirs("files", exist_ok=True)

@router.post("/")
async def create_file(file: UploadFile):
    contents = await file.read()
    # TODO: Analyze file to prevent security risks
    if not re.search(r"\.(csv|tsv)$", file.filename, re.IGNORECASE):
        raise HTTPException(status_code=400, detail="File type not supported")
    # Save file
    file_id = str(uuid.uuid4())
    csv_route = "files/%s.csv" % (file_id)
    os.makedirs(os.path.dirname(csv_route), exist_ok=True)
    with open(csv_route, "x") as f:
        f.write(contents.decode().replace("\r\n", "\n"))
    # Return File id
    csv = CSVFile(csv_route)
    csv_types = convert_python_types_to_string(csv.all_key_types())
    
    data = {
        "file_id": file_id,
        "types": csv_types
    }
    return data

@router.get("/{file_id}")
def get_csv_info(file_id:str):
    csv_route = check_file_id_exists(file_id)
    csv = CSVFile(csv_route)
    try:
        info = convert_python_types_to_string(csv.all_key_types())
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return info

@router.put("/{file_id}/rename-key/")
def rename_key(file_id: str, rename_key_model: RenameKeyModel):
    csv_route = check_file_id_exists(file_id)
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
    csv_route = check_file_id_exists(file_id)
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
    csv_route = check_file_id_exists(file_id)
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
    csv_route = check_file_id_exists(file_id)
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
    csv_route = check_file_id_exists(file_id)
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
    csv_route = check_file_id_exists(file_id)
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


@router.post("/{file_id}/transform")
def transformed_file(file_id: str, data: list[TransformModel] = Body(...)):
    # Found file
    csv_route = check_file_id_exists(file_id)
    csv = CSVFile(csv_route)
    renaming_keys = {}
    removing_keys = []
    for item in data:
        # Check for key remove
        if item.is_active:
            # Check for key name changes
            if item.new_key_name:
                renaming_keys[item.old_key_name] = item.new_key_name
            # Check for key type changes
            if item.new_type == "positive_number":
                csv.to_positive_number(item.old_key_name)
            elif item.new_type == "negative_number":
                csv.to_negative_number(item.old_key_name)
            elif item.new_type == "datetime":
                csv.to_date(item.old_key_name)
        else:
            removing_keys.append(item.old_key_name)

    if removing_keys:
        csv.remove_keys(removing_keys)
    if renaming_keys:
        csv.rename_keys(renaming_keys)
    
    
    # Create files_response folder
    new_csv_route = "files_response/%s_transformed.csv" % (file_id)
    os.makedirs(os.path.dirname(new_csv_route), exist_ok=True)
    csv.save(new_csv_route)
    return FileResponse(new_csv_route)

@router.post("/{file_id}/encrypt_config_file")
def encrypt_config_file(file_id: str, configuration: list[TransformModel] = Body(...)):
    config_file = "config_files/%s_config.cfg" % (file_id)
    os.makedirs(os.path.dirname(config_file), exist_ok=True)
    # Write configuration
    with open(config_file, "w") as f:
        f.write("[")
        for i, config in enumerate(configuration):
            f.write(str(config.model_dump()))
            if i < len(configuration) - 1:
                f.write(",")
        f.write("]")
    
    with open(config_file) as f:
        original = f.read().encode()
    
    
    raw_file_key = os.environ["FILE_ENCRYPT_KEY"]
    key = raw_file_key.encode("utf-8") 
    fernet = Fernet(key)
    encrypted = fernet.encrypt(original).decode()
    # Write configuration
    with open(config_file, "w") as f:
        f.write(encrypted)

    return FileResponse(config_file)

@router.post("/{file_id}/decrypt_config_file")
def decrypt_config_file(file_id: str, file: UploadFile):
    original = file.file.read()
    raw_file_key = os.environ["FILE_ENCRYPT_KEY"]
    key = raw_file_key.encode("utf-8") 
    fernet = Fernet(key)
    decrypted = fernet.decrypt(original).decode()
    data = ast.literal_eval(decrypted)
    return JSONResponse(content=data)