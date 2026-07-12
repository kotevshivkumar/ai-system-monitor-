from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
app = FastAPI()
templates = Jinja2Templates(directory="templates")
devices = {}

class SystemData(BaseModel):
    hostname: str
    operating_system: str
    cpu_usage: float
    ram_usage: float
    disk_usage: float

@app.get("/")
def home():
    return {"message": "AI Monitoring Server is Running"}

@app.post("/system")
def receive_data(data: SystemData):

    devices[data.hostname] = data.dict()

    print("\n====== DATA RECEIVED ======")
    print(data)

    return {"status": "received"}

@app.get("/devices")
def get_devices():
    return devices

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "devices": devices
        }
    )