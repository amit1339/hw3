from role import Role
from employee import Employee
from unit import Unit


class Organization:
    """Manages the organization, employees, units, and their relationships.

    This class handles all business logic for managing employees, units, hierarchies,
    and validating organizational constraints (e.g., only one HEAD_OF_ORGANIZATION).

    Attributes:
        employees_by_id (dict): Dictionary mapping employee IDs to Employee objects.
        units_by_name (dict): Dictionary mapping unit names to Unit objects.
        next_id (int): Counter for generating unique employee IDs.
        head_id (int): ID of the HEAD_OF_ORGANIZATION employee.
    """

    def __init__(self):
        """Initialize an empty organization."""
        self.employees_by_id = {}
        self.units_by_name = {}
        self.next_id = 0
        self.head_id = None

    def add_unit(self, unit_name):
        """Add a new unit to the organization.

        Args:
            unit_name (str): Name of the unit to add.

        Prints:
            Success message or error if unit already exists.
        """
        if unit_name in self.units_by_name:
            print(f"Unit {unit_name} already exists.")
            return

        new_unit = Unit(unit_name)
        self.units_by_name[unit_name] = new_unit
        print(f"Unit {unit_name} added successfully")

    def add_employee(self, name, unit_name, age, role, manager_id=None):
        """Add a new employee to the organization.

        Validates that:
        - The unit exists
        - The role is valid
        - Only one HEAD_OF_ORGANIZATION exists
        - Non-HEAD employees have a valid manager
        - The manager can manage (has appropriate role)

        Args:
            name (str): Name of the employee.
            unit_name (str): Name of the unit the employee belongs to.
            age (int): Age of the employee.
            role (str): Role of the employee (must be a valid Role).
            manager_id (int, optional): ID of the employee's manager. Required unless role is HEAD_OF_ORGANIZATION.

        Prints:
            Success message with assigned ID or error message if validation fails.
        """
        if unit_name not in self.units_by_name:
            print(f"Unit {unit_name} does not exists.")
            return

        if not Role.exists(role):
            print("Wrong format for add employee command.")
            print("\trole must be a valid employee role")
            return

        if role == Role.HEAD_OF_ORGANIZATION:
            if self.head_id is not None:
                print("Organization can have only a single HEAD_OF_ORGANIZATION")
                return
            manager_id = None
        else:
            if manager_id is None:
                print("Wrong format for add employee command.")
                print("\tEmployee must have a manager, unless they are the HEAD_OF_ORGANIZATION.")
                return

            if manager_id not in self.employees_by_id:
                print(f"Manager with id {manager_id} not found.")
                return

            manager = self.employees_by_id[manager_id]
            if not Role.can_manage(manager.role):
                print(f"Employee with role {manager.role} can not manage.")
                return

        new_id = self.next_id
        self.next_id += 1

        new_emp = Employee(new_id, name, unit_name, age, role, manager_id)

        self.employees_by_id[new_id] = new_emp
        self.units_by_name[unit_name].add_employee(new_emp)

        if role == Role.HEAD_OF_ORGANIZATION:
            self.head_id = new_id
        elif manager_id is not None:
            self.employees_by_id[manager_id].children_ids.append(new_id)
            self.employees_by_id[manager_id].children_ids.sort()

        print(f"Employee added successfully and was assigned id {new_id}")

    def delete_employee(self, emp_id):
        """Delete an employee from the organization.

        Validates that:
        - The employee exists
        - The employee is not the HEAD_OF_ORGANIZATION
        - The employee has no direct reports

        Args:
            emp_id (int): ID of the employee to delete.

        Prints:
            Success message or error message if validation fails.
        """
        if emp_id not in self.employees_by_id:
            print("Employee with this id was not found.")
            return

        emp = self.employees_by_id[emp_id]

        if emp.role == Role.HEAD_OF_ORGANIZATION:
            print("HEAD_OF_ORGANIZATION can never be deleted!")
            return

        if len(emp.children_ids) > 0:
            print("Employee has reporters - can't delete")
            return

        if emp.unit_name in self.units_by_name:
            self.units_by_name[emp.unit_name].remove_employee(emp_id)

        if emp.manager_id is not None and emp.manager_id in self.employees_by_id:
            manager = self.employees_by_id[emp.manager_id]
            if emp_id in manager.children_ids:
                manager.children_ids.remove(emp_id)

        del self.employees_by_id[emp_id]
        print(f"Employee with id {emp_id} deleted successfully")

    def assign_manager(self, emp_id, new_manager_id):
        """Assign a manager to an employee.

        Validates that:
        - Both employees exist
        - The employee is not the HEAD_OF_ORGANIZATION
        - The new manager has a role that can manage

        Args:
            emp_id (int): ID of the employee.
            new_manager_id (int): ID of the new manager.

        Prints:
            Success message or error message if validation fails.
        """
        if emp_id not in self.employees_by_id:
            print("Employee with this id was not found.")
            return

        if new_manager_id not in self.employees_by_id:
            print("Manager with this id was not found.")
            return

        emp = self.employees_by_id[emp_id]
        new_manager = self.employees_by_id[new_manager_id]

        if emp.role == Role.HEAD_OF_ORGANIZATION:
            print("HEAD_OF_ORGANIZATION has no managers!")
            return

        if not Role.can_manage(new_manager.role):
            print(f"Employee with role {new_manager.role} can not manage.")
            return

        if emp.manager_id is not None and emp.manager_id in self.employees_by_id:
            old_manager = self.employees_by_id[emp.manager_id]
            if emp_id in old_manager.children_ids:
                old_manager.children_ids.remove(emp_id)

        emp.manager_id = new_manager_id
        new_manager.children_ids.append(emp_id)
        new_manager.children_ids.sort()

        print(f"Assigned employee {emp_id} to manager {new_manager_id}")

    def move_to_unit(self, emp_id, unit_name):
        """Move an employee to a different unit.

        Validates that:
        - The employee exists
        - The target unit exists

        Args:
            emp_id (int): ID of the employee.
            unit_name (str): Name of the target unit.

        Prints:
            Success message or error message if validation fails.
        """
        if emp_id not in self.employees_by_id:
            print("Employee with this id was not found.")
            return

        if unit_name not in self.units_by_name:
            print(f"Unit {unit_name} does not exist.")
            return

        emp = self.employees_by_id[emp_id]
        old_unit_name = emp.unit_name

        if old_unit_name in self.units_by_name:
            self.units_by_name[old_unit_name].remove_employee(emp_id)

        emp.unit_name = unit_name
        self.units_by_name[unit_name].add_employee(emp)

        print(f"Employee {emp_id} moved to unit {unit_name}.")

    def print_employee(self, emp_id):
        """Print details of a specific employee.

        Args:
            emp_id (int): ID of the employee to print.

        Prints:
            Employee information or error message if employee not found.
        """
        if emp_id not in self.employees_by_id:
            print("Employee with this id was not found.")
            return
        print(self.employees_by_id[emp_id])

    def print_org(self):
        """Print the organization hierarchy starting from HEAD_OF_ORGANIZATION.

        The hierarchy is printed with indentation showing the reporting structure
        using a depth-first traversal of the organization tree.

        Prints:
            Organization hierarchy with employees indented by their depth in the tree.
        """
        if self.head_id is None:
            return

        def print_recursive(emp_id, depth):
            """Recursively print employee and their direct reports.

            Args:
                emp_id (int): ID of the employee to print.
                depth (int): Current depth in the hierarchy (used for indentation).
            """
            if emp_id not in self.employees_by_id:
                return

            employee = self.employees_by_id[emp_id]
            indent = "\t" * depth
            print(f"{indent}{employee}")

            for child_id in employee.children_ids:
                print_recursive(child_id, depth + 1)

        print_recursive(self.head_id, 0)

    def print_units(self):
        """Print all units and their employees in order of unit creation.

        Each unit shows:
        - Unit name and number of employees
        - List of employees in the unit (sorted by ID)

        Prints:
            Units with their employee lists.
        """
        for unit_name in self.units_by_name.keys():
            unit = self.units_by_name[unit_name]
            print(f"{unit.name} | number of employees = {len(unit)}")
            for employee in unit:
                print(f"\t{employee}")