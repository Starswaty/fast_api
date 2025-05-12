import os
import io
import uuid
import math
import pandas as pd
from fastapi import FastAPI, UploadFile, Form
import tempfile
from functions import *
from fastapi.responses import HTMLResponse
from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse


app = FastAPI(title="Excel Analysis API")
templates = Jinja2Templates(directory="templates")

OUTPUT_DIR = "saved_outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def save_output_excel(df, base_filename):
    output_path = os.path.join(OUTPUT_DIR, f"{base_filename}_{uuid.uuid4().hex}.xlsx")
    df.to_excel(output_path, index=False)
    return output_path

# POST Endpoints

@app.post("/zero_interest_accounts/")
async def zero_interest_accounts(file: UploadFile, int_rate_col: str = Form(...)):
    df = get_zero_interest_accounts(io.BytesIO(await file.read()), int_rate_col)
    output_file = save_output_excel(df, "zero_interest_accounts")
    return FileResponse(output_file, filename=os.path.basename(output_file))

@app.post("/get_matured_with_balance/")  
async def matured_with_balance(file: UploadFile, maturity_col: str = Form(...), balance_col: str = Form(...), cutoff_date: str = Form(...)):
    df = get_matured_with_balance(io.BytesIO(await file.read()), maturity_col, balance_col, cutoff_date)
    output_file = save_output_excel(df, "matured_with_balance")
    return FileResponse(output_file, filename=os.path.basename(output_file))

@app.post("/disbursement_and_writeoff/")
async def disbursement_and_writeoff_api(
    file: UploadFile,
    disbursement_column: str = Form(...),
    writeoff_column: str = Form(...),
    account_number_column: str = Form(...),
    cif_id_column: str = Form(...),
    disbursement_months: str = Form(...)  # Comma-separated e.g., "1,2,3"
):
    months = list(map(int, disbursement_months.split(',')))
    df = disbursement_and_writeoff(io.BytesIO(await file.read()), disbursement_column, writeoff_column, account_number_column, cif_id_column, months)
    output_file = save_output_excel(df, "disbursement_writeoff")
    return FileResponse(output_file, filename=os.path.basename(output_file))

@app.post("/disbursement_and_npa/")
async def disbursement_and_npa_api(
    file: UploadFile,
    disbursement_column: str = Form(...),
    npa_column: str = Form(...),
    account_number_column: str = Form(...),
    cif_id_column: str = Form(...),
    disbursement_months: str = Form(...)  # Comma-separated e.g., "1,2,3"
):
    months = list(map(int, disbursement_months.split(',')))
    df = disbursement_and_npa(io.BytesIO(await file.read()), disbursement_column, npa_column, account_number_column, cif_id_column, months)
    output_file = save_output_excel(df, "disbursement_npa")
    return FileResponse(output_file, filename=os.path.basename(output_file))

@app.post("/same_day_closure_disbursement/")
async def same_day_closure_disbursement(file: UploadFile, disbursement_column: str = Form(...), closure_date: str = Form(...)):
    df = get_same_day_closure_disbursement(io.BytesIO(await file.read()), disbursement_column, closure_date)
    output_file = save_output_excel(df, "same_day_closure_disbursement")
    return FileResponse(output_file, filename=os.path.basename(output_file))

@app.post("/filter_by_quarter/")
async def filter_by_quarter(file: UploadFile, date_column: str = Form(...), quarter_str: str = Form(...)):
    df = load_and_filter_by_quarter(io.BytesIO(await file.read()), date_column, quarter_str)
    output_file = save_output_excel(df, "filtered_by_quarter")
    return FileResponse(output_file, filename=os.path.basename(output_file))

    
    


# GET Endpoint to render an HTML page with available API endpoints
@app.get("/access_all_apis", response_class=HTMLResponse)
async def access_all_apis(request: Request):  # Pass the Request object
    return templates.TemplateResponse("index.html", {"request": request})  # Correct the context with the request object
