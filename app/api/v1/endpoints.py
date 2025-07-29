import uuid
from fastapi import UploadFile, APIRouter
from csv_remapper_lib import CSVFile

from app.api.v1.schemas import RenameKeyModel

router = APIRouter()

@router.post("/create_csv_object/")
async def create_upload_file(file: UploadFile):
    contents = await file.read()
    # TODO: Analyze file toprevent security risks
    # Save file
    unique_uid = uuid.uuid4()
    csv_route = "files/%s" % (str(unique_uid) + ".csv")
    with open(csv_route, "x") as f:
        str_content = contents.decode()
        f.write(contents.decode().replace("\r\n", "\n"))
    return {"csv_uuid": str(unique_uid)}

@router.post("/rename_key/")
def rename_key(key_names: RenameKeyModel):
    if key_names.file_uuid == "":
        return {"Error, file not found"}
    # Found file
    csv_route = "files/%s" % (str(key_names.file_uuid) + ".csv")
    csv = CSVFile(csv_route)
    csv.rename_key(key_names.key_names[0], key_names.key_names[1])
    csv.save()
    return {"Rename success"}

@router.post("/remove_key/")
def rename_key(key_names: RenameKeyModel):
    if key_names.file_uuid == "":
        return {"Error, file not found"}
    # Found file
    csv_route = "files/%s" % (str(key_names.file_uuid) + ".csv")
    csv = CSVFile(csv_route)
    csv.rename_key(key_names.key_names[0], key_names.key_names[1])
    csv.save()
    return {"Rename success"}