from fastapi import FastAPI
from pydantic import BaseModel
from utils import generateSchTable, getSchedule
from undistributedUtils import undistGetSchedule

app = FastAPI()

class Req(BaseModel):
    employees: list
    shifts: list
    hour_bank: int
    flex_hours: int

@app.get("/")
def root():
    return {"hello": "world"}

@app.post("/scheduleJason")
def schedule(req: Req):
    employees = req.employees
    shifts = req.shifts
    hour_bank = req.hour_bank
    flex_hours = req.flex_hours
    schTable = generateSchTable(employees, shifts)
    schedule = getSchedule(employees, shifts, schTable, hour_bank, flex_hours)
    return schedule

@app.post("/undistributed-schedule")
def undist_schedule(req: Req):
    """
    Generate Schedule Without Equal Distribution.
    """
    employees = req.employees
    shifts = req.shifts
    schedule = undistGetSchedule(employees, shifts)
    return schedule


