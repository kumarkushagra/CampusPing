import logging
from fastapi import FastAPI, Form, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import csv
import os

logging.basicConfig(level=logging.INFO)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.on_event("startup")
async def startup_event():
    if not os.path.exists("student_data.csv"):
        with open("student_data.csv", "w", newline="") as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(["Name", "Roll Number", "Email ID", "Phone", "Tags"])
    logging.info("CSV file setup complete.")

@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("test.html", {"request": request})

@app.post("/submit")
async def submit_form(
    name: str = Form(...),
    rollNumber: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    tags: str = Form(...)
):
    try:
        with open("student_data.csv", "a", newline="") as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow([name, rollNumber, email, phone, tags])
        logging.info(f"Data saved: {name}, {rollNumber}, {email}, {phone}, {tags}")
        return JSONResponse(content={"message": "Data submitted successfully!"})
    except Exception as e:
        logging.error(f"Error saving data: {e}")
        return JSONResponse(content={"message": "An error occurred."}, status_code=500)
