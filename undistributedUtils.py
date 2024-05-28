from ortools.sat.python import cp_model
import json

class Employee:
    def __init__(self, name, shiftPref):
        self.emp_name = name
        self.shiftPref = shiftPref

""" 
This function is self written but optimized using ChatGPT 4.0 

prompt: ".. entire code snippet from undistributedUtils.py .. 'fix the code of taking unavailable shifts into account in the model.'"
"""
def generateSchTable(employee_json, shifts):
    num_days = 7
    num_shifts = len(shifts)
    shift_requests = [[[0]*num_shifts for _ in range(num_days)] for _ in employee_json]

    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    for i, emp in enumerate(employee_json):
        for j, day in enumerate(days_of_week):
            pref = emp["shiftPref"][day]
            if pref == "NA":
                shift_requests[i][j] = [-1] * num_shifts  # All shifts are unavailable
            elif pref == "any":
                shift_requests[i][j] = [1] * num_shifts  # Flexible for all shifts
            else:
                shift_requests[i][j] = [0] * num_shifts
                shift_requests[i][j][pref] = 1  # Preferred shift

    return shift_requests

""" 
This function is sourced from google OR-Tools examples https://developers.google.com/optimization/scheduling/employee_scheduling#python_21 and optimized using ChatGPT 4.0
prompt: ".. entire code snippet from undistributedUtils.py .. 'fix the code of taking unavailable shifts into account in the model.'"
"""
def undistGetSchedule(employee_json, shifts_json):
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

    # Constraint: Exactly one employee per shift per day
    for d in all_days:
        for s in all_shifts:
            model.add_exactly_one(shifts_var[(n, d, s)] for n in all_employees)

    # Constraint: At most one shift per employee per day
    for n in all_employees:
        for d in all_days:
            model.add_at_most_one(shifts_var[(n, d, s)] for s in all_shifts)

    # Incorporate shift requests into the model
    shift_requests = generateSchTable(employee_json, shifts)

    for n in all_employees:
        for d in all_days:
            for s in all_shifts:
                if shift_requests[n][d][s] == -1:
                    model.add(shifts_var[(n, d, s)] == 0)  # Ensure no assignment if unavailable

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

    result = {"schedule": []}
    print("Status:")
    print("Optimal:", status == cp_model.OPTIMAL)
    print("Infeasible:", status == cp_model.INFEASIBLE)
    print("Feasible:", status == cp_model.FEASIBLE)
    print("Unknown:", status == cp_model.UNKNOWN)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
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
        result["objective_value"] = solver.ObjectiveValue()
    else:
        result["error"] = "No optimal solution found!"

    result["statistics"] = {
        "conflicts": solver.NumConflicts(),
        "branches": solver.NumBranches(),
        "wall_time": solver.WallTime()
    }

    return result