import uvicorn
import uuid
from fastapi import FastAPI, File, UploadFile
from csv_remapper_lib import CSVFile
from pydantic import BaseModel

app = FastAPI()

class RenameKeyModel(BaseModel):
    file_uuid: str
    key_names: list[str]


@app.post("/create_csv_object/")
async def create_upload_file(file: UploadFile):
    contents = await file.read()
    unique_uid = uuid.uuid4()
    csv_route = "files/%s" % (str(unique_uid) + ".csv")
    # Save file
    with open(csv_route, "x") as f:
        str_content = contents.decode()
        f.write(contents.decode().replace("\r\n", "\n"))
    return {"csv_uuid": str(unique_uid)}

@app.post("/rename_key/")
def rename_key(key_names: RenameKeyModel):
    if key_names.file_uuid == "":
        return {"Error, file not found"}
    # Found file
    csv_route = "files/%s" % (str(key_names.file_uuid) + ".csv")
    csv = CSVFile(csv_route)
    csv.rename_key(key_names.key_names[0], key_names.key_names[1])
    csv.save()
    return {"Rename success"}

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)