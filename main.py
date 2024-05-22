from fastapi import FastAPI
from pydantic import BaseModel
from utils import generateSchTable, getSchedule
app = FastAPI()

class req(BaseModel):
    employees : list
    shifts : list
    high_traffic: list

@app.get("/")
def root():
    return{"hello": "world"}


@app.post("/schedule")
def Schedule(req: req):
    employees = req.employees
    shifts = req.shifts
    high_traffic = req.high_traffic
    schTable = generateSchTable(employees, shifts)
    schedule = getSchedule(employees, shifts, schTable, high_traffic)
    return schedule