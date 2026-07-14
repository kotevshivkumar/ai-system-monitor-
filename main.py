from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import time

app = FastAPI()

# Templates folder
templates = Jinja2Templates(directory="templates")

# Store connected devices
devices = {}

# Dashboard
@app.get("/")
def home(request: Request):

    current_time = time.time()

    for hostname, data in devices.items():

        seconds = current_time - data["last_seen"]

        print("Hostname:", hostname)
        print("Current Time:", current_time)
        print("Last Seen:", data["last_seen"])
        print("Difference:", seconds)

        if seconds <= 15:
            data["status"] = "ONLINE"
        else:
            data["status"] = "OFFLINE"
            print(devices)
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

    # Save the last time this PC contacted the server
    data["last_seen"] = time.time()

    devices[hostname] = data

    return {"status": "received"}