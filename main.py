from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import time

app = FastAPI()

templates = Jinja2Templates(directory="templates")

# Store connected devices
devices = {}

# Dashboard

@app.get("/")
def home(request: Request):

    current_time = time.time()

    for hostname in devices:
        if current_time - devices[hostname]["last_seen"] < 15:
            devices[hostname]["status"] = "ONLINE"
        else:
            devices[hostname]["status"] = "OFFLINE"

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "request": request,
            "devices": devices
        }
    )
# Receive data from client PCs
@app.post("/system")
def receive_data(data: dict):
    hostname = data["hostname"]

    # Save the time when data was received
    data["last_seen"] = time.time()

    devices[hostname] = data

    return {"status": "received"}@app.get("/")
def home(request: Request):

    for hostname, data in devices.items():

        seconds = (time.now() - data["last_seen"]).total_seconds()

        if seconds <= 15:
            data["status"] = "ONLINE"
    return {"status": "received"}