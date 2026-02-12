class Employee:
    """Represents an employee in the organization.

    Attributes:
        id (int): Unique identifier for the employee.
        name (str): Name of the employee.
        unit_name (str): Name of the unit the employee belongs to.
        age (int): Age of the employee.
        role (str): Role/position of the employee (e.g., MANAGER, STAFF_MEMBER).
        manager_id (int): ID of the employee's manager, or None for HEAD_OF_ORGANIZATION.
        children_ids (list): List of IDs of employees who report to this employee.
    """

    def __init__(self, emp_id, name, unit_name, age, role, manager_id):
        """Initialize an employee.

        Args:
            emp_id (int): Unique identifier for the employee.
            name (str): Name of the employee.
            unit_name (str): Name of the unit the employee belongs to.
            age (int): Age of the employee.
            role (str): Role/position of the employee.
            manager_id (int): ID of the employee's manager, or None for HEAD_OF_ORGANIZATION.
        """
        self.id = emp_id
        self.name = name
        self.unit_name = unit_name
        self.age = age
        self.role = role
        self.manager_id = manager_id
        self.children_ids = []

    def __str__(self):
        """Return formatted string representation of the employee.

        Returns:
            str: Formatted employee information including role, unit, id, name, and age.
        """
        return f"|--{self.role} | {self.unit_name} | {self.id} | {self.name} - {self.age}"