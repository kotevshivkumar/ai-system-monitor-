from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import time
from database import conn, cursor

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

    cursor.execute("""
    INSERT OR REPLACE INTO devices
    (hostname, username, operating_system, ip_address,
     cpu_usage, ram_usage, disk_usage, last_seen)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["hostname"],
        data["username"],
        data["operating_system"],
        data["ip_address"],
        data["cpu_usage"],
        data["ram_usage"],
        data["disk_usage"],
        data["last_seen"]
    ))

    conn.commit()
    devices[hostname] = data

    return {"status": "received"}