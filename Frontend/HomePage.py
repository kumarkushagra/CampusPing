from fastapi import FastAPI, Form, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import csv
import os
import uvicorn

app = FastAPI()

# Set up templates and static files
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory=".")

@app.on_event("startup")
async def startup_event():
    # Check if the CSV file exists; if not, create it with headers
    if not os.path.exists("user_data.csv"):
        with open("user_data.csv", "w", newline="") as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(["Name","Tags","Roll Number", "Email ID", "Phone", ])

@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("test.html", {"request": request})

@app.post("/submit")
async def submit_form(
    name: str = Form(...),
    tags: str = Form(...),
    rollNumber: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...)
    
):
    # Append data to the CSV file
    with open("user_data.csv", "a", newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow([name, tags,rollNumber, email, phone ])

    return JSONResponse(content={"message": "Data submitted successfully!"})

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
