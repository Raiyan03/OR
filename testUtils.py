from ortools.sat.python import cp_model
import json

class Employee:
    def __init__(self, name, shiftPref, status, role="employee"):
        self.emp_name = name
        self.shiftPref = shiftPref
        self.status = status
        self.role = role  # Include role to distinguish supervisors

def totalHours(start, end):
    return int((end - start) / 3600000)

def TestgetSchedule(employee_json, shifts_json, shift_requests, hour_bank):
    employee = [
        Employee(emp["name"], emp["shiftPref"], emp["status"], emp.get("role", "employee"))
        for emp in employee_json
    ]
    shifts = shifts_json

    num_employee = len(employee)
    num_shifts = len(shifts)
    num_days = 7
    all_employee = range(num_employee)
    all_shifts = range(num_shifts)
    all_days = range(num_days)

    model = cp_model.CpModel()

    shifts_var = {}
    for n in all_employee:
        for d in all_days:
            for s in all_shifts:
                shifts_var[(n, d, s)] = model.NewBoolVar(f"shift_n{n}_d{d}_s{s}")

    # Each shift on each day must be assigned to exactly one employee
    for d in all_days:
        for s in all_shifts:
            model.AddExactlyOne(shifts_var[(n, d, s)] for n in all_employee)

    # Ensure each employee works at most one shift per day
    for n in all_employee:
        for d in all_days:
            model.AddAtMostOne(shifts_var[(n, d, s)] for s in all_shifts)

    # Add constraints for hours based on employment status
    for n in all_employee:
        total_hours_worked = sum(shifts_var[(n, d, s)] * totalHours(shifts[s][0], shifts[s][1])
                                for d in all_days for s in all_shifts)
        if employee[n].status == "parttime":
            model.Add(total_hours_worked >= 12)
            model.Add(total_hours_worked <= 20)
        elif employee[n].status == "fulltime":
            model.Add(total_hours_worked >= 30)
            model.Add(total_hours_worked <= 40)

    # Modify the objective function to prioritize supervisors
    model.Maximize(
        sum(shift_requests[n][d][s] * shifts_var[(n, d, s)] * (10 if employee[n].role == "supervisor" else 1)
        for n in all_employee for d in all_days for s in all_shifts)
    )

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
                        if result["remaining_hour_bank"] - shift_hours >= 0:
                            employee_hours[employee[n].emp_name] += shift_hours
                            shift_detail = {"employee": employee[n].emp_name, "shift": shifts[s], "requested": shift_requests[n][d][s] == 1, "hours": shift_hours}
                            day_schedule["shifts"].append(shift_detail)
                            result["remaining_hour_bank"] -= shift_hours
                        else:
                            print(f"Warning: Not enough hours left in hour bank to schedule {employee[n].emp_name} for shift {shifts[s]} on day {d}")
            result["schedule"].append(day_schedule)
        result["total_hours_per_employee"] = employee_hours
        result["objective_value"] = solver.ObjectiveValue()
    else:
        print("No optimal solution found within the time limit.")

    result["statistics"] = {"conflicts": solver.NumConflicts(), "branches": solver.NumBranches(), "wall_time": solver.WallTime()}

    return result

# Example JSON data handling should be adapted accordingly to include 'role' where necessary



def generateShiftArray(num_shift):
    return [0] * num_shift

def TestgenerateSchTable(employees, shifts):
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
