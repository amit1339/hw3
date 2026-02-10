from role import Role
from employee import Employee
from unit import Unit


class Organization:
    """
    Manages the organization data, logic, and constraints.
    """
    def __init__(self):
        self.employees_by_id = {}
        self.units_by_name = {}
        self.next_id = 0
        self.head_id = None

    def add_unit(self, unit_name):
        if unit_name in self.units_by_name:
            # Per prompt: "prints appropriate error message on error (for example – unit with the same name exists)."
            # The example input does not trigger this, but the functionality is required.
            print(f"Unit {unit_name} already exists.")
            return

        new_unit = Unit(unit_name)
        self.units_by_name[unit_name] = new_unit
        print(f"Unit {unit_name} added successfully")

    def add_employee(self, name, unit_name, age, role, manager_id=None):
        # Validation order is critical to match example output.
        # 1. Validate Unit existence.
        if unit_name not in self.units_by_name:
            print(f"Unit {unit_name} does not exists.")
            return

        # 2. Validate Role string.
        if not Role.exists(role):
            print("Wrong format for add employee command.")
            print("\trole must be a valid employee role")
            return

        # 3. Validate HEAD_OF_ORGANIZATION constraints.
        if role == Role.HEAD_OF_ORGANIZATION:
            if self.head_id is not None:
                print("Organization can have only a single HEAD_OF_ORGANIZATION")
                return
            manager_id = None  # Head of Org has no manager.
        else:
            # 4. For non-HEAD roles, validate manager.
            if manager_id is None:
                print("Wrong format for add employee command.")
                print("\tEmployee must have a manager, unless they are the HEAD_OF_ORGANIZATION.")
                return

            if manager_id not in self.employees_by_id:
                # This error is not in the add_employee example, but is logical and in assign_manager.
                print(f"Manager with id {manager_id} not found.")
                return

            manager = self.employees_by_id[manager_id]
            if not Role.can_manage(manager.role):
                print(f"Employee with role {manager.role} can not manage.")
                return

        # All validations passed. Create the employee.
        new_id = self.next_id
        self.next_id += 1

        new_emp = Employee(new_id, name, unit_name, age, role, manager_id)

        # Add employee to data structures.
        self.employees_by_id[new_id] = new_emp
        self.units_by_name[unit_name].add_employee(new_emp)

        if role == Role.HEAD_OF_ORGANIZATION:
            self.head_id = new_id
        elif manager_id is not None:
            self.employees_by_id[manager_id].children_ids.append(new_id)
            # Ensure children are sorted by ID for printing
            self.employees_by_id[manager_id].children_ids.sort()

        print(f"Employee added successfully and was assigned id {new_id}")

    def delete_employee(self, emp_id):
        if emp_id not in self.employees_by_id:
            print("Employee with this id was not found.")
            return

        emp = self.employees_by_id[emp_id]

        # 1. Check if employee is the Head of Organization.
        if emp.role == Role.HEAD_OF_ORGANIZATION:
            print("HEAD_OF_ORGANIZATION can never be deleted!")
            return

        # 2. Check if employee has direct reports.
        if len(emp.children_ids) > 0:
            print("Employee has reporters - can't delete")
            return

        # Remove from Unit
        if emp.unit_name in self.units_by_name:
            self.units_by_name[emp.unit_name].remove_employee(emp_id)

        # 4. Remove from their manager's list of children.
        if emp.manager_id is not None and emp.manager_id in self.employees_by_id:
            manager = self.employees_by_id[emp.manager_id]
            if emp_id in manager.children_ids:
                manager.children_ids.remove(emp_id)

        # 5. Remove from the main employee registry.
        del self.employees_by_id[emp_id]
        print(f"Employee with id {emp_id} deleted successfully")

    def assign_manager(self, emp_id, new_manager_id):
        if emp_id not in self.employees_by_id:
            print("Employee with this id was not found.")
            return

        if new_manager_id not in self.employees_by_id:
            print("Manager with this id was not found.")
            return

        emp = self.employees_by_id[emp_id]
        new_manager = self.employees_by_id[new_manager_id]

        if emp.role == Role.HEAD_OF_ORGANIZATION:
            print("HEAD_OF_ORGANIZATION has no managers!") # Not in example, but a critical constraint.
            return

        if not Role.can_manage(new_manager.role):
            print(f"Employee with role {new_manager.role} can not manage.")
            return

        # Update Hierarchy
        # 1. Remove from old manager's children list.
        if emp.manager_id is not None and emp.manager_id in self.employees_by_id:
            old_manager = self.employees_by_id[emp.manager_id]
            if emp_id in old_manager.children_ids:
                old_manager.children_ids.remove(emp_id)

        # 2. Update employee's manager and add to new manager's children list.
        emp.manager_id = new_manager_id
        new_manager.children_ids.append(emp_id)
        new_manager.children_ids.sort()

        print(f"Assigned employee {emp_id} to manager {new_manager_id}")

    def move_to_unit(self, emp_id, unit_name):
        if emp_id not in self.employees_by_id:
            print("Employee with this id was not found.")
            return

        if unit_name not in self.units_by_name:
            print(f"Unit {unit_name} does not exist.")
            return

        emp = self.employees_by_id[emp_id]
        old_unit_name = emp.unit_name

        # 1. Remove from the old unit.
        if old_unit_name in self.units_by_name:
            self.units_by_name[old_unit_name].remove_employee(emp_id)

        # 2. Update employee's unit and add to the new unit.
        emp.unit_name = unit_name
        self.units_by_name[unit_name].add_employee(emp)

        print(f"Employee {emp_id} moved to unit {unit_name}.")

    def print_employee(self, emp_id):
        if emp_id not in self.employees_by_id:
            print("Employee with this id was not found.")
            return
        print(self.employees_by_id[emp_id])

    def print_org(self):
        if self.head_id is None:
            return

        # Recursive helper for Pre-order DFS traversal.
        def print_recursive(emp_id, depth):
            if emp_id not in self.employees_by_id:
                return

            employee = self.employees_by_id[emp_id]
            indent = "\t" * depth
            print(f"{indent}{employee}")

            for child_id in employee.children_ids:
                print_recursive(child_id, depth + 1)

        print_recursive(self.head_id, 0)

    def print_units(self):
        # Sort unit names alphabetically to match the example output.
        sorted_unit_names = sorted(self.units_by_name.keys())

        for unit_name in sorted_unit_names:
            unit = self.units_by_name[unit_name]
            print(f"{unit.name} | number of employees = {len(unit)}")
            for employee in unit:  # The Unit class is iterable and sorted by employee ID.
                print(employee)