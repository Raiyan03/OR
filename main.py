from fastapi import FastAPI
from pydantic import BaseModel
from utils import generateSchTable, getSchedule
from undistributedUtils import undistGetSchedule

app = FastAPI()

class req(BaseModel):
    employees : list
    shifts : list

@app.get("/")
def root():
    return{"hello": "world"}


@app.post("/schedule")
def Schedule(req: req):
    """
    Generate Equally Distributed Schedule.

    This endpoint generates a schedule where shifts are equally distributed 
    among employees based on their preferences. Unavailability ('NA') is 
    respected to ensure employees are not scheduled for shifts they cannot work.

    Args:
        req (RequestBody): The request body containing the list of employees and shifts.

    Returns:
        dict: A dictionary containing the generated schedule, objective value, 
        and solver statistics.
    """
    employees = req.employees
    shifts = req.shifts
    schTable = generateSchTable(employees, shifts)
    schedule = getSchedule(employees, shifts, schTable)
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
    schedule = undistGetSchedule(employees, shifts)
    return schedule
