from fastapi import FastAPI
from pydantic import BaseModel
from utils import generateSchTable, getSchedule
app = FastAPI()

class req(BaseModel):
    employees : list
    shifts : list

@app.get("/")
def root():
    return{"hello": "world"}


@app.post("/schedule")
def Schedule(req: req):
    employees = req.employees
    shifts = req.shifts
    schTable = generateSchTable(employees, shifts)
    schedule = getSchedule(employees, shifts, schTable)
    return schedule