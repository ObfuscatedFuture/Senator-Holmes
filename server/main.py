from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# "html=True" automatically serves index.html at the root of the mount path
app.mount("/", StaticFiles(directory="./client", html=True), name="static")