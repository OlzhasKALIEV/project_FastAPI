import pandas as pd
import io
from fastapi import FastAPI, UploadFile, File, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()

security = HTTPBasic()


@app.get("/users/")
def read_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    return {"username": credentials.username, "password": credentials.password}


@app.post("/table", dependencies=[Depends(read_current_user)])
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    file_obj = io.BytesIO(contents)
    df = pd.read_csv(file_obj)
    columns = df.columns.tolist()
    return {"filename": file.filename, "columns": columns}


@app.post("/process", dependencies=[Depends(read_current_user)])
async def process_file(file: UploadFile = File(...), filter_column: str = None, filter_value: str = None,
                       sort_columns: str = None):
    contents = await file.read()
    file_obj = io.BytesIO(contents)
    df = pd.read_csv(file_obj)

    if filter_column and filter_value:
        filtered_df = df[df[filter_column] == float(filter_value)]
    else:
        filtered_df = df

    if sort_columns:
        sort_columns = sort_columns.split(",")
        filtered_df = filtered_df.sort_values(by=sort_columns)

    result = filtered_df.to_dict(orient="records")

    return {"filename": file.filename, "data": result}
