from fastapi import FastAPI
from pydantic import BaseModel
from utils import generateSchTable, getSchedule
from testUtils import TestgetSchedule, TestgenerateSchTable

app = FastAPI()

class req(BaseModel):
    employees: list
    shifts: list
    hour_bank: int
    flex_hours: int

@app.get("/")
def root():
    return {"hello": "world"}

@app.post("/scheduleJason")
def Schedule(req: req):
    employees = req.employees
    shifts = req.shifts
    hour_bank = req.hour_bank
    flex_hours = req.flex_hours
    schTable = generateSchTable(employees, shifts)
    schedule = getSchedule(employees, shifts, schTable, hour_bank, flex_hours)
    return schedule

@app.post("/undistributed-schedule")
def Schedule(req: req):
    """
    Generate Schedule Without Equal Distribution.

    This endpoint generates a schedule without ensuring equal distribution of 
    shifts among employees. It focuses on covering all shifts based on employee 
    availability and preferences, without prioritizing equal shift distribution.

    Args:
        req (RequestBody): The request body containing the list of employees and shifts.

    Returns:
        dict: A dictionary containing the generated schedule.
    """
    employees = req.employees
    shifts = req.shifts
    hour_bank = req.hour_bank
    schTable = TestgenerateSchTable(employees, shifts)
    schedule = TestgetSchedule(employees, shifts, schTable, hour_bank)
    return schedule

