from ortools.sat.python import cp_model
import json
from helper import totalHours

class Employee:
    def __init__(self, name, shiftPref, status):
        self.emp_name = name
        self.shiftPref = shiftPref
        self.status = status  # 'fulltime' or 'parttime'

""" 
This function is self written but optimized using ChatGPT 4.0 

prompt: ".. entire code snippet from undistributedUtils.py .. 'fix the code of taking unavailable shifts into account in the model.'"
"""
def generateSchTable(employee_json, shifts):
    num_days = 7
    num_shifts = len(shifts)
    shift_requests = [[[0]*num_shifts for _ in range(num_days)] for _ in employee_json]

    days_of_week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    for i, emp in enumerate(employee_json):
        for j, day in enumerate(days_of_week):
            pref = emp["shiftPref"][day]
            if pref == "NA":
                shift_requests[i][j] = [-1] * num_shifts  # All shifts are unavailable
            elif pref == "any":
                shift_requests[i][j] = [1] * num_shifts  # Flexible for all shifts
            else:
                shift_requests[i][j] = [0] * num_shifts
                shift_requests[i][j][int(pref)] = 1  # Preferred shift

    return shift_requests

""" 
This function is sourced from google OR-Tools examples https://developers.google.com/optimization/scheduling/employee_scheduling#python_21 and optimized using ChatGPT 4.0
prompt: ".. entire code snippet from undistributedUtils.py .. 'fix the code of taking unavailable shifts into account in the model.'"
"""
from ortools.sat.python import cp_model
import json
from helper import totalHours

class Employee:
    def __init__(self, name, shiftPref, status):
        self.emp_name = name
        self.shiftPref = shiftPref
        self.status = status  # 'fulltime' or 'parttime'

def generateSchTable(employee_json, shifts):
    num_days = 7
    num_shifts = len(shifts)
    shift_requests = [[[0]*num_shifts for _ in range(num_days)] for _ in employee_json]
    days_of_week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    for i, emp in enumerate(employee_json):
        for j, day in enumerate(days_of_week):
            pref = emp["shiftPref"][day]
            if pref == "NA":
                shift_requests[i][j] = [-1] * num_shifts  # All shifts are unavailable
            elif pref == "any":
                shift_requests[i][j] = [1] * num_shifts  # Flexible for all shifts
            else:
                shift_requests[i][j] = [0] * num_shifts
                shift_requests[i][j][int(pref)] = 1  # Preferred shift
    return shift_requests

def undistGetSchedule(employee_json, shifts_json, hour_bank):
    employees = [Employee(emp["name"], emp["shiftPref"], emp["status"]) for emp in employee_json]
    shifts = shifts_json

    num_employees = len(employees)
    num_shifts = len(shifts)
    num_days = 7
    all_employees = range(num_employees)
    all_shifts = range(num_shifts)
    all_days = range(num_days)

    model = cp_model.CpModel()
    shifts_var = {}
    weekly_hours = {}

    for n in all_employees:
        weekly_hours[n] = model.new_int_var(0, 40, f'weekly_hours_{n}')
        for d in all_days:
            for s in all_shifts:
                shifts_var[(n, d, s)] = model.new_bool_var(f"shift_n{n}_d{d}_s{s}")

    for n in all_employees:
        model.Add(sum(shifts_var[(n, d, s)] * totalHours(shifts[s][0], shifts[s][1])
                   for d in all_days for s in all_shifts) == weekly_hours[n])

    for n in all_employees:
        if employees[n].status == 'fulltime':
            model.AddLinearConstraint(weekly_hours[n], 32, 40)
        elif employees[n].status == 'parttime':
            model.AddLinearConstraint(weekly_hours[n], 12, 20)

    shift_requests = generateSchTable(employee_json, shifts)

    for n in all_employees:
        for d in all_days:
            for s in all_shifts:
                if shift_requests[n][d][s] == -1:
                    model.Add(shifts_var[(n, d, s)] == 0)  # Ensure no assignment if unavailable

    model.maximize(
        sum(
            shift_requests[n][d][s] * shifts_var[(n, d, s)]
            for n in all_employees
            for d in all_days
            for s in all_shifts
            if shift_requests[n][d][s] >= 0
        )
    )

    solver = cp_model.CpSolver()
    status = solver.solve(model)

    result = {"schedule": [], "remaining_hour_bank": hour_bank, "statistics": {}}

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        employee_hours = {emp.emp_name: 0 for emp in employees}
        
        for d in all_days:
            day_schedule = {"day": d, "shifts": []}
            for n in all_employees:
                for s in all_shifts:
                    if solver.value(shifts_var[(n, d, s)]) == 1:
                        shift_start, shift_end = shifts[s]
                        shift_hours = totalHours(shift_start, shift_end)
                        employee_hours[employees[n].emp_name] += shift_hours
                        result["remaining_hour_bank"] -= shift_hours
                        
                        shift_detail = {
                            "employee": employees[n].emp_name,
                            "shift": (shift_start, shift_end),
                            "requested": shift_requests[n][d][s] == 1,
                            "hours": shift_hours
                        }
                        day_schedule["shifts"].append(shift_detail)
            result["schedule"].append(day_schedule)
        result["total_hours_per_employee"] = employee_hours
        result["objective_value"] = solver.ObjectiveValue()
    else:
        result["error"] = "No optimal solution found!"

    result["statistics"] = {
        "conflicts": solver.NumConflicts(),
        "branches": solver.NumBranches(),
        "wall_time": solver.WallTime()
    }

    return result
