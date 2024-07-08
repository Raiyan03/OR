from ortools.sat.python import cp_model
import json

class Employee:
    def __init__(self, name, shiftPref):
        self.emp_name = name
        self.shiftPref = shiftPref

def totalHours(start, end):
    return (end - start) / (1000 * 60 * 60)

def getSchedule(employee_json, shifts_json, shift_requests, hour_bank, flex_hours):
    day_mapping = {
        "Sun": 0,
        "Mon": 1,
        "Tue": 2,
        "Wed": 3,
        "Thu": 4,
        "Fri": 5,
        "Sat": 6
    }
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
                shifts_var[(n, d, s)] = model.NewBoolVar(f"shift_n{n}_d{d}_s{s}")

    # Each shift is assigned to exactly one employee.
    for d in all_days:
        for s in all_shifts:
            model.AddExactlyOne(shifts_var[(n, d, s)] for n in all_employee)

    # Each employee works at most one shift per day.
    for n in all_employee:
        for d in all_days:
            model.AddAtMostOne(shifts_var[(n, d, s)] for s in all_shifts)

    # Distribute shifts evenly.
    min_shifts_per_employee = (num_shifts * num_days) // num_employee
    max_shifts_per_employee = min_shifts_per_employee + 1 if num_shifts * num_days % num_employee != 0 else min_shifts_per_employee

    for n in all_employee:
        num_shifts_worked = sum(shifts_var[(n, d, s)] for d in all_days for s in all_shifts)
        model.Add(min_shifts_per_employee <= num_shifts_worked)
        model.Add(num_shifts_worked <= max_shifts_per_employee)

    # Maximize the number of fulfilled shift requests.
    model.Maximize(
        sum(
            shift_requests[n][d][s] * shifts_var[(n, d, s)]
            for n in all_employee
            for d in all_days
            for s in all_shifts
        )
    )

    # Creates the solver and solves the model.
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 60.0
    status = solver.Solve(model)

    result = {"schedule": [], "remaining_hour_bank": hour_bank}
    employee_hours = {emp.emp_name: 0 for emp in employee}

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        for d in all_days:
            day_schedule = {"day": d, "shifts": []}
            for n in all_employee:
                for s in all_shifts:
                    if solver.Value(shifts_var[(n, d, s)]) == 1:
                        shift_start, shift_end = shifts[s]
                        shift_hours = totalHours(shift_start, shift_end)
                        if result["remaining_hour_bank"] - shift_hours >= flex_hours:
                            employee_hours[employee[n].emp_name] += shift_hours

                            shift_detail = {
                                "employee": employee[n].emp_name,
                                "shift": shifts[s],
                                "requested": shift_requests[n][d][s] == 1,
                                "hours": shift_hours
                            }
                            day_schedule["shifts"].append(shift_detail)
                            result["remaining_hour_bank"] -= shift_hours
                        else:
                            print(f"Warning: Not enough hours left in hour bank to schedule {employee[n].emp_name} for shift {shifts[s]} on day {d}")
            result["schedule"].append(day_schedule)
        result["total_hours_per_employee"] = employee_hours
        result["objective_value"] = solver.ObjectiveValue()
    else:
        for d in all_days:
            day_schedule = {"day": d, "shifts": []}
            assigned_employees = set()
            for s in all_shifts:
                for n in all_employee:
                    if n not in assigned_employees:
                        shift_start, shift_end = shifts[s]
                        shift_hours = totalHours(shift_start, shift_end)
                        if result["remaining_hour_bank"] - shift_hours >= flex_hours:
                            shift_requested = shift_requests[n][d][s] == 1
                            any_shift_requested = any(shift_requests[n][d][x] == 1 for x in range(num_shifts))
                            shift_detail = {
                                "employee": employee[n].emp_name,
                                "shift": shifts[s],
                                "requested": shift_requested or any_shift_requested,
                                "hours": shift_hours
                            }
                            day_schedule["shifts"].append(shift_detail)
                            assigned_employees.add(n)
                            result["remaining_hour_bank"] -= shift_hours
                            break
            result["schedule"].append(day_schedule)
        result["objective_value"] = "No optimal solution found, default schedule generated"

    result["statistics"] = {
        "conflicts": solver.NumConflicts(),
        "branches": solver.NumBranches(),
        "wall_time": solver.WallTime()
    }

    return result

def generateShiftArray(num_shift):
    return [0] * num_shift

def generateSchTable(employees, shifts):
    day_mapping = {
        "Sun": 0,
        "Mon": 1,
        "Tue": 2,
        "Wed": 3,
        "Thu": 4,
        "Fri": 5,
        "Sat": 6
    }
    num_shifts = len(shifts)
    shiftReq = []

    for emp in range(len(employees)):
        empArray = []
        shiftDict = employees[emp]['shiftPref']

        for day in day_mapping:
            shift = generateShiftArray(num_shifts)
            if day in shiftDict:
                if shiftDict[day] == "any":
                    empArray.append(shift)
                else:
                    indx = int(shiftDict[day])
                    if 0 <= indx < num_shifts:
                        shift[indx] = 1
                    else:
                        print(f"Warning: Invalid shift index {indx} for employee {employees[emp]['name']} on {day}")
                    empArray.append(shift)
            else:
                empArray.append(shift)
        shiftReq.append(empArray)
    return shiftReq



