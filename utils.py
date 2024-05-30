from ortools.sat.python import cp_model
import json

class Employee:
    def __init__(self, name, shiftPref):
        self.emp_name = name
        self.shiftPref = shiftPref

""" 
This function is sourced from google OR-Tools examples https://developers.google.com/optimization/scheduling/employee_scheduling#python_21 and optimized using ChatGPT 4.0

prompt: ".. entire code snippet from undistributedUtils.py .. 'fix the code of taking unavailable shifts into account in the model.'"
"""
def getSchedule(employee_json, shifts_json, shift_requests):
    employees = [Employee(emp["name"], emp["shiftPref"]) for emp in employee_json]
    shifts = shifts_json

    num_employees = len(employees)
    num_shifts = len(shifts)
    num_days = 7
    all_employees = range(num_employees)
    all_shifts = range(num_shifts)
    all_days = range(num_days)

    model = cp_model.CpModel()
    shifts_var = {}
    for n in all_employees:
        for d in all_days:
            for s in all_shifts:
                shifts_var[(n, d, s)] = model.new_bool_var(f"shift_n{n}_d{d}_s{s}")

    for d in all_days:
        for s in all_shifts:
            model.add_exactly_one(shifts_var[(n, d, s)] for n in all_employees)

    for n in all_employees:
        for d in all_days:
            model.add_at_most_one(shifts_var[(n, d, s)] for s in all_shifts)

    min_shifts_per_employee = (num_shifts * num_days) // num_employees
    max_shifts_per_employee = min_shifts_per_employee + 1 if (num_shifts * num_days) % num_employees != 0 else min_shifts_per_employee

    for n in all_employees:
        num_shifts_worked = sum(shifts_var[(n, d, s)] for d in all_days for s in all_shifts)
        model.add(min_shifts_per_employee <= num_shifts_worked)
        model.add(num_shifts_worked <= max_shifts_per_employee)

    model.maximize(
        sum(
            shift_requests[n][d][s] * shifts_var[(n, d, s)]
            for n in all_employees
            for d in all_days
            for s in all_shifts
            if shift_requests[n][d][s] >= 0
        )
    )

    for n in all_employees:
        for d in all_days:
            for s in all_shifts:
                if shift_requests[n][d][s] == -1:
                    model.add(shifts_var[(n, d, s)] == 0)

    solver = cp_model.CpSolver()
    status = solver.solve(model)

    result = {"schedule": []}
    if status == cp_model.OPTIMAL:
        for d in all_days:
            day_schedule = {"day": d, "shifts": []}
            for n in all_employees:
                for s in all_shifts:
                    if solver.value(shifts_var[(n, d, s)]) == 1:
                        shift_detail = {
                            "employee": employees[n].emp_name,
                            "shift": shifts[s],
                            "requested": shift_requests[n][d][s] == 1
                        }
                        day_schedule["shifts"].append(shift_detail)
            result["schedule"].append(day_schedule)
        result["objective_value"] = solver.objective_value
    else:
        result["error"] = "No optimal solution found!"

    result["statistics"] = {
        "conflicts": solver.num_conflicts,
        "branches": solver.num_branches,
        "wall_time": solver.wall_time
    }

    return result

def generateShiftArray(num_shifts):
    return [0] * num_shifts

def generateUnavailableArray(num_shifts):
    return [-1] * num_shifts

""" 
This function is self written but optimized using ChatGPT 4.0 

prompt: ".. entire code snippet from undistributedUtils.py .. 'fix the code of taking unavailable shifts into account in the model.'"
"""

def generateSchTable(employees, shifts):
    num_shifts = len(shifts)
    days_of_week = ["Mon", "Tue", "Wed", "Thur", "Fri", "Sat", "Sun"]
    shiftReq = []

    for employee in employees:
        empArray = []
        for day in days_of_week:
            # shift_pref = employee['shiftPref'].get(day, "any")  # Default to "any" if not specified
            shift_pref = employee['shiftPref'].get(day, "any")
            print(shift_pref)
            if shift_pref == "any":
                empArray.append(generateShiftArray(num_shifts))
            elif shift_pref == "NA":
                empArray.append(generateUnavailableArray(num_shifts))
            else:
                shift_array = generateShiftArray(num_shifts)
                shift_array[int(shift_pref)] = 1
                empArray.append(shift_array)
        shiftReq.append(empArray)

    return shiftReq