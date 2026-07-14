from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")

# Store connected devices
devices = {}

# Dashboard
@app.get("/")
def home(request: Request):
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
    devices[hostname] = data
    return {"status": "received"}