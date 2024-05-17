from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()

class req(BaseModel):
    employees : list
    shifts : list

@app.get("/")
def root():
    return{"hello": "world"}


@app.post("/schedule")
def getSchedule(req: req):
    print(req)
    return req