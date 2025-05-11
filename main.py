import math
import pandas as pd
from fastapi import FastAPI, UploadFile, Form
import tempfile
from functions import *
from fastapi.responses import HTMLResponse
from fastapi import Request
from fastapi.templating import Jinja2Templates


app = FastAPI(title="Excel Analysis API")
templates = Jinja2Templates(directory="templates")


def save_uploaded_file(upload_file: UploadFile):
    suffix = '.' + upload_file.filename.split('.')[-1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(upload_file.file.read())
        return tmp.name

# POST Endpoints
@app.post("/load_by_quarter/")
async def filter_by_quarter(file: UploadFile, date_column: str = Form(...), quarter_str: str = Form(...)):
    path = save_uploaded_file(file)
    df = load_and_filter_by_quarter(path, date_column, quarter_str)
    
    # Replace NaN and Inf with None (or 0 if you prefer)
    df = df.applymap(lambda x: None if isinstance(x, (float)) and (math.isnan(x) or math.isinf(x)) else x)
    
    return df.to_dict(orient='records')


@app.post("/zero_interest_accounts/")
async def zero_interest_accounts(file: UploadFile, int_rate_col: str = Form(...)):
    path = save_uploaded_file(file)
    df = get_zero_interest_accounts(path, int_rate_col)
    
    # Replace NaN and Inf with None
    df = df.applymap(lambda x: None if isinstance(x, (float)) and (math.isnan(x) or math.isinf(x)) else x)
    
    return df.to_dict(orient='records')


    
    


# GET Endpoint to render an HTML page with available API endpoints
@app.get("/access_all_apis", response_class=HTMLResponse)
async def access_all_apis(request: Request):  # Pass the Request object
    return templates.TemplateResponse("index.html", {"request": request})  # Correct the context with the request object
