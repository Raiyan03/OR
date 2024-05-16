from ortools.sat.python import cp_model
import json


class Employee:
    def __init__(self, name, shiftPref):
        self.emp_name = name
        self.shiftPref = shiftPref


def getSchedule(employee_json, shifts_json, shift_requests):
    employee = [Employee(emp["name"], emp["shiftPref"]) for emp in employee_json]
    shifts = shifts_json
    shift_requests = shift_requests

    num_employee = len(employee)
    num_shifts = len(shifts)
    num_days = 7
    all_employee = range(num_employee)
    all_shifts = range(num_shifts)
    all_days = range(num_days)

    # Creates the model.
    model = cp_model.CpModel()

    # Creates shift variables.
    shifts_var = {}
    for n in all_employee:
        for d in all_days:
            for s in all_shifts:
                shifts_var[(n, d, s)] = model.new_bool_var(f"shift_n{n}_d{d}_s{s}")

    # Each shift is assigned to exactly one employee.
    for d in all_days:
        for s in all_shifts:
            model.add_exactly_one(shifts_var[(n, d, s)] for n in all_employee)

    # Each employee works at most one shift per day.
    for n in all_employee:
        for d in all_days:
            model.add_at_most_one(shifts_var[(n, d, s)] for s in all_shifts)

    # Distribute shifts evenly.
    min_shifts_per_employee = (num_shifts * num_days) // num_employee
    max_shifts_per_employee = min_shifts_per_employee + 1 if num_shifts * num_days % num_employee != 0 else min_shifts_per_employee

    for n in all_employee:
        num_shifts_worked = sum(shifts_var[(n, d, s)] for d in all_days for s in all_shifts)
        model.add(min_shifts_per_employee <= num_shifts_worked)
        model.add(num_shifts_worked <= max_shifts_per_employee)

    # Maximize the number of fulfilled shift requests.
    model.maximize(
        sum(
            shift_requests[n][d][s] * shifts_var[(n, d, s)]
            for n in all_employee
            for d in all_days
            for s in all_shifts
        )
    )

    # Creates the solver and solves the model.
    solver = cp_model.CpSolver()
    status = solver.solve(model)

    result = {"schedule": []}
    if status == cp_model.OPTIMAL:
        for d in all_days:
            day_schedule = {"day": d, "shifts": []}
            for n in all_employee:
                for s in all_shifts:
                    if solver.value(shifts_var[(n, d, s)]) == 1:
                        shift_detail = {
                            "employee": employee[n].emp_name,
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


def generateShiftArray(num_shift):
    array = [0] * num_shift
    return array

def generateSchTable(employees, shifts):
    # print(f"Generating shift table for \n {employees}")
    num_shifts = len(shifts)
    shiftReq = []
    
    for emp in range(len(employees)):
        # print(f"\nGenerating shift table for {employees[emp]}")
        empArray = []
        shiftDict = employees[emp]['shiftPref']
        # print(f"\nShift preference {shiftDict}")
        
        for day in shiftDict:
            shift = generateShiftArray(num_shifts)
            if shiftDict[day] == "any":
                empArray.append(shift)
            else:
                indx = shiftDict[day]
                shift[indx] = 1
                empArray.append(shift)
                
        shiftReq.append(empArray)
    
    return shiftReq