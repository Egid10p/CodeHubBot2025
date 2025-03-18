import threading
import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "El servidor está corriendo 🔥"}

@app.head("/")
async def head_home():
    return {}

@app.get("/status")
def status():
    return {"status": "online"}

def run_server():
    uvicorn.run(app, host="0.0.0.0", port=8000)

def keep_alive():
    server = threading.Thread(target=run_server)
    server.start()
